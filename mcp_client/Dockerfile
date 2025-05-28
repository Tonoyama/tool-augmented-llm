FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install requests openai

WORKDIR /workspace
COPY . /workspace

CMD ["bash"]
