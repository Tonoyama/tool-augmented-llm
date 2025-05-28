# mcp_server/server.py
from fastapi import FastAPI, Request
from mcp_server.function_registry import handle_tool_call, handle_list_tools

app = FastAPI()

@app.post("/jsonrpc")
async def jsonrpc_router(request: Request):
    json_data = await request.json()
    method = json_data.get("method")

    if method == "tools/call":
        result = handle_tool_call(json_data.get("params", {}))
        return {
            "jsonrpc": "2.0",
            "id": json_data.get("id"),
            "result": {
                "tool_name": result.get("tool_name"),
                "type": "tool_result",
                "isError": result.get("isError", False),
                "result": result.get("result")
            }
        }
    elif method == "tools/list":
        tools = handle_list_tools()
        return {
            "jsonrpc": "2.0",
            "id": json_data.get("id"),
            "result": tools
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": json_data.get("id"),
            "error": {
                "code": -32601,
                "message": f"Unknown method: {method}"
            }
        }
