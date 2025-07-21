# Reference
## History
<details><summary><code>client.history.<a href="src/elevenlabs/history/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of your generated audio.
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
client.history.list()

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

**voice_id:** `typing.Optional[str]` — ID of the voice to be filtered for. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search term used for filtering history items. If provided, source becomes required.
    
</dd>
</dl>

<dl>
<dd>

**source:** `typing.Optional[HistoryListRequestSource]` — Source of the generated history item
    
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

Retrieves a history item.
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
    history_item_id="VW7YKqPnjY4h39yTbx2L",
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

**history_item_id:** `str` — ID of the history item to be used. You can use the [Get generated items](/docs/api-reference/history/get-all) endpoint to retrieve a list of history items.
    
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
    history_item_id="VW7YKqPnjY4h39yTbx2L",
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

**history_item_id:** `str` — ID of the history item to be used. You can use the [Get generated items](/docs/api-reference/history/get-all) endpoint to retrieve a list of history items.
    
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

Turn text into sound effects for your videos, voice-overs or video games using the most advanced sound effects model in the world.
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

**output_format:** `typing.Optional[TextToSoundEffectsConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
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
## Samples
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
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**sample_id:** `str` — ID of the sample to be used. You can use the [Get voices](/docs/api-reference/voices/get) endpoint list all the available samples for a voice.
    
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

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[TextToSpeechConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.
    
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

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[BodyTextToSpeechV1TextToSpeechVoiceIdPostApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' or 'eleven_flash_v2_5' models.
    
</dd>
</dl>

<dl>
<dd>

**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.
    
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

Generate speech from text with precise character-level timing information for audio-text synchronization.
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
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="This is a test for the API of ElevenLabs.",
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

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[TextToSpeechConvertWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.
    
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

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
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
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' or 'eleven_flash_v2_5' models.
    
</dd>
</dl>

<dl>
<dd>

**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.
    
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

<details><summary><code>client.text_to_speech.<a href="src/elevenlabs/text_to_speech/client.py">stream</a>(...)</code></summary>
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
client.text_to_speech.stream(
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

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[TextToSpeechStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.
    
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

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
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
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' or 'eleven_flash_v2_5' models.
    
</dd>
</dl>

<dl>
<dd>

**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.
    
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
for chunk in response.data:
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

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text that will get converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[TextToSpeechStreamWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model. Currently only Turbo v2.5 and Flash v2.5 support language enforcement. For other models, an error will be returned if language code is provided.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.
    
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

**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.
    
</dd>
</dl>

<dl>
<dd>

**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.
    
</dd>
</dl>

<dl>
<dd>

**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.
    
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
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. Cannot be turned on for 'eleven_turbo_v2_5' or 'eleven_flash_v2_5' models.
    
</dd>
</dl>

<dl>
<dd>

**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.
    
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

## TextToDialogue
<details><summary><code>client.text_to_dialogue.<a href="src/elevenlabs/text_to_dialogue/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Warning>Eleven v3 API access is currently not publicly available, but will be soon.</Warning><br/>Converts a list of text and voice ID pairs into speech (dialogue) and returns audio.
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
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_dialogue.convert(
    inputs=[
        DialogueInput(
            text="Knock knock",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
        ),
        DialogueInput(
            text="Who is there?",
            voice_id="Aw4FAjKCGjjNkVhN1Xmq",
        ),
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

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[TextToDialogueConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.text_to_dialogue.<a href="src/elevenlabs/text_to_dialogue/client.py">stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

<Warning>Eleven v3 API access is currently not publicly available, but will be soon.</Warning><br/>Converts a list of text and voice ID pairs into speech (dialogue) and returns an audio stream.
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
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_dialogue.stream(
    inputs=[
        DialogueInput(
            text="Knock knock",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
        ),
        DialogueInput(
            text="Who is there?",
            voice_id="Aw4FAjKCGjjNkVhN1Xmq",
        ),
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

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `typing.Optional[TextToDialogueStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.
    
</dd>
</dl>

<dl>
<dd>

**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
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

Transform audio from one voice to another. Maintain full control over emotion, timing and delivery.
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

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[SpeechToSpeechConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set, will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.
    
</dd>
</dl>

<dl>
<dd>

**file_format:** `typing.Optional[SpeechToSpeechConvertRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.
    
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

<details><summary><code>client.speech_to_speech.<a href="src/elevenlabs/speech_to_speech/client.py">stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Stream audio from one voice to another. Maintain full control over emotion, timing and delivery.
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
client.speech_to_speech.stream(
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

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**output_format:** `typing.Optional[SpeechToSpeechStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.
    
</dd>
</dl>

<dl>
<dd>

**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set, will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.
    
</dd>
</dl>

<dl>
<dd>

**file_format:** `typing.Optional[SpeechToSpeechStreamRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.
    
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

## TextToVoice
<details><summary><code>client.text_to_voice.<a href="src/elevenlabs/text_to_voice/client.py">create_previews</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a voice from a text prompt.
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
    voice_description="A sassy squeaky mouse",
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

**output_format:** `typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat]` — The output format of the generated audio.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[str]` — Text to generate, text length has to be between 100 and 1000.
    
</dd>
</dl>

<dl>
<dd>

**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.
    
</dd>
</dl>

<dl>
<dd>

**loudness:** `typing.Optional[float]` — Controls the volume level of the generated voice. -1 is quietest, 1 is loudest, 0 corresponds to roughly -24 LUFS.
    
</dd>
</dl>

<dl>
<dd>

**quality:** `typing.Optional[float]` — Higher quality results in better voice output but less variety.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — Random number that controls the voice generation. Same seed with same inputs produces same voice.
    
</dd>
</dl>

<dl>
<dd>

**guidance_scale:** `typing.Optional[float]` — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.
    
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

Add a generated voice to the voice library.
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
    voice_name="Sassy squeaky mouse",
    voice_description="A sassy squeaky mouse",
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

**generated_voice_id:** `str` — The generated_voice_id to create, call POST /v1/text-to-voice/create-previews and fetch the generated_voice_id from the response header if don't have one yet.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Optional, metadata to add to the created voice. Defaults to None.
    
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

<details><summary><code>client.text_to_voice.<a href="src/elevenlabs/text_to_voice/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using POST /v1/text-to-voice/design or POST /v1/text-to-voice/:voice_id/remix.
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
client.text_to_voice.create(
    voice_name="Sassy squeaky mouse",
    voice_description="A sassy squeaky mouse",
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

**generated_voice_id:** `str` — The generated_voice_id to create, call POST /v1/text-to-voice/create-previews and fetch the generated_voice_id from the response header if don't have one yet.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Optional, metadata to add to the created voice. Defaults to None.
    
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

<details><summary><code>client.text_to_voice.<a href="src/elevenlabs/text_to_voice/client.py">design</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Design a voice via a prompt. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. To create a voice use the generated_voice_id of the preferred preview with the /v1/text-to-voice endpoint.
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
client.text_to_voice.design(
    voice_description="A sassy squeaky mouse",
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

**output_format:** `typing.Optional[TextToVoiceDesignRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `typing.Optional[VoiceDesignRequestModelModelId]` — Model to use for the voice generation. Possible values: eleven_multilingual_ttv_v2, eleven_ttv_v3.
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[str]` — Text to generate, text length has to be between 100 and 1000.
    
</dd>
</dl>

<dl>
<dd>

**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.
    
</dd>
</dl>

<dl>
<dd>

**loudness:** `typing.Optional[float]` — Controls the volume level of the generated voice. -1 is quietest, 1 is loudest, 0 corresponds to roughly -24 LUFS.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — Random number that controls the voice generation. Same seed with same inputs produces same voice.
    
</dd>
</dl>

<dl>
<dd>

**guidance_scale:** `typing.Optional[float]` — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.
    
</dd>
</dl>

<dl>
<dd>

**stream_previews:** `typing.Optional[bool]` — Determines whether the Text to Voice previews should be included in the response. If true, only the generated IDs will be returned which can then be streamed via the /v1/text-to-voice/:generated_voice_id/stream endpoint.
    
</dd>
</dl>

<dl>
<dd>

**quality:** `typing.Optional[float]` — Higher quality results in better voice output but less variety.
    
</dd>
</dl>

<dl>
<dd>

**reference_audio_base_64:** `typing.Optional[str]` — Reference audio to use for the voice generation. The audio should be base64 encoded. Only supported when using the  eleven_ttv_v3 model.
    
</dd>
</dl>

<dl>
<dd>

**prompt_strength:** `typing.Optional[float]` — Controls the balance of prompt versus reference audio when generating voice samples. 0 means almost no prompt influence, 1 means almost no reference audio influence. Only supported when using the eleven_ttv_v3 model and providing reference audio.
    
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

## user
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

## Voices
<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">get_all</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of all available voices for a user.
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

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">search</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets a list of all available voices for a user with search, filtering and pagination.
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
client.voices.search(
    include_total_count=True,
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

**next_page_token:** `typing.Optional[str]` — The next page token to use for pagination. Returned from the previous request.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many voices to return at maximum. Can not exceed 100, defaults to 10. Page 0 may include more voices due to default voices being included.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search term to filter voices by. Searches in name, description, labels, category.
    
</dd>
</dl>

<dl>
<dd>

**sort:** `typing.Optional[str]` — Which field to sort by, one of 'created_at_unix' or 'name'. 'created_at_unix' may not be available for older voices.
    
</dd>
</dl>

<dl>
<dd>

**sort_direction:** `typing.Optional[str]` — Which direction to sort the voices in. 'asc' or 'desc'.
    
</dd>
</dl>

<dl>
<dd>

**voice_type:** `typing.Optional[str]` — Type of the voice to filter by. One of 'personal', 'community', 'default', 'workspace', 'non-default'. 'non-default' is equal to all but 'default'.
    
</dd>
</dl>

<dl>
<dd>

**category:** `typing.Optional[str]` — Category of the voice to filter by. One of 'premade', 'cloned', 'generated', 'professional'
    
</dd>
</dl>

<dl>
<dd>

**fine_tuning_state:** `typing.Optional[str]` — State of the voice's fine tuning to filter by. Applicable only to professional voices clones. One of 'draft', 'not_verified', 'not_started', 'queued', 'fine_tuning', 'fine_tuned', 'failed', 'delayed'
    
</dd>
</dl>

<dl>
<dd>

**collection_id:** `typing.Optional[str]` — Collection ID to filter voices by.
    
</dd>
</dl>

<dl>
<dd>

**include_total_count:** `typing.Optional[bool]` — Whether to include the total count of voices found in the response. Incurs a performance cost.
    
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
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
</dd>
</dl>

<dl>
<dd>

**with_settings:** `typing.Optional[bool]` — This parameter is now deprecated. It is ignored and will be removed in a future version.
    
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
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">update</a>(...)</code></summary>
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
client.voices.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

**description:** `typing.Optional[str]` — A description of the voice.
    
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

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">share</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a shared voice to your collection of Voices
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
client.voices.share(
    public_user_id="63e06b7e7cafdc46be4d2e0b3f045940231ae058d508589653d74d1265a574ca",
    voice_id="21m00Tcm4TlvDq8ikWAM",
    new_name="John Smith",
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

Retrieves a list of shared voices.
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
    featured=True,
    reader_app_enabled=True,
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

**category:** `typing.Optional[VoicesGetSharedRequestCategory]` — Voice category used for filtering
    
</dd>
</dl>

<dl>
<dd>

**gender:** `typing.Optional[str]` — Gender used for filtering
    
</dd>
</dl>

<dl>
<dd>

**age:** `typing.Optional[str]` — Age used for filtering
    
</dd>
</dl>

<dl>
<dd>

**accent:** `typing.Optional[str]` — Accent used for filtering
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — Language used for filtering
    
</dd>
</dl>

<dl>
<dd>

**locale:** `typing.Optional[str]` — Locale used for filtering
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — Search term used for filtering
    
</dd>
</dl>

<dl>
<dd>

**use_cases:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Use-case used for filtering
    
</dd>
</dl>

<dl>
<dd>

**descriptives:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search term used for filtering
    
</dd>
</dl>

<dl>
<dd>

**featured:** `typing.Optional[bool]` — Filter featured voices
    
</dd>
</dl>

<dl>
<dd>

**min_notice_period_days:** `typing.Optional[int]` — Filter voices with a minimum notice period of the given number of days.
    
</dd>
</dl>

<dl>
<dd>

**include_custom_rates:** `typing.Optional[bool]` — Include/exclude voices with custom rates
    
</dd>
</dl>

<dl>
<dd>

**include_live_moderated:** `typing.Optional[bool]` — Include/exclude voices that are live moderated
    
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

**sort:** `typing.Optional[str]` — Sort criteria
    
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

<details><summary><code>client.voices.<a href="src/elevenlabs/voices/client.py">find_similar_voices</a>(...)</code></summary>
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
client.voices.find_similar_voices()

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

**similarity_threshold:** `typing.Optional[float]` — Threshold for voice similarity between provided sample and library voices. Values range from 0 to 2. The smaller the value the more similar voices will be returned.
    
</dd>
</dl>

<dl>
<dd>

**top_k:** `typing.Optional[int]` — Number of most similar voices to return. If similarity_threshold is provided, less than this number of voices may be returned. Values range from 1 to 100.
    
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

## Studio
<details><summary><code>client.studio.<a href="src/elevenlabs/studio/client.py">create_podcast</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create and auto-convert a podcast project. Currently, the LLM cost is covered by us but you will still be charged for the audio generation. In the future, you will be charged for both the LLM and audio generation costs.
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
from elevenlabs import (
    ElevenLabs,
    PodcastConversationModeData,
    PodcastTextSource,
)
from elevenlabs.studio import (
    BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.create_podcast(
    model_id="eleven_multilingual_v2",
    mode=BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(
        conversation=PodcastConversationModeData(
            host_voice_id="aw1NgEzBg83R7vgmiJt6",
            guest_voice_id="aw1NgEzBg83R7vgmiJt7",
        ),
    ),
    source=PodcastTextSource(
        text="This is a test podcast.",
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

**model_id:** `str` — The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.
    
</dd>
</dl>

<dl>
<dd>

**mode:** `BodyCreatePodcastV1StudioPodcastsPostMode` — The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.
    
</dd>
</dl>

<dl>
<dd>

**source:** `BodyCreatePodcastV1StudioPodcastsPostSource` — The source content for the Podcast.
    
</dd>
</dl>

<dl>
<dd>

**quality_preset:** `typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset]` 

Output quality of the generated audio. Must be one of:
standard - standard output format, 128kbps with 44.1kHz sample rate.
high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.
    
</dd>
</dl>

<dl>
<dd>

**duration_scale:** `typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale]` 

Duration of the generated podcast. Must be one of:
short - produces podcasts shorter than 3 minutes.
default - produces podcasts roughly between 3-7 minutes.
long - produces podcasts longer than 7 minutes.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — An optional language of the Studio project. Two-letter language code (ISO 639-1).
    
</dd>
</dl>

<dl>
<dd>

**intro:** `typing.Optional[str]` — The intro text that will always be added to the beginning of the podcast.
    
</dd>
</dl>

<dl>
<dd>

**outro:** `typing.Optional[str]` — The outro text that will always be added to the end of the podcast.
    
</dd>
</dl>

<dl>
<dd>

**instructions_prompt:** `typing.Optional[str]` — Additional instructions prompt for the podcast generation used to adjust the podcast's style and tone.
    
</dd>
</dl>

<dl>
<dd>

**highlights:** `typing.Optional[typing.Sequence[str]]` — A brief summary or highlights of the Studio project's content, providing key points or themes. This should be between 10 and 70 characters.
    
</dd>
</dl>

<dl>
<dd>

**callback_url:** `typing.Optional[str]` 


    A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion
    Messages:
    1. When project was converted successfully:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "success",
        project_snapshot_id: "22m00Tcm4TlvDq8ikMAT",
        error_details: None,
      }
    }
    2. When project conversion failed:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "error",
        project_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }

    3. When chapter was converted successfully:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "success",
        chapter_snapshot_id: "23m00Tcm4TlvDq8ikMAV",
        error_details: None,
      }
    }
    4. When chapter conversion failed:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "error",
        chapter_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }
    
    
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
<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the dubs you have access to.
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
client.dubbing.list()

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

**page_size:** `typing.Optional[int]` — How many dubs to return at maximum. Can not exceed 200, defaults to 100.
    
</dd>
</dl>

<dl>
<dd>

**dubbing_status:** `typing.Optional[DubbingListRequestDubbingStatus]` — Status of the dubbing, either 'in_progress', 'completed' or 'failed'.
    
</dd>
</dl>

<dl>
<dd>

**filter_by_creator:** `typing.Optional[DubbingListRequestFilterByCreator]` — Filters who created the resources being listed, whether it was the user running the request or someone else that shared the resource with them.
    
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

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Dubs a provided audio or video file into given language.
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
client.dubbing.create()

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

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**csv_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**foreground_audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**background_audio_file:** `from __future__ import annotations

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

**target_lang:** `typing.Optional[str]` — The Target language to dub the content into.
    
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

**dubbing_studio:** `typing.Optional[bool]` — Whether to prepare dub for edits in dubbing studio or edits as a dubbing resource.
    
</dd>
</dl>

<dl>
<dd>

**disable_voice_cloning:** `typing.Optional[bool]` — [BETA] Instead of using a voice clone in dubbing, use a similar voice from the ElevenLabs Voice Library.
    
</dd>
</dl>

<dl>
<dd>

**mode:** `typing.Optional[str]` — automatic or manual. Manual mode is only supported when creating a dubbing studio project
    
</dd>
</dl>

<dl>
<dd>

**csv_fps:** `typing.Optional[float]` — Frames per second to use when parsing a CSV file for dubbing. If not provided, FPS will be inferred from timecodes.
    
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

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">get</a>(...)</code></summary>
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
client.dubbing.get(
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

<details><summary><code>client.dubbing.<a href="src/elevenlabs/dubbing/client.py">delete</a>(...)</code></summary>
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
client.dubbing.delete(
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

## Models
<details><summary><code>client.models.<a href="src/elevenlabs/models/client.py">list</a>()</code></summary>
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
client.models.list()

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

Creates Audio Native enabled project, optionally starts conversion and returns project ID and embeddable HTML snippet.
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

<details><summary><code>client.audio_native.<a href="src/elevenlabs/audio_native/client.py">get_settings</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get player settings for the specific project.
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
client.audio_native.get_settings(
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

**project_id:** `str` — The ID of the Studio project.
    
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

<details><summary><code>client.audio_native.<a href="src/elevenlabs/audio_native/client.py">update</a>(...)</code></summary>
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
client.audio_native.update(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
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

## usage
<details><summary><code>client.usage.<a href="src/elevenlabs/usage/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the usage metrics for the current user or the entire workspace they are part of. The response provides a time axis based on the specified aggregation interval (default: day), with usage values for each interval along that axis. Usage is broken down by the selected breakdown type. For example, breakdown type "voice" will return the usage of each voice for each interval along the time axis.
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
client.usage.get(
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

**aggregation_interval:** `typing.Optional[UsageAggregationInterval]` — How to aggregate usage data over time. Can be "hour", "day", "week", "month", or "cumulative".
    
</dd>
</dl>

<dl>
<dd>

**metric:** `typing.Optional[MetricType]` — Which metric to aggregate.
    
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

## PronunciationDictionaries
<details><summary><code>client.pronunciation_dictionaries.<a href="src/elevenlabs/pronunciation_dictionaries/client.py">create_from_file</a>(...)</code></summary>
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
client.pronunciation_dictionaries.create_from_file(
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

**workspace_access:** `typing.Optional[PronunciationDictionariesCreateFromFileRequestWorkspaceAccess]` — Should be one of 'admin', 'editor' or 'viewer'. If not provided, defaults to no access.
    
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

<details><summary><code>client.pronunciation_dictionaries.<a href="src/elevenlabs/pronunciation_dictionaries/client.py">create_from_rules</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new pronunciation dictionary from provided rules.
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
from elevenlabs.pronunciation_dictionaries import (
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.create_from_rules(
    rules=[
        BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias(
            string_to_replace="Thailand",
            alias="tie-land",
        )
    ],
    name="My Dictionary",
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

**rules:** `typing.Sequence[
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem
]` 

List of pronunciation rules. Rule can be either:
    an alias rule: {'string_to_replace': 'a', 'type': 'alias', 'alias': 'b', }
    or a phoneme rule: {'string_to_replace': 'a', 'type': 'phoneme', 'phoneme': 'b', 'alphabet': 'ipa' }
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the pronunciation dictionary, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — A description of the pronunciation dictionary, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**workspace_access:** `typing.Optional[
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostWorkspaceAccess
]` — Should be one of 'admin', 'editor' or 'viewer'. If not provided, defaults to no access.
    
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

<details><summary><code>client.pronunciation_dictionaries.<a href="src/elevenlabs/pronunciation_dictionaries/client.py">get</a>(...)</code></summary>
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
client.pronunciation_dictionaries.get(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
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

<details><summary><code>client.pronunciation_dictionaries.<a href="src/elevenlabs/pronunciation_dictionaries/client.py">list</a>(...)</code></summary>
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
client.pronunciation_dictionaries.list()

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

**sort:** `typing.Optional[PronunciationDictionariesListRequestSort]` — Which field to sort by, one of 'created_at_unix' or 'name'.
    
</dd>
</dl>

<dl>
<dd>

**sort_direction:** `typing.Optional[str]` — Which direction to sort the voices in. 'ascending' or 'descending'.
    
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

## Webhooks
<details><summary><code>client.webhooks.<a href="src/elevenlabs/webhooks/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all webhooks for a workspace
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
client.webhooks.list(
    include_usages=False,
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

**include_usages:** `typing.Optional[bool]` — Whether to include active usages of the webhook, only usable by admins
    
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

## SpeechToText
<details><summary><code>client.speech_to_text.<a href="src/elevenlabs/speech_to_text/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe an audio or video file. If webhook is set to true, the request will be processed asynchronously and results sent to configured webhooks.
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
client.speech_to_text.convert(
    model_id="model_id",
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

**model_id:** `str` — The ID of the model to use for transcription, currently only 'scribe_v1' and 'scribe_v1_experimental' are available.
    
</dd>
</dl>

<dl>
<dd>

**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.
    
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

**language_code:** `typing.Optional[str]` — An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.
    
</dd>
</dl>

<dl>
<dd>

**tag_audio_events:** `typing.Optional[bool]` — Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.
    
</dd>
</dl>

<dl>
<dd>

**num_speakers:** `typing.Optional[int]` — The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.
    
</dd>
</dl>

<dl>
<dd>

**timestamps_granularity:** `typing.Optional[SpeechToTextConvertRequestTimestampsGranularity]` — The granularity of the timestamps in the transcription. 'word' provides word-level timestamps and 'character' provides character-level timestamps per word.
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Whether to annotate which speaker is currently talking in the uploaded file.
    
</dd>
</dl>

<dl>
<dd>

**diarization_threshold:** `typing.Optional[float]` — Diarization threshold to apply during speaker diarization. A higher value means there will be a lower chance of one speaker being diarized as two different speakers but also a higher chance of two different speakers being diarized as one speaker (less total speakers predicted). A low value means there will be a higher chance of one speaker being diarized as two different speakers but also a lower chance of two different speakers being diarized as one speaker (more total speakers predicted). Can only be set when diarize=True and num_speakers=None. Defaults to None, in which case we will choose a threshold based on the model_id (0.22 usually).
    
</dd>
</dl>

<dl>
<dd>

**additional_formats:** `typing.Optional[AdditionalFormats]` — A list of additional formats to export the transcript to.
    
</dd>
</dl>

<dl>
<dd>

**file_format:** `typing.Optional[SpeechToTextConvertRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.
    
</dd>
</dl>

<dl>
<dd>

**cloud_storage_url:** `typing.Optional[str]` — The valid AWS S3, Cloudflare R2 or Google Cloud Storage URL of the file to transcribe. Exactly one of the file or cloud_storage_url parameters must be provided. The file must be a valid publicly accessible cloud storage URL. The file size must be less than 2GB. URL can be pre-signed.
    
</dd>
</dl>

<dl>
<dd>

**webhook:** `typing.Optional[bool]` — Whether to send the transcription result to configured speech-to-text webhooks.  If set the request will return early without the transcription, which will be delivered later via webhook.
    
</dd>
</dl>

<dl>
<dd>

**webhook_id:** `typing.Optional[str]` — Optional specific webhook ID to send the transcription result to. Only valid when webhook is set to true. If not provided, transcription will be sent to all configured speech-to-text webhooks.
    
</dd>
</dl>

<dl>
<dd>

**temperature:** `typing.Optional[float]` — Controls the randomness of the transcription output. Accepts values between 0.0 and 2.0, where higher values result in more diverse and less deterministic results. If omitted, we will use a temperature based on the model you selected which is usually 0.
    
</dd>
</dl>

<dl>
<dd>

**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be an integer between 0 and 2147483647.
    
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

## ForcedAlignment
<details><summary><code>client.forced_alignment.<a href="src/elevenlabs/forced_alignment/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Force align an audio file to text. Use this endpoint to get the timing information for each character and word in an audio file based on a provided text transcript.
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
client.forced_alignment.create(
    text="text",
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

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The text to align with the audio. The input text can be in any format, however diarization is not supported at this time.
    
</dd>
</dl>

<dl>
<dd>

**enabled_spooled_file:** `typing.Optional[bool]` — If true, the file will be streamed to the server and processed in chunks. This is useful for large files that cannot be loaded into memory. The default is false.
    
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
<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">add_to_knowledge_base</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Upload a file or webpage URL to create a knowledge base document. <br> <Note> After creating the document, update the agent's knowledge base by calling [Update agent](/docs/conversational-ai/api-reference/agents/update-agent). </Note>
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
client.conversational_ai.add_to_knowledge_base()

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

**agent_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A custom, human-readable name for the document.
    
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

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">get_document_rag_indexes</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Provides information about all RAG indexes of the specified knowledgebase document.
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
client.conversational_ai.get_document_rag_indexes(
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
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

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">delete_document_rag_index</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete RAG index for the knowledgebase document.
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
client.conversational_ai.delete_document_rag_index(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    rag_index_id="21m00Tcm4TlvDq8ikWAM",
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**rag_index_id:** `str` — The id of RAG index of document from the knowledge base.
    
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

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">rag_index_overview</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Provides total size and other information of RAG indexes used by knowledgebase documents
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
client.conversational_ai.rag_index_overview()

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

<details><summary><code>client.conversational_ai.<a href="src/elevenlabs/conversational_ai/client.py">update_secret</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing secret for the workspace
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
client.conversational_ai.update_secret(
    secret_id="secret_id",
    name="name",
    value="value",
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

**secret_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**value:** `str` 
    
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

## ConversationalAi Conversations
<details><summary><code>client.conversational_ai.conversations.<a href="src/elevenlabs/conversational_ai/conversations/client.py">get_signed_url</a>(...)</code></summary>
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
client.conversational_ai.conversations.get_signed_url(
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

<details><summary><code>client.conversational_ai.conversations.<a href="src/elevenlabs/conversational_ai/conversations/client.py">list</a>(...)</code></summary>
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
client.conversational_ai.conversations.list()

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

**call_start_before_unix:** `typing.Optional[int]` — Unix timestamp (in seconds) to filter conversations up to this start date.
    
</dd>
</dl>

<dl>
<dd>

**call_start_after_unix:** `typing.Optional[int]` — Unix timestamp (in seconds) to filter conversations after to this start date.
    
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

<details><summary><code>client.conversational_ai.conversations.<a href="src/elevenlabs/conversational_ai/conversations/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.conversations.get(
    conversation_id="123",
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

<details><summary><code>client.conversational_ai.conversations.<a href="src/elevenlabs/conversational_ai/conversations/client.py">delete</a>(...)</code></summary>
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
client.conversational_ai.conversations.delete(
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

## ConversationalAi Twilio
<details><summary><code>client.conversational_ai.twilio.<a href="src/elevenlabs/conversational_ai/twilio/client.py">outbound_call</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Handle an outbound call via Twilio
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
client.conversational_ai.twilio.outbound_call(
    agent_id="agent_id",
    agent_phone_number_id="agent_phone_number_id",
    to_number="to_number",
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

**agent_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**agent_phone_number_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**to_number:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**conversation_initiation_client_data:** `typing.Optional[ConversationInitiationClientDataRequestInput]` 
    
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

## ConversationalAi Agents
<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">create</a>(...)</code></summary>
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
client.conversational_ai.agents.create(
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

**platform_settings:** `typing.Optional[AgentPlatformSettingsRequestModel]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.
    
</dd>
</dl>

<dl>
<dd>

**workflow:** `typing.Optional[typing.Optional[typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A name to make the agent easier to find
    
</dd>
</dl>

<dl>
<dd>

**tags:** `typing.Optional[typing.Sequence[str]]` — Tags to help classify and filter the agent
    
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.agents.get(
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">delete</a>(...)</code></summary>
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
client.conversational_ai.agents.delete(
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">update</a>(...)</code></summary>
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
client.conversational_ai.agents.update(
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

**conversation_config:** `typing.Optional[ConversationalConfig]` — Conversation configuration for an agent
    
</dd>
</dl>

<dl>
<dd>

**platform_settings:** `typing.Optional[AgentPlatformSettingsRequestModel]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.
    
</dd>
</dl>

<dl>
<dd>

**workflow:** `typing.Optional[typing.Optional[typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A name to make the agent easier to find
    
</dd>
</dl>

<dl>
<dd>

**tags:** `typing.Optional[typing.Sequence[str]]` — Tags to help classify and filter the agent
    
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of your agents and their metadata.
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
client.conversational_ai.agents.list()

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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">duplicate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new agent by duplicating an existing one
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
client.conversational_ai.agents.duplicate(
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">simulate_conversation</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run a conversation between the agent and a simulated user.
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
from elevenlabs import ConversationSimulationSpecification, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.simulate_conversation(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    simulation_specification=ConversationSimulationSpecification(
        simulated_user_config={
            "first_message": "Hello, how can I help you today?",
            "language": "en",
        },
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

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**simulation_specification:** `ConversationSimulationSpecification` — A specification detailing how the conversation should be simulated
    
</dd>
</dl>

<dl>
<dd>

**extra_evaluation_criteria:** `typing.Optional[typing.Sequence[PromptEvaluationCriteria]]` — A list of evaluation criteria to test
    
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

<details><summary><code>client.conversational_ai.agents.<a href="src/elevenlabs/conversational_ai/agents/client.py">simulate_conversation_stream</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Run a conversation between the agent and a simulated user and stream back the response. Response is streamed back as partial lists of messages that should be concatenated and once the conversation has complete a single final message with the conversation analysis will be sent.
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
from elevenlabs import ConversationSimulationSpecification, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.simulate_conversation_stream(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    simulation_specification=ConversationSimulationSpecification(
        simulated_user_config={
            "first_message": "Hello, how can I help you today?",
            "language": "en",
        },
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

**agent_id:** `str` — The id of an agent. This is returned on agent creation.
    
</dd>
</dl>

<dl>
<dd>

**simulation_specification:** `ConversationSimulationSpecification` — A specification detailing how the conversation should be simulated
    
</dd>
</dl>

<dl>
<dd>

**extra_evaluation_criteria:** `typing.Optional[typing.Sequence[PromptEvaluationCriteria]]` — A list of evaluation criteria to test
    
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

## ConversationalAi PhoneNumbers
<details><summary><code>client.conversational_ai.phone_numbers.<a href="src/elevenlabs/conversational_ai/phone_numbers/client.py">list</a>()</code></summary>
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
client.conversational_ai.phone_numbers.list()

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

<details><summary><code>client.conversational_ai.phone_numbers.<a href="src/elevenlabs/conversational_ai/phone_numbers/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Import Phone Number from provider configuration (Twilio or SIP trunk)
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
from elevenlabs.conversational_ai.phone_numbers import (
    PhoneNumbersCreateRequestBody_Twilio,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.create(
    request=PhoneNumbersCreateRequestBody_Twilio(
        phone_number="phone_number",
        label="label",
        sid="sid",
        token="token",
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

**request:** `PhoneNumbersCreateRequestBody` 
    
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

<details><summary><code>client.conversational_ai.phone_numbers.<a href="src/elevenlabs/conversational_ai/phone_numbers/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.phone_numbers.get(
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

<details><summary><code>client.conversational_ai.phone_numbers.<a href="src/elevenlabs/conversational_ai/phone_numbers/client.py">delete</a>(...)</code></summary>
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
client.conversational_ai.phone_numbers.delete(
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

<details><summary><code>client.conversational_ai.phone_numbers.<a href="src/elevenlabs/conversational_ai/phone_numbers/client.py">update</a>(...)</code></summary>
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
client.conversational_ai.phone_numbers.update(
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

## ConversationalAi LlmUsage
<details><summary><code>client.conversational_ai.llm_usage.<a href="src/elevenlabs/conversational_ai/llm_usage/client.py">calculate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of LLM models and the expected cost for using them based on the provided values.
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
client.conversational_ai.llm_usage.calculate(
    prompt_length=1,
    number_of_pages=1,
    rag_enabled=True,
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

**prompt_length:** `int` — Length of the prompt in characters.
    
</dd>
</dl>

<dl>
<dd>

**number_of_pages:** `int` — Pages of content in PDF documents or URLs in the agent's knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**rag_enabled:** `bool` — Whether RAG is enabled.
    
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

## ConversationalAi KnowledgeBase
<details><summary><code>client.conversational_ai.knowledge_base.<a href="src/elevenlabs/conversational_ai/knowledge_base/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a list of available knowledge base documents
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
client.conversational_ai.knowledge_base.list()

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

**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[str]` — If specified, the endpoint returns only such knowledge base documents whose names start with this string.
    
</dd>
</dl>

<dl>
<dd>

**show_only_owned_documents:** `typing.Optional[bool]` — If set to true, the endpoint will return only documents owned by you (and not shared from somebody else).
    
</dd>
</dl>

<dl>
<dd>

**types:** `typing.Optional[
    typing.Union[
        KnowledgeBaseDocumentType, typing.Sequence[KnowledgeBaseDocumentType]
    ]
]` — If present, the endpoint will return only documents of the given types.
    
</dd>
</dl>

<dl>
<dd>

**use_typesense:** `typing.Optional[bool]` — If set to true, the endpoint will use typesense DB to search for the documents).
    
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

## ConversationalAi Tools
<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all available tools available in the workspace.
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
client.conversational_ai.tools.list()

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

<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a new tool to the available tools in the workspace.
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
from elevenlabs import (
    ElevenLabs,
    ToolRequestModel,
    ToolRequestModelToolConfig_Client,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.create(
    request=ToolRequestModel(
        tool_config=ToolRequestModelToolConfig_Client(
            name="name",
            description="description",
            expects_response=False,
        ),
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

**request:** `ToolRequestModel` 
    
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

<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get tool that is available in the workspace.
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
client.conversational_ai.tools.get(
    tool_id="tool_id",
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

**tool_id:** `str` — ID of the requested tool.
    
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

<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete tool from the workspace.
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
client.conversational_ai.tools.delete(
    tool_id="tool_id",
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

**tool_id:** `str` — ID of the requested tool.
    
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

<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update tool that is available in the workspace.
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
from elevenlabs import (
    ElevenLabs,
    ToolRequestModel,
    ToolRequestModelToolConfig_Client,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.update(
    tool_id="tool_id",
    request=ToolRequestModel(
        tool_config=ToolRequestModelToolConfig_Client(
            name="name",
            description="description",
            expects_response=False,
        ),
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

**tool_id:** `str` — ID of the requested tool.
    
</dd>
</dl>

<dl>
<dd>

**request:** `ToolRequestModel` 
    
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

<details><summary><code>client.conversational_ai.tools.<a href="src/elevenlabs/conversational_ai/tools/client.py">get_dependent_agents</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a list of agents depending on this tool
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
client.conversational_ai.tools.get_dependent_agents(
    tool_id="tool_id",
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

**tool_id:** `str` — ID of the requested tool.
    
</dd>
</dl>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.
    
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

## ConversationalAi Settings
<details><summary><code>client.conversational_ai.settings.<a href="src/elevenlabs/conversational_ai/settings/client.py">get</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve Convai settings for the workspace
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
client.conversational_ai.settings.get()

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

<details><summary><code>client.conversational_ai.settings.<a href="src/elevenlabs/conversational_ai/settings/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update Convai settings for the workspace
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
client.conversational_ai.settings.update()

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

**conversation_initiation_client_data_webhook:** `typing.Optional[ConversationInitiationClientDataWebhook]` 
    
</dd>
</dl>

<dl>
<dd>

**webhooks:** `typing.Optional[ConvAiWebhooks]` 
    
</dd>
</dl>

<dl>
<dd>

**can_use_mcp_servers:** `typing.Optional[bool]` — Whether the workspace can use MCP servers
    
</dd>
</dl>

<dl>
<dd>

**rag_retention_period_days:** `typing.Optional[int]` 
    
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

## ConversationalAi Secrets
<details><summary><code>client.conversational_ai.secrets.<a href="src/elevenlabs/conversational_ai/secrets/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all workspace secrets for the user
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
client.conversational_ai.secrets.list()

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

<details><summary><code>client.conversational_ai.secrets.<a href="src/elevenlabs/conversational_ai/secrets/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new secret for the workspace
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
client.conversational_ai.secrets.create(
    name="name",
    value="value",
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

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**value:** `str` 
    
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

<details><summary><code>client.conversational_ai.secrets.<a href="src/elevenlabs/conversational_ai/secrets/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a workspace secret if it's not in use
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
client.conversational_ai.secrets.delete(
    secret_id="secret_id",
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

**secret_id:** `str` 
    
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

## ConversationalAi BatchCalls
<details><summary><code>client.conversational_ai.batch_calls.<a href="src/elevenlabs/conversational_ai/batch_calls/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Submit a batch call request to schedule calls for multiple recipients.
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
from elevenlabs import ElevenLabs, OutboundCallRecipient

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.create(
    call_name="call_name",
    agent_id="agent_id",
    agent_phone_number_id="agent_phone_number_id",
    recipients=[
        OutboundCallRecipient(
            phone_number="phone_number",
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

**call_name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**agent_phone_number_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**recipients:** `typing.Sequence[OutboundCallRecipient]` 
    
</dd>
</dl>

<dl>
<dd>

**scheduled_time_unix:** `typing.Optional[int]` 
    
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

<details><summary><code>client.conversational_ai.batch_calls.<a href="src/elevenlabs/conversational_ai/batch_calls/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get all batch calls for the current workspace.
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
client.conversational_ai.batch_calls.list()

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

**limit:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**last_doc:** `typing.Optional[str]` 
    
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

<details><summary><code>client.conversational_ai.batch_calls.<a href="src/elevenlabs/conversational_ai/batch_calls/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get detailed information about a batch call including all recipients.
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
client.conversational_ai.batch_calls.get(
    batch_id="batch_id",
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

**batch_id:** `str` 
    
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

<details><summary><code>client.conversational_ai.batch_calls.<a href="src/elevenlabs/conversational_ai/batch_calls/client.py">cancel</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Cancel a running batch call and set all recipients to cancelled status.
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
client.conversational_ai.batch_calls.cancel(
    batch_id="batch_id",
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

**batch_id:** `str` 
    
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

<details><summary><code>client.conversational_ai.batch_calls.<a href="src/elevenlabs/conversational_ai/batch_calls/client.py">retry</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retry a batch call, calling failed and no-response recipients again.
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
client.conversational_ai.batch_calls.retry(
    batch_id="batch_id",
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

**batch_id:** `str` 
    
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

## ConversationalAi SipTrunk
<details><summary><code>client.conversational_ai.sip_trunk.<a href="src/elevenlabs/conversational_ai/sip_trunk/client.py">outbound_call</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Handle an outbound call via SIP trunk
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
client.conversational_ai.sip_trunk.outbound_call(
    agent_id="agent_id",
    agent_phone_number_id="agent_phone_number_id",
    to_number="to_number",
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

**agent_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**agent_phone_number_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**to_number:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**conversation_initiation_client_data:** `typing.Optional[ConversationInitiationClientDataRequestInput]` 
    
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

## ConversationalAi McpServers
<details><summary><code>client.conversational_ai.mcp_servers.<a href="src/elevenlabs/conversational_ai/mcp_servers/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all MCP server configurations available in the workspace.
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
client.conversational_ai.mcp_servers.list()

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

<details><summary><code>client.conversational_ai.mcp_servers.<a href="src/elevenlabs/conversational_ai/mcp_servers/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new MCP server configuration in the workspace.
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
from elevenlabs import ElevenLabs, McpServerConfigInput

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.create(
    config=McpServerConfigInput(
        url="url",
        name="name",
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

**config:** `McpServerConfigInput` — Configuration details for the MCP Server.
    
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

<details><summary><code>client.conversational_ai.mcp_servers.<a href="src/elevenlabs/conversational_ai/mcp_servers/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific MCP server configuration from the workspace.
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
client.conversational_ai.mcp_servers.get(
    mcp_server_id="mcp_server_id",
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

**mcp_server_id:** `str` — ID of the MCP Server.
    
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

## ConversationalAi Agents Widget
<details><summary><code>client.conversational_ai.agents.widget.<a href="src/elevenlabs/conversational_ai/agents/widget/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.agents.widget.get(
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

**conversation_signature:** `typing.Optional[str]` — An expiring token that enables a websocket conversation to start. These can be generated for an agent using the /v1/convai/conversation/get-signed-url endpoint
    
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

## ConversationalAi Agents Link
<details><summary><code>client.conversational_ai.agents.link.<a href="src/elevenlabs/conversational_ai/agents/link/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.agents.link.get(
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

## ConversationalAi Agents KnowledgeBase
<details><summary><code>client.conversational_ai.agents.knowledge_base.<a href="src/elevenlabs/conversational_ai/agents/knowledge_base/client.py">size</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the number of pages in the agent's knowledge base.
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
client.conversational_ai.agents.knowledge_base.size(
    agent_id="agent_id",
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

**agent_id:** `str` 
    
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

## ConversationalAi Agents LlmUsage
<details><summary><code>client.conversational_ai.agents.llm_usage.<a href="src/elevenlabs/conversational_ai/agents/llm_usage/client.py">calculate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Calculates expected number of LLM tokens needed for the specified agent.
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
client.conversational_ai.agents.llm_usage.calculate(
    agent_id="agent_id",
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

**agent_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**prompt_length:** `typing.Optional[int]` — Length of the prompt in characters.
    
</dd>
</dl>

<dl>
<dd>

**number_of_pages:** `typing.Optional[int]` — Pages of content in pdf documents OR urls in agent's Knowledge Base.
    
</dd>
</dl>

<dl>
<dd>

**rag_enabled:** `typing.Optional[bool]` — Whether RAG is enabled.
    
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

## ConversationalAi Agents Widget Avatar
<details><summary><code>client.conversational_ai.agents.widget.avatar.<a href="src/elevenlabs/conversational_ai/agents/widget/avatar/client.py">create</a>(...)</code></summary>
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
client.conversational_ai.agents.widget.avatar.create(
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

## ConversationalAi Conversations Audio
## ConversationalAi Conversations Feedback
<details><summary><code>client.conversational_ai.conversations.feedback.<a href="src/elevenlabs/conversational_ai/conversations/feedback/client.py">create</a>(...)</code></summary>
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
client.conversational_ai.conversations.feedback.create(
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

## ConversationalAi Dashboard Settings
<details><summary><code>client.conversational_ai.dashboard.settings.<a href="src/elevenlabs/conversational_ai/dashboard/settings/client.py">get</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve Convai dashboard settings for the workspace
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
client.conversational_ai.dashboard.settings.get()

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

<details><summary><code>client.conversational_ai.dashboard.settings.<a href="src/elevenlabs/conversational_ai/dashboard/settings/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update Convai dashboard settings for the workspace
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
client.conversational_ai.dashboard.settings.update()

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

**charts:** `typing.Optional[typing.Sequence[PatchConvAiDashboardSettingsRequestChartsItem]]` 
    
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

## ConversationalAi KnowledgeBase Documents
<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">create_from_url</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a knowledge base document generated by scraping the given webpage.
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
client.conversational_ai.knowledge_base.documents.create_from_url(
    url="url",
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

**url:** `str` — URL to a page of documentation that the agent will have access to in order to interact with users.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A custom, human-readable name for the document.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">create_from_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a knowledge base document generated form the uploaded file.
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
client.conversational_ai.knowledge_base.documents.create_from_file()

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

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A custom, human-readable name for the document.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">create_from_text</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a knowledge base document containing the provided text.
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
client.conversational_ai.knowledge_base.documents.create_from_text(
    text="text",
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

**text:** `str` — Text content to be added to the knowledge base.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — A custom, human-readable name for the document.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">get</a>(...)</code></summary>
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
client.conversational_ai.knowledge_base.documents.get(
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a document from the knowledge base
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
client.conversational_ai.knowledge_base.documents.delete(
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**force:** `typing.Optional[bool]` — If set to true, the document will be deleted regardless of whether it is used by any agents and it will be deleted from the dependent agents.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update the name of a document
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
client.conversational_ai.knowledge_base.documents.update(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — A custom, human-readable name for the document.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">get_agents</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a list of agents depending on this knowledge base document
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
client.conversational_ai.knowledge_base.documents.get_agents(
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.
    
</dd>
</dl>

<dl>
<dd>

**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.
    
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

<details><summary><code>client.conversational_ai.knowledge_base.documents.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/client.py">get_content</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the entire content of a document from the knowledge base
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
client.conversational_ai.knowledge_base.documents.get_content(
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
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

## ConversationalAi KnowledgeBase Document
<details><summary><code>client.conversational_ai.knowledge_base.document.<a href="src/elevenlabs/conversational_ai/knowledge_base/document/client.py">compute_rag_index</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

In case the document is not RAG indexed, it triggers rag indexing task, otherwise it just returns the current status.
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
client.conversational_ai.knowledge_base.document.compute_rag_index(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    model="e5_mistral_7b_instruct",
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**model:** `EmbeddingModelEnum` 
    
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

## ConversationalAi KnowledgeBase Documents Chunk
<details><summary><code>client.conversational_ai.knowledge_base.documents.chunk.<a href="src/elevenlabs/conversational_ai/knowledge_base/documents/chunk/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get details about a specific documentation part used by RAG.
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
client.conversational_ai.knowledge_base.documents.chunk.get(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    chunk_id="chunk_id",
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

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.
    
</dd>
</dl>

<dl>
<dd>

**chunk_id:** `str` — The id of a document RAG chunk from the knowledge base.
    
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

## ConversationalAi McpServers Tools
<details><summary><code>client.conversational_ai.mcp_servers.tools.<a href="src/elevenlabs/conversational_ai/mcp_servers/tools/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve all tools available for a specific MCP server configuration.
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
client.conversational_ai.mcp_servers.tools.list(
    mcp_server_id="mcp_server_id",
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

**mcp_server_id:** `str` — ID of the MCP Server.
    
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

## ConversationalAi McpServers ApprovalPolicy
<details><summary><code>client.conversational_ai.mcp_servers.approval_policy.<a href="src/elevenlabs/conversational_ai/mcp_servers/approval_policy/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update the approval policy configuration for an MCP server.
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
client.conversational_ai.mcp_servers.approval_policy.update(
    mcp_server_id="mcp_server_id",
    approval_policy="auto_approve_all",
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

**mcp_server_id:** `str` — ID of the MCP Server.
    
</dd>
</dl>

<dl>
<dd>

**approval_policy:** `McpApprovalPolicy` — The approval mode to set for the MCP server
    
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

## ConversationalAi McpServers ToolApprovals
<details><summary><code>client.conversational_ai.mcp_servers.tool_approvals.<a href="src/elevenlabs/conversational_ai/mcp_servers/tool_approvals/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add approval for a specific MCP tool when using per-tool approval mode.
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
client.conversational_ai.mcp_servers.tool_approvals.create(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
    tool_description="tool_description",
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

**mcp_server_id:** `str` — ID of the MCP Server.
    
</dd>
</dl>

<dl>
<dd>

**tool_name:** `str` — The name of the MCP tool
    
</dd>
</dl>

<dl>
<dd>

**tool_description:** `str` — The description of the MCP tool
    
</dd>
</dl>

<dl>
<dd>

**input_schema:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — The input schema of the MCP tool (the schema defined on the MCP server before ElevenLabs does any extra processing)
    
</dd>
</dl>

<dl>
<dd>

**approval_policy:** `typing.Optional[McpToolApprovalPolicy]` — The tool-level approval policy
    
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

<details><summary><code>client.conversational_ai.mcp_servers.tool_approvals.<a href="src/elevenlabs/conversational_ai/mcp_servers/tool_approvals/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove approval for a specific MCP tool when using per-tool approval mode.
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
client.conversational_ai.mcp_servers.tool_approvals.delete(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
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

**mcp_server_id:** `str` — ID of the MCP Server.
    
</dd>
</dl>

<dl>
<dd>

**tool_name:** `str` — Name of the MCP tool to remove approval for.
    
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

## Dubbing Resource
<details><summary><code>client.dubbing.resource.<a href="src/elevenlabs/dubbing/resource/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Given a dubbing ID generated from the '/v1/dubbing' endpoint with studio enabled, returns the dubbing resource.
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
client.dubbing.resource.get(
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

<details><summary><code>client.dubbing.resource.<a href="src/elevenlabs/dubbing/resource/client.py">transcribe</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Regenerate the transcriptions for the specified segments. Does not automatically regenerate translations or dubs.
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
client.dubbing.resource.transcribe(
    dubbing_id="dubbing_id",
    segments=["segments"],
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

**segments:** `typing.Sequence[str]` — Transcribe this specific list of segments.
    
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

<details><summary><code>client.dubbing.resource.<a href="src/elevenlabs/dubbing/resource/client.py">translate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Regenerate the translations for either the entire resource or the specified segments/languages. Will automatically transcribe missing transcriptions. Will not automatically regenerate the dubs.
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
client.dubbing.resource.translate(
    dubbing_id="dubbing_id",
    segments=["segments"],
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

**segments:** `typing.Sequence[str]` — Translate only this list of segments.
    
</dd>
</dl>

<dl>
<dd>

**languages:** `typing.Optional[typing.Sequence[str]]` — Translate only these languages for each segment.
    
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

<details><summary><code>client.dubbing.resource.<a href="src/elevenlabs/dubbing/resource/client.py">dub</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Regenerate the dubs for either the entire resource or the specified segments/languages. Will automatically transcribe and translate any missing transcriptions and translations.
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
client.dubbing.resource.dub(
    dubbing_id="dubbing_id",
    segments=["segments"],
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

**segments:** `typing.Sequence[str]` — Dub only this list of segments.
    
</dd>
</dl>

<dl>
<dd>

**languages:** `typing.Optional[typing.Sequence[str]]` — Dub only these languages for each segment.
    
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

<details><summary><code>client.dubbing.resource.<a href="src/elevenlabs/dubbing/resource/client.py">render</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Regenerate the output media for a language using the latest Studio state. Please ensure all segments have been dubbed before rendering, otherwise they will be omitted. Renders are generated asynchronously, and to check the status of all renders please use the 'Get Dubbing Resource' endpoint.
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
client.dubbing.resource.render(
    dubbing_id="dubbing_id",
    language="language",
    render_type="mp4",
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

**language:** `str` — Render this language
    
</dd>
</dl>

<dl>
<dd>

**render_type:** `RenderType` — The type of the render. One of ['mp4', 'aac', 'mp3', 'wav', 'aaf', 'tracks_zip', 'clips_zip']
    
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

## Dubbing Audio
## Dubbing Transcript
<details><summary><code>client.dubbing.transcript.<a href="src/elevenlabs/dubbing/transcript/client.py">get_transcript_for_dub</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns transcript for the dub as an SRT or WEBVTT file.
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
client.dubbing.transcript.get_transcript_for_dub(
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

**format_type:** `typing.Optional[TranscriptGetTranscriptForDubRequestFormatType]` — Format to use for the subtitle file, either 'srt' or 'webvtt'
    
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

## Dubbing Resource Language
<details><summary><code>client.dubbing.resource.language.<a href="src/elevenlabs/dubbing/resource/language/client.py">add</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds the given ElevenLab Turbo V2/V2.5 language code to the resource. Does not automatically generate transcripts/translations/audio.
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
client.dubbing.resource.language.add(
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

**language:** `typing.Optional[str]` — The Target language.
    
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

## Dubbing Resource Segment
<details><summary><code>client.dubbing.resource.segment.<a href="src/elevenlabs/dubbing/resource/segment/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Modifies a single segment with new text and/or start/end times. Will update the values for only a specific language of a segment. Does not automatically regenerate the dub.
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
client.dubbing.resource.segment.update(
    dubbing_id="dubbing_id",
    segment_id="segment_id",
    language="language",
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

**segment_id:** `str` — ID of the segment
    
</dd>
</dl>

<dl>
<dd>

**language:** `str` — ID of the language.
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[str]` 
    
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

<details><summary><code>client.dubbing.resource.segment.<a href="src/elevenlabs/dubbing/resource/segment/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a single segment from the dubbing.
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
client.dubbing.resource.segment.delete(
    dubbing_id="dubbing_id",
    segment_id="segment_id",
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

**segment_id:** `str` — ID of the segment
    
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

## Dubbing Resource Speaker
<details><summary><code>client.dubbing.resource.speaker.<a href="src/elevenlabs/dubbing/resource/speaker/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Amend the metadata associated with a speaker, such as their voice. Both voice cloning and using voices from the ElevenLabs library are supported.
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
client.dubbing.resource.speaker.update(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
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

**speaker_id:** `str` — ID of the speaker.
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `typing.Optional[str]` — Either the identifier of a voice from the ElevenLabs voice library, or one of ['track-clone', 'clip-clone'].
    
</dd>
</dl>

<dl>
<dd>

**languages:** `typing.Optional[typing.Sequence[str]]` — Languages to apply these changes to. If empty, will apply to all languages.
    
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

<details><summary><code>client.dubbing.resource.speaker.<a href="src/elevenlabs/dubbing/resource/speaker/client.py">find_similar_voices</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Fetch the top 10 similar voices to a speaker, including the voice IDs, names, descriptions, and, where possible, a sample audio recording.
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
client.dubbing.resource.speaker.find_similar_voices(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
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

**speaker_id:** `str` — ID of the speaker.
    
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

## Dubbing Resource Speaker Segment
<details><summary><code>client.dubbing.resource.speaker.segment.<a href="src/elevenlabs/dubbing/resource/speaker/segment/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new segment in dubbing resource with a start and end time for the speaker in every available language. Does not automatically generate transcripts/translations/audio.
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
client.dubbing.resource.speaker.segment.create(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
    start_time=1.1,
    end_time=1.1,
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

**speaker_id:** `str` — ID of the speaker.
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**text:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**translations:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` 
    
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

## PronunciationDictionaries Rules
<details><summary><code>client.pronunciation_dictionaries.rules.<a href="src/elevenlabs/pronunciation_dictionaries/rules/client.py">add</a>(...)</code></summary>
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
from elevenlabs.pronunciation_dictionaries.rules import (
    PronunciationDictionaryRule_Alias,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.rules.add(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
    rules=[
        PronunciationDictionaryRule_Alias(
            string_to_replace="Thailand",
            alias="tie-land",
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

<details><summary><code>client.pronunciation_dictionaries.rules.<a href="src/elevenlabs/pronunciation_dictionaries/rules/client.py">remove</a>(...)</code></summary>
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
client.pronunciation_dictionaries.rules.remove(
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

## Studio Projects
<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of your Studio projects with metadata.
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
client.studio.projects.list()

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

<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new Studio project, it can be either initialized as blank, from a document or from a URL.
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
client.studio.projects.create(
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

**name:** `str` — The name of the Studio project, used for identification only.
    
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

**default_model_id:** `str` — The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.
    
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

**from_content_json:** `typing.Optional[str]` 


    An optional content to initialize the Studio project with. If this is set, 'from_url' and 'from_document' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.
    
    Example:
    [{"name": "Chapter A", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "A", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "B", "type": "tts_node"}]}, {"sub_type": "h1", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "C", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "D", "type": "tts_node"}]}]}, {"name": "Chapter B", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "E", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "F", "type": "tts_node"}]}, {"sub_type": "h2", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "G", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "H", "type": "tts_node"}]}]}]
    
    
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

**title:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**author:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — An optional description of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**genres:** `typing.Optional[typing.List[str]]` — An optional list of genres associated with the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**target_audience:** `typing.Optional[ProjectsCreateRequestTargetAudience]` — An optional target audience of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — An optional language of the Studio project. Two-letter language code (ISO 639-1).
    
</dd>
</dl>

<dl>
<dd>

**content_type:** `typing.Optional[str]` — An optional content type of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**original_publication_date:** `typing.Optional[str]` — An optional original publication date of the Studio project, in the format YYYY-MM-DD or YYYY.
    
</dd>
</dl>

<dl>
<dd>

**mature_content:** `typing.Optional[bool]` — An optional specification of whether this Studio project contains mature content.
    
</dd>
</dl>

<dl>
<dd>

**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the Studio project you want to create, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**acx_volume_normalization:** `typing.Optional[bool]` — [Deprecated] When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
</dd>
</dl>

<dl>
<dd>

**volume_normalization:** `typing.Optional[bool]` — When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Optional[typing.List[str]]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text. A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'. Note that multiple dictionaries are not currently supported by our UI which will only show the first.
    
</dd>
</dl>

<dl>
<dd>

**callback_url:** `typing.Optional[str]` 


    A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion
    Messages:
    1. When project was converted successfully:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "success",
        project_snapshot_id: "22m00Tcm4TlvDq8ikMAT",
        error_details: None,
      }
    }
    2. When project conversion failed:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "error",
        project_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }

    3. When chapter was converted successfully:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "success",
        chapter_snapshot_id: "23m00Tcm4TlvDq8ikMAV",
        error_details: None,
      }
    }
    4. When chapter conversion failed:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "error",
        chapter_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }
    
    
</dd>
</dl>

<dl>
<dd>

**fiction:** `typing.Optional[ProjectsCreateRequestFiction]` — An optional specification of whether the content of this Studio project is fiction.
    
</dd>
</dl>

<dl>
<dd>

**apply_text_normalization:** `typing.Optional[ProjectsCreateRequestApplyTextNormalization]` 


    This parameter controls text normalization with four modes: 'auto', 'on', 'apply_english' and 'off'.
    When set to 'auto', the system will automatically decide whether to apply text normalization
    (e.g., spelling out numbers). With 'on', text normalization will always be applied, while
    with 'off', it will be skipped. 'apply_english' is the same as 'on' but will assume that text is in English.
    
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the Studio project to audio or not.
    
</dd>
</dl>

<dl>
<dd>

**auto_assign_voices:** `typing.Optional[bool]` — [Alpha Feature] Whether automatically assign voices to phrases in the create Project.
    
</dd>
</dl>

<dl>
<dd>

**source_type:** `typing.Optional[ProjectsCreateRequestSourceType]` — The type of Studio project to create.
    
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

<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns information about a specific Studio project. This endpoint returns more detailed information about a project than `GET /v1/studio`.
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
client.studio.projects.get(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
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

<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the specified Studio project by setting the values of the parameters passed.
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
client.studio.projects.update(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="Project 1",
    default_title_voice_id="21m00Tcm4TlvDq8ikWAM",
    default_paragraph_voice_id="21m00Tcm4TlvDq8ikWAM",
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the Studio project, used for identification only.
    
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

**title:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**author:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the Studio project you want to create, this will be added as metadata to the mp3 file on Studio project or chapter download.
    
</dd>
</dl>

<dl>
<dd>

**volume_normalization:** `typing.Optional[bool]` — When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements
    
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

<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a Studio project.
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
client.studio.projects.delete(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
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

<details><summary><code>client.studio.projects.<a href="src/elevenlabs/studio/projects/client.py">convert</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Starts conversion of a Studio project and all of its chapters.
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
client.studio.projects.convert(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
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

## Studio Projects Content
<details><summary><code>client.studio.projects.content.<a href="src/elevenlabs/studio/projects/content/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates Studio project content.
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
client.studio.projects.content.update(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.
    
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

**from_content_json:** `typing.Optional[str]` 


    An optional content to initialize the Studio project with. If this is set, 'from_url' and 'from_document' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.
    
    Example:
    [{"name": "Chapter A", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "A", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "B", "type": "tts_node"}]}, {"sub_type": "h1", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "C", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "D", "type": "tts_node"}]}]}, {"name": "Chapter B", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "E", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "F", "type": "tts_node"}]}, {"sub_type": "h2", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "G", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "H", "type": "tts_node"}]}]}]
    
    
</dd>
</dl>

<dl>
<dd>

**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the Studio project to audio or not.
    
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

## Studio Projects Snapshots
<details><summary><code>client.studio.projects.snapshots.<a href="src/elevenlabs/studio/projects/snapshots/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a list of snapshots for a Studio project.
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
client.studio.projects.snapshots.list(
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

**project_id:** `str` — The ID of the Studio project.
    
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

<details><summary><code>client.studio.projects.snapshots.<a href="src/elevenlabs/studio/projects/snapshots/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the project snapshot.
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
client.studio.projects.snapshots.get(
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

**project_id:** `str` — The ID of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**project_snapshot_id:** `str` — The ID of the Studio project snapshot.
    
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

## Studio Projects Chapters
<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a list of a Studio project's chapters.
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
client.studio.projects.chapters.list(
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

**project_id:** `str` — The ID of the Studio project.
    
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

<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">create</a>(...)</code></summary>
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
client.studio.projects.chapters.create(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="Chapter 1",
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

**project_id:** `str` — The ID of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the chapter, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.
    
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

<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">get</a>(...)</code></summary>
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
client.studio.projects.chapters.get(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.
    
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

<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates a chapter.
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
client.studio.projects.chapters.update(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The name of the chapter, used for identification only.
    
</dd>
</dl>

<dl>
<dd>

**content:** `typing.Optional[ChapterContentInputModel]` — The chapter content to use.
    
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

<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a chapter.
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
client.studio.projects.chapters.delete(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.
    
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

<details><summary><code>client.studio.projects.chapters.<a href="src/elevenlabs/studio/projects/chapters/client.py">convert</a>(...)</code></summary>
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
client.studio.projects.chapters.convert(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.
    
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

## Studio Projects PronunciationDictionaries
<details><summary><code>client.studio.projects.pronunciation_dictionaries.<a href="src/elevenlabs/studio/projects/pronunciation_dictionaries/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a set of pronunciation dictionaries acting on a project. This will automatically mark text within this project as requiring reconverting where the new dictionary would apply or the old one no longer does.
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
client.studio.projects.pronunciation_dictionaries.create(
    project_id="21m00Tcm4TlvDq8ikWAM",
    pronunciation_dictionary_locators=[
        PronunciationDictionaryVersionLocator(
            pronunciation_dictionary_id="pronunciation_dictionary_id",
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dictionary_locators:** `typing.Sequence[PronunciationDictionaryVersionLocator]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text. A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'. Note that multiple dictionaries are not currently supported by our UI which will only show the first.
    
</dd>
</dl>

<dl>
<dd>

**invalidate_affected_text:** `typing.Optional[bool]` — This will automatically mark text in this project for reconversion when the new dictionary applies or the old one no longer does.
    
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

## Studio Projects Chapters Snapshots
<details><summary><code>client.studio.projects.chapters.snapshots.<a href="src/elevenlabs/studio/projects/chapters/snapshots/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets information about all the snapshots of a chapter. Each snapshot can be downloaded as audio. Whenever a chapter is converted a snapshot will automatically be created.
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
client.studio.projects.chapters.snapshots.list(
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

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.
    
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

<details><summary><code>client.studio.projects.chapters.snapshots.<a href="src/elevenlabs/studio/projects/chapters/snapshots/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the chapter snapshot.
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
client.studio.projects.chapters.snapshots.get(
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

**project_id:** `str` — The ID of the Studio project.
    
</dd>
</dl>

<dl>
<dd>

**chapter_id:** `str` — The ID of the chapter.
    
</dd>
</dl>

<dl>
<dd>

**chapter_snapshot_id:** `str` — The ID of the chapter snapshot.
    
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

## TextToVoice Preview
## User Subscription
<details><summary><code>client.user.subscription.<a href="src/elevenlabs/user/subscription/client.py">get</a>()</code></summary>
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
client.user.subscription.get()

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

## Voices Settings
<details><summary><code>client.voices.settings.<a href="src/elevenlabs/voices/settings/client.py">get_default</a>()</code></summary>
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
client.voices.settings.get_default()

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

<details><summary><code>client.voices.settings.<a href="src/elevenlabs/voices/settings/client.py">get</a>(...)</code></summary>
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
client.voices.settings.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

<details><summary><code>client.voices.settings.<a href="src/elevenlabs/voices/settings/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit your settings for a specific voice. "similarity_boost" corresponds to "Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.
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
client.voices.settings.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    request=VoiceSettings(
        stability=1.0,
        use_speaker_boost=True,
        similarity_boost=1.0,
        style=0.0,
        speed=1.0,
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

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.
    
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

## Voices Ivc
<details><summary><code>client.voices.ivc.<a href="src/elevenlabs/voices/ivc/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a voice clone and add it to your Voices
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
client.voices.ivc.create(
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

**description:** `typing.Optional[str]` — A description of the voice.
    
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

## Voices Pvc
<details><summary><code>client.voices.pvc.<a href="src/elevenlabs/voices/pvc/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new PVC voice with metadata but no samples
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
client.voices.pvc.create(
    name="John Smith",
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

**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.
    
</dd>
</dl>

<dl>
<dd>

**language:** `str` — Language used in the samples.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Description to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Serialized labels dictionary for the voice.
    
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

<details><summary><code>client.voices.pvc.<a href="src/elevenlabs/voices/pvc/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Edit PVC voice metadata
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
client.voices.pvc.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**name:** `typing.Optional[str]` — The name that identifies this voice. This will be displayed in the dropdown of the website.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — Language used in the samples.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — Description to use for the created voice.
    
</dd>
</dl>

<dl>
<dd>

**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Serialized labels dictionary for the voice.
    
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

<details><summary><code>client.voices.pvc.<a href="src/elevenlabs/voices/pvc/client.py">train</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start PVC training process for a voice.
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
client.voices.pvc.train(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**model_id:** `typing.Optional[str]` — The model ID to use for the conversion.
    
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

## Voices Pvc Samples
<details><summary><code>client.voices.pvc.samples.<a href="src/elevenlabs/voices/pvc/samples/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add audio samples to a PVC voice
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
client.voices.pvc.samples.create(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.pvc.samples.<a href="src/elevenlabs/voices/pvc/samples/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a PVC voice sample - apply noise removal, or select speaker.
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
client.voices.pvc.samples.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.
    
</dd>
</dl>

<dl>
<dd>

**selected_speaker_ids:** `typing.Optional[typing.Sequence[str]]` — Speaker IDs to be used for PVC training. Make sure you send all the speaker IDs you want to use for PVC training in one request because the last request will override the previous ones.
    
</dd>
</dl>

<dl>
<dd>

**trim_start_time:** `typing.Optional[int]` — The start time of the audio to be used for PVC training. Time should be in milliseconds
    
</dd>
</dl>

<dl>
<dd>

**trim_end_time:** `typing.Optional[int]` — The end time of the audio to be used for PVC training. Time should be in milliseconds
    
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

<details><summary><code>client.voices.pvc.samples.<a href="src/elevenlabs/voices/pvc/samples/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a sample from a PVC voice.
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
client.voices.pvc.samples.delete(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
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

## Voices Pvc Verification
<details><summary><code>client.voices.pvc.verification.<a href="src/elevenlabs/voices/pvc/verification/client.py">request</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Request manual verification for a PVC voice.
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
client.voices.pvc.verification.request(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**files:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**extra_text:** `typing.Optional[str]` — Extra text to be used in the manual verification process.
    
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

## Voices Pvc Samples Audio
<details><summary><code>client.voices.pvc.samples.audio.<a href="src/elevenlabs/voices/pvc/samples/audio/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the first 30 seconds of voice sample audio with or without noise removal.
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
client.voices.pvc.samples.audio.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
    remove_background_noise=True,
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

**sample_id:** `str` — Sample ID to be used
    
</dd>
</dl>

<dl>
<dd>

**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.
    
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

## Voices Pvc Samples Waveform
<details><summary><code>client.voices.pvc.samples.waveform.<a href="src/elevenlabs/voices/pvc/samples/waveform/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the visual waveform of a voice sample.
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
client.voices.pvc.samples.waveform.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
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

## Voices Pvc Samples Speakers
<details><summary><code>client.voices.pvc.samples.speakers.<a href="src/elevenlabs/voices/pvc/samples/speakers/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the status of the speaker separation process and the list of detected speakers if complete.
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
client.voices.pvc.samples.speakers.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
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

<details><summary><code>client.voices.pvc.samples.speakers.<a href="src/elevenlabs/voices/pvc/samples/speakers/client.py">separate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Start speaker separation process for a sample
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
client.voices.pvc.samples.speakers.separate(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
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

## Voices Pvc Samples Speakers Audio
<details><summary><code>client.voices.pvc.samples.speakers.audio.<a href="src/elevenlabs/voices/pvc/samples/speakers/audio/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the separated audio for a specific speaker.
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
client.voices.pvc.samples.speakers.audio.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
    speaker_id="VW7YKqPnjY4h39yTbx2L",
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

**sample_id:** `str` — Sample ID to be used
    
</dd>
</dl>

<dl>
<dd>

**speaker_id:** `str` — Speaker ID to be used, you can use GET https://api.elevenlabs.io/v1/voices/{voice_id}/samples/{sample_id}/speakers to list all the available speakers for a sample.
    
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

## Voices Pvc Verification Captcha
<details><summary><code>client.voices.pvc.verification.captcha.<a href="src/elevenlabs/voices/pvc/verification/captcha/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get captcha for PVC voice verification.
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
client.voices.pvc.verification.captcha.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

<details><summary><code>client.voices.pvc.verification.captcha.<a href="src/elevenlabs/voices/pvc/verification/captcha/client.py">verify</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Submit captcha verification for PVC voice.
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
client.voices.pvc.verification.captcha.verify(
    voice_id="21m00Tcm4TlvDq8ikWAM",
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

**recording:** `from __future__ import annotations

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

## Voices Samples Audio
## Workspace Groups
<details><summary><code>client.workspace.groups.<a href="src/elevenlabs/workspace/groups/client.py">search</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Searches for user groups in the workspace. Multiple or no groups may be returned.
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
client.workspace.groups.search(
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

**name:** `str` — Name of the target group.
    
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

## Workspace Invites
<details><summary><code>client.workspace.invites.<a href="src/elevenlabs/workspace/invites/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sends an email invitation to join your workspace to the provided email. If the user doesn't have an account they will be prompted to create one. If the user accepts this invite they will be added as a user to your workspace and your subscription using one of your seats. This endpoint may only be called by workspace administrators. If the user is already in the workspace a 400 error will be returned.
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
client.workspace.invites.create(
    email="john.doe@testmail.com",
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

**group_ids:** `typing.Optional[typing.Sequence[str]]` — The group ids of the user
    
</dd>
</dl>

<dl>
<dd>

**workspace_permission:** `typing.Optional[BodyInviteUserV1WorkspaceInvitesAddPostWorkspacePermission]` — The workspace permission of the user
    
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

<details><summary><code>client.workspace.invites.<a href="src/elevenlabs/workspace/invites/client.py">create_batch</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Sends email invitations to join your workspace to the provided emails. Requires all email addresses to be part of a verified domain. If the users don't have an account they will be prompted to create one. If the users accept these invites they will be added as users to your workspace and your subscription using one of your seats. This endpoint may only be called by workspace administrators.
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
client.workspace.invites.create_batch(
    emails=["emails"],
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

**emails:** `typing.Sequence[str]` — The email of the customer
    
</dd>
</dl>

<dl>
<dd>

**group_ids:** `typing.Optional[typing.Sequence[str]]` — The group ids of the user
    
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

<details><summary><code>client.workspace.invites.<a href="src/elevenlabs/workspace/invites/client.py">delete</a>(...)</code></summary>
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
client.workspace.invites.delete(
    email="john.doe@testmail.com",
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

## Workspace Members
<details><summary><code>client.workspace.members.<a href="src/elevenlabs/workspace/members/client.py">update</a>(...)</code></summary>
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
client.workspace.members.update(
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

<details><summary><code>client.workspace.members.<a href="src/elevenlabs/workspace/members/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a workspace member. This endpoint may only be called by workspace administrators.
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
client.workspace.members.delete(
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Workspace Resources
<details><summary><code>client.workspace.resources.<a href="src/elevenlabs/workspace/resources/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Gets the metadata of a resource by ID.
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
client.workspace.resources.get(
    resource_id="resource_id",
    resource_type="voice",
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

**resource_id:** `str` — The ID of the target resource.
    
</dd>
</dl>

<dl>
<dd>

**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.
    
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

<details><summary><code>client.workspace.resources.<a href="src/elevenlabs/workspace/resources/client.py">share</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Grants a role on a workspace resource to a user or a group. It overrides any existing role this user/service account/group/workspace api key has on the resource. To target a user or service account, pass only the user email. The user must be in your workspace. To target a group, pass only the group id. To target a workspace api key, pass the api key id. The resource will be shared with the service account associated with the api key. You must have admin access to the resource to share it.
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
client.workspace.resources.share(
    resource_id="resource_id",
    role="admin",
    resource_type="voice",
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

**resource_id:** `str` — The ID of the target resource.
    
</dd>
</dl>

<dl>
<dd>

**role:** `BodyShareWorkspaceResourceV1WorkspaceResourcesResourceIdSharePostRole` — Role to update the target principal with.
    
</dd>
</dl>

<dl>
<dd>

**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.
    
</dd>
</dl>

<dl>
<dd>

**user_email:** `typing.Optional[str]` — The email of the user or service account.
    
</dd>
</dl>

<dl>
<dd>

**group_id:** `typing.Optional[str]` — The ID of the target group. To target the permissions principals have by default on this resource, use the value 'default'.
    
</dd>
</dl>

<dl>
<dd>

**workspace_api_key_id:** `typing.Optional[str]` — The ID of the target workspace API key. This isn't the same as the key itself that would you pass in the header for authentication. Workspace admins can find this in the workspace settings UI.
    
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

<details><summary><code>client.workspace.resources.<a href="src/elevenlabs/workspace/resources/client.py">unshare</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes any existing role on a workspace resource from a user, service account, group or workspace api key. To target a user or service account, pass only the user email. The user must be in your workspace. To target a group, pass only the group id. To target a workspace api key, pass the api key id. The resource will be unshared from the service account associated with the api key. You must have admin access to the resource to unshare it. You cannot remove permissions from the user who created the resource.
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
client.workspace.resources.unshare(
    resource_id="resource_id",
    resource_type="voice",
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

**resource_id:** `str` — The ID of the target resource.
    
</dd>
</dl>

<dl>
<dd>

**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.
    
</dd>
</dl>

<dl>
<dd>

**user_email:** `typing.Optional[str]` — The email of the user or service account.
    
</dd>
</dl>

<dl>
<dd>

**group_id:** `typing.Optional[str]` — The ID of the target group. To target the permissions principals have by default on this resource, use the value 'default'.
    
</dd>
</dl>

<dl>
<dd>

**workspace_api_key_id:** `typing.Optional[str]` — The ID of the target workspace API key. This isn't the same as the key itself that would you pass in the header for authentication. Workspace admins can find this in the workspace settings UI.
    
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

## Workspace Groups Members
<details><summary><code>client.workspace.groups.members.<a href="src/elevenlabs/workspace/groups/members/client.py">remove</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a member from the specified group. This endpoint may only be called by workspace administrators.
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
client.workspace.groups.members.remove(
    group_id="group_id",
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

**group_id:** `str` — The ID of the target group.
    
</dd>
</dl>

<dl>
<dd>

**email:** `str` — The email of the target workspace member.
    
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

<details><summary><code>client.workspace.groups.members.<a href="src/elevenlabs/workspace/groups/members/client.py">add</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adds a member of your workspace to the specified group. This endpoint may only be called by workspace administrators.
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
client.workspace.groups.members.add(
    group_id="group_id",
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

**group_id:** `str` — The ID of the target group.
    
</dd>
</dl>

<dl>
<dd>

**email:** `str` — The email of the target workspace member.
    
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

