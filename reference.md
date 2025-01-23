# Reference
## History
<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">get_all</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata about all your generated audio.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.get_all()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many history items to return at maximum. Can not exceed 1000, defaults to 100.
    
</dd>
</dl>

<dl>
<dd>

**start_after_history_item_id:** `typing.Optional[str]` — After which ID to start fetching, use this parameter to paginate across a large collection of history items. In case this parameter is not provided history items will be fetched starting from the most recently created one ordered descending by their creation date.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `typing.Optional[str]` — Voice ID to be filtered for, you can use GET https://api.elevenlabs.io/v1/voices to receive a list of voices and their IDs.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — search term used for filtering
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[HistoryGetAllRequestSource]` — Source of the generated history item
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns information about an history item by its ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.get(
    history_item_id="HISTORY_ITEM_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**history_item_id:** `str` — History item ID to be used, you can use GET https://api.elevenlabs.io/v1/history to receive a list of history items and their IDs.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a history item by its ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.delete(
    history_item_id="HISTORY_ITEM_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**history_item_id:** `str` — History item ID to be used, you can use GET https://api.elevenlabs.io/v1/history to receive a list of history items and their IDs.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">get_audio</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the audio of an history item.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.get_audio(
    history_item_id="HISTORY_ITEM_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**history_item_id:** `str` — History item ID to be used, you can use GET https://api.elevenlabs.io/v1/history to receive a list of history items and their IDs.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">download</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Download one or more history items. If one history item ID is provided, we will return a single audio file. If more than one history item IDs are provided, we will provide the history items packed into a .zip file.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.download(
    history_item_ids=["HISTORY_ITEM_ID"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**history_item_ids:** `typing.Sequence[str]` — A list of history items to download, you can get IDs of history items and other metadata using the GET https://api.elevenlabs.io/v1/history endpoint.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[str]` — Output format to transcode the audio file, can be wav or default.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## TextToSoundEffects
<details><summary><code>client.text_to_sound_effects.<a href="src/elevenlabs/text_to_sound_effects/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Converts a text of your choice into sound
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_sound_effects.convert(
    text="Spacious braam suitable for high-impact movie trailer moments",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**text:** `str` — The text that will get converted into a sound effect.
    
</dd>
</dl>

<dl>
<dd>

**duration_seconds:** `typing.Optional[float]` — The duration of the sound which will be generated in seconds. Must be at least 0.5 and at most 22. If set to None we will guess the optimal duration using the prompt. Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**prompt_influence:** `typing.Optional[float]` — A higher prompt influence makes your generation follow the prompt more closely while also making generations less variable. Must be a value between 0 and 1. Defaults to 0.3.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## AudioIsolation
## samples
<details><summary><code>client.samples.<a href="src/elevenlabs/samples/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a sample by its ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.samples.delete(
    voice_id="VOICE_ID",
    sample_id="SAMPLE_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**sample_id:** `str` — Sample ID to be used, you can use GET https://api.elevenlabs.io/v1/voices/{voice_id} to list all the available samples for a voice.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.samples.<a href="src/elevenlabs/samples/client.py">get_audio</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the audio corresponding to a sample attached to a voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.samples.get_audio(
    voice_id="VOICE_ID",
    sample_id="SAMPLE_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**sample_id:** `str` — Sample ID to be used, you can use GET https://api.elevenlabs.io/v1/voices/{voice_id} to list all the available samples for a voice.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## TextToSpeech
<details><summary><code>client.text_to_speech.<a href="src/elevenlabs/text_to_speech/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Converts text into speech using a voice of your choice and returns audio.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 supports language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[BodyTextToSpeechV1TextToSpeechVoiceIdPostApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.text_to_speech.<a href="src/elevenlabs/text_to_speech/client.py">convert_with_timestamps</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Converts text into speech using a voice of your choice and returns JSON containing audio as a base64 encoded string together with information on when which character was spoken.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.convert_with_timestamps(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 supports language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[
    BodyTextToSpeechWithTimestampsV1TextToSpeechVoiceIdWithTimestampsPostApplyTextNormalization
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.text_to_speech.<a href="src/elevenlabs/text_to_speech/client.py">convert_as_stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Converts text into speech using a voice of your choice and returns audio as an audio stream.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.convert_as_stream(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 supports language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[
    BodyTextToSpeechStreamingV1TextToSpeechVoiceIdStreamPostApplyTextNormalization
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.text_to_speech.<a href="src/elevenlabs/text_to_speech/client.py">stream_with_timestamps</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Converts text into speech using a voice of your choice and returns a stream of JSONs containing audio as a base64 encoded string together with information on when which character was spoken.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
response = client.text_to_speech.stream_with_timestamps(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)
for chunk in response:
    yield chunk

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 supports language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the flow of prosody when concatenating together multiple generations or to influence the prosody in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the flow of prosody when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[
    BodyTextToSpeechStreamingWithTimestampsV1TextToSpeechVoiceIdStreamWithTimestampsPostApplyTextNormalization
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' model.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## SpeechToSpeech
<details><summary><code>client.speech_to_speech.<a href="src/elevenlabs/speech_to_speech/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create speech by combining the content and emotion of the uploaded audio with a voice of your choice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    model_id="eleven_multilingual_sts_v2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**audio:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.speech_to_speech.<a href="src/elevenlabs/speech_to_speech/client.py">convert_as_stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create speech by combining the content and emotion of the uploaded audio with a voice of your choice and returns an audio stream.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_speech.convert_as_stream(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    model_id="eleven_multilingual_sts_v2",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**audio:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false full privacy mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Full privacy mode may only be used by enterprise customers.
    
</dd>
</dl>

<dl>
<dd>

**optimize_streaming_latency:** `typing.Optional[int]` 

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[OutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored setttings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## VoiceGeneration
<details><summary><code>client.voice_generation.<a href="src/elevenlabs/voice_generation/client.py">generate_parameters</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get possible parameters for the /v1/voice-generation/generate-voice endpoint.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voice_generation.generate_parameters()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voice_generation.<a href="src/elevenlabs/voice_generation/client.py">generate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generate a random voice based on parameters. This method returns a generated_voice_id in the response header, and a sample of the voice in the body. If you like the generated voice call /v1/voice-generation/create-voice with the generated_voice_id to create the voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voice_generation.generate(
    gender="female",
    accent="american",
    age="middle_aged",
    accent_strength=2.0,
    text="It sure does, Jackie… My mama always said: “In Carolina, the air's so thick you can wear it!”",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**gender:** `Gender` — Category code corresponding to the gender of the generated voice. Possible values: female, male.
    
</dd>
</dl>

<dl>
<dd>

**accent:** `str` — Category code corresponding to the accent of the generated voice. Possible values: british, american, african, australian, indian.
    
</dd>
</dl>

<dl>
<dd>

**age:** `Age` — Category code corresponding to the age of the generated voice. Possible values: young, middle_aged, old.
    
</dd>
</dl>

<dl>
<dd>

**accent_strength:** `float` — The strength of the accent of the generated voice. Has to be between 0.3 and 2.0.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — Text to generate, text length has to be between 100 and 1000.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voice_generation.<a href="src/elevenlabs/voice_generation/client.py">create_a_previously_generated_voice</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a previously generated voice. This endpoint should be called after you fetched a generated_voice_id using /v1/voice-generation/generate-voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voice_generation.create_a_previously_generated_voice(
    voice_name="Alex",
    voice_description="Middle-aged American woman",
    generated_voice_id="rbVJFu6SGRD1dbWpKnWl",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_name:** `str` — Name to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**voice_description:** `str` — Description to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**generated_voice_id:** `str` — The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.
    
</dd>
</dl>

<dl>
<dd>

**played_not_selected_voice_ids:** `typing.Optional[typing.Sequence[str]]` — List of voice ids that the user has played but not selected. Used for RLHF.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, str]]` — Optional, metadata to add to the created voice. Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## TextToVoice
<details><summary><code>client.text_to_voice.<a href="src/elevenlabs/text_to_voice/client.py">create_previews</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generate a custom voice based on voice description. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. If you like the a voice previewand want to create the voice call /v1/text-to-voice/create-voice-from-preview with the generated_voice_id to create the voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.create_previews(
    voice_description="A sassy little squeaky mouse",
    text="Every act of kindness, no matter how small, carries value and can make a difference, as no gesture of goodwill is ever wasted.",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_description:** `str` — Description to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — Text to generate, text length has to be between 100 and 1000.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat]` 

Output format of the generated audio. Must be one of:
mp3_22050_32 - output format, mp3 with 22.05kHz sample rate at 32kbps.
mp3_44100_32 - output format, mp3 with 44.1kHz sample rate at 32kbps.
mp3_44100_64 - output format, mp3 with 44.1kHz sample rate at 64kbps.
mp3_44100_96 - output format, mp3 with 44.1kHz sample rate at 96kbps.
mp3_44100_128 - default output format, mp3 with 44.1kHz sample rate at 128kbps.
mp3_44100_192 - output format, mp3 with 44.1kHz sample rate at 192kbps. Requires you to be subscribed to Creator tier or above.
pcm_16000 - PCM format (S16LE) with 16kHz sample rate.
pcm_22050 - PCM format (S16LE) with 22.05kHz sample rate.
pcm_24000 - PCM format (S16LE) with 24kHz sample rate.
pcm_44100 - PCM format (S16LE) with 44.1kHz sample rate. Requires you to be subscribed to Pro tier or above.
ulaw_8000 - μ-law format (sometimes written mu-law, often approximated as u-law) with 8kHz sample rate. Note that this format is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.text_to_voice.<a href="src/elevenlabs/text_to_voice/client.py">create_voice_from_preview</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using /v1/text-to-voice/create-previews.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.create_voice_from_preview(
    voice_name="Little squeaky mouse",
    voice_description="A sassy little squeaky mouse",
    generated_voice_id="37HceQefKmEi3bGovXjL",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_name:** `str` — Name to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**voice_description:** `str` — Description to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**generated_voice_id:** `str` — The generated_voice_id to create, call POST /v1/voice-generation/generate-voice and fetch the generated_voice_id from the response header if don't have one yet.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, str]]` — Optional, metadata to add to the created voice. Defaults to None.
    
</dd>
</dl>

<dl>
<dd>

**played_not_selected_voice_ids:** `typing.Optional[typing.Sequence[str]]` — List of voice ids that the user has played but not selected. Used for RLHF.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## User
<details><summary><code>client.user.<a href="src/elevenlabs/user/client.py">get_subscription</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets extended information about the users subscription
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.user.get_subscription()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.user.<a href="src/elevenlabs/user/client.py">get</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets information about the user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.user.get()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## voices
<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_all</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets a list of all available voices for a user.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_all()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**show_legacy:** `typing.Optional[bool]` — If set to true, legacy premade voices will be included in responses from /v1/voices
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_default_settings</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets the default settings for voices. "similarity_boost" corresponds to"Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_default_settings()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_settings</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the settings for a specific voice. "similarity_boost" corresponds to"Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_settings(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata about a specific voice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**with_settings:** `typing.Optional[bool]` — If set will return settings information corresponding to the voice, requires authorization.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a voice by its ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.delete(
    voice_id="VOICE_ID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">edit_settings</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit your settings for a specific voice. "similarity_boost" corresponds to"Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.edit_settings(
    voice_id="VOICE_ID",
    request=VoiceSettings(
        stability=0.1,
        similarity_boost=0.3,
        style=0.2,
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**request:** `VoiceSettings` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">add</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a new voice to your collection of voices in VoiceLab.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.add(
    name="Alex",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.
    
</dd>
</dl>

<dl>
<dd>

**files:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — How would you describe the voice?
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[str]` — Serialized labels dictionary for the voice.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">edit</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit a voice created by you.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.edit(
    voice_id="VOICE_ID",
    name="George",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.
    
</dd>
</dl>

<dl>
<dd>

**files:** `from __future__ import annotations

typing.Optional[typing.List[core.File]]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — How would you describe the voice?
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[str]` — Serialized labels dictionary for the voice.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">add_sharing_voice</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a sharing voice to your collection of voices in VoiceLab.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.add_sharing_voice(
    public_user_id="63e84100a6bf7874ba37a1bab9a31828a379ec94b891b401653b655c5110880f",
    voice_id="sB1b5zUrxQVAFl2PhZFp",
    new_name="Alita",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**public_user_id:** `str` — Public user ID used to publicly identify ElevenLabs users.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**new_name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_shared</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets a list of shared voices.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_shared(
    page_size=1,
    gender="female",
    language="en",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many shared voices to return at maximum. Can not exceed 100, defaults to 30.
    
</dd>
</dl>

<dl>
<dd>

**category:** `typing.Optional[str]` — voice category used for filtering
    
</dd>
</dl>

<dl>
<dd>

**gender:** `typing.Optional[str]` — gender used for filtering
    
</dd>
</dl>

<dl>
<dd>

**age:** `typing.Optional[str]` — age used for filtering
    
</dd>
</dl>

<dl>
<dd>

**accent:** `typing.Optional[str]` — accent used for filtering
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — language used for filtering
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — search term used for filtering
    
</dd>
</dl>

<dl>
<dd>

**use_cases:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — use-case used for filtering
    
</dd>
</dl>

<dl>
<dd>

**descriptives:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — search term used for filtering
    
</dd>
</dl>

<dl>
<dd>

**featured:** `typing.Optional[bool]` — Filter featured voices
    
</dd>
</dl>

<dl>
<dd>

**reader_app_enabled:** `typing.Optional[bool]` — Filter voices that are enabled for the reader app
    
</dd>
</dl>

<dl>
<dd>

**owner_id:** `typing.Optional[str]` — Filter voices by public owner ID
    
</dd>
</dl>

<dl>
<dd>

**sort:** `typing.Optional[str]` — sort criteria
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_similar_library_voices</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of shared voices similar to the provided audio sample. If neither similarity_threshold nor top_k is provided, we will apply default values.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_similar_library_voices()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**similarity_threshold:** `typing.Optional[float]` — Threshold for voice similarity between provided sample and library voices. Must be in range <0, 2>. The smaller the value the more similar voices will be returned.
    
</dd>
</dl>

<dl>
<dd>

**top_k:** `typing.Optional[int]` — Number of most similar voices to return. If similarity_threshold is provided, less than this number of voices may be returned. Must be in range <1, 100>.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_a_profile_page</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets a profile page based on a handle
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_a_profile_page(
    handle="talexgeorge",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**handle:** `str` — Handle for a VA's profile page
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## projects
<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">get_all</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of your projects together and its metadata.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.get_all()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">add</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new project, it can be either initialized as blank, from a document or from a URL.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.add(
    name="name",
    default_title_voice_id="default_title_voice_id",
    default_paragraph_voice_id="default_paragraph_voice_id",
    default_model_id="default_model_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the project, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**default_title_voice_id:** `str` — The voice_id that corresponds to the default voice used for new titles.
    
</dd>
</dl>

<dl>
<dd>

**default_paragraph_voice_id:** `str` — The voice_id that corresponds to the default voice used for new paragraphs.
    
</dd>
</dl>

<dl>
<dd>

**default_model_id:** `str` — The model_id of the model to be used for this project, you can query GET https://api.elevenlabs.io/v1/models to list all available models.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the project. If this is set, 'from_url' must be null. If neither 'from_url' or 'from_document' are provided we will initialize the project as blank.
    
</dd>
</dl>

<dl>
<dd>

**from_document:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**quality_preset:** `typing.Optional[str]` 

Output quality of the generated audio. Must be one of:
standard - standard output format, 128kbps with 44.1kHz sample rate.
high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.

    
</dd>
</dl>

<dl>
<dd>

**title:** `typing.Optional[str]` — An optional name of the author of the project, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**author:** `typing.Optional[str]` — An optional name of the author of the project, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the project.
    
</dd>
</dl>

<dl>
<dd>

**genres:** `typing.Optional[typing.List[str]]` — An optional list of genres associated with the project.
    
</dd>
</dl>

<dl>
<dd>

**target_audience:** `typing.Optional[ProjectsAddRequestTargetAudience]` — An optional target audience of the project.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — An optional language of the project. Two-letter language code (ISO 639-1).
    
</dd>
</dl>

<dl>
<dd>

**content_type:** `typing.Optional[str]` — An optional content type of the project.
    
</dd>
</dl>

<dl>
<dd>

**original_publication_date:** `typing.Optional[str]` — An optional original publication date of the project, in the format YYYY-MM-DD or YYYY.
    
</dd>
</dl>

<dl>
<dd>

**mature_content:** `typing.Optional[bool]` — An optional mature content of the project.
    
</dd>
</dl>

<dl>
<dd>

**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the project you want to create, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**acx_volume_normalization:** `typing.Optional[bool]` — [Deprecated] When the project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
</dd>
</dl>

<dl>
<dd>

**volume_normalization:** `typing.Optional[bool]` — When the project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.List[str]]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text.  A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'. Note that multiple dictionaries are not currently supported by our UI which will only show the first.
    
</dd>
</dl>

<dl>
<dd>

**fiction:** `typing.Optional[ProjectsAddRequestFiction]` — An optional fiction of the project.
    
</dd>
</dl>

<dl>
<dd>

**quality_check_on:** `typing.Optional[bool]` — [Depracated] Whether to run quality check on the generated audio and regenerate if needed. Applies to individual block conversion.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[ProjectsAddRequestApplyTextNormalization]` 


    This parameter controls text normalization with four modes: 'auto', 'on', 'apply_english' and 'off'.
    When set to 'auto', the system will automatically decide whether to apply text normalization 
    (e.g., spelling out numbers). With 'on', text normalization will always be applied, while 
    with 'off', it will be skipped. 'apply_english' is the same as 'on' but will assume that text is in English.
    
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.
    
</dd>
</dl>

<dl>
<dd>

**auto_assign_voices:** `typing.Optional[bool]` — [Alpha Feature] Whether automatically assign voices to phrases in the create Project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns information about a specific project. This endpoint returns more detailed information about a project than GET api.elevenlabs.io/v1/projects.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">edit_basic_project_info</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edits basic project info.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.edit_basic_project_info(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="name",
    default_title_voice_id="default_title_voice_id",
    default_paragraph_voice_id="default_paragraph_voice_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the project, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**default_title_voice_id:** `str` — The voice_id that corresponds to the default voice used for new titles.
    
</dd>
</dl>

<dl>
<dd>

**default_paragraph_voice_id:** `str` — The voice_id that corresponds to the default voice used for new paragraphs.
    
</dd>
</dl>

<dl>
<dd>

**title:** `typing.Optional[str]` — An optional name of the author of the project, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**author:** `typing.Optional[str]` — An optional name of the author of the project, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the project you want to create, this will be added as metadata to the mp3 file on project / chapter download.
    
</dd>
</dl>

<dl>
<dd>

**volume_normalization:** `typing.Optional[bool]` — When the project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
</dd>
</dl>

<dl>
<dd>

**quality_check_on:** `typing.Optional[bool]` — [Depracated] Whether to run quality check on the generated audio and regenerate if needed. Applies to individual block conversion.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a project by its project_id.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.delete(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">update_content</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edits project content.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.update_content(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the project. If this is set, 'from_url' must be null. If neither 'from_url' or 'from_document' are provided we will initialize the project as blank.
    
</dd>
</dl>

<dl>
<dd>

**from_document:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Starts conversion of a project and all of its chapters.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.convert(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">get_snapshots</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets the snapshots of a project.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.get_snapshots(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">stream_archive</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Streams archive with project audio.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.stream_archive(
    project_id="21m00Tcm4TlvDq8ikWAM",
    project_snapshot_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**project_snapshot_id:** `str` — The project_snapshot_id of the project snapshot. You can query GET /v1/projects/{project_id}/snapshots to list all available snapshots for a project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.projects.<a href="src/elevenlabs/projects/client.py">update_pronunciation_dictionaries</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the set of pronunciation dictionaries acting on a project. This will automatically mark text within this project as requiring reconverting where the new dictionary would apply or the old one no longer does.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs, PronunciationDictionaryVersionLocator

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.projects.update_pronunciation_dictionaries(
    project_id="21m00Tcm4TlvDq8ikWAM",
    pronunciation_dictionary_locators=[
        PronunciationDictionaryVersionLocator(
            pronunciation_dictionary_id="pronunciation_dictionary_id",
            version_id="version_id",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Sequence[PronunciationDictionaryVersionLocator]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text.  A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'. Note that multiple dictionaries are not currently supported by our UI which will only show the first.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Chapters
<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">get_all</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of your chapters for a project together and its metadata.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.get_all(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns information about a specific chapter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a chapter by its chapter_id.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.delete(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new chapter either as blank or from a URL.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.create(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the chapter, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the project. If this is set, 'from_url' must be null. If neither 'from_url' or 'from_document' are provided we will initialize the project as blank.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Starts conversion of a specific chapter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.convert(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">get_all_snapshots</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets information about all the snapshots of a chapter, each snapshot corresponds can be downloaded as audio. Whenever a chapter is converted a snapshot will be automatically created.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.get_all_snapshots(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.chapters.<a href="src/elevenlabs/chapters/client.py">stream_snapshot</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Stream the audio from a chapter snapshot. Use `GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots` to return the chapter snapshots of a chapter.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.chapters.stream_snapshot(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
    chapter_snapshot_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The chapter_id of the chapter. You can query GET https://api.elevenlabs.io/v1/projects/{project_id}/chapters to list all available chapters for a project.
    
</dd>
</dl>

<dl>
<dd>

**chapter_snapshot_id:** `str` — The chapter_snapshot_id of the chapter snapshot. You can query GET /v1/projects/{project_id}/chapters/{chapter_id}/snapshots to the all available snapshots for a chapter.
    
</dd>
</dl>

<dl>
<dd>

**convert_to_mpeg:** `typing.Optional[bool]` — Whether to convert the audio to mpeg format.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Dubbing
<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">dub_a_video_or_an_audio_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Dubs provided audio or video file into given language.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.dub_a_video_or_an_audio_file(
    target_lang="target_lang",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**target_lang:** `str` — The Target language to dub the content into.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — Name of the dubbing project.
    
</dd>
</dl>

<dl>
<dd>

**source_url:** `typing.Optional[str]` — URL of the source video/audio file.
    
</dd>
</dl>

<dl>
<dd>

**source_lang:** `typing.Optional[str]` — Source language.
    
</dd>
</dl>

<dl>
<dd>

**num_speakers:** `typing.Optional[int]` — Number of speakers to use for the dubbing. Set to 0 to automatically detect the number of speakers
    
</dd>
</dl>

<dl>
<dd>

**watermark:** `typing.Optional[bool]` — Whether to apply watermark to the output video.
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[int]` — Start time of the source video/audio file.
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[int]` — End time of the source video/audio file.
    
</dd>
</dl>

<dl>
<dd>

**highest_resolution:** `typing.Optional[bool]` — Whether to use the highest resolution available.
    
</dd>
</dl>

<dl>
<dd>

**drop_background_audio:** `typing.Optional[bool]` — An advanced setting. Whether to drop background audio from the final dub. This can improve dub quality where it's known that audio shouldn't have a background track such as for speeches or monologues.
    
</dd>
</dl>

<dl>
<dd>

**use_profanity_filter:** `typing.Optional[bool]` — [BETA] Whether transcripts should have profanities censored with the words '[censored]'
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">get_dubbing_project_metadata</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata about a dubbing project, including whether it's still in progress or not
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.get_dubbing_project_metadata(
    dubbing_id="dubbing_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**dubbing_id:** `str` — ID of the dubbing project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">delete_dubbing_project</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a dubbing project.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.delete_dubbing_project(
    dubbing_id="dubbing_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**dubbing_id:** `str` — ID of the dubbing project.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">get_transcript_for_dub</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns transcript for the dub as an SRT file.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.get_transcript_for_dub(
    dubbing_id="dubbing_id",
    language_code="language_code",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**dubbing_id:** `str` — ID of the dubbing project.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `str` — ID of the language.
    
</dd>
</dl>

<dl>
<dd>

**format_type:** `typing.Optional[DubbingGetTranscriptForDubRequestFormatType]` — Format to use for the subtitle file, either 'srt' or 'webvtt'
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## models
<details><summary><code>client.models.<a href="src/elevenlabs/models/client.py">get_all</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets a list of available models.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.models.get_all()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## AudioNative
<details><summary><code>client.audio_native.<a href="src/elevenlabs/audio_native/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates AudioNative enabled project, optionally starts conversion and returns project id and embeddable html snippet.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.audio_native.create(
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Project name.
    
</dd>
</dl>

<dl>
<dd>

**image:** `typing.Optional[str]` — (Deprecated) Image URL used in the player. If not provided, default image set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**author:** `typing.Optional[str]` — Author used in the player and inserted at the start of the uploaded article. If not provided, the default author set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**title:** `typing.Optional[str]` — Title used in the player and inserted at the top of the uploaded article. If not provided, the default title set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**small:** `typing.Optional[bool]` — (Deprecated) Whether to use small player or not. If not provided, default value set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**text_color:** `typing.Optional[str]` — Text color used in the player. If not provided, default text color set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**background_color:** `typing.Optional[str]` — Background color used in the player. If not provided, default background color set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**sessionization:** `typing.Optional[int]` — (Deprecated) Specifies for how many minutes to persist the session across page reloads. If not provided, default sessionization set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `typing.Optional[str]` — Voice ID used to voice the content. If not provided, default voice ID set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — TTS Model ID used in the player. If not provided, default model ID set in the Player settings is used.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.audio_native.<a href="src/elevenlabs/audio_native/client.py">update_content</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates content for the specific AudioNative Project.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.audio_native.update_content(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The project_id of the project, you can query GET https://api.elevenlabs.io/v1/projects to list all available projects.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.
    
</dd>
</dl>

<dl>
<dd>

**auto_publish:** `typing.Optional[bool]` — Whether to auto publish the new project snapshot after it's converted.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Usage
<details><summary><code>client.usage.<a href="src/elevenlabs/usage/client.py">get_characters_usage_metrics</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the credit usage metrics for the current user or the entire workspace they are part of. The response will return a time axis with unix timestamps for each day and daily usage along that axis. The usage will be broken down by the specified breakdown type. For example, breakdown type "voice" will return the usage of each voice along the time axis.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.usage.get_characters_usage_metrics(
    start_unix=1,
    end_unix=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**start_unix:** `int` — UTC Unix timestamp for the start of the usage window, in milliseconds. To include the first day of the window, the timestamp should be at 00:00:00 of that day.
    
</dd>
</dl>

<dl>
<dd>

**end_unix:** `int` — UTC Unix timestamp for the end of the usage window, in milliseconds. To include the last day of the window, the timestamp should be at 23:59:59 of that day.
    
</dd>
</dl>

<dl>
<dd>

**include_workspace_metrics:** `typing.Optional[bool]` — Whether or not to include the statistics of the entire workspace.
    
</dd>
</dl>

<dl>
<dd>

**breakdown_type:** `typing.Optional[BreakdownTypes]` — How to break down the information. Cannot be "user" if include_workspace_metrics is False.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## PronunciationDictionary
<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">add_from_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new pronunciation dictionary from a lexicon .PLS file
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.add_from_file(
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the pronunciation dictionary, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — A description of the pronunciation dictionary, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**workspace_access:** `typing.Optional[PronunciationDictionaryAddFromFileRequestWorkspaceAccess]` — Should be one of 'editor' or 'viewer'. If not provided, defaults to no access.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">add_rules</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add rules to the pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs
from elevenlabs.pronunciation_dictionary import (
    PronunciationDictionaryRule_Phoneme,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.add_rules(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
    rules=[
        PronunciationDictionaryRule_Phoneme(
            string_to_replace="rules",
            phoneme="rules",
            alphabet="rules",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**rules:** `typing.Sequence[PronunciationDictionaryRule]` 

List of pronunciation rules. Rule can be either:
    an alias rule: {'string_to_replace': 'a', 'type': 'alias', 'alias': 'b', }
    or a phoneme rule: {'string_to_replace': 'a', 'type': 'phoneme', 'phoneme': 'b', 'alphabet': 'ipa' }
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">remove_rules</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove rules from the pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.remove_rules(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
    rule_strings=["rule_strings"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**rule_strings:** `typing.Sequence[str]` — List of strings to remove from the pronunciation dictionary.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">download</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get PLS file with a pronunciation dictionary version rules
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.download(
    dictionary_id="Fm6AvNgS53NXe6Kqxp3e",
    version_id="KZFyRUq3R6kaqhKI146w",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**dictionary_id:** `str` — The id of the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**version_id:** `str` — The id of the version of the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get metadata for a pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.get(
    pronunciation_dictionary_id="Fm6AvNgS53NXe6Kqxp3e",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dictionary.<a href="src/elevenlabs/pronunciation_dictionary/client.py">get_all</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a list of the pronunciation dictionaries you have access to and their metadata
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionary.get_all(
    page_size=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many pronunciation dictionaries to return at maximum. Can not exceed 100, defaults to 30.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Workspace
<details><summary><code>client.workspace.<a href="src/elevenlabs/workspace/client.py">invite_user</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sends an email invitation to join your workspace to the provided email. If the user doesn't have an account they will be prompted to create one. If the user accepts this invite they will be added as a user to your workspace and your subscription using one of your seats. This endpoint may only be called by workspace administrators.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.invite_user(
    email="email",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — The email of the customer
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.workspace.<a href="src/elevenlabs/workspace/client.py">delete_existing_invitation</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Invalidates an existing email invitation. The invitation will still show up in the inbox it has been delivered to, but activating it to join the workspace won't work. This endpoint may only be called by workspace administrators.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.delete_existing_invitation(
    email="email",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — The email of the customer
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.workspace.<a href="src/elevenlabs/workspace/client.py">update_member</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates attributes of a workspace member. Apart from the email identifier, all parameters will remain unchanged unless specified. This endpoint may only be called by workspace administrators.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.update_member(
    email="email",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — Email of the target user.
    
</dd>
</dl>

<dl>
<dd>

**is_locked:** `typing.Optional[bool]` — Whether to lock or unlock the user account.
    
</dd>
</dl>

<dl>
<dd>

**workspace_role:** `typing.Optional[BodyUpdateMemberV1WorkspaceMembersPostWorkspaceRole]` — Role dictating permissions in the workspace.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ConversationalAi
<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_signed_url</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a signed url to start a conversation with an agent with an agent that requires authorization
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_signed_url(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of the agent you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">create_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create an agent from a config object
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ConversationalConfig, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.create_agent(
    conversation_config=ConversationalConfig(),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_config:** `ConversationalConfig` — Conversation configuration for an agent
    
</dd>
</dl>

<dl>
<dd>

**platform_settings:** `typing.Optional[AgentPlatformSettings]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A name to make the agent easier to find
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve config for an agent
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_agent(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">delete_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete an agent
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.delete_agent(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">update_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Patches an Agent settings
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.update_agent(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**conversation_config:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — Conversation configuration for an agent
    
</dd>
</dl>

<dl>
<dd>

**platform_settings:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.
    
</dd>
</dl>

<dl>
<dd>

**secrets:** `typing.Optional[
    typing.Sequence[
        BodyPatchesAnAgentSettingsV1ConvaiAgentsAgentIdPatchSecretsItem
    ]
]` — A list of secrets for the agent. Can be used to add new secrets or update and delete the existing ones
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A name to make the agent easier to find
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_agent_widget</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the widget configuration for an agent
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_agent_widget(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**conversation_signature:** `typing.Optional[str]` — An expiring token that enables a conversation to start. These can be generated for an agent using the /v1/convai/conversation/get_signed_url endpoint
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_agent_link</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the current link used to share the agent with others
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_agent_link(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">post_agent_avatar</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sets the avatar for an agent displayed in the widget
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.post_agent_avatar(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**avatar_file:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_agent_knowledge_base_document_by_id</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details about a specific documentation making up the agent's knowledge base
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_agent_knowledge_base_document_by_id(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    documentation_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**documentation_id:** `str` — The id of a document from the agent's knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">add_agent_secret</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Uploads a file or reference a webpage for the agent to use as part of it's knowledge base
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.add_agent_secret(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    name="name",
    secret_value="secret_value",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — A name to help identify a particular agent secret
    
</dd>
</dl>

<dl>
<dd>

**secret_value:** `str` — A value to be encrypted and used by the agent
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">add_to_agent_knowledge_base</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Uploads a file or reference a webpage for the agent to use as part of it's knowledge base
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.add_to_agent_knowledge_base(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` — URL to a page of documentation that the agent will have access to in order to interact with users.
    
</dd>
</dl>

<dl>
<dd>

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_agents</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a page of your agents and their metadata.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_agents()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many Agents to return at maximum. Can not exceed 100, defaults to 30.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search by agents name.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_conversations</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all conversations of agents that user owns. With option to restrict to a specific agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_conversations(
    agent_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — The id of the agent you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**call_successful:** `typing.Optional[EvaluationSuccessResult]` — The result of the success evaluation
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many conversations to return at maximum. Can not exceed 100, defaults to 30.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_conversation</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the details of a particular conversation
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_conversation(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_id:** `str` — The id of the conversation you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">delete_conversation</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a particular conversation
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.delete_conversation(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_id:** `str` — The id of the conversation you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_conversation_audio</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the audio recording of a particular conversation
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_conversation_audio(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_id:** `str` — The id of the conversation you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">post_conversation_feedback</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Send the feedback for the given conversation
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.post_conversation_feedback(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
    feedback="like",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**conversation_id:** `str` — The id of the conversation you're taking the action on.
    
</dd>
</dl>

<dl>
<dd>

**feedback:** `UserFeedbackScore` — Either 'like' or 'dislike' to indicate the feedback for the conversation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">create_phone_number</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Import Phone Number from Twilio configuration
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.create_phone_number(
    phone_number="phone_number",
    label="label",
    sid="sid",
    token="token",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — Phone number
    
</dd>
</dl>

<dl>
<dd>

**label:** `str` — Label for the phone number
    
</dd>
</dl>

<dl>
<dd>

**sid:** `str` — Twilio Account SID
    
</dd>
</dl>

<dl>
<dd>

**token:** `str` — Twilio Token
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_phone_number</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve Phone Number details by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_phone_number(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">delete_phone_number</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete Phone Number by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.delete_phone_number(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">update_phone_number</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update Phone Number details by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.update_phone_number(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_phone_numbers</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all Phone Numbers
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_phone_numbers()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

