import openai
import os

MODEL_NAME = "facebook/opt-125m"

def query_llm(prompt: str) -> str:
    client = openai.OpenAI(
        base_url=os.getenv("VLLM_API_BASE", "http://localhost:8000/v1"),
        api_key="EMPTY"
    )

    response = client.completions.create(
        model=MODEL_NAME,
        prompt=prompt,
        max_tokens=256,
        temperature=0.7
    )

    return response.choices[0].text.strip()
