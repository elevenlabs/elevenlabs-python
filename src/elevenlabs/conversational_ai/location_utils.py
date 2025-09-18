from enum import Enum
from typing import Dict


class Location(Enum):
    """Location enum for data residency and region selection."""
    US = "us"
    EU_RESIDENCY = "eu-residency"
    IN_RESIDENCY = "in-residency"
    GLOBAL = "global"


def get_origin_for_location(location: Location) -> str:
    """
    Get the WebSocket API origin URL for a given location.

    Args:
        location: The location enum value

    Returns:
        The WebSocket URL for the specified location
    """
    origin_map: Dict[Location, str] = {
        Location.US: "wss://api.elevenlabs.io",
        Location.EU_RESIDENCY: "wss://api.eu.residency.elevenlabs.io",
        Location.IN_RESIDENCY: "wss://api.in.residency.elevenlabs.io",
        Location.GLOBAL: "wss://api.elevenlabs.io",
    }

    return origin_map[location]


def get_livekit_url_for_location(location: Location) -> str:
    """
    Get the LiveKit WebRTC URL for a given location.

    Args:
        location: The location enum value

    Returns:
        The LiveKit URL for the specified location
    """
    livekit_url_map: Dict[Location, str] = {
        Location.US: "wss://livekit.rtc.elevenlabs.io",
        Location.EU_RESIDENCY: "wss://livekit.rtc.eu.residency.elevenlabs.io",
        Location.IN_RESIDENCY: "wss://livekit.rtc.in.residency.elevenlabs.io",
        Location.GLOBAL: "wss://livekit.rtc.elevenlabs.io",
    }

    return livekit_url_map[location]