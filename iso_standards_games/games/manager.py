"""Game manager for handling game instances."""

from typing import Dict, List, Optional

from iso_standards_games.core.models import GameSession, ScenarioResponse
from iso_standards_games.games.base import Game
from iso_standards_games.games.quality_quest import QualityQuest


class GameManager:
    """Manager for game instances and sessions."""
    
    def __init__(self):
        """Initialize the game manager."""
        self.games: Dict[str, Game] = {}
        self._load_games()
    
    def _load_games(self):
        """Load all available games."""
        # Add QualityQuest
        quality_quest = QualityQuest()
        self.games[quality_quest.id] = quality_quest
        
        # TODO: Add other games here as they are implemented
    
    def list_games(self):
        """Get a list of all available games."""
        return [game.to_info() for game in self.games.values()]
    
    def get_game(self, game_id: str) -> Optional[Game]:
        """Get a game by ID."""
        return self.games.get(game_id)
    
    async def start_session(self, game_id: str) -> Optional[GameSession]:
        """Start a new game session."""
        game = self.get_game(game_id)
        if not game:
            return None
        
        return await game.start_session()
    
    async def process_response(
        self, 
        game_id: str, 
        session_id: str, 
        user_response: Dict
    ) -> Optional[ScenarioResponse]:
        """Process a user response within a game session."""
        game = self.get_game(game_id)
        if not game:
            return None
        
        return await game.evaluate_response(session_id, user_response)


_game_manager: Optional[GameManager] = None


def get_game_manager() -> GameManager:
    """Get or create the global game manager instance."""
    global _game_manager
    if _game_manager is None:
        _game_manager = GameManager()
    return _game_manager