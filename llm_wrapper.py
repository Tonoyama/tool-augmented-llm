import openai
import os

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

def query_llm(prompt: str) -> str:
    client = openai.OpenAI(
        base_url=os.getenv("VLLM_API_BASE", "http://localhost:8000/v1"),
        api_key="not-needed"  # vLLMはAPIキー不要
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
