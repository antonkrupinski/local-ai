import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Local LLM Web UI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "backend/models/ggml-model.bin")

llm = None
try:
    if os.path.exists(MODEL_PATH):
        from llama_cpp import Llama
        llm = Llama(model_path=MODEL_PATH)
except Exception:
    llm = None


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7


@app.post("/api/chat")
async def chat(req: ChatRequest):
    global llm
    if llm is None:
        if not os.path.exists(MODEL_PATH):
            return {"error": "Model not found. Set LLAMA_MODEL_PATH or place model at backend/models/ggml-model.bin"}
        from llama_cpp import Llama
        llm = Llama(model_path=MODEL_PATH)

    # Call the model (synchronous call inside async endpoint is acceptable for small demos)
    resp = llm.create(prompt=req.prompt, max_tokens=req.max_tokens, temperature=req.temperature)
    text = ""
    try:
        # llama-cpp-python returns dict with choices
        text = resp.get("choices", [{}])[0].get("text", "")
    except Exception:
        text = str(resp)

    return {"text": text}


# Serve frontend static files (frontend directory at repo root)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
