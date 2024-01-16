from typing import Optional

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Model(pydantic.BaseModel):
    model_id: str
    name: Optional[str] = None
    token_cost_factor: Optional[float] = None
    description: Optional[str] = None