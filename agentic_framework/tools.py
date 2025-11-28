"""
Tool system for extending agent capabilities.
"""

import logging
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Abstract base class for agent tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool's schema for LLM function calling."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._get_parameters()
        }
    
    @abstractmethod
    def _get_parameters(self) -> Dict[str, Any]:
        """Get the tool's parameter schema."""
        pass


class WebSearchTool(BaseTool):
    """Tool for web searching."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information"
        )
    
    async def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Execute web search."""
        logger.info(f"Executing web search: {query}")
        
        # Placeholder implementation
        # In production, integrate with actual search API
        return {
            "query": query,
            "results": [
                {"title": f"Result {i}", "url": f"https://example.com/{i}", "snippet": "..."}
                for i in range(num_results)
            ]
        }
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "num_results": {"type": "integer", "description": "Number of results"}
            },
            "required": ["query"]
        }


class CalculatorTool(BaseTool):
    """Tool for mathematical calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations"
        )
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        """Execute calculation."""
        logger.info(f"Calculating: {expression}")
        
        try:
            # Safe evaluation of mathematical expressions
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
            },
            "required": ["expression"]
        }


class DatabaseTool(BaseTool):
    """Tool for database operations."""
    
    def __init__(self, connection_string: str):
        super().__init__(
            name="database",
            description="Query and interact with databases"
        )
        self.connection_string = connection_string
    
    async def execute(self, operation: str, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute database operation."""
        logger.info(f"Database operation: {operation}")
        
        # Placeholder implementation
        return {
            "operation": operation,
            "query": query,
            "result": "Database operation executed successfully",
            "success": True
        }
    
    def _get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "description": "Database operation (select, insert, update, delete)"},
                "query": {"type": "string", "description": "SQL query"},
                "params": {"type": "object", "description": "Query parameters"}
            },
            "required": ["operation", "query"]
        }


class Tool:
    """Factory class for creating tools."""
    
    @staticmethod
    def create_custom_tool(
        name: str,
        description: str,
        execute_fn: Callable,
        parameters: Dict[str, Any]
    ) -> BaseTool:
        """Create a custom tool."""
        
        class CustomTool(BaseTool):
            def __init__(self):
                super().__init__(name, description)
                self.execute_fn = execute_fn
                self.params = parameters
            
            async def execute(self, **kwargs) -> Any:
                return await self.execute_fn(**kwargs)
            
            def _get_parameters(self) -> Dict[str, Any]:
                return self.params
        
        return CustomTool()