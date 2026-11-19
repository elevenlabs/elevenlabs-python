import dataclasses
import itertools
import json
import re
import typing
import urllib.parse

import httpx

from elevenlabs import AsyncElevenLabs, ElevenLabs

Json = typing.Dict[str, typing.Any]


@dataclasses.dataclass
class Call:
    method: str
    path: str
    query: typing.Dict[str, str]
    body: typing.Optional[Json]


class FakeServer:
    """An in-memory stand-in for the agents and tools endpoints `push` and `pull` use, behind an httpx transport."""

    def __init__(self) -> None:
        self.tools: typing.Dict[str, Json] = {}
        self.agents: typing.Dict[str, Json] = {}
        # Branch configs by (agent id, branch id). Only the main branch counts for `used_by_agent_id`, as in the API.
        self.branches: typing.Dict[typing.Tuple[str, str], Json] = {}
        self.calls: typing.List[Call] = []
        # Fails every request whose `METHOD path` matches.
        self.fail_on: typing.Optional[str] = None
        self._next = itertools.count(1)

    def add_tool(self, id: str, config: Json, used_by: typing.Sequence[str] = ()) -> None:
        self.tools[id] = {"config": config, "used_by": list(used_by)}

    def add_agent(self, id: str, config: Json) -> None:
        self.agents[id] = config

    def client(self) -> ElevenLabs:
        return ElevenLabs(
            api_key="test",
            base_url="https://api.test",
            httpx_client=httpx.Client(transport=httpx.MockTransport(self._handle)),
        )

    def async_client(self) -> AsyncElevenLabs:
        return AsyncElevenLabs(
            api_key="test",
            base_url="https://api.test",
            httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(self._handle)),
        )

    def writes(self) -> typing.List[str]:
        """The calls that change something, as `METHOD path`."""
        return [f"{call.method} {call.path}" for call in self.calls if call.method != "GET"]

    def _handle(self, request: httpx.Request) -> httpx.Response:
        method = request.method
        path = request.url.path
        query = dict(urllib.parse.parse_qsl(request.url.query.decode()))
        body = json.loads(request.content) if request.content else None
        self.calls.append(Call(method=method, path=path, query=query, body=body))
        if self.fail_on is not None and re.search(self.fail_on, f"{method} {path}"):
            return httpx.Response(500, json={"detail": "boom"})
        parts = path.split("/")  # /v1/convai/<kind>/<id>
        kind = parts[3]
        id = parts[4] if len(parts) > 4 else None
        if kind == "tools":
            if method == "GET" and id is None:
                agent_id = query.get("used_by_agent_id")
                tools = [
                    _tool_response(tool_id, tool["config"])
                    for tool_id, tool in self.tools.items()
                    if agent_id is None or agent_id in tool["used_by"]
                ]
                return httpx.Response(200, json={"tools": tools, "has_more": False})
            if method == "POST":
                assert body is not None
                tool_id = f"tool_new_{next(self._next)}"
                self.tools[tool_id] = {"config": body["tool_config"], "used_by": []}
                return httpx.Response(200, json=_tool_response(tool_id, body["tool_config"]))
            tool = self.tools.get(typing.cast(str, id))
            if tool is None:
                return httpx.Response(404, json={"detail": "not found"})
            if method == "PATCH":
                assert body is not None
                tool["config"] = body["tool_config"]
            return httpx.Response(200, json=_tool_response(typing.cast(str, id), tool["config"]))
        if kind == "agents":
            if method == "POST" and id == "create":
                assert body is not None
                agent_id = f"agent_new_{next(self._next)}"
                self._store_agent(agent_id, body)
                return httpx.Response(200, json={"agent_id": agent_id})
            branch_id = query.get("branch_id")
            if branch_id is not None and id is not None:
                if method == "PATCH":
                    assert body is not None
                    self.branches[(id, branch_id)] = {**self.branches.get((id, branch_id), {}), **body}
                branch = self.branches.get((id, branch_id))
                if branch is None:
                    return httpx.Response(404, json={"detail": "not found"})
                return httpx.Response(200, json=_agent_response(id, branch))
            if method == "PATCH":
                assert body is not None and id is not None
                self._store_agent(id, {**self.agents.get(id, {}), **body})
                return httpx.Response(200, json=_agent_response(id, self.agents[id]))
            agent = self.agents.get(typing.cast(str, id))
            if agent is None:
                return httpx.Response(404, json={"detail": "not found"})
            return httpx.Response(200, json=_agent_response(typing.cast(str, id), agent))
        raise AssertionError(f"unexpected request {method} {path}")

    def _store_agent(self, agent_id: str, config: Json) -> None:
        self.agents[agent_id] = config
        prompt = ((config.get("conversation_config") or {}).get("agent") or {}).get("prompt") or {}
        ids = list(prompt.get("tool_ids") or [])
        for node in ((config.get("workflow") or {}).get("nodes") or {}).values():
            ids.extend(tool["tool_id"] for tool in node.get("tools") or [])
            ids.extend(node.get("additional_tool_ids") or [])
        for tool_id, tool in self.tools.items():
            tool["used_by"] = [a for a in tool["used_by"] if a != agent_id]
            if tool_id in ids:
                tool["used_by"].append(agent_id)


def _tool_response(id: str, config: Json) -> Json:
    return {
        "id": id,
        "tool_config": config,
        "access_info": {"is_creator": True, "creator_name": "a", "creator_email": "a@example.com", "role": "admin"},
        "usage_stats": {"avg_latency_secs": 0.1},
    }


def _with_server_defaults(workflow: Json) -> Json:
    """The defaults the API fills into a stored workflow, which the response model requires."""
    nodes = {
        id: (
            {
                "conversation_config": {},
                "additional_knowledge_base": [],
                "additional_tool_ids": [],
                "entry_behavior": "generate_immediately",
                "allow_interruptions_on_entry": True,
                **node,
            }
            if node.get("type") == "override_agent"
            else node
        )
        for id, node in (workflow.get("nodes") or {}).items()
    }
    edges = {id: {"reroutes": [], **edge} for id, edge in (workflow.get("edges") or {}).items()}
    return {"prevent_subagent_loops": False, **workflow, "nodes": nodes, "edges": edges}


def _agent_response(id: str, config: Json) -> Json:
    response = {
        "agent_id": id,
        "metadata": {"created_at_unix_secs": 1, "updated_at_unix_secs": 1},
        "created_at_unix_secs": 1,
        "updated_at_unix_secs": 1,
        "version_id": "ver_1",
        **config,
    }
    if config.get("workflow") is not None:
        response["workflow"] = _with_server_defaults(config["workflow"])
    return response
