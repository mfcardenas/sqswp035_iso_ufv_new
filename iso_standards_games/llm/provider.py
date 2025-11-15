"""LLM provider abstraction."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from iso_standards_games.core.config import LLMProvider, settings


class LLMInterface(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate text based on a prompt."""
        pass
    
    @abstractmethod
    async def generate_structured_output(
        self,
        prompt: str,
        output_schema: Dict,
        temperature: float = 0.7
    ) -> Dict:
        """Generate structured output based on a prompt and schema."""
        pass


class OllamaProvider(LLMInterface):
    """Ollama LLM provider implementation."""
    
    def __init__(self):
        """Initialize the Ollama provider."""
        import httpx
        # Use longer timeout for batch generation (5 minutes)
        timeout = httpx.Timeout(300.0)
        self.client = httpx.AsyncClient(base_url=settings.OLLAMA_BASE_URL, timeout=timeout)
        self.model = settings.OLLAMA_MODEL
    
    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate text using Ollama API."""
        response = await self.client.post(
            "/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                }
            }
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    
    async def generate_structured_output(
        self,
        prompt: str,
        output_schema: Dict,
        temperature: float = 0.7
    ) -> Dict:
        """Generate structured output using Ollama API."""
        # For Ollama, we include the schema in the prompt
        structured_prompt = f"""
        {prompt}
        
        Please provide your response in the following JSON structure:
        {output_schema}
        
        Response (JSON only):
        """
        
        response = await self.generate_text(
            prompt=structured_prompt,
            temperature=temperature,
        )
        
        # Extract JSON from response
        import json
        try:
            # Try to find JSON in the response text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            return json.loads(response)
        except json.JSONDecodeError:
            # Return error if JSON parsing fails
            return {"error": "Failed to parse JSON response", "text": response}


class AzureOpenAIProvider(LLMInterface):
    """Azure OpenAI provider implementation."""
    
    def __init__(self):
        """Initialize the Azure OpenAI provider."""
        from openai import AsyncAzureOpenAI
        
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        )
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    
    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate text using Azure OpenAI API."""
        response = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    async def generate_structured_output(
        self,
        prompt: str,
        output_schema: Dict,
        temperature: float = 0.7
    ) -> Dict:
        """Generate structured output using Azure OpenAI API."""
        response = await self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "text": response.choices[0].message.content}


def get_llm_provider() -> LLMInterface:
    """Get the configured LLM provider instance."""
    if settings.LLM_PROVIDER == LLMProvider.OLLAMA:
        return OllamaProvider()
    elif settings.LLM_PROVIDER == LLMProvider.AZURE:
        return AzureOpenAIProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")