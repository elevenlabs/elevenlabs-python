"""SpeechEngineSession — WebSocket session for Speech Engine conversations."""

import asyncio
import json
import logging
import typing

from .types import ConversationMessage, WebSocketLike, wrap_websocket

logger = logging.getLogger("elevenlabs.speech_engine")


def _make_log(
    debug: bool,
) -> typing.Callable[..., None]:
    """Return a per-instance log function, mirroring the JS SDK pattern."""
    if debug:
        def _log(msg: str, *args: typing.Any) -> None:
            print("[SpeechEngine]", msg % args if args else msg)
        return _log
    return lambda *_args, **_kw: None

Callback = typing.Callable[..., typing.Any]


# ---------------------------------------------------------------------------
# LLM stream text extraction
# ---------------------------------------------------------------------------


def _get(obj: typing.Any, key: str) -> typing.Any:
    """Attribute-or-key access helper for LLM stream chunks."""
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _extract_text(chunk: typing.Any) -> typing.Optional[str]:
    """Extract text content from an LLM stream chunk.

    Handles plain strings and common LLM streaming formats:

    - OpenAI Responses API  (``response.output_text.delta``)
    - OpenAI Chat Completions API (``choices[0].delta.content``)
    - Anthropic Messages API (``content_block_delta`` with ``text_delta``)
    - Google Gemini API (``candidates[0].content.parts[0].text``)
    """
    if isinstance(chunk, str):
        return chunk
    if chunk is None or isinstance(chunk, (int, float, bool)):
        return None

    # OpenAI Responses API
    if _get(chunk, "type") == "response.output_text.delta":
        delta = _get(chunk, "delta")
        if isinstance(delta, str):
            return delta

    # OpenAI Chat Completions API
    choices = _get(chunk, "choices")
    if isinstance(choices, (list, tuple)) and len(choices) > 0:
        delta = _get(choices[0], "delta")
        if delta is not None:
            content = _get(delta, "content")
            if isinstance(content, str):
                return content

    # Anthropic Messages API
    if _get(chunk, "type") == "content_block_delta":
        delta = _get(chunk, "delta")
        if delta is not None:
            if _get(delta, "type") == "text_delta":
                text = _get(delta, "text")
                if isinstance(text, str):
                    return text

    # Google Gemini API
    candidates = _get(chunk, "candidates")
    if isinstance(candidates, (list, tuple)) and len(candidates) > 0:
        content = _get(candidates[0], "content")
        if content is not None:
            parts = _get(content, "parts")
            if isinstance(parts, (list, tuple)) and len(parts) > 0:
                text = _get(parts[0], "text")
                if isinstance(text, str):
                    return text

    return None


# ---------------------------------------------------------------------------
# Handler wiring (kwargs -> event emitter)
# ---------------------------------------------------------------------------


def _wire_handlers(
    session: "SpeechEngineSession",
    handlers: typing.Dict[str, typing.Any],
) -> None:
    """Wire keyword-argument handlers onto *session* events."""
    on_init = handlers.get("on_init")
    on_transcript = handlers.get("on_transcript")
    on_close = handlers.get("on_close")
    on_disconnect = handlers.get("on_disconnect")
    on_error = handlers.get("on_error")

    if on_init:
        async def _init_handler(conversation_id: str) -> None:
            result = on_init(conversation_id, session)
            if asyncio.iscoroutine(result):
                await result
        session.on("init", _init_handler)

    if on_transcript:
        async def _transcript_handler(
            transcript: typing.List[ConversationMessage],
        ) -> None:
            result = on_transcript(transcript, session)
            if asyncio.iscoroutine(result):
                await result
        session.on("user_transcript", _transcript_handler)

    if on_close:
        async def _close_handler() -> None:
            result = on_close(session)
            if asyncio.iscoroutine(result):
                await result
        session.on("close", _close_handler)

    if on_disconnect:
        async def _disconnect_handler() -> None:
            result = on_disconnect(session)
            if asyncio.iscoroutine(result):
                await result
        session.on("disconnected", _disconnect_handler)

    if on_error:
        async def _error_handler(err: Exception) -> None:
            result = on_error(err, session)
            if asyncio.iscoroutine(result):
                await result
        session.on("error", _error_handler)


# ---------------------------------------------------------------------------
# SpeechEngineSession
# ---------------------------------------------------------------------------


class SpeechEngineSession:
    """Wraps a WebSocket connection from the ElevenLabs Speech Engine API.

    Each connection represents one conversation.  The session emits events
    for transcripts and lifecycle changes, and provides methods to send LLM
    responses back.  When a new transcript arrives the previous transcript's
    handler task is cancelled automatically, interrupting any in-flight LLM
    call.

    Example::

        session = SpeechEngineSession(ws, debug=True)

        async def handle(transcript):
            stream = await openai.responses.create(...)
            await session.send_response(stream)

        session.on("user_transcript", handle)
        await session.run()
    """

    def __init__(
        self,
        ws: typing.Any,
        *,
        debug: bool = False,
    ) -> None:
        self._ws = wrap_websocket(ws)
        self._conversation_id = None  # type: typing.Optional[str]
        self._current_task = None  # type: typing.Optional[asyncio.Task]  # type: ignore[type-arg]
        self._current_event_id = None  # type: typing.Optional[int]
        self._closed = False
        self._event_handlers = {}  # type: typing.Dict[str, typing.List[Callback]]
        self._once_handlers = {}  # type: typing.Dict[str, typing.List[Callback]]
        self._log = _make_log(debug)

    # ------------------------------------------------------------------
    # Event emitter interface
    # ------------------------------------------------------------------

    def on(self, event: str, handler: Callback) -> "SpeechEngineSession":
        """Register *handler* for *event*."""
        self._event_handlers.setdefault(event, []).append(handler)
        return self

    def off(self, event: str, handler: Callback) -> "SpeechEngineSession":
        """Remove *handler* from *event*."""
        handlers = self._event_handlers.get(event, [])
        try:
            handlers.remove(handler)
        except ValueError:
            pass
        return self

    def once(self, event: str, handler: Callback) -> "SpeechEngineSession":
        """Register *handler* for *event*, removed after the first call."""
        self._once_handlers.setdefault(event, []).append(handler)
        return self

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def conversation_id(self) -> typing.Optional[str]:
        """The conversation ID assigned by the Speech Engine API.

        Available after the ``init`` event fires.
        """
        return self._conversation_id

    @property
    def is_open(self) -> bool:
        """Whether the session is still open."""
        return not self._closed

    # ------------------------------------------------------------------
    # Main message loop
    # ------------------------------------------------------------------

    async def run(self) -> None:
        """Run the receive loop until the WebSocket closes.

        This is the main entry point after constructing a session.  It
        processes incoming messages and dispatches events to registered
        handlers.
        """
        try:
            while not self._closed:
                try:
                    raw = await self._ws.recv()
                except asyncio.CancelledError:
                    raise
                except Exception:
                    self._log("WebSocket connection lost")
                    break

                try:
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8")
                    msg = json.loads(raw)
                except (ValueError, TypeError, UnicodeDecodeError) as e:
                    await self._emit("error", e)
                    continue

                await self._handle_message(msg)
        except asyncio.CancelledError:
            raise
        finally:
            if not self._closed:
                self._closed = True
                await self._cancel_current_and_wait()
                await self._emit("disconnected")

    # ------------------------------------------------------------------
    # Sending responses
    # ------------------------------------------------------------------

    async def send_response(
        self,
        response: typing.Any,
    ) -> None:
        """Send an LLM response back for TTS synthesis.

        Accepts:

        * A plain **string** — sent as a single agent response.
        * An **async iterator** yielding strings or LLM stream event objects
          (OpenAI, Anthropic, Gemini formats are auto-detected).

        This method is a coroutine so the caller can ``await`` it to know
        when the full response has been sent.
        """
        if self._closed:
            raise RuntimeError("Cannot send response: session is closed")

        if self._current_event_id is None:
            logger.warning(
                "sendResponse() called outside of an on_transcript handler. "
                "Responses can only be sent in reply to a user transcript. "
                "To have the agent speak first, set a first message in your "
                "Speech Engine conversation config on the client."
            )
            return

        if isinstance(response, str):
            self._log(
                'sending string response: "%s", event_id=%s',
                response,
                self._current_event_id,
            )
            await self._send_agent_response(response, False)
            await self._send_agent_response("", True)
        else:
            self._log(
                "starting streamed response, event_id=%s",
                self._current_event_id,
            )
            await self._stream_response(response)

    def close(self) -> None:
        """Close the session and the underlying WebSocket connection."""
        if self._closed:
            return
        self._closed = True
        self._cancel_current()
        try:
            asyncio.ensure_future(self._ws.close())
        except RuntimeError:
            # No running event loop — best-effort.
            pass

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    async def _handle_message(self, msg: typing.Dict[str, typing.Any]) -> None:
        msg_type = msg.get("type")

        if msg_type == "init":
            self._conversation_id = msg.get("conversation_id")
            self._log(
                "session initialized, conversation_id=%s",
                self._conversation_id,
            )
            await self._emit("init", self._conversation_id)

        elif msg_type == "user_transcript":
            incoming_event_id = msg.get("event_id")

            if (
                incoming_event_id == self._current_event_id
                and self._current_task is not None
                and not self._current_task.done()
            ):
                self._log(
                    "skipping duplicate transcript, event_id=%s",
                    incoming_event_id,
                )
                return

            was_active = (
                self._current_task is not None
                and not self._current_task.done()
            )
            await self._cancel_current_and_wait()
            if was_active:
                self._log(
                    "interrupted: cancelling previous response "
                    "(event_id=%s) for new transcript (event_id=%s)",
                    self._current_event_id,
                    incoming_event_id,
                )

            self._current_event_id = incoming_event_id
            transcript_data = msg.get("user_transcript", [])
            self._log(
                "received transcript, event_id=%s, messages=%d",
                self._current_event_id,
                len(transcript_data),
            )

            try:
                transcript = [
                    ConversationMessage(role=m["role"], content=m["content"])
                    for m in transcript_data
                ]
            except (KeyError, TypeError) as e:
                await self._emit("error", e)
                return

            handlers = list(
                self._event_handlers.get("user_transcript", [])
            )
            once_handlers = self._once_handlers.pop("user_transcript", [])
            all_handlers = handlers + once_handlers

            if all_handlers:
                self._current_task = asyncio.create_task(
                    self._run_transcript_handlers(all_handlers, transcript)
                )
                # Yield so the handler task can start before the next
                # message is read.  This mirrors the JS behaviour where
                # emitter.emit() invokes listeners synchronously.
                await asyncio.sleep(0)

        elif msg_type == "ping":
            await self._send({"type": "pong"})

        elif msg_type == "close":
            await self._cancel_current_and_wait()
            await self._emit("close")

        elif msg_type == "error":
            await self._emit("error", Exception(msg.get("message", "")))

        # Unknown types are silently ignored for forward compatibility.

    async def _run_transcript_handlers(
        self,
        handlers: typing.List[Callback],
        transcript: typing.List[ConversationMessage],
    ) -> None:
        try:
            for handler in handlers:
                result = handler(transcript)
                if asyncio.iscoroutine(result):
                    await result
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self._emit("error", e)

    async def _stream_response(self, stream: typing.Any) -> None:
        event_id = self._current_event_id
        chunks = 0
        try:
            async for chunk in stream:
                if self._closed:
                    self._log(
                        "stream stopped: session closed after %d chunks, "
                        "event_id=%s",
                        chunks,
                        event_id,
                    )
                    return
                text = _extract_text(chunk)
                if text:
                    chunks += 1
                    await self._send_agent_response(text, False, event_id)
            if not self._closed:
                self._log(
                    "stream complete: %d chunks sent, event_id=%s",
                    chunks,
                    event_id,
                )
                await self._send_agent_response("", True, event_id)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            await self._emit("error", e)

    async def _send_agent_response(
        self,
        content: str,
        is_final: bool,
        event_id: typing.Optional[int] = None,
    ) -> None:
        if event_id is None:
            event_id = self._current_event_id
        await self._send(
            {
                "type": "agent_response",
                "content": content,
                "event_id": event_id,
                "is_final": is_final,
            }
        )

    async def _send(self, msg: typing.Dict[str, typing.Any]) -> None:
        if self._closed:
            return
        try:
            await self._ws.send(json.dumps(msg))
        except asyncio.CancelledError:
            raise
        except Exception:
            # Send failed — the recv loop will detect the closed connection.
            pass

    async def _emit(self, event: str, *args: typing.Any) -> None:
        handlers = list(self._event_handlers.get(event, []))
        once_handlers = self._once_handlers.pop(event, [])
        all_handlers = handlers + once_handlers

        for handler in all_handlers:
            try:
                result = handler(*args)
                if asyncio.iscoroutine(result):
                    await result
            except asyncio.CancelledError:
                raise
            except Exception as e:
                if event != "error":
                    await self._emit("error", e)
                else:
                    logger.exception("unhandled error in error handler")

    async def _cancel_current_and_wait(self) -> None:
        """Cancel the current handler task and wait for cleanup."""
        task = self._current_task
        self._current_task = None
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass

    def _cancel_current(self) -> None:
        """Cancel the current handler task (fire-and-forget)."""
        if self._current_task is not None and not self._current_task.done():
            self._current_task.cancel()
        self._current_task = None
