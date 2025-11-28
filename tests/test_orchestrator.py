"""
Tests for AgentOrchestrator functionality
"""

import pytest
from unittest.mock import AsyncMock

from agentic_framework import Agent, AgentConfig, AgentOrchestrator, Task
from agentic_framework.orchestrator import ExecutionMode
from agentic_framework.llm import LLMProvider


class MockLLMProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        return "Mock response"
    
    async def generate_structured(self, prompt: str, schema: dict) -> dict:
        return {"result": "mock"}


@pytest.fixture
def mock_agents():
    llm = MockLLMProvider()
    agent1 = Agent(
        config=AgentConfig(name="Agent1", role="Role1", goal="Goal1", memory_enabled=False),
        llm_provider=llm
    )
    agent2 = Agent(
        config=AgentConfig(name="Agent2", role="Role2", goal="Goal2", memory_enabled=False),
        llm_provider=llm
    )
    return [agent1, agent2]


@pytest.mark.asyncio
async def test_orchestrator_creation():
    """Test orchestrator creation."""
    orchestrator = AgentOrchestrator()
    assert len(orchestrator.agents) == 0


@pytest.mark.asyncio
async def test_add_remove_agents(mock_agents):
    """Test adding and removing agents."""
    orchestrator = AgentOrchestrator()
    
    orchestrator.add_agent(mock_agents[0])
    assert len(orchestrator.agents) == 1
    
    orchestrator.add_agent(mock_agents[1])
    assert len(orchestrator.agents) == 2
    
    orchestrator.remove_agent("Agent1")
    assert len(orchestrator.agents) == 1


@pytest.mark.asyncio
async def test_sequential_execution(mock_agents):
    """Test sequential task execution."""
    orchestrator = AgentOrchestrator()
    for agent in mock_agents:
        orchestrator.add_agent(agent)
    
    task = Task(
        description="Test task",
        expected_output="Test output",
        agent_sequence=mock_agents,
        execution_mode=ExecutionMode.SEQUENTIAL
    )
    
    result = await orchestrator.execute_task(task)
    
    assert result["success"] is True
    assert "result" in result
    assert result["result"]["mode"] == "sequential"


@pytest.mark.asyncio
async def test_parallel_execution(mock_agents):
    """Test parallel task execution."""
    orchestrator = AgentOrchestrator()
    for agent in mock_agents:
        orchestrator.add_agent(agent)
    
    task = Task(
        description="Test task",
        expected_output="Test output",
        agent_sequence=mock_agents,
        execution_mode=ExecutionMode.PARALLEL
    )
    
    result = await orchestrator.execute_task(task)
    
    assert result["success"] is True
    assert result["result"]["mode"] == "parallel"