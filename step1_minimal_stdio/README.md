# Step 1: MCP 最小構成 (stdio通信)

このステップでは、**Model Context Protocol (MCP)** の基本概念を体験するために、最小限の構成でサーバとクライアントを実装します。

---

## 🎯 目的

* MCPの基本構造（サーバ・クライアント・プロトコル）を体験する
* `FastMCP` を使って最小限のツールを登録する
* `ClientSession` で `initialize` → `list_tools` → `call_tool` の流れを体験する

---

## 📁 構成ファイル

```
step1_minimal_stdio/
├── server.py         # MCPサーバ（addツールを公開）
├── client.py         # MCPクライアント（サーバを起動してツールを呼び出す）
└── README.md         # このドキュメント
```

---

## 🚀 実行方法

### 1. 仮想環境の作成とパッケージインストール

```bash
uv init step1_minimal_stdio
cd step1_minimal_stdio
uv add "mcp[cli]"
```

### 2. サーバを起動（別ターミナル）

```bash
uv run python3 server.py
```

### 3. クライアントを実行

```bash
uv run python3 client.py
```

---

## ✅ 期待される出力

```bash
[05/29/25 09:18:29] INFO     Processing request of type ListToolsRequest                      server.py:551
利用可能なツール:
- ('meta', None)
- ('nextCursor', None)
- ('tools', [Tool(name='add', description='2つの数値を加算します。', inputSchema={'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'addArguments', 'type': 'object'}, annotations=None)])
                    INFO     Processing request of type CallToolRequest                       server.py:551
add(5, 3) の結果: [TextContent(type='text', text='8', annotations=None)]
```

---

## 🧠 解説

* `FastMCP("Demo")` によってMCPツールサーバを作成
* `@mcp.tool()` で `add(a: int, b: int)` 関数を登録
* `ClientSession` によって `initialize()`、`list_tools()`、`call_tool()` を順に実行

---

## 🛠 トラブルシューティング

* `ModuleNotFoundError: No module named 'mcp'` → 仮想環境が有効か確認し、`uv add "mcp[cli]"` を実行
* `AttributeError: 'str' object has no attribute 'name'` → `list_tools()` の返り値は `(key, value)` のタプルなので、辞書に変換して `tools` キーを参照してください

---

## 🔄 次のステップへ

* Step 2: JSON-RPC を手動で書くクライアント実装へ進み、プロトコル層を理解
* または ReActクライアントやTool自動登録へ発展

ご希望に応じて、次のステップも提供可能です。
