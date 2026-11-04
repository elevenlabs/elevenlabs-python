"""Regression coverage for Speech Engine helpers.

Covers ``_extract_text`` (LLM stream text extraction in
``elevenlabs.speech_engine.session``) and ``wrap_websocket``
(``elevenlabs.speech_engine.types``). Neither had any direct test
coverage: responses sent back for TTS synthesis depend on extraction
recognizing each provider's stream format, and FastAPI/Starlette
integration depends on the ASGI adapter delegating correctly.
"""

from types import SimpleNamespace

import pytest

from elevenlabs.speech_engine.session import _extract_text
from elevenlabs.speech_engine.types import _ASGIWebSocketAdapter, wrap_websocket


class TestExtractTextPassthrough:
    def test_plain_string_returned_as_is(self):
        assert _extract_text("hello") == "hello"

    def test_none_returns_none(self):
        assert _extract_text(None) is None

    def test_non_string_scalars_return_none(self):
        assert _extract_text(0) is None
        assert _extract_text(3.14) is None
        assert _extract_text(True) is None

    def test_unknown_shapes_return_none(self):
        assert _extract_text({}) is None
        assert _extract_text({"type": "something_else"}) is None
        assert _extract_text([]) is None


class TestExtractTextOpenAIResponses:
    def test_dict_chunk(self):
        chunk = {"type": "response.output_text.delta", "delta": "hello"}
        assert _extract_text(chunk) == "hello"

    def test_object_chunk(self):
        chunk = SimpleNamespace(type="response.output_text.delta", delta="hello")
        assert _extract_text(chunk) == "hello"

    def test_non_string_delta_returns_none(self):
        chunk = {"type": "response.output_text.delta", "delta": {"text": "hello"}}
        assert _extract_text(chunk) is None

    def test_missing_delta_returns_none(self):
        assert _extract_text({"type": "response.output_text.delta"}) is None


class TestExtractTextOpenAIChatCompletions:
    def test_dict_chunk(self):
        chunk = {"choices": [{"delta": {"content": "hi"}}]}
        assert _extract_text(chunk) == "hi"

    def test_object_chunk(self):
        chunk = SimpleNamespace(delta=SimpleNamespace(content="hi"))
        chunk = {"choices": [chunk]}
        assert _extract_text(chunk) == "hi"

    def test_empty_choices_returns_none(self):
        assert _extract_text({"choices": []}) is None

    def test_missing_or_non_string_content_returns_none(self):
        assert _extract_text({"choices": [{"delta": {}}]}) is None
        assert _extract_text({"choices": [{"delta": None}]}) is None
        assert _extract_text({"choices": [{"delta": {"content": 42}}]}) is None


class TestExtractTextAnthropic:
    def test_dict_chunk(self):
        chunk = {
            "type": "content_block_delta",
            "delta": {"type": "text_delta", "text": "hey"},
        }
        assert _extract_text(chunk) == "hey"

    def test_object_chunk(self):
        chunk = SimpleNamespace(
            type="content_block_delta",
            delta=SimpleNamespace(type="text_delta", text="hey"),
        )
        assert _extract_text(chunk) == "hey"

    def test_non_text_delta_returns_none(self):
        chunk = {
            "type": "content_block_delta",
            "delta": {"type": "input_json_delta", "partial_json": "{}"},
        }
        assert _extract_text(chunk) is None

    def test_missing_text_returns_none(self):
        chunk = {"type": "content_block_delta", "delta": {"type": "text_delta"}}
        assert _extract_text(chunk) is None


class TestExtractTextGemini:
    def test_dict_chunk(self):
        chunk = {"candidates": [{"content": {"parts": [{"text": "yo"}]}}]}
        assert _extract_text(chunk) == "yo"

    def test_object_chunk(self):
        chunk = SimpleNamespace(
            candidates=[SimpleNamespace(content=SimpleNamespace(parts=[SimpleNamespace(text="yo")]))]
        )
        assert _extract_text(chunk) == "yo"

    def test_empty_candidates_or_parts_return_none(self):
        assert _extract_text({"candidates": []}) is None
        assert _extract_text({"candidates": [{"content": {"parts": []}}]}) is None

    def test_non_string_text_returns_none(self):
        chunk = {"candidates": [{"content": {"parts": [{"text": None}]}}]}
        assert _extract_text(chunk) is None


class TestWrapWebsocket:
    def test_websockets_style_returned_as_is(self):
        ws = SimpleNamespace(recv=lambda: "x", send=lambda data: None, close=lambda: None)
        assert wrap_websocket(ws) is ws

    def test_asgi_style_wrapped_in_adapter(self):
        ws = SimpleNamespace(receive_text=lambda: "x", send_text=lambda data: None, close=lambda: None)
        wrapped = wrap_websocket(ws)
        assert isinstance(wrapped, _ASGIWebSocketAdapter)

    def test_unknown_style_raises_type_error(self):
        with pytest.raises(TypeError, match="Cannot wrap"):
            wrap_websocket(object())

    @pytest.mark.asyncio
    async def test_asgi_adapter_delegates(self):
        calls = []

        class FakeAsgiWebSocket:
            async def receive_text(self):
                calls.append("receive_text")
                return "hello"

            async def send_text(self, data):
                calls.append(("send_text", data))

            async def close(self):
                calls.append("close")

        adapter = _ASGIWebSocketAdapter(FakeAsgiWebSocket())

        assert await adapter.recv() == "hello"
        await adapter.send("world")
        await adapter.close()

        assert calls == ["receive_text", ("send_text", "world"), "close"]
