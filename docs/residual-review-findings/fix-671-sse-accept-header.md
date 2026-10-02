## Residual Review Findings

- P2 — `src/elevenlabs/core/http_sse/_api.py:93` — Broadened Accept header breaks strict servers, invites JSON responses — filed as [elevenlabs-python#847](https://github.com/elevenlabs/elevenlabs-python/issues/847)
- P2 — `src/elevenlabs/core/http_sse/_api.py:93` — Broadened Accept header breaks strict servers, invites JSON responses — settled_conflict with KTD-1 (session-settled, user-approved: send combined `application/json, text/event-stream`; caller-supplied Accept overwrite is an explicit non-goal). Preference-grade alternative (`headers.setdefault(...)`), routed advisory/human, report-only — not applied.

Source run context: ce-code-review run 20260815-232345-90a6cd57 on branch fix/671-sse-accept-header (base origin/main ea95897, head 584ae39), review of fix for issue #671 (SSE Accept header). Reviewers: correctness, project-standards, testing, adversarial (in-process fallback; cross-model peer not started — host un-attestable).
