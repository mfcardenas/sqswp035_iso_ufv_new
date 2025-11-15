"""Game-related API endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from iso_standards_games.core.models import (
    GameList,
    GameDetail,
    GameSession,
    ScenarioResponse
)
from iso_standards_games.games.manager import get_game_manager

router = APIRouter()


@router.get("/", response_model=GameList)
async def list_games():
    """Get a list of all available games."""
    game_manager = get_game_manager()
    return GameList(games=game_manager.list_games())


@router.get("/{game_id}", response_model=GameDetail)
async def get_game_details(game_id: str):
    """Get detailed information about a specific game."""
    game_manager = get_game_manager()
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameDetail.from_game(game)


@router.post("/{game_id}/sessions", response_model=GameSession)
async def start_game_session(game_id: str):
    """Start a new game session."""
    game_manager = get_game_manager()
    session = await game_manager.start_session(game_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game not found")
    return session


@router.post("/{game_id}/sessions/{session_id}/response", response_model=ScenarioResponse)
async def submit_response(
    game_id: str,
    session_id: str,
    user_response: dict
):
    """Submit a response to a game scenario."""
    game_manager = get_game_manager()
    response = await game_manager.process_response(game_id, session_id, user_response)
    if not response:
        raise HTTPException(status_code=404, detail="Session not found")
    return response