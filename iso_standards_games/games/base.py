"""Base game class definition."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set
from uuid import UUID, uuid4

from iso_standards_games.agents.game_agents import ScenarioGenerator, ResponseEvaluator
from iso_standards_games.core.models import (
    GameInfo, 
    GameDetail, 
    Scenario, 
    ScenarioResponse, 
    GameSession
)


class Game(ABC):
    """Base class for all games."""
    
    def __init__(
        self,
        game_id: str,
        name: str,
        description: str,
        difficulty: int,
        tags: List[str],
        standards_covered: List[str],
        estimated_duration_minutes: int,
    ):
        """Initialize a game.
        
        Args:
            game_id: Unique identifier for the game
            name: Display name of the game
            description: Brief description
            difficulty: Difficulty level (1-5)
            tags: List of tags
            standards_covered: ISO standards covered
            estimated_duration_minutes: Estimated play time in minutes
        """
        self.id = game_id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.tags = tags
        self.standards_covered = standards_covered
        self.estimated_duration_minutes = estimated_duration_minutes
        self.objectives: List[str] = []
        
        self._active_sessions: Dict[str, GameSession] = {}
        
        # Create agents lazily (only when needed)
        self._scenario_generator = None
        self._response_evaluator = None
    
    def _create_scenario_generator(self) -> ScenarioGenerator:
        """Create a scenario generator agent for this game."""
        return ScenarioGenerator(
            game_id=self.id,
            standard=self.standards_covered[0],  # Primary standard
            difficulty=self.difficulty,
        )
    
    def _create_response_evaluator(self) -> ResponseEvaluator:
        """Create a response evaluator agent for this game."""
        return ResponseEvaluator(
            game_id=self.id,
            standard=self.standards_covered[0],  # Primary standard
        )
    
    @property
    def scenario_generator(self) -> ScenarioGenerator:
        """Get the scenario generator, creating it if needed."""
        if self._scenario_generator is None:
            self._scenario_generator = self._create_scenario_generator()
        return self._scenario_generator
    
    @property
    def response_evaluator(self) -> ResponseEvaluator:
        """Get the response evaluator, creating it if needed."""
        if self._response_evaluator is None:
            self._response_evaluator = self._create_response_evaluator()
        return self._response_evaluator
    
    def to_info(self) -> GameInfo:
        """Convert to GameInfo model."""
        return GameInfo(
            id=self.id,
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            tags=self.tags,
        )
    
    def to_detail(self) -> GameDetail:
        """Convert to GameDetail model."""
        return GameDetail(
            id=self.id,
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            tags=self.tags,
            objectives=self.objectives,
            standards_covered=self.standards_covered,
            estimated_duration_minutes=self.estimated_duration_minutes,
        )
    
    @abstractmethod
    async def generate_scenario(self, session_id: str) -> Scenario:
        """Generate a new scenario for the session."""
        pass
    
    @abstractmethod
    async def evaluate_response(
        self, 
        session_id: str, 
        user_response: Dict
    ) -> ScenarioResponse:
        """Evaluate user response and generate feedback."""
        pass
    
    async def start_session(self) -> GameSession:
        """Start a new game session.
        
        Returns:
            A new GameSession
        """
        session_id = str(uuid4())
        scenario = await self.generate_scenario(session_id)
        
        session = GameSession(
            id=session_id,
            game_id=self.id,
            current_scenario=scenario,
        )
        
        self._active_sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get a session by ID."""
        return self._active_sessions.get(session_id)