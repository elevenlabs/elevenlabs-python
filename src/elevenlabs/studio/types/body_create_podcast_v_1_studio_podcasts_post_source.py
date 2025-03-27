# This file was auto-generated by Fern from our API Definition.

import typing
from ...types.podcast_text_source import PodcastTextSource
from ...types.podcast_url_source import PodcastUrlSource
from .body_create_podcast_v_1_studio_podcasts_post_source_item import (
    BodyCreatePodcastV1StudioPodcastsPostSourceItem,
)

BodyCreatePodcastV1StudioPodcastsPostSource = typing.Union[
    PodcastTextSource,
    PodcastUrlSource,
    typing.List[BodyCreatePodcastV1StudioPodcastsPostSourceItem],
]
