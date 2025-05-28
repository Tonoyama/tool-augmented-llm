import openai
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "facebook/opt-125m"

client = openai.OpenAI(
    base_url=os.getenv("VLLM_API_BASE", "http://llm:8001/v1"),
    api_key="EMPTY"
)

def query_llm(prompt: str) -> str:
    response = client.completions.create(
        model=MODEL_NAME,
        prompt=prompt,
        max_tokens=256,
        temperature=0.7
    )
    return response.choices[0].text.strip()
