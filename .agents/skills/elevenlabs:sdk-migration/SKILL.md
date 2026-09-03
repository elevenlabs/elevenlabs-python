---
name: elevenlabs:sdk-migration
description: Migrate code from the elevenlabs Python SDK v2.x to v3. Use when updating code that uses client.conversational_ai, elevenlabs.conversational_ai.conversation, OnPremInitiationData, on_prem_config, ScribeRealtime, RealtimeConnection, convert_realtime, voices.get_all, text_to_voice.create_previews, or related APIs. Also trigger when users mention upgrading the ElevenLabs Python SDK, fixing breaking changes after a pip install -U elevenlabs, or encountering ImportError/AttributeError after updating to v3.
license: MIT
---

# ElevenLabs Python SDK v2 → v3 Migration

Migration guide for the `elevenlabs` package v3 breaking changes.

## Migration order

1. **Check the runtime** — v3 requires Python ≥ 3.10 and Pydantic ≥ 2 (3.8/3.9 and the Pydantic v1 compatibility layer are dropped).
2. **Install**: `pip install "elevenlabs>=3,<4"` (during prerelease: `pip install --pre elevenlabs`).
3. **Rename the namespace** — every `client.conversational_ai.*` becomes `client.agents.*`, and imports move from `elevenlabs.conversational_ai.*` to `elevenlabs.agents.*`.
4. **Replace removed endpoints** — deprecated v2 endpoints are gone (table below).
5. **Rename on-prem config** — `OnPremInitiationData` is now `OrchestratorConfig`.
6. **Migrate realtime code** — the hand-written realtime clients are replaced by generated WebSocket clients.
7. **Run mypy/tests** and fix renamed helper types (verb-first names).

## `conversational_ai` → `agents`

API URLs are unchanged (`/v1/convai/*`); only the SDK namespace moves. The former `agents` sub-resource is flattened onto the group:

```python
# Before
client.conversational_ai.agents.create(conversation_config={})
client.conversational_ai.conversations.list()
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# After
client.agents.create(conversation_config={})
client.agents.conversations.list()
from elevenlabs.agents.conversation import Conversation, ClientTools
from elevenlabs.agents.default_audio_interface import DefaultAudioInterface
```

Mechanical rule: `client.conversational_ai.agents.<x>` → `client.agents.<x>`; every other `client.conversational_ai.<x>` → `client.agents.<x>`. One exception: the per-agent LLM usage endpoint is `client.agents.agents.llm_usage.calculate` (the workspace-level one is `client.agents.llm_usage.calculate`). Tests that patch module paths as strings (`mock.patch("elevenlabs.conversational_ai...")`) must be updated too.

## On-prem / self-hosted orchestrator rename

`OnPremInitiationData` is renamed to `OrchestratorConfig` (aligning with the `@elevenlabs/client` JS SDK), the `Conversation` parameter is `orchestrator_config`, and the URL field is `url`. All optional fields are keyword-only, and the URL must be `ws://` or `wss://`.

```python
# Before
from elevenlabs.conversational_ai.conversation import Conversation, OnPremInitiationData

conversation = Conversation(
    client, agent_id, requires_auth=False,
    on_prem_config=OnPremInitiationData(
        on_prem_conversation_url="wss://my-host/sagemaker/convai/conversation",
        agent_config_dict=config,
    ),
)

# After
from elevenlabs.agents.conversation import Conversation, OrchestratorConfig

conversation = Conversation(
    client, agent_id, requires_auth=False,
    orchestrator_config=OrchestratorConfig(
        "wss://my-host/sagemaker/convai/conversation",
        agent_config_dict=config,
    ),
)
```

The wire format (`enclave_setup_config`) is unchanged — no server-side changes needed.

## Removed endpoints

Removed | Use instead
-- | --
`client.voices.get_all(...)` | `client.voices.search(...)`
`client.text_to_voice.create_previews(...)` | `client.text_to_voice.design(...)`
`client.conversational_ai.add_to_knowledge_base(...)` | `client.agents.knowledge_base.documents.create_from_file/from_url/from_text`
`client.conversational_ai.agents.simulate_conversation(...)` (+ `_stream`) | agent-testing endpoints under `client.agents.tests.*`
`client.conversational_ai.mcp_servers.approval_policy.update(...)` | `client.agents.mcp_servers.update(...)`
`client.usage.get(...)` | workspace analytics usage queries
`client.dubbing.resource.*` (all 13 methods) | Dubbing Studio endpoints
`cloud_storage_url` param on `speech_to_text.convert` | `source_url`

## Realtime speech-to-text

The hand-written `elevenlabs.realtime` package (`ScribeRealtime`, `RealtimeConnection`, `RealtimeEvents`, `AudioFormat`, `CommitStrategy`, `RealtimeAudioOptions`, `RealtimeUrlOptions` — also re-exported from the package root) is removed. `client.speech_to_text.realtime` is now a generated method returning a typed socket client, available in sync and async flavors.

**Before:**

```python
connection = await client.speech_to_text.realtime.connect({
    "model_id": "scribe_v2_realtime",
    "audio_format": AudioFormat.PCM_16000,
    "sample_rate": 16000,
})
connection.on(RealtimeEvents.TRANSCRIPT, print)
await connection.send({"audio_base_64": chunk})
```

**After:**

```python
with client.speech_to_text.realtime(model_id="scribe_v2_realtime", audio_format="pcm_16000") as socket:
    socket.send_publish(InputAudioChunk(audio_base_64=chunk_base64))
    for message in socket:
        print(message)

# or async:
async with async_client.speech_to_text.realtime(model_id="scribe_v2_realtime") as socket:
    await socket.send_publish(InputAudioChunk(audio_base_64=chunk_base64))
    async for message in socket:
        print(message)
```

URL-based streaming (the v2 `url` option that shelled out to ffmpeg) has no generated equivalent — stream the audio yourself and send chunks.

## Realtime text-to-speech

`RealtimeTextToSpeechClient.convert_realtime(...)` is removed. Use the generated websocket client, now also available on the async client (v2 had no async realtime TTS):

```python
# Before
audio_stream = client.text_to_speech.convert_realtime(voice_id, text=text_iterator)

# After
with client.text_to_speech.realtime(voice_id, model_id="eleven_flash_v2_5") as socket:
    ...
```

Dialogue, multi-context, and translation websockets have equivalent generated clients.

## Speech Engine internals

The public exports of `elevenlabs.speech_engine` (`SpeechEngineServer`, `SpeechEngineSession`, `SpeechEngineResource`, `verify_speech_engine_jwt`, etc.) are unchanged. The internal `elevenlabs.speech_engine.types` module was renamed to `elevenlabs.speech_engine.session_types` to make room for the generated `types/` package — update any deep imports.

## Renamed helper types

Per-endpoint request/response helper types are renamed verb-first, e.g. `conversations_get_request_format` → `get_conversations_request_format` (module names) and the matching class names. When an import breaks, search for the same words reordered verb-first.
