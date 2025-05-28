import json
import os
from llm.llm_wrapper import query_llm
from mcp_server.function_registry import handle_tool_call

def build_prompt(user_input: str) -> str:
    template_path = os.path.join(os.path.dirname(__file__), "..", "llm", "prompt_template.txt")
    with open(template_path) as f:
        system_prompt = f.read()
    return system_prompt + f"\nUser: {user_input}\nAssistant:"

def main():
    user_input = "Add 4 and 5"
    print("User input:", user_input)
    prompt = build_prompt(user_input)
    
    llm_output = query_llm(prompt)
    print("\nLLM output:\n", llm_output)

    try:
        json_str = llm_output[llm_output.index('{'):]
        json_data = json.loads(json_str)
        tool_result = handle_tool_call(json_data)
        print("\nTool result:\n", tool_result)
    except Exception as e:
        print("\nFailed to parse or call tool:\n", e)

if __name__ == "__main__":
    main()
