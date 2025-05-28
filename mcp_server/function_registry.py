# mcp_server/function_registry.py
from mcp_server.functions import get_weather, add

functions = {
    "get_weather": {
        "description": "Get weather for a location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        },
        "function": get_weather,
    },
    "add": {
        "description": "Add two numbers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        },
        "function": add,
    },
}

def handle_tool_call(json_data: dict):
    try:
        params = json_data.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name not in functions:
            return {
                "tool_name": tool_name,
                "isError": True,
                "result": f"Unknown tool: {tool_name}"
            }

        func = functions[tool_name]["function"]
        result = func(**args)
        return {
            "tool_name": tool_name,
            "isError": False,
            "result": result
        }
    except Exception as e:
        return {
            "tool_name": json_data.get("params", {}).get("name"),
            "isError": True,
            "result": f"Tool call error: {e}"
        }

def handle_list_tools():
    tool_list = []
    for name, meta in functions.items():
        tool_list.append({
            "name": name,
            "description": meta["description"],
            "input_schema": meta["input_schema"]
        })
    return {"tools": tool_list}
