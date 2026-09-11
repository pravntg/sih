"""
Project ORCA — FastAPI Application Entrypoint
Serves microservices (/v1/chat, /v1/analytics/pfz, /health) and static command center dashboard.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .api.routes import analytics, chat, health

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Agentic Marine Intelligence Platform backend microservices, PFZ analytics, and conversational advisory."
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

# Serve Frontend static assets & index.html fallback for Vercel & local execution
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if os.path.exists(frontend_dir):
    src_dir = os.path.join(frontend_dir, "src")
    styles_dir = os.path.join(frontend_dir, "styles")

    if os.path.exists(src_dir):
        app.mount("/src", StaticFiles(directory=src_dir), name="src")
    if os.path.exists(styles_dir):
        app.mount("/styles", StaticFiles(directory=styles_dir), name="styles")

    @app.get("/")
    async def serve_index():
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"status": "healthy", "message": "Project ORCA Backend API Active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
