import os
import json
import requests
from llm.llm_wrapper import query_llm

def build_react_prompt(history):
    template_path = os.path.join(os.path.dirname(__file__), "..", "llm", "react_prompt_template.txt")
    with open(template_path) as f:
        base = f.read()
    return base + "\n" + "\n".join(history)

def main():
    history = []
    user_input = input("You: ")
    history.append(f"User: {user_input}")

    while True:
        prompt = build_react_prompt(history)
        response = query_llm(prompt)
        print("\nLLM output:", response)

        history.append(f"Assistant: {response}")

        # Try to extract tool_call from LLM response
        try:
            json_start = response.index("{")
            json_data = json.loads(response[json_start:])
            tool_call = json_data.get("tool_call")
            if not tool_call:
                print("No more tool calls. Final Answer:")
                break

            tool_result = requests.post("http://localhost:8000/tool-call", json=json_data).json()["result"]
            print("Tool result:", tool_result)
            history.append(f"Observation: {tool_result}")

        except Exception as e:
            print("Error parsing tool call:", e)
            break

if __name__ == "__main__":
    main()
