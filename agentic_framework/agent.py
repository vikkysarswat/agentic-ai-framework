"""
Core Agent implementation with reasoning, memory, and tool integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from agentic_framework.llm import LLMProvider
from agentic_framework.memory import MemorySystem
from agentic_framework.tools import BaseTool
from agentic_framework.reasoning import ChainOfThoughtReasoner

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    """Configuration for an AI Agent."""
    
    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent's role/specialty")
    goal: str = Field(..., description="Agent's primary goal")
    backstory: str = Field(default="", description="Agent's background and expertise")
    verbose: bool = Field(default=False, description="Enable verbose logging")
    allow_delegation: bool = Field(default=True, description="Allow delegating to other agents")
    max_iterations: int = Field(default=10, description="Maximum reasoning iterations")
    memory_enabled: bool = Field(default=True, description="Enable memory system")
    tools: List[str] = Field(default_factory=list, description="List of available tools")
    temperature: float = Field(default=0.7, description="LLM temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens for LLM responses")


class Agent:
    """An autonomous AI agent capable of reasoning, using tools, and maintaining memory."""
    
    def __init__(
        self,
        config: AgentConfig,
        llm_provider: Optional[LLMProvider] = None,
        memory_system: Optional[MemorySystem] = None,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.config = config
        self.llm_provider = llm_provider
        self.memory_system = memory_system if config.memory_enabled else None
        self.tools = tools or []
        self.reasoner = ChainOfThoughtReasoner(llm_provider)
        
        self.execution_history: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        
        logger.info(f"Agent '{config.name}' initialized with role: {config.role}")
    
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task with reasoning and tool usage."""
        logger.info(f"Agent '{self.config.name}' executing task: {task}")
        
        try:
            # Retrieve relevant memories
            memories = await self._retrieve_memories(task) if self.memory_system else []
            
            # Build prompt with context
            prompt = self._build_prompt(task, context, memories)
            
            # Reason through the task
            reasoning_result = await self.reasoner.reason(
                prompt,
                max_iterations=self.config.max_iterations
            )
            
            # Execute tools if needed
            if reasoning_result.get("requires_tools"):
                tool_results = await self._execute_tools(reasoning_result["tool_calls"])
                reasoning_result["tool_results"] = tool_results
            
            # Generate final response
            response = await self._generate_response(reasoning_result)
            
            # Store in memory
            if self.memory_system:
                await self._store_memory(task, response)
            
            # Track execution
            execution_record = {
                "task": task,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "reasoning_steps": reasoning_result.get("steps", []),
            }
            self.execution_history.append(execution_record)
            
            return {
                "success": True,
                "response": response,
                "reasoning": reasoning_result,
                "agent": self.config.name,
            }
            
        except Exception as e:
            logger.error(f"Agent '{self.config.name}' failed to execute task: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.config.name,
            }
    
    def _build_prompt(self, task: str, context: Optional[Dict], memories: List[str]) -> str:
        """Build the prompt for the LLM."""
        prompt_parts = [
            f"You are {self.config.name}, a {self.config.role}.",
            f"Your goal: {self.config.goal}",
        ]
        
        if self.config.backstory:
            prompt_parts.append(f"Background: {self.config.backstory}")
        
        if memories:
            prompt_parts.append(f"Relevant memories: {' '.join(memories)}")
        
        if context:
            prompt_parts.append(f"Context: {context}")
        
        prompt_parts.append(f"Task: {task}")
        
        return "\n\n".join(prompt_parts)
    
    async def _retrieve_memories(self, query: str) -> List[str]:
        """Retrieve relevant memories from the memory system."""
        if not self.memory_system:
            return []
        return await self.memory_system.retrieve(query, k=5)
    
    async def _store_memory(self, task: str, response: Dict[str, Any]) -> None:
        """Store the task and response in memory."""
        if not self.memory_system:
            return
        
        memory_text = f"Task: {task}\nResponse: {response.get('content', '')}\nAgent: {self.config.name}"
        await self.memory_system.store(memory_text)
    
    async def _execute_tools(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute the requested tools."""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("arguments", {})
            
            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                try:
                    result = await tool.execute(**tool_args)
                    results.append({
                        "tool": tool_name,
                        "success": True,
                        "result": result,
                    })
                except Exception as e:
                    logger.error(f"Tool '{tool_name}' execution failed: {str(e)}")
                    results.append({
                        "tool": tool_name,
                        "success": False,
                        "error": str(e),
                    })
        
        return results
    
    async def _generate_response(self, reasoning_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final response based on reasoning."""
        # Extract the final answer from reasoning steps
        final_step = reasoning_result.get("steps", [])[-1] if reasoning_result.get("steps") else {}
        
        return {
            "content": final_step.get("output", ""),
            "confidence": reasoning_result.get("confidence", 0.8),
            "reasoning_steps": len(reasoning_result.get("steps", [])),
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "name": self.config.name,
            "role": self.config.role,
            "executions": len(self.execution_history),
            "created_at": self.created_at.isoformat(),
            "memory_enabled": self.config.memory_enabled,
            "tools_available": len(self.tools),
        }