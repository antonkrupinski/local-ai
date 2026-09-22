# Local LLM Web UI

A minimal website that runs a local LLM (via `llama-cpp-python`) and exposes a simple chat UI.

Quick steps (macOS):

1. Install system deps (Homebrew):

```bash
brew install cmake
brew install python@3.11
```

2. Create and activate a virtualenv, then install Python deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

3. Download a ggml-compatible model (e.g., a LLaMA/Alpaca/other converted ggml file) and set `LLAMA_MODEL_PATH` env var, or place it at `backend/models/ggml-model.bin`.

4. Run the server:

```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

5. Open http://localhost:8000 in your browser and try the chat UI.

Notes:
- This project uses `llama-cpp-python` which requires a ggml model file. Follow the model author's licensing and usage rules.
- If you prefer another local model runner (text-generation-webui, vLLM, etc.), replace the backend call accordingly.

Deployment notes

- Frontend (Vercel): The `frontend` folder can be deployed as a static site on Vercel. Use the `vercel` CLI or the Vercel dashboard and set the project root to this repo; `vercel.json` is included to help configure the static build.

- Backend (NOT recommended on Vercel): Running a local ggml model with `llama-cpp-python` requires compiling native libraries and loading large model binaries. Vercel serverless functions do not provide the runtime environment, disk space, or CPU/RAM stability necessary for hosting large local models. Therefore, deploy the backend to a service that supports containers or dedicated VMs (Render, Fly.io, DigitalOcean, AWS EC2, etc.).

Recommended backend deployment (Docker):

1. Build the image locally:

```bash
docker build -t local-llm-backend -f backend/Dockerfile .
```

2. Run locally:

```bash
docker run --rm -p 8080:8080 -e LLAMA_MODEL_PATH=/app/models/ggml-model.bin -v /path/to/your/model:/app/models local-llm-backend
```

3. Deploy to a container host (Render/Fly.io): follow their Docker deployment guides and set `LLAMA_MODEL_PATH` and attach model storage.

Alternative: host the model on a VPS you control and keep the FastAPI app there; set `LLAMA_MODEL_PATH` to the model location.

Option for pure Vercel deployment (if you cannot host a model externally):

- Use a hosted inference API (Replicate, OpenAI, etc.) in the backend and deploy the API as a Vercel Serverless function that calls the hosted API. This avoids heavy native builds and binary model files but uses a paid hosted service.

Render deployment (recommended for backend):

- Render supports Docker-based Web Services and Persistent Disks which makes it a good choice to host a local ggml model.

Steps:

1. Push this repository to GitHub (or connect your Git provider to Render).

2. In the Render dashboard, create a new service -> Web Service -> Connect a repository and point the service to this repo. Choose "Docker" as the environment and set the Dockerfile path to `backend/Dockerfile`.

3. Create a Persistent Disk in the same region (Render UI -> Persistent Disks) named `model-data` (size >= 20-50 GB depending on your model). Attach it to the service and set the mount path to `/data`.

4. Set the environment variable `LLAMA_MODEL_PATH` to `/data/models/ggml-model.bin` in the service's Environment tab.

5. Upload your ggml model to the disk. Options:
	- Use the Render dashboard file manager or the web shell to upload the model to `/data/models/`.
	- Alternatively, host the model in private cloud storage (S3) and add a startup step to download it to `/data/models/` during deploy.

6. Deploy. The container uses `backend/start.sh` to read `$PORT` and `$LLAMA_MODEL_PATH` and starts `uvicorn` accordingly.

Notes:
- Ensure your selected plan provides enough CPU and RAM for the model you choose.
- The provided `render.yaml` can be used with Render's Infrastructure-as-Code if you prefer to create services using the manifest.


