"""
Tests for Memory systems
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from agentic_framework.memory import VectorMemory, ConversationMemory


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.mark.asyncio
async def test_vector_memory_store_retrieve(temp_dir):
    """Test storing and retrieving from vector memory."""
    memory = VectorMemory(
        collection_name="test_memory",
        persist_directory=temp_dir
    )
    
    # Store some content
    await memory.store("AI agents are autonomous systems")
    await memory.store("Machine learning powers AI agents")
    
    # Retrieve similar content
    results = await memory.retrieve("What are AI agents?", k=2)
    
    assert len(results) <= 2
    assert any("agents" in r.lower() for r in results)


@pytest.mark.asyncio
async def test_vector_memory_clear(temp_dir):
    """Test clearing vector memory."""
    memory = VectorMemory(
        collection_name="test_clear",
        persist_directory=temp_dir
    )
    
    await memory.store("Test content")
    await memory.clear()
    
    results = await memory.retrieve("Test", k=5)
    assert len(results) == 0


def test_conversation_memory():
    """Test conversation memory."""
    memory = ConversationMemory(max_messages=5)
    
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")
    
    messages = memory.get_messages()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["content"] == "Hi there!"


def test_conversation_memory_max_limit():
    """Test conversation memory max limit."""
    memory = ConversationMemory(max_messages=3)
    
    for i in range(5):
        memory.add_message("user", f"Message {i}")
    
    messages = memory.get_messages()
    assert len(messages) == 3
    assert messages[0]["content"] == "Message 2"