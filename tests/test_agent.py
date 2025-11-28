"""
Tests for Agent functionality
"""

import pytest
from unittest.mock import Mock, AsyncMock

from agentic_framework import Agent, AgentConfig
from agentic_framework.llm import LLMProvider


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""
    
    async def generate(self, prompt: str, **kwargs) -> str:
        return "Mock response"
    
    async def generate_structured(self, prompt: str, schema: dict) -> dict:
        return {"result": "mock"}


@pytest.fixture
def mock_llm():
    return MockLLMProvider()


@pytest.fixture
def agent_config():
    return AgentConfig(
        name="TestAgent",
        role="Test role",
        goal="Test goal",
        memory_enabled=False
    )


@pytest.mark.asyncio
async def test_agent_creation(agent_config, mock_llm):
    """Test agent creation."""
    agent = Agent(config=agent_config, llm_provider=mock_llm)
    
    assert agent.config.name == "TestAgent"
    assert agent.config.role == "Test role"
    assert len(agent.execution_history) == 0


@pytest.mark.asyncio
async def test_agent_execute(agent_config, mock_llm):
    """Test agent task execution."""
    agent = Agent(config=agent_config, llm_provider=mock_llm)
    
    result = await agent.execute("Test task")
    
    assert result["success"] is True
    assert "response" in result
    assert result["agent"] == "TestAgent"
    assert len(agent.execution_history) == 1


@pytest.mark.asyncio
async def test_agent_stats(agent_config, mock_llm):
    """Test agent statistics."""
    agent = Agent(config=agent_config, llm_provider=mock_llm)
    
    await agent.execute("Task 1")
    await agent.execute("Task 2")
    
    stats = agent.get_stats()
    
    assert stats["name"] == "TestAgent"
    assert stats["executions"] == 2
    assert stats["memory_enabled"] is False