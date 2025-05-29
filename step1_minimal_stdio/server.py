from mcp.server.fastmcp import FastMCP

# MCP サーバーのインスタンスを作成
mcp = FastMCP("Demo")

# 'add' ツールを追加
@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数値を加算します。"""
    return a + b

# サーバーを stdio トランスポートで実行
if __name__ == "__main__":
    print("Starting MCP server in stdio mode")
    mcp.run(transport="stdio")
