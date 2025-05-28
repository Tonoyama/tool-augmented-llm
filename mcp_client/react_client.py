import os
import json
import requests
from llm.llm_wrapper import query_llm

def build_react_prompt(history):
    template_path = os.path.join(os.path.dirname(__file__), "..", "llm", "react_prompt_template.txt")
    with open(template_path) as f:
        base_prompt = f.read()
    return base_prompt + "\n" + "\n".join(history)

def main():
    history = []
    user_input = input("You: ")
    history.append(f"User: {user_input}")
    history.append("Assistant:")

    while True:
        prompt = build_react_prompt(history)
        llm_output = query_llm(prompt)
        print("\nLLM output:\n", llm_output)
        history.append(llm_output)

        # ツール呼び出しの抽出
        try:
            json_start = llm_output.index("{")
            json_data = json.loads(llm_output[json_start:])
            tool_call = json_data.get("tool_call")

            if not tool_call:
                print("\n✅ Final Answer:")
                break

            # ツール呼び出し
            tool_response = requests.post("http://mcp_server:8000/tool-call", json=json_data)
            observation = tool_response.json()["result"]
            print("\n🛠 Tool result:", observation)

            # Observationを履歴に追加し、次の思考に繋げる
            history.append(f"Observation: {observation}")

        except Exception as e:
            print("\n❌ Failed to parse or execute tool call:", e)
            break

if __name__ == "__main__":
    main()
