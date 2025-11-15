"""QualityQuest game implementation."""

from typing import Dict, List, Optional

from iso_standards_games.games.base import Game
from iso_standards_games.core.models import Scenario, ScenarioResponse


class QualityQuest(Game):
    """Game focusing on ISO/IEC 25010 quality attributes."""
    
    def __init__(self):
        """Initialize QualityQuest game."""
        super().__init__(
            game_id="quality_quest",
            name="QualityQuest: The Quality Challenge",
            description=(
                "Become a Quality Consultant and learn to identify the 8 quality "
                "attributes from ISO/IEC 25010 in various software scenarios."
            ),
            difficulty=1,
            tags=["ISO 25010", "Quality", "Beginner"],
            standards_covered=["ISO/IEC 25010"],
            estimated_duration_minutes=20,
        )
        
        self.objectives = [
            "Identify the 8 quality attributes of ISO/IEC 25010",
            "Recognize quality issues in software systems",
            "Learn how quality attributes impact software success",
            "Understand the relationships between different quality attributes",
        ]
        
        # Quality attributes from ISO/IEC 25010
        self.quality_attributes = [
            "Functional Suitability",
            "Performance Efficiency",
            "Compatibility",
            "Usability",
            "Reliability",
            "Security",
            "Maintainability",
            "Portability",
        ]
    
    async def generate_scenario(self, session_id: str) -> Scenario:
        """Generate a new scenario for the session."""
        # NO hardcoded scenarios - delegate to the server's database system
        raise NotImplementedError("Scenarios are now handled by the unified server system")
    
    async def evaluate_response(
        self, 
        session_id: str, 
        user_response: Dict
    ) -> ScenarioResponse:
        """Evaluate user response and generate feedback."""
        session = self.get_session(session_id)
        if not session:
            return ScenarioResponse(
                correct=False,
                explanation="Session not found",
                points_earned=0,
                game_completed=False,
            )
        
        current_scenario = session.current_scenario
        
        # Get evaluation from agent
        eval_data = await self.response_evaluator.process({
            "scenario": {
                "description": current_scenario.content,
                "options": current_scenario.options,
                "correctOptionId": "A",  # Temporary - this would be stored with the scenario
            },
            "user_response": user_response,
        })
        
        is_correct = eval_data.get("correct", False)
        points = eval_data.get("pointsEarned", 0 if not is_correct else 10)
        
        # Update session score
        session.score += points
        
        # Check if game should continue or end
        # For simplicity, we'll just generate a new scenario here
        # In a real implementation, we'd track progress and end after X scenarios
        if session.score >= 50:
            # Game completed after 5 correct answers
            game_completed = True
            next_scenario = None
        else:
            # Generate next scenario
            game_completed = False
            next_scenario = await self.generate_scenario(session_id)
            session.current_scenario = next_scenario
        
        return ScenarioResponse(
            correct=is_correct,
            explanation=eval_data.get("explanation", ""),
            points_earned=points,
            next_scenario=next_scenario,
            game_completed=game_completed,
            feedback="\n".join(eval_data.get("learningPoints", [])),
        )