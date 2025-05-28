FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

WORKDIR /workspace
COPY . /workspace

EXPOSE 8000
CMD ["uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "8000"]
