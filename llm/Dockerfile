FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install openai>=1.52.2 vllm>=0.6.3 triton>=3.1.0 python-dotenv

WORKDIR /workspace
COPY . /workspace

CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "facebook/opt-125m", "--port", "8001"]
