

## Run Tests

_Run the following commands from the root of the repo._

### Run all tests
```sh
ELEVEN_API_KEY=<YOUR_API_KEY> PLAY= pytest -s -v
```

### Run specific test
_e.g. `test_voice_design` in the `elevenlabs/tests/api/test_voice.py` file_
```sh
ELEVEN_API_KEY=<YOUR_API_KEY> PLAY= pytest elevenlabs/tests/api/test_voice.py::test_voice_design -s -v
```
