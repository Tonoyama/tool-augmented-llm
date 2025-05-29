import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python3", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("利用可能なツール:")
            for tool_name in tools:
                print(f"- {tool_name}")

            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(f"add(5, 3) の結果: {result.content}")

if __name__ == "__main__":
    asyncio.run(main())
