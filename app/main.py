from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import infer
import os

app = FastAPI(
    title="AI Image Analysis Service",
    description="API for analyzing images using LangChain and Azure OpenAI",
    version="1.0.0",
)

app.include_router(infer.router)

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=FileResponse)
async def serve_index():
    return os.path.join(static_dir, "index.html")
