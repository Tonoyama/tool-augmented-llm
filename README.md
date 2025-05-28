# 🧠 MCP関連を1から作ってみた

## 概要

ミニマムなMCP（Model Context Protocol）形式のLLM + Tool Calling サンプル。

- vLLM API 経由で LLM を呼び出す
- JSON出力に基づき FastAPI ベースのサーバで関数を呼び出す

## ディレクトリ構成

```
.
├── Dockerfile
├── requirements.txt
├── .env
├── .dockerignore
├── .gitignore
├── llm/                      # LLMとのやりとりに関するコード
│   ├── llm_wrapper.py       # vLLMのOpenAI互換APIを呼び出すクライアント
│   └── prompt_template.txt  # プロンプトテンプレート（ツール呼び出しの指示例など）
│
├── mcp_client/               # クライアント実装
│   ├── client.py            # ユーザーからの入力をプロンプトに変換→LLM→結果をAPI送信
│   └── main.py              # JSON出力を直接ローカルで処理（サーバを経由しないテスト用）
│
└── mcp_server/               # FastAPIベースのMCPサーバ
     ├── server.py            # /tool-call エンドポイント定義
     ├── functions.py         # 実行対象となるツール関数の実体
     └── function_registry.py # ツール名→関数のルーティングと安全な呼び出しラッパー
```

## 実行方法

### 1. vLLMサーバ起動
別途vLLMサーバを `--model facebook/opt-125m` などで起動しておく必要があります。

例：
```bash
python3 -m vllm.entrypoints.openai.api_server --model facebook/opt-125m
```

### 2. FastAPIサーバをDockerで起動
```bash
docker build -t mcp-app .
docker run -it -p 8000:8000 mcp-app
```

### 3. クライアント起動（ホスト側で）
```bash
python3 mcp_client/client.py
```

## main.pyの実行（ローカルで完結させたい場合）
`mcp_client/main.py` はFastAPIを使わず、直接関数呼び出しします。

```bash
python3 mcp_client/main.py
```

## 必要要件
- vLLM server（別途起動が必要）
- Docker
- CUDA 12.1対応GPU環境（例：RTX 3090, VRAM 24GB）

## 備考

- prompt_template.txt にTool Callの例を記載するとツール呼び出し精度が上がります。
- JSONが壊れる場合は `temperature` を下げる、 `max_tokens` を制限するなど調整してください。
