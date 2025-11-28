"""
Reasoning engine with chain-of-thought capabilities.
"""

import logging
from typing import Any, Dict, List, Optional

from agentic_framework.llm import LLMProvider

logger = logging.getLogger(__name__)


class ChainOfThoughtReasoner:
    """Implements chain-of-thought reasoning for enhanced decision-making."""
    
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm_provider = llm_provider
    
    async def reason(self, prompt: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Perform chain-of-thought reasoning."""
        logger.info("Starting chain-of-thought reasoning")
        
        reasoning_steps = []
        
        # Step 1: Problem Understanding
        understanding = await self._understand_problem(prompt)
        reasoning_steps.append({
            "step": 1,
            "type": "understanding",
            "output": understanding
        })
        
        # Step 2: Break down into sub-problems
        sub_problems = await self._decompose_problem(prompt, understanding)
        reasoning_steps.append({
            "step": 2,
            "type": "decomposition",
            "output": sub_problems
        })
        
        # Step 3: Solve each sub-problem
        solutions = []
        for i, sub_problem in enumerate(sub_problems[:max_iterations]):
            solution = await self._solve_sub_problem(sub_problem)
            solutions.append(solution)
            reasoning_steps.append({
                "step": 3 + i,
                "type": "solution",
                "output": solution
            })
        
        # Step 4: Synthesize final answer
        final_answer = await self._synthesize_answer(prompt, solutions)
        reasoning_steps.append({
            "step": len(reasoning_steps) + 1,
            "type": "synthesis",
            "output": final_answer
        })
        
        return {
            "steps": reasoning_steps,
            "confidence": self._calculate_confidence(reasoning_steps),
            "requires_tools": self._check_tool_requirements(reasoning_steps)
        }
    
    async def _understand_problem(self, prompt: str) -> str:
        """Understand the problem being asked."""
        if not self.llm_provider:
            return f"Understanding: {prompt}"
        
        understanding_prompt = f"""Analyze this problem and explain what is being asked:
        
        Problem: {prompt}
        
        Provide a clear understanding of:
        1. What is the main question or goal?
        2. What information is provided?
        3. What might be needed to solve this?
        """
        
        return await self.llm_provider.generate(understanding_prompt)
    
    async def _decompose_problem(self, prompt: str, understanding: str) -> List[str]:
        """Break down the problem into smaller sub-problems."""
        if not self.llm_provider:
            return ["Sub-problem 1", "Sub-problem 2"]
        
        decomposition_prompt = f"""Break this problem into 2-4 smaller, manageable sub-problems:
        
        Original problem: {prompt}
        Understanding: {understanding}
        
        List each sub-problem on a new line.
        """
        
        response = await self.llm_provider.generate(decomposition_prompt)
        return [line.strip() for line in response.split('\n') if line.strip()]
    
    async def _solve_sub_problem(self, sub_problem: str) -> str:
        """Solve a single sub-problem."""
        if not self.llm_provider:
            return f"Solution to: {sub_problem}"
        
        solution_prompt = f"""Solve this specific sub-problem:
        
        Sub-problem: {sub_problem}
        
        Provide a clear, step-by-step solution.
        """
        
        return await self.llm_provider.generate(solution_prompt)
    
    async def _synthesize_answer(self, original_prompt: str, solutions: List[str]) -> str:
        """Synthesize the final answer from all solutions."""
        if not self.llm_provider:
            return "Final synthesized answer"
        
        synthesis_prompt = f"""Given these solutions to sub-problems, provide a comprehensive final answer:
        
        Original question: {original_prompt}
        
        Solutions:
        {chr(10).join(f'{i+1}. {sol}' for i, sol in enumerate(solutions))}
        
        Synthesize a clear, complete final answer.
        """
        
        return await self.llm_provider.generate(synthesis_prompt)
    
    def _calculate_confidence(self, reasoning_steps: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on reasoning quality."""
        # Simple heuristic: more steps and longer outputs = higher confidence
        if not reasoning_steps:
            return 0.0
        
        base_confidence = 0.5
        step_bonus = min(len(reasoning_steps) * 0.05, 0.3)
        
        return min(base_confidence + step_bonus, 1.0)
    
    def _check_tool_requirements(self, reasoning_steps: List[Dict[str, Any]]) -> bool:
        """Check if tools are required based on reasoning."""
        # Check if any step mentions needing external data or tools
        keywords = ["search", "calculate", "query", "fetch", "retrieve"]
        
        for step in reasoning_steps:
            output = str(step.get("output", "")).lower()
            if any(keyword in output for keyword in keywords):
                return True
        
        return False