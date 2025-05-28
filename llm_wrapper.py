import openai
import os

openai.base_url = os.getenv("VLLM_API_BASE", "http://localhost:8000/v1")
openai.api_key = "not-needed"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

def query_llm(prompt: str) -> str:
    client = openai.OpenAI(base_url=openai.base_url, api_key=openai.api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
