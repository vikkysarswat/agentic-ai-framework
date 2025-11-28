"""
Parallel Agent Execution Example

Demonstrates multiple agents working simultaneously on the same task.
"""

import asyncio
import os
from dotenv import load_dotenv

from agentic_framework import Agent, AgentConfig, AgentOrchestrator, Task
from agentic_framework.llm import OpenAIProvider
from agentic_framework.orchestrator import ExecutionMode

load_dotenv()


async def main():
    # Initialize LLM provider
    llm_provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4"
    )
    
    # Create agents with different perspectives
    technical_expert = Agent(
        config=AgentConfig(
            name="TechnicalExpert",
            role="Technical architect",
            goal="Evaluate technical feasibility and architecture",
            backstory="Senior engineer with deep expertise in system design"
        ),
        llm_provider=llm_provider
    )
    
    business_analyst = Agent(
        config=AgentConfig(
            name="BusinessAnalyst",
            role="Business strategist",
            goal="Assess business value and ROI",
            backstory="Experienced analyst focused on business outcomes"
        ),
        llm_provider=llm_provider
    )
    
    security_expert = Agent(
        config=AgentConfig(
            name="SecurityExpert",
            role="Security specialist",
            goal="Identify security risks and mitigation strategies",
            backstory="Cybersecurity expert with focus on AI systems"
        ),
        llm_provider=llm_provider
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    orchestrator.add_agent(technical_expert)
    orchestrator.add_agent(business_analyst)
    orchestrator.add_agent(security_expert)
    
    print("\n" + "="*70)
    print("Parallel Agent Execution: AI Agent Implementation Review")
    print("="*70 + "\n")
    
    # Define task for parallel execution
    task = Task(
        description="Evaluate the implementation of an AI agent system for customer service automation. Provide your expert perspective.",
        expected_output="Expert evaluation from multiple perspectives",
        agent_sequence=[technical_expert, business_analyst, security_expert],
        execution_mode=ExecutionMode.PARALLEL,
        timeout=300
    )
    
    print("Executing agents in parallel...\n")
    print("- Technical Expert: Evaluating technical aspects")
    print("- Business Analyst: Assessing business value")
    print("- Security Expert: Analyzing security implications")
    print("\n" + "-"*70 + "\n")
    
    # Execute the task
    result = await orchestrator.execute_task(task)
    
    if result["success"]:
        print("\n" + "="*70)
        print("Parallel Execution Results")
        print("="*70 + "\n")
        
        # Display each agent's perspective
        for agent_result in result["result"]["results"]:
            if agent_result.get("success"):
                print(f"\n{agent_result['agent']} Perspective:")
                print("-" * 70)
                content = agent_result["response"]["content"]
                print(content[:500] + "..." if len(content) > 500 else content)
                print()
        
        print("\n" + "="*70)
        print("Execution Summary")
        print("="*70)
        print(f"Execution Mode: Parallel")
        print(f"Total Time: {result['execution_time']:.2f} seconds")
        print(f"Successful Agents: {result['result']['successful_agents']}/{len(task.agent_sequence)}")
        print("\nBenefit: All agents provided input simultaneously, saving time!")
    else:
        print(f"\nTask failed: {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())