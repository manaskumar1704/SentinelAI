"""
SentinelAI Backend API

Main entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers import user, onboarding, counsellor, universities


from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("🚀 SentinelAI Backend starting...")
    settings = get_settings()
    print(f"📡 Server running on {settings.host}:{settings.port}")
    
    # Initialize database
    try:
        await init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
    
    yield
    
    # Shutdown
    print("👋 SentinelAI Backend shutting down...")
    await close_db()


app = FastAPI(
    title="SentinelAI API",
    description="AI-powered study abroad counselling platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(counsellor.router, prefix="/api/counsellor", tags=["AI Counsellor"])
app.include_router(universities.router, prefix="/api/universities", tags=["Universities"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sentinelai-backend"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SentinelAI API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
