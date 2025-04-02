# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations


class ElevenLabsEnvironment:
    PRODUCTION: ElevenLabsEnvironment
    PRODUCTION_US: ElevenLabsEnvironment

    def __init__(self, *, base: str, api: str):
        self.base = base
        self.api = api


ElevenLabsEnvironment.PRODUCTION = ElevenLabsEnvironment(
    base="https://api.elevenlabs.io", api="wss://api.elevenlabs.io"
)
ElevenLabsEnvironment.PRODUCTION_US = ElevenLabsEnvironment(
    base="https://api.us.elevenlabs.io", api="wss://api.elevenlabs.io"
)
