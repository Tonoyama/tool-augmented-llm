import os, json, re, requests
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

        try:
            match = re.search(r'{.*}', llm_output, re.DOTALL)
            if not match:
                raise ValueError("Tool call JSON not found")
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
            observation = response.json().get("result", {})
            print("\n🛠 Tool result:", observation)

            history.append(f"Observation: {observation}")

            if "Final Answer:" in llm_output:
                break

        except Exception as e:
            print("\n❌ Failed to parse or execute tool call:", e)
            break

if __name__ == "__main__":
    main()
