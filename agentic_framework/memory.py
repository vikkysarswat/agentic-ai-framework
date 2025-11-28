"""
Memory system for agents with vector storage and retrieval.
"""

import logging
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

logger = logging.getLogger(__name__)


class MemorySystem(ABC):
    """Abstract base class for memory systems."""
    
    @abstractmethod
    async def store(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Store content in memory."""
        pass
    
    @abstractmethod
    async def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant memories."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all memories."""
        pass


class VectorMemory(MemorySystem):
    """Vector-based memory system using ChromaDB."""
    
    def __init__(self, collection_name: str = "agent_memory", persist_directory: str = "./data/chroma"):
        if chromadb is None:
            raise ImportError("chromadb is required for VectorMemory. Install with: pip install chromadb")
        
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"VectorMemory initialized with collection: {collection_name}")
    
    async def store(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Store content in vector memory."""
        doc_id = f"doc_{datetime.now().timestamp()}"
        
        metadata = metadata or {}
        metadata["timestamp"] = datetime.now().isoformat()
        
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        logger.debug(f"Stored memory: {doc_id}")
    
    async def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant memories using similarity search."""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        if results and results["documents"]:
            return results["documents"][0]
        
        return []
    
    async def clear(self) -> None:
        """Clear all memories from the collection."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Cleared collection: {self.collection_name}")


class ConversationMemory:
    """Simple conversation memory for tracking dialogue history."""
    
    def __init__(self, max_messages: int = 100):
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim old messages if exceeding max
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation messages."""
        if last_n:
            return self.messages[-last_n:]
        return self.messages
    
    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []
    
    def format_for_llm(self) -> str:
        """Format messages for LLM context."""
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])