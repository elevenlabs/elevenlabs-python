import json
import pathlib

import pytest
from .fixture_runner import run_fixture

# Shared golden fixtures. Every SDK runs the same files, copied from the reference SDK (elevenlabs-js,
# docs/agents-as-code/fixtures); `expected` is produced there, never here.
FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"
FILES = sorted(path.name for path in FIXTURE_DIR.glob("*.json"))


def test_there_are_fixtures() -> None:
    assert len(FILES) >= 8


@pytest.mark.parametrize("file", FILES)
def test_fixture(file: str) -> None:
    fixture = json.loads((FIXTURE_DIR / file).read_text(encoding="utf-8"))
    result = run_fixture(fixture)

    if "errors" in fixture:
        assert sorted(result.get("errors") or []) == sorted(fixture["errors"])
        return
    assert "errors" not in result
    # Byte-identical to JSON.stringify(expected, null, 2) in the reference SDK.
    assert result["json"] == json.dumps(fixture["expected"], indent=2, ensure_ascii=False) + "\n"
