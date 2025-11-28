"""
Tests for Tool system
"""

import pytest

from agentic_framework.tools import WebSearchTool, CalculatorTool, DatabaseTool, Tool


@pytest.mark.asyncio
async def test_web_search_tool():
    """Test web search tool."""
    tool = WebSearchTool()
    
    result = await tool.execute(query="AI agents", num_results=3)
    
    assert "query" in result
    assert "results" in result
    assert len(result["results"]) == 3


@pytest.mark.asyncio
async def test_calculator_tool():
    """Test calculator tool."""
    tool = CalculatorTool()
    
    result = await tool.execute(expression="2 + 2")
    
    assert result["success"] is True
    assert result["result"] == 4


@pytest.mark.asyncio
async def test_calculator_tool_invalid():
    """Test calculator with invalid expression."""
    tool = CalculatorTool()
    
    result = await tool.execute(expression="invalid")
    
    assert result["success"] is False
    assert "error" in result


@pytest.mark.asyncio
async def test_database_tool():
    """Test database tool."""
    tool = DatabaseTool(connection_string="sqlite:///:memory:")
    
    result = await tool.execute(
        operation="select",
        query="SELECT * FROM users"
    )
    
    assert "operation" in result
    assert result["success"] is True


@pytest.mark.asyncio
async def test_custom_tool_creation():
    """Test creating a custom tool."""
    
    async def custom_execute(**kwargs):
        return {"custom": True, "input": kwargs}
    
    tool = Tool.create_custom_tool(
        name="custom_tool",
        description="A custom tool",
        execute_fn=custom_execute,
        parameters={
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            }
        }
    )
    
    result = await tool.execute(param1="test")
    
    assert result["custom"] is True
    assert result["input"]["param1"] == "test"