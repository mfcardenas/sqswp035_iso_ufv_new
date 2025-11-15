"""Base agent implementation."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from iso_standards_games.llm.provider import LLMInterface, get_llm_provider


class Agent(ABC):
    """Base agent class for creating intelligent game agents."""
    
    def __init__(self, name: str, description: str):
        """Initialize the agent.
        
        Args:
            name: Agent's name
            description: Brief description of the agent's role
        """
        self.name = name
        self.description = description
        self.llm = get_llm_provider()
        self.memory: List[Dict[str, Any]] = []
    
    def add_to_memory(self, item: Dict[str, Any]) -> None:
        """Add an item to the agent's memory."""
        self.memory.append(item)
    
    def get_memory_context(self) -> str:
        """Get a string representation of the agent's memory for context."""
        if not self.memory:
            return ""
        
        context = "Previous interactions:\n"
        for i, item in enumerate(self.memory[-5:]):  # Last 5 items only
            context += f"{i+1}. {item.get('type', 'interaction')}: {item.get('content', '')}\n"
        return context
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input data and return a response."""
        pass
    
    @abstractmethod
    async def generate_prompt(self, input_data: Any) -> str:
        """Generate a prompt for the LLM based on input data."""
        pass