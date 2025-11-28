"""
Agent Orchestrator for managing multi-agent collaboration and workflows.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

from agentic_framework.agent import Agent

logger = logging.getLogger(__name__)


class ExecutionMode(str, Enum):
    """Execution modes for multi-agent workflows."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"


class Task(BaseModel):
    """A task to be executed by agents."""
    
    description: str = Field(..., description="Task description")
    expected_output: str = Field(..., description="Expected output format")
    agent_sequence: List[Agent] = Field(default_factory=list, description="Sequence of agents")
    execution_mode: ExecutionMode = Field(default=ExecutionMode.SEQUENTIAL)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    timeout: int = Field(default=300, description="Task timeout in seconds")


class AgentOrchestrator:
    """Orchestrates multiple agents working together on complex tasks."""
    
    def __init__(self, max_concurrent_agents: int = 5):
        self.agents: Dict[str, Agent] = {}
        self.max_concurrent_agents = max_concurrent_agents
        self.execution_history: List[Dict[str, Any]] = []
        
        logger.info("AgentOrchestrator initialized")
    
    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the orchestrator."""
        self.agents[agent.config.name] = agent
        logger.info(f"Added agent: {agent.config.name}")
    
    def remove_agent(self, agent_name: str) -> None:
        """Remove an agent from the orchestrator."""
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"Removed agent: {agent_name}")
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using the configured agents."""
        logger.info(f"Executing task: {task.description}")
        start_time = datetime.now()
        
        try:
            if task.execution_mode == ExecutionMode.SEQUENTIAL:
                result = await self._execute_sequential(task)
            elif task.execution_mode == ExecutionMode.PARALLEL:
                result = await self._execute_parallel(task)
            elif task.execution_mode == ExecutionMode.CONDITIONAL:
                result = await self._execute_conditional(task)
            else:
                raise ValueError(f"Unknown execution mode: {task.execution_mode}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            execution_record = {
                "task": task.description,
                "result": result,
                "execution_time": execution_time,
                "timestamp": start_time.isoformat(),
            }
            self.execution_history.append(execution_record)
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
            }
            
        except asyncio.TimeoutError:
            logger.error(f"Task execution timed out after {task.timeout} seconds")
            return {
                "success": False,
                "error": "Task execution timeout",
            }
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }
    
    async def _execute_sequential(self, task: Task) -> Dict[str, Any]:
        """Execute agents sequentially, passing output from one to the next."""
        results = []
        context = task.context or {}
        
        for agent in task.agent_sequence:
            # Each agent builds upon the previous agent's output
            agent_task = task.description if not results else results[-1].get("response", {})
            
            result = await asyncio.wait_for(
                agent.execute(str(agent_task), context),
                timeout=task.timeout
            )
            
            results.append(result)
            
            # Update context with the result
            context["previous_results"] = results
            
            if not result.get("success"):
                logger.warning(f"Agent {agent.config.name} failed, stopping sequential execution")
                break
        
        return {
            "mode": "sequential",
            "results": results,
            "final_output": results[-1] if results else None,
        }
    
    async def _execute_parallel(self, task: Task) -> Dict[str, Any]:
        """Execute multiple agents in parallel on the same task."""
        # Create tasks for all agents
        agent_tasks = [
            agent.execute(task.description, task.context)
            for agent in task.agent_sequence
        ]
        
        # Execute with timeout
        results = await asyncio.wait_for(
            asyncio.gather(*agent_tasks, return_exceptions=True),
            timeout=task.timeout
        )
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "agent": task.agent_sequence[i].config.name,
                    "error": str(result),
                })
            else:
                processed_results.append(result)
        
        return {
            "mode": "parallel",
            "results": processed_results,
            "successful_agents": sum(1 for r in processed_results if r.get("success")),
        }
    
    async def _execute_conditional(self, task: Task) -> Dict[str, Any]:
        """Execute agents conditionally based on previous results."""
        results = []
        context = task.context or {}
        
        for i, agent in enumerate(task.agent_sequence):
            # Check if we should execute this agent based on previous results
            should_execute = self._evaluate_condition(results, context)
            
            if not should_execute:
                logger.info(f"Skipping agent {agent.config.name} based on conditions")
                continue
            
            result = await asyncio.wait_for(
                agent.execute(task.description, context),
                timeout=task.timeout
            )
            
            results.append(result)
            context["results"] = results
        
        return {
            "mode": "conditional",
            "results": results,
            "executed_agents": len(results),
        }
    
    def _evaluate_condition(self, previous_results: List[Dict], context: Dict) -> bool:
        """Evaluate whether to execute the next agent."""
        # Simple condition: execute if previous agent succeeded or if it's the first agent
        if not previous_results:
            return True
        
        last_result = previous_results[-1]
        return last_result.get("success", False)
    
    async def agent_handoff(self, from_agent: str, to_agent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hand off work from one agent to another."""
        logger.info(f"Agent handoff: {from_agent} -> {to_agent}")
        
        if to_agent not in self.agents:
            raise ValueError(f"Agent '{to_agent}' not found in orchestrator")
        
        target_agent = self.agents[to_agent]
        
        # Extract the handoff task from context
        task = context.get("handoff_task", "Continue the work")
        
        return await target_agent.execute(task, context)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "total_agents": len(self.agents),
            "agents": list(self.agents.keys()),
            "total_executions": len(self.execution_history),
            "max_concurrent_agents": self.max_concurrent_agents,
        }