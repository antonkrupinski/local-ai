FROM python:3.11-slim
WORKDIR /app

# Install build deps for llama-cpp-python if needed (keep minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential cmake git curl libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY backend/start.sh ./start.sh
RUN chmod +x ./start.sh

EXPOSE 8080
CMD ["./start.sh"]
