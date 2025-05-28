import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "not-needed"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

def query_llm(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages
    )

    return response["choices"][0]["message"]["content"]
