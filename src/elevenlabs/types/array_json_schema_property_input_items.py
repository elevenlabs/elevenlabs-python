# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
import typing
from .literal_json_schema_property import LiteralJsonSchemaProperty
import typing

if typing.TYPE_CHECKING:
    from .object_json_schema_property_input import ObjectJsonSchemaPropertyInput
    from .array_json_schema_property_input import ArrayJsonSchemaPropertyInput
ArrayJsonSchemaPropertyInputItems = typing.Union[
    LiteralJsonSchemaProperty, "ObjectJsonSchemaPropertyInput", "ArrayJsonSchemaPropertyInput"
]
