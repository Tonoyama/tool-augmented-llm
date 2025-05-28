import json
import os, re
import requests
from llm.llm_wrapper import query_llm

def build_prompt(user_input: str) -> str:
    template_path = os.path.join(os.path.dirname(__file__), "..", "llm", "prompt_template.txt")
    with open(template_path) as f:
        template = f.read()
    return f"{template}\nUser: {user_input}\nAssistant:"

def main():
    user_input = input("You: ")
    prompt = build_prompt(user_input)
    llm_response = query_llm(prompt)

    print("\nLLM output:", llm_response)

    try:
        match = re.search(r'{.*}', llm_response, re.DOTALL)
        if not match:
            raise ValueError("Tool call JSON not found in LLM output")

        tool_call = json.loads(match.group())["tool_call"]

        request_payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_call["name"],
                "arguments": tool_call["arguments"]
            },
            "id": 1
        }

        response = requests.post("http://mcp_server:8000/jsonrpc", json=request_payload)
        print("\nTool result:", response.json())

    except Exception as e:
        print("\nFailed to handle tool call:", e)

if __name__ == "__main__":
    main()
