"""
AI Video Generator - FastAPI Backend

Modular backend for video generation with:
- JWT Authentication
- Video generation pipeline
- User video management
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth_routes import router as auth_router
from backend.routes.video_routes import router as video_router

app = FastAPI(
    title="AI Video Generator API",
    description="Generate videos from text prompts using AI",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(video_router)


@app.get("/")
async def root():
    return {"message": "AI Video Generator API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
