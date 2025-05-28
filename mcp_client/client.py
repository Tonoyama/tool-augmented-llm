import json
import os
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
        json_str = llm_response[llm_response.index("{"):]
        json_data = json.loads(json_str)

        response = requests.post("http://localhost:8000/tool-call", json=json_data)
        print("\nTool result:", response.json())

    except Exception as e:
        print("\nFailed to handle tool call:", e)

if __name__ == "__main__":
    main()
