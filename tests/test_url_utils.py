"""Tests for the build_ws_url utility."""

import pytest

from elevenlabs.url_utils import build_ws_url


class TestSchemeConversion:
    def test_https_to_wss(self):
        url = build_ws_url("https://api.example.com", ["v1"], {})
        assert url.startswith("wss://")

    def test_http_to_ws(self):
        url = build_ws_url("http://localhost:8080", ["v1"], {})
        assert url.startswith("ws://")

    def test_wss_preserved(self):
        url = build_ws_url("wss://api.example.com", ["v1"], {})
        assert url.startswith("wss://")

    def test_ws_preserved(self):
        url = build_ws_url("ws://localhost:8080", ["v1"], {})
        assert url.startswith("ws://")


class TestPathSegments:
    def test_segments_joined(self):
        url = build_ws_url("wss://api.example.com", ["v1", "speech", "realtime"], {})
        assert url == "wss://api.example.com/v1/speech/realtime"

    def test_segments_percent_encoded(self):
        url = build_ws_url("wss://api.example.com", ["v1", "hello world"], {})
        assert "/v1/hello%20world" in url

    def test_special_characters_encoded(self):
        url = build_ws_url("wss://api.example.com", ["v1", "a/b", "c?d", "e&f"], {})
        assert "/v1/a%2Fb/c%3Fd/e%26f" in url

    def test_non_string_segments_converted(self):
        url = build_ws_url("wss://api.example.com", ["v1", 42, True], {})
        assert "/v1/42/True" in url

    def test_appended_to_existing_base_path(self):
        url = build_ws_url("wss://api.example.com/base", ["v1", "endpoint"], {})
        assert url == "wss://api.example.com/base/v1/endpoint"

    def test_base_path_trailing_slash_not_duplicated(self):
        url = build_ws_url("wss://api.example.com/base/", ["v1"], {})
        assert "//v1" not in url
        assert "/base/v1" in url


class TestQueryParams:
    def test_dict_params(self):
        url = build_ws_url("wss://api.example.com", ["v1"], {"key": "value"})
        assert url.endswith("?key=value")

    def test_tuple_params(self):
        url = build_ws_url("wss://api.example.com", ["v1"], [("a", "1"), ("b", "2")])
        assert "a=1" in url
        assert "b=2" in url

    def test_params_percent_encoded(self):
        url = build_ws_url("wss://api.example.com", ["v1"], {"term": "hello world"})
        assert "term=hello%20world" in url

    def test_repeated_keys(self):
        url = build_ws_url("wss://api.example.com", ["v1"], [("k", "a"), ("k", "b")])
        assert "k=a" in url
        assert "k=b" in url

    def test_empty_params(self):
        url = build_ws_url("wss://api.example.com", ["v1"], {})
        assert url == "wss://api.example.com/v1"


class TestPortPreserved:
    def test_custom_port(self):
        url = build_ws_url("http://localhost:9090", ["v1"], {})
        assert url == "ws://localhost:9090/v1"
