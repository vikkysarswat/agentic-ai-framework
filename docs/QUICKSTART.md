# 🚀 Quick Start Guide

Get up and running with Agentic AI Framework in 5 minutes!

## Prerequisites

- Python 3.10+
- OpenAI API key (or Anthropic Claude API key)
- Basic understanding of async/await in Python

## Installation

### Option 1: Clone from GitHub

```bash
git clone https://github.com/vikkysarswat/agentic-ai-framework.git
cd agentic-ai-framework
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Using Poetry

```bash
git clone https://github.com/vikkysarswat/agentic-ai-framework.git
cd agentic-ai-framework
poetry install
poetry shell
```

## Configuration

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

## Your First Agent (5 Lines of Code!)

Create a file `my_first_agent.py`:

```python
import asyncio
import os
from agentic_framework import Agent, AgentConfig
from agentic_framework.llm import OpenAIProvider

async def main():
    llm = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    agent = Agent(
        config=AgentConfig(
            name="Assistant",
            role="Helpful AI assistant",
            goal="Help users with their tasks"
        ),
        llm_provider=llm
    )
    
    result = await agent.execute("Explain AI agents in simple terms")
    print(result["response"]["content"])

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python my_first_agent.py
```

## Tutorial: Building a Research Team

Let's build a team of agents that work together!

### Step 1: Create Specialized Agents

```python
import asyncio
import os
from agentic_framework import Agent, AgentConfig, AgentOrchestrator, Task
from agentic_framework.llm import OpenAIProvider
from agentic_framework.orchestrator import ExecutionMode

# Initialize LLM
llm = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))

# Create specialized agents
researcher = Agent(
    config=AgentConfig(
        name="Researcher",
        role="Research specialist",
        goal="Find and analyze information"
    ),
    llm_provider=llm
)

writer = Agent(
    config=AgentConfig(
        name="Writer",
        role="Content writer",
        goal="Create engaging content"
    ),
    llm_provider=llm
)
```

### Step 2: Create the Orchestrator

```python
# Create orchestrator
orchestrator = AgentOrchestrator()
orchestrator.add_agent(researcher)
orchestrator.add_agent(writer)
```

### Step 3: Define and Execute Task

```python
# Define task
task = Task(
    description="Research AI trends and write a brief summary",
    expected_output="A well-researched summary",
    agent_sequence=[researcher, writer],
    execution_mode=ExecutionMode.SEQUENTIAL
)

# Execute
async def main():
    result = await orchestrator.execute_task(task)
    print(result["result"]["final_output"])

asyncio.run(main())
```

## Adding Memory

Agents can remember past conversations:

```python
from agentic_framework.memory import VectorMemory

# Create memory system
memory = VectorMemory(
    collection_name="my_agent_memory",
    persist_directory="./data/memory"
)

# Create agent with memory
agent = Agent(
    config=AgentConfig(
        name="MemoryAgent",
        role="Assistant with memory",
        goal="Remember our conversations",
        memory_enabled=True
    ),
    llm_provider=llm,
    memory_system=memory
)

# Now the agent will remember context!
async def main():
    await agent.execute("My name is John")
    result = await agent.execute("What's my name?")  # Will remember!
    print(result["response"]["content"])
```

## Adding Tools

Extend your agent's capabilities with tools:

```python
from agentic_framework.tools import WebSearchTool, CalculatorTool

tools = [
    WebSearchTool(),
    CalculatorTool()
]

agent = Agent(
    config=AgentConfig(
        name="PowerfulAgent",
        role="Multi-tool agent",
        goal="Complete tasks using available tools"
    ),
    llm_provider=llm,
    tools=tools
)

async def main():
    # Agent can now search and calculate!
    result = await agent.execute(
        "Search for the GDP of USA and calculate the growth rate"
    )
```

## Running Examples

We've included several complete examples:

```bash
# Simple agent
python examples/simple_agent.py

# Multi-agent team
python examples/multi_agent_team.py

# Research assistant with memory
python examples/research_assistant.py

# Customer support agent
python examples/customer_support.py

# Parallel execution
python examples/parallel_agents.py
```

## Common Patterns

### Pattern 1: Sequential Workflow

Agents work one after another:
```python
task = Task(
    agent_sequence=[agent1, agent2, agent3],
    execution_mode=ExecutionMode.SEQUENTIAL
)
```

### Pattern 2: Parallel Processing

Agents work simultaneously:
```python
task = Task(
    agent_sequence=[expert1, expert2, expert3],
    execution_mode=ExecutionMode.PARALLEL
)
```

### Pattern 3: Agent Handoff

One agent delegates to another:
```python
result = await orchestrator.agent_handoff(
    from_agent="Agent1",
    to_agent="Agent2",
    context={"handoff_task": "Continue this work"}
)
```

## Next Steps

1. **Read the docs**: Check out [docs/](.) for detailed documentation
2. **Explore examples**: See [examples/](../examples) for more use cases
3. **Join community**: Star the repo and join discussions
4. **Build something**: Create your own AI agent application!

## Troubleshooting

### Issue: Import errors

```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

### Issue: API key not working

```bash
# Check your .env file
cat .env

# Verify the key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: ChromaDB errors

```bash
# Install ChromaDB if using vector memory
pip install chromadb
```

## Resources

- [Full Documentation](README.md)
- [API Reference](api_reference.md)
- [Best Practices](best_practices.md)
- [Examples](../examples)

## Get Help

- **Issues**: [GitHub Issues](https://github.com/vikkysarswat/agentic-ai-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vikkysarswat/agentic-ai-framework/discussions)
- **Email**: support@example.com

Happy building! 🎉