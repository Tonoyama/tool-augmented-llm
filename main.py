import json
from llm_wrapper import query_llm
from tool_registry import handle_tool_call


def build_prompt(user_input: str) -> str:
    with open("prompt_template.txt") as f:
        system_prompt = f.read()
    return system_prompt + f"\nUser: {user_input}"

def main():
    user_input = "How is the weather in Tokyo?"
    print("User input:", user_input)
    prompt = build_prompt(user_input)
    
    llm_output = query_llm(prompt)
    print("\nLLM output:\n", llm_output)

    try:
        json_str = llm_output[llm_output.index('{'):]  # 粗い抽出
        json_data = json.loads(json_str)
        tool_result = handle_tool_call(json_data)
        print("\nTool result:\n", tool_result)
    except Exception as e:
        print("\nFailed to parse or call tool:\n", e)

if __name__ == "__main__":
    main()
