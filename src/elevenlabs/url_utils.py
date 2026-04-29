import urllib.parse
from typing import Any, Sequence, Tuple, Union


_WS_SCHEME = {"https": "wss", "http": "ws"}


def build_ws_url(
    base_url: str,
    path_segments: Sequence[Any],
    params: Union[Sequence[Tuple[str, str]], dict],
) -> str:
    """Build a WebSocket URL with proper percent-encoding.

    Converts http(s) schemes to ws(s), appends percent-encoded
    *path_segments* beneath the existing base path, and encodes
    *params* as the query string.
    """
    parsed = urllib.parse.urlparse(base_url)
    path = "/".join(urllib.parse.quote(str(seg), safe="") for seg in path_segments)
    return urllib.parse.urlunparse((
        _WS_SCHEME.get(parsed.scheme, parsed.scheme),
        parsed.netloc,
        parsed.path.rstrip("/") + "/" + path,
        "",
        urllib.parse.urlencode(params, quote_via=urllib.parse.quote),
        "",
    ))
