from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")

if hf_token is None:
    raise RuntimeError("Missing HUGGINGFACE_HUB_TOKEN in .env")

login(hf_token)

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # 任意のモデル

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

def query_llm(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
