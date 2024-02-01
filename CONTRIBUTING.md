## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us! 

On the other hand, contributions to the README are always very welcome!

### Tests

Run the following commands from the root of the repo

```sh
ELEVEN_API_KEY=<YOUR_API_KEY> poetry run pytest -sv
```

### Run a specific test
_e.g. `test_voice_design` in the `elevenlabs/tests/api/test_voice.py` file_
```sh
ELEVEN_API_KEY=<YOUR_API_KEY> poerty run pytest elevenlabs/tests/api/test_voice.py::test_voice_design -sv
```