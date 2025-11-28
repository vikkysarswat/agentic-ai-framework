"""
Research Assistant Example

Demonstrates an agent with memory and tool usage for research tasks.
"""

import asyncio
import os
from dotenv import load_dotenv

from agentic_framework import Agent, AgentConfig
from agentic_framework.llm import OpenAIProvider
from agentic_framework.memory import VectorMemory
from agentic_framework.tools import WebSearchTool, CalculatorTool

load_dotenv()


async def main():
    # Initialize components
    llm_provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4"
    )
    
    memory_system = VectorMemory(
        collection_name="research_memory",
        persist_directory="./data/research_memory"
    )
    
    tools = [
        WebSearchTool(),
        CalculatorTool()
    ]
    
    # Create research assistant
    research_assistant = Agent(
        config=AgentConfig(
            name="ResearchAssistant",
            role="Advanced research assistant",
            goal="Conduct thorough research and provide actionable insights",
            backstory="AI-powered assistant with access to web search and analytical tools",
            verbose=True,
            memory_enabled=True,
            allow_delegation=True
        ),
        llm_provider=llm_provider,
        memory_system=memory_system,
        tools=tools
    )
    
    print("\n" + "="*70)
    print("Research Assistant with Memory and Tools")
    print("="*70 + "\n")
    
    # Task 1: Research task
    print("Task 1: Initial Research")
    print("-" * 70)
    task1 = "Research the latest developments in AI agents and their enterprise applications"
    result1 = await research_assistant.execute(task1)
    
    if result1["success"]:
        print(f"\nResponse: {result1['response']['content'][:400]}...\n")
    
    # Task 2: Follow-up question (should use memory)
    print("\nTask 2: Follow-up Question (Using Memory)")
    print("-" * 70)
    task2 = "Based on what we discussed, what are the top 3 challenges in implementing AI agents?"
    result2 = await research_assistant.execute(task2)
    
    if result2["success"]:
        print(f"\nResponse: {result2['response']['content'][:400]}...\n")
    
    # Task 3: Calculation task
    print("\nTask 3: Market Size Calculation")
    print("-" * 70)
    task3 = "If the AI agents market is $5 billion today and grows at 30% annually, what will it be in 3 years?"
    result3 = await research_assistant.execute(task3)
    
    if result3["success"]:
        print(f"\nResponse: {result3['response']['content']}\n")
    
    # Display agent stats
    stats = research_assistant.get_stats()
    print("\n" + "="*70)
    print("Agent Statistics")
    print("="*70)
    print(f"Total Executions: {stats['executions']}")
    print(f"Memory Enabled: {stats['memory_enabled']}")
    print(f"Tools Available: {stats['tools_available']}")
    print(f"Active Since: {stats['created_at']}")


if __name__ == "__main__":
    asyncio.run(main())