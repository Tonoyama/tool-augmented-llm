# 🧠 MCP関連を1から作ってみた

## 概要

ミニマムな MCP（Model Context Protocol）形式の LLM + Tool Calling デモ。

* vLLM API 経由で LLM を呼び出す
* JSON 出力に基づき FastAPI サーバが関数（ツール）を呼び出す
* ReActループによる連続的なツール使用もサポート

## ディレクトリ構成

```
.
├── docker-compose.yml
├── requirements.txt
├── llm/
│   ├── Dockerfile
│   ├── llm_wrapper.py
│   ├── prompt_template.txt
│   └── react_prompt_template.txt
├── mcp_client/
│   ├── Dockerfile
│   ├── client.py
│   └── react_client.py
├── mcp_server/
│   ├── Dockerfile
│   ├── function_registry.py
│   ├── functions.py
│   └── server.py
```

## 起動方法

### 1. `.env` ファイルの作成

```bash
echo 'VLLM_API_BASE=http://llm:8001/v1' > .env
```

### 2. vLLM起動（Dockerで起動する場合）

`llm/Dockerfile` をビルド・実行することで `vllm.entrypoints.openai.api_server` が起動されます。

### 3. docker-compose で起動

```bash
docker-compose build
docker-compose up
```

### 4. クライアントの使用（ReAct含む）

```bash
docker-compose run mcp_client
```

## 各コンポーネントの役割

* `llm/llm_wrapper.py`: OpenAI互換API経由でプロンプトを送信し、応答を取得
* `mcp_client/client.py`: ユーザー入力をプロンプトにし、LLM → Tool Call を自動で実行
* `mcp_client/react_client.py`: ReAct形式に従い、LLMとTool Callをループ処理
* `mcp_server/`: JSON tool\_callを受け取り、適切なPython関数を呼び出す

## 開発に役立つ Tips

* prompt_template.txt に複数例を書くと、Tool Calling の精度が上がる
* JSON出力が壊れる場合は temperature を 0.2–0.5 に下げると安定
* ReAct形式では履歴を丁寧に保持することで推論が向上する

## 今後の拡張案

* tool registry をJSON Schemaベースにする
* tool functionを自動登録（importlib + inspectでscan）
* GPT-4など大規模モデルへの切替
* vLLMのmulti-GPU推論設定（PagedAttention, CUDA配分）
