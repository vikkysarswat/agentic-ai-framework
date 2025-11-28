"""
Customer Support Agent Example

Demonstrates an AI agent for handling customer support queries.
"""

import asyncio
import os
from dotenv import load_dotenv

from agentic_framework import Agent, AgentConfig
from agentic_framework.llm import OpenAIProvider
from agentic_framework.memory import ConversationMemory

load_dotenv()


class CustomerSupportAgent:
    """Customer support agent with conversation memory."""
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.conversation_memory = ConversationMemory(max_messages=50)
    
    async def handle_query(self, customer_query: str) -> str:
        """Handle a customer query."""
        # Add customer query to conversation memory
        self.conversation_memory.add_message("customer", customer_query)
        
        # Build context with conversation history
        context = {
            "conversation_history": self.conversation_memory.format_for_llm(),
            "customer_query": customer_query
        }
        
        # Execute agent
        result = await self.agent.execute(customer_query, context)
        
        if result["success"]:
            response = result["response"]["content"]
            self.conversation_memory.add_message("agent", response)
            return response
        else:
            return "I apologize, but I encountered an error. Please try again or contact human support."
    
    def get_conversation_history(self):
        """Get the conversation history."""
        return self.conversation_memory.get_messages()


async def main():
    # Initialize LLM provider
    llm_provider = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
        temperature=0.5  # Lower temperature for more consistent support
    )
    
    # Create customer support agent
    agent = Agent(
        config=AgentConfig(
            name="SupportAgent",
            role="Customer support specialist",
            goal="Provide helpful, accurate, and empathetic customer support",
            backstory="Experienced support agent trained to handle various customer inquiries with professionalism",
            verbose=True,
            memory_enabled=False  # Using conversation memory instead
        ),
        llm_provider=llm_provider
    )
    
    support_agent = CustomerSupportAgent(agent)
    
    print("\n" + "="*70)
    print("Customer Support Agent - Interactive Demo")
    print("="*70 + "\n")
    
    # Simulate a customer support conversation
    queries = [
        "Hi, I'm having trouble logging into my account",
        "I've tried resetting my password but I'm not receiving the email",
        "What other options do I have to recover my account?",
        "Thank you for your help!"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"Customer Query #{i}")
        print(f"{'='*70}")
        print(f"Customer: {query}\n")
        
        response = await support_agent.handle_query(query)
        
        print(f"Agent: {response}\n")
        
        # Small delay for readability
        await asyncio.sleep(1)
    
    # Display conversation summary
    print("\n" + "="*70)
    print("Conversation Summary")
    print("="*70)
    
    history = support_agent.get_conversation_history()
    print(f"Total Messages: {len(history)}")
    print(f"Customer Messages: {sum(1 for m in history if m['role'] == 'customer')}")
    print(f"Agent Responses: {sum(1 for m in history if m['role'] == 'agent')}")
    
    # Display agent stats
    stats = agent.get_stats()
    print("\n" + "="*70)
    print("Agent Statistics")
    print("="*70)
    print(f"Agent Name: {stats['name']}")
    print(f"Total Executions: {stats['executions']}")


if __name__ == "__main__":
    asyncio.run(main())