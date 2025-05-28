import asyncio
from mcp.client.http import http_client, HttpServerParameters
from mcp import ClientSession

async def main():
    # HTTP サーバに接続するための設定（FastMCPが起動している必要あり）
    server_params = HttpServerParameters(
        base_url="http://localhost:8080"
    )

    async with http_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            result = await session.call_tool("get_weather", {"location": "Osaka"})
            print("Weather:", result.content)

            result = await session.call_tool("add", {"a": 7, "b": 5})
            print("Sum:", result.content)

if __name__ == "__main__":
    asyncio.run(main())
