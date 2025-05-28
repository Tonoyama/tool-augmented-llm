from fastapi import FastAPI, Request
from mcp_server.function_registry import handle_tool_call

app = FastAPI()

@app.post("/tool-call")
async def tool_call(request: Request):
    data = await request.json()
    result = handle_tool_call(data)
    return {"result": result}
