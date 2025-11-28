"""
LLM Provider abstraction for different AI models.
"""

import logging
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured response."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.7):
        if AsyncOpenAI is None:
            raise ImportError("openai is required. Install with: pip install openai")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        
        logger.info(f"OpenAI provider initialized with model: {model}")
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from OpenAI."""
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", 2000)
        )
        
        return response.choices[0].message.content
    
    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured response using function calling."""
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=[schema],
            function_call={"name": schema["name"]}
        )
        
        import json
        function_call = response.choices[0].message.function_call
        return json.loads(function_call.arguments)


class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM provider."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.7):
        if AsyncAnthropic is None:
            raise ImportError("anthropic is required. Install with: pip install anthropic")
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        
        logger.info(f"Anthropic provider initialized with model: {model}")
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from Claude."""
        response = await self.client.messages.create(
            model=kwargs.get("model", self.model),
            max_tokens=kwargs.get("max_tokens", 2000),
            temperature=kwargs.get("temperature", self.temperature),
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured response."""
        # Anthropic doesn't have direct structured output yet
        # We'll use prompt engineering to get JSON
        enhanced_prompt = f"{prompt}\n\nRespond with JSON matching this schema: {schema}"
        response = await self.generate(enhanced_prompt)
        
        import json
        return json.loads(response)