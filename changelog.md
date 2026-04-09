## 2.43.0 - 2026-04-09
* The `get_content` method on `DocumentsClient` (and its async counterpart) now returns the document content as a `str` instead of `None`. Similarly, the Twilio `register_call` method now returns the TwiML response body as a `str` instead of `None`, making the response data directly accessible. The SDK clients now also automatically read the `ELEVENLABS_API_KEY` environment variable as the default value for `api_key`, so explicit key passing is no longer required when the environment variable is set.

