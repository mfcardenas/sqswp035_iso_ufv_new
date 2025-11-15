"""User-related API endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from iso_standards_games.core.models import UserProfile, UserStats

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_user_profile():
    """Get the current user's profile."""
    # Mock implementation - would normally use authentication
    return UserProfile(
        user_id="demo_user",
        username="Demo User",
        preferred_locale="en",
    )


@router.get("/stats", response_model=UserStats)
async def get_user_stats():
    """Get the current user's game statistics."""
    # Mock implementation - would normally fetch from database
    return UserStats(
        games_played=0,
        points_earned=0,
        badges_earned=[],
        completed_games=[],
    )