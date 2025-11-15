"""FastAPI application creation and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from iso_standards_games.api.routes import router
from iso_standards_games.core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Interactive educational games for learning ISO standards",
        debug=settings.DEBUG,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(router, prefix="/api")
    
    # Mount static files (frontend)
    try:
        app.mount("/", StaticFiles(directory="iso_standards_games/frontend/dist", html=True))
    except RuntimeError:
        # Frontend not built yet, development mode
        if settings.DEBUG:
            print("Frontend static files not found. Running in API-only mode.")
    
    return app