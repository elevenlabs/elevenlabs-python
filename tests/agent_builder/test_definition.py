from elevenlabs.agent_builder._definition import tool_definition
from elevenlabs.agent_tools import Schema, Tool


def test_ignores_unmodeled_keys_inside_optional_unions_of_models() -> None:
    # An array's `items` is an optional union of schema models; a key none of them declares isn't part of the
    # definition there either, so a tool rebuilt in code still matches the stored copy.
    in_code = Tool.client("pick", "Pick items").param(
        "items", Schema.array(Schema.object().property("sku", Schema.string().describe("SKU"))).describe("Items")
    )
    stored = in_code.to_json()
    stored["parameters"]["properties"]["items"]["items"]["x_unmodeled"] = 1
    assert tool_definition(Tool.from_json(stored)) == tool_definition(in_code)


def test_modeled_changes_still_count() -> None:
    a = Tool.client("pick", "Pick items").param("sku", Schema.string().describe("SKU"))
    b = Tool.client("pick", "Pick items").param("sku", Schema.string().describe("The SKU"))
    assert tool_definition(a) != tool_definition(b)
