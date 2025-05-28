from tools import get_weather, add

tools = {
    "get_weather": {
        "description": "Get weather for a location.",
        "parameters": ["location"],
        "function": get_weather,
    },
    "add": {
        "description": "Add two numbers.",
        "parameters": ["a", "b"],
        "function": add,
    }
}

def handle_tool_call(json_data: dict):
    try:
        call = json_data["tool_call"]
        tool_name = call["name"]
        args = call["arguments"]
        
        if tool_name not in tools:
            return f"Unknown tool: {tool_name}"
        
        func = tools[tool_name]["function"]
        return func(**args)
    except Exception as e:
        return f"Tool call error: {e}"
