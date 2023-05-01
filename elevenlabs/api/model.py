from __future__ import annotations

from typing import List, Optional

from .base import API, api_base_url_v1


class Model(API):
    model_id: str
    name: Optional[str]
    token_cost_factor: Optional[float]
    description: Optional[str]


class Models(API):
    models: List[Model]

    @classmethod
    def from_api(cls) -> Models:
        url = f"{api_base_url_v1}/models"
        response = cls.get(url).json()
        return cls(models=response)

    def __getitem__(self, idx: int) -> Model:
        return self.models[idx]

    def __iter__(self):
        return iter(self.models)
