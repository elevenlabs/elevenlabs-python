"""
Real-time speech-to-text WebSocket helpers for ElevenLabs API.

This module provides classes for streaming audio to the ElevenLabs
speech-to-text API and receiving real-time transcription results.
"""

from .connection import RealtimeConnection, RealtimeEvents
from .scribe import (
    AudioFormat,
    CommitStrategy,
    RealtimeAudioOptions,
    RealtimeEntityDetection,
    RealtimeUrlOptions,
    ScribeRealtime,
)

__all__ = [
    "RealtimeConnection",
    "RealtimeEvents",
    "ScribeRealtime",
    "AudioFormat",
    "CommitStrategy",
    "RealtimeEntityDetection",
    "RealtimeAudioOptions",
    "RealtimeUrlOptions",
]

