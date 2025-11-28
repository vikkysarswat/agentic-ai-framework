"""
Multi-Agent Team Example

Demonstrates multiple agents collaborating on a complex task.
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
    
    # Create specialized agents
    researcher = Agent(
        config=AgentConfig(
            name="Researcher",
            role="Research specialist",
            goal="Gather comprehensive information on given topics",
            backstory="Expert at finding and synthesizing information from multiple sources",
            verbose=True
        ),
        llm_provider=llm_provider
    )
    
    analyst = Agent(
        config=AgentConfig(
            name="Analyst",
            role="Data analyst",
            goal="Analyze information and extract key insights",
            backstory="Skilled at identifying patterns and drawing meaningful conclusions",
            verbose=True
        ),
        llm_provider=llm_provider
    )
    
    writer = Agent(
        config=AgentConfig(
            name="Writer",
            role="Content writer",
            goal="Create engaging and well-structured content",
            backstory="Professional writer with expertise in technical communication",
            verbose=True
        ),
        llm_provider=llm_provider
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    orchestrator.add_agent(researcher)
    orchestrator.add_agent(analyst)
    orchestrator.add_agent(writer)
    
    print("\n" + "="*70)
    print("Multi-Agent Team Example: AI Agents Blog Post")
    print("="*70 + "\n")
    
    # Define a complex task
    task = Task(
        description="Research AI agents trends for 2025, analyze the key insights, and write a comprehensive blog post",
        expected_output="A well-researched, analyzed, and written blog post about AI agents",
        agent_sequence=[researcher, analyst, writer],
        execution_mode=ExecutionMode.SEQUENTIAL,
        timeout=600
    )
    
    print("Starting sequential execution...\n")
    print("Stage 1: Research (Researcher agent)")
    print("Stage 2: Analysis (Analyst agent)")
    print("Stage 3: Writing (Writer agent)")
    print("\n" + "-"*70 + "\n")
    
    # Execute the task
    result = await orchestrator.execute_task(task)
    
    if result["success"]:
        print("\n" + "="*70)
        print("Task Completed Successfully!")
        print("="*70 + "\n")
        
        # Display results from each agent
        for i, agent_result in enumerate(result["result"]["results"], 1):
            print(f"\nAgent {i}: {agent_result['agent']}")
            print("-" * 50)
            print(agent_result["response"]["content"][:500] + "...")
            print()
        
        print("\n" + "="*70)
        print("Execution Summary")
        print("="*70)
        print(f"Total Execution Time: {result['execution_time']:.2f} seconds")
        print(f"Agents Involved: {len(result['result']['results'])}")
    else:
        print(f"\nTask failed: {result['error']}")
    
    # Get orchestrator statistics
    stats = orchestrator.get_stats()
    print("\n" + "="*70)
    print("Orchestrator Statistics")
    print("="*70)
    print(f"Total Agents: {stats['total_agents']}")
    print(f"Agents: {', '.join(stats['agents'])}")
    print(f"Total Executions: {stats['total_executions']}")


if __name__ == "__main__":
    asyncio.run(main())