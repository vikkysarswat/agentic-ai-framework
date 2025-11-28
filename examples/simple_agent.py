"""
Simple Agent Example

Demonstrates basic agent usage with a single task.
"""

import asyncio
import os
from dotenv import load_dotenv

from agentic_framework import Agent, AgentConfig
from agentic_framework.llm import OpenAIProvider

load_dotenv()


async def main():
    # Initialize LLM provider
    llm_provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
        temperature=0.7
    )
    
    # Create an agent
    agent = Agent(
        config=AgentConfig(
            name="ResearchAssistant",
            role="Research specialist",
            goal="Provide accurate and comprehensive research insights",
            backstory="An experienced researcher with expertise in technology and business trends",
            verbose=True,
            memory_enabled=False  # Disable for simple example
        ),
        llm_provider=llm_provider
    )
    
    # Execute a task
    print("\n" + "="*50)
    print("Simple Agent Example")
    print("="*50 + "\n")
    
    task = "Explain what AI agents are and why they are important in 2025"
    print(f"Task: {task}\n")
    
    result = await agent.execute(task)
    
    if result["success"]:
        print("\nAgent Response:")
        print("-" * 50)
        print(result["response"]["content"])
        print("-" * 50)
        print(f"\nConfidence: {result['response']['confidence']:.2f}")
        print(f"Reasoning Steps: {result['response']['reasoning_steps']}")
    else:
        print(f"\nError: {result['error']}")
    
    # Get agent statistics
    stats = agent.get_stats()
    print("\n" + "="*50)
    print("Agent Statistics")
    print("="*50)
    print(f"Name: {stats['name']}")
    print(f"Role: {stats['role']}")
    print(f"Total Executions: {stats['executions']}")
    print(f"Memory Enabled: {stats['memory_enabled']}")


if __name__ == "__main__":
    asyncio.run(main())