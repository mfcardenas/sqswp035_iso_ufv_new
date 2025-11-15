"""Main API routes for the application."""

from fastapi import APIRouter

from iso_standards_games.api.v1.games import router as games_router
from iso_standards_games.api.v1.users import router as users_router

# Main router
router = APIRouter()

# Include versioned API routes
router.include_router(games_router, prefix="/v1/games", tags=["Games"])
router.include_router(users_router, prefix="/v1/users", tags=["Users"])