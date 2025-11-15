"""Core data models for the application."""

from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class GameInfo(BaseModel):
    """Basic information about a game."""

    id: str
    name: str
    description: str
    difficulty: int = Field(ge=1, le=5)
    tags: List[str]


class GameList(BaseModel):
    """List of available games."""

    games: List[GameInfo]


class GameDetail(BaseModel):
    """Detailed information about a game."""

    id: str
    name: str
    description: str
    difficulty: int = Field(ge=1, le=5)
    tags: List[str]
    objectives: List[str]
    standards_covered: List[str]
    estimated_duration_minutes: int
    
    @classmethod
    def from_game(cls, game):
        """Create GameDetail from a game object."""
        return cls(
            id=game.id,
            name=game.name,
            description=game.description,
            difficulty=game.difficulty,
            tags=game.tags,
            objectives=game.objectives,
            standards_covered=game.standards_covered,
            estimated_duration_minutes=game.estimated_duration_minutes,
        )


class Scenario(BaseModel):
    """A game scenario presented to the user."""

    id: str
    content: str
    options: Optional[List[Dict[str, str]]] = None
    type: str = "multiple_choice"  # multiple_choice, open_ended, etc.
    media_url: Optional[str] = None


class ScenarioResponse(BaseModel):
    """Response to a user's answer to a scenario."""

    correct: bool
    explanation: str
    points_earned: int
    next_scenario: Optional[Scenario] = None
    game_completed: bool = False
    feedback: Optional[str] = None


class GameSession(BaseModel):
    """An active game session."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    game_id: str
    current_scenario: Scenario
    score: int = 0
    started_at: datetime = Field(default_factory=datetime.now)
    completed: bool = False


class UserProfile(BaseModel):
    """User profile information."""

    user_id: str
    username: str
    preferred_locale: str = "en"
    avatar_url: Optional[str] = None


class Badge(BaseModel):
    """Achievement badge earned by a user."""

    id: str
    name: str
    description: str
    icon_url: str
    earned_at: datetime


class CompletedGame(BaseModel):
    """Information about a completed game."""

    game_id: str
    score: int
    completed_at: datetime
    badges_earned: List[str] = []


class UserStats(BaseModel):
    """User game statistics."""

    games_played: int
    points_earned: int
    badges_earned: List[Badge] = []
    completed_games: List[CompletedGame] = []