"""Game-specific agents."""

from typing import Any, Dict, List, Optional

from iso_standards_games.agents.base import Agent


class ScenarioGenerator(Agent):
    """Agent responsible for generating game scenarios."""
    
    def __init__(
        self,
        game_id: str,
        standard: str,
        difficulty: int = 1,
    ):
        """Initialize the scenario generator.
        
        Args:
            game_id: ID of the game
            standard: ISO standard to focus on
            difficulty: Difficulty level (1-5)
        """
        super().__init__(
            name="Scenario Generator",
            description=f"Generates {standard} scenarios for {game_id}"
        )
        self.game_id = game_id
        self.standard = standard
        self.difficulty = difficulty
    
    async def generate_prompt(self, input_data: Any = None) -> str:
        """Generate a prompt for creating a new scenario."""
        memory_context = self.get_memory_context()
        
        prompt = f"""
        You are a educational game designer specializing in creating scenarios about ISO standards.
        
        Create a {self.difficulty}/5 difficulty scenario for a game about {self.standard}.
        
        {memory_context}
        
        The scenario should:
        1. Present a realistic software development situation
        2. Relate directly to {self.standard}
        3. Include 4 possible answers (only one correct)
        4. Provide an educational explanation for the correct answer
        5. Be engaging and thought-provoking
        
        Format the scenario with:
        - A title
        - A detailed description
        - 4 possible answers (labeled A, B, C, D)
        - The correct answer letter
        - An explanation of why the answer is correct
        """
        
        return prompt
    
    async def process(self, input_data: Any = None) -> Dict[str, Any]:
        """Generate a new game scenario.
        
        Args:
            input_data: Optional context for scenario generation
            
        Returns:
            Dictionary containing scenario details
        """
        prompt = await self.generate_prompt(input_data)
        
        # Get structured output from LLM
        schema = {
            "title": "string",
            "description": "string",
            "options": [
                {
                    "id": "string",
                    "text": "string"
                }
            ],
            "correctOptionId": "string",
            "explanation": "string"
        }
        
        result = await self.llm.generate_structured_output(prompt, schema)
        
        # Add to memory
        self.add_to_memory({
            "type": "scenario_generated",
            "content": result.get("title", "Untitled scenario")
        })
        
        return result


class ResponseEvaluator(Agent):
    """Agent responsible for evaluating user responses to scenarios."""
    
    def __init__(
        self,
        game_id: str,
        standard: str,
    ):
        """Initialize the response evaluator.
        
        Args:
            game_id: ID of the game
            standard: ISO standard to focus on
        """
        super().__init__(
            name="Response Evaluator",
            description=f"Evaluates user responses for {standard} scenarios"
        )
        self.game_id = game_id
        self.standard = standard
    
    async def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """Generate a prompt for evaluating a user response."""
        scenario = input_data.get("scenario", {})
        user_response = input_data.get("user_response", {})
        
        prompt = f"""
        You are an educational evaluator specializing in ISO standards.
        
        Evaluate the user's response to this scenario about {self.standard}:
        
        SCENARIO: {scenario.get("description", "")}
        
        OPTIONS:
        {[f"{opt.get('id')}: {opt.get('text')}" for opt in scenario.get("options", [])]}
        
        CORRECT ANSWER: {scenario.get("correctOptionId", "")}
        
        USER'S RESPONSE: {user_response.get("selected_option_id", "")}
        
        Please provide:
        1. Whether the answer is correct (true/false)
        2. An educational explanation of why the answer is correct or incorrect
        3. Additional learning points about {self.standard} relevant to this scenario
        """
        
        return prompt
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a user's response to a scenario.
        
        Args:
            input_data: Dictionary containing scenario and user response
            
        Returns:
            Dictionary with evaluation results
        """
        prompt = await self.generate_prompt(input_data)
        
        # Get structured output from LLM
        schema = {
            "correct": "boolean",
            "explanation": "string",
            "learningPoints": ["string"],
            "pointsEarned": "number"
        }
        
        result = await self.llm.generate_structured_output(prompt, schema)
        
        # Add to memory
        self.add_to_memory({
            "type": "response_evaluated",
            "content": f"User response was {result.get('correct', False)}"
        })
        
        return result