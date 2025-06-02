"""
Memory system base interfaces for AIOSv3 platform.

Provides memory management for agent conversations, context tracking,
and knowledge persistence across agent interactions.
"""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MemoryType(Enum):
    """Types of memory storage."""

    CONVERSATION = "conversation"  # Chat history and context
    KNOWLEDGE = "knowledge"  # Long-term facts and information
    PROCEDURAL = "procedural"  # How-to knowledge and procedures
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # General concepts and relationships


class MemoryPriority(Enum):
    """Memory importance levels for retention policies."""

    CRITICAL = "critical"  # Must retain indefinitely
    HIGH = "high"  # Retain for extended periods
    MEDIUM = "medium"  # Standard retention
    LOW = "low"  # Short-term retention
    EPHEMERAL = "ephemeral"  # Delete after session


class MemoryScope(Enum):
    """Scope of memory accessibility."""

    GLOBAL = "global"  # Accessible to all agents
    AGENT_TYPE = "agent_type"  # Accessible to agents of same type
    AGENT_INSTANCE = "agent_instance"  # Private to specific agent
    SESSION = "session"  # Limited to current session
    TEAM = "team"  # Shared within agent team


class MemoryEntry(BaseModel):
    """Individual memory entry."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    memory_type: MemoryType
    priority: MemoryPriority = MemoryPriority.MEDIUM
    scope: MemoryScope = MemoryScope.AGENT_INSTANCE

    # Context information
    agent_id: str
    session_id: str | None = None
    conversation_id: str | None = None
    task_id: str | None = None

    # Temporal information
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    accessed_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None

    # Semantic information
    keywords: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    embedding: list[float] | None = None

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)
    source: str | None = None
    confidence: float = 1.0  # 0.0-1.0 confidence in memory accuracy

    def update_access_time(self) -> None:
        """Update the last accessed timestamp."""
        self.accessed_at = datetime.utcnow()


class ConversationContext(BaseModel):
    """Context for a conversation thread."""

    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    session_id: str

    # Message history
    messages: list[dict[str, Any]] = Field(default_factory=list)
    total_messages: int = 0

    # Token management
    total_tokens: int = 0
    max_context_tokens: int = 32768
    compression_threshold: int = 24576  # 75% of max

    # Context state
    current_topic: str | None = None
    active_tasks: list[str] = Field(default_factory=list)
    mentioned_entities: list[str] = Field(default_factory=list)

    # Temporal tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    # Memory links
    related_memories: list[str] = Field(default_factory=list)
    summary: str | None = None

    def add_message(self, message: dict[str, Any], tokens: int = 0) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.total_messages += 1
        self.total_tokens += tokens
        self.last_activity = datetime.utcnow()

    def needs_compression(self) -> bool:
        """Check if conversation needs token compression."""
        return self.total_tokens > self.compression_threshold


class MemoryQuery(BaseModel):
    """Query for retrieving memories."""

    # Content filtering
    query_text: str | None = None
    keywords: list[str] | None = None
    categories: list[str] | None = None

    # Type and scope filtering
    memory_types: list[MemoryType] | None = None
    scopes: list[MemoryScope] | None = None
    priorities: list[MemoryPriority] | None = None

    # Context filtering
    agent_id: str | None = None
    session_id: str | None = None
    conversation_id: str | None = None
    task_id: str | None = None

    # Temporal filtering
    created_after: datetime | None = None
    created_before: datetime | None = None
    accessed_after: datetime | None = None

    # Semantic search
    use_semantic_search: bool = True
    similarity_threshold: float = 0.7

    # Result configuration
    limit: int = 10
    offset: int = 0
    include_expired: bool = False


class MemorySearchResult(BaseModel):
    """Result from memory search."""

    entry: MemoryEntry
    relevance_score: float = 0.0
    similarity_score: float | None = None
    match_reasons: list[str] = Field(default_factory=list)


class MemoryStats(BaseModel):
    """Statistics about memory usage."""

    total_entries: int = 0
    entries_by_type: dict[str, int] = Field(default_factory=dict)
    entries_by_scope: dict[str, int] = Field(default_factory=dict)
    entries_by_priority: dict[str, int] = Field(default_factory=dict)

    # Storage metrics
    total_size_bytes: int = 0
    embedding_count: int = 0
    expired_entries: int = 0

    # Activity metrics
    daily_accesses: int = 0
    weekly_accesses: int = 0
    most_accessed_entries: list[str] = Field(default_factory=list)

    # Performance metrics
    avg_query_time_ms: float = 0.0
    cache_hit_rate: float = 0.0


class MemoryBackend(ABC):
    """Abstract base class for memory storage backends."""

    def __init__(self, config: dict[str, Any]):
        """Initialize the memory backend."""
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the backend connection and resources."""
        pass

    @abstractmethod
    async def store_memory(self, entry: MemoryEntry) -> str:
        """Store a memory entry and return its ID."""
        pass

    @abstractmethod
    async def get_memory(self, memory_id: str) -> MemoryEntry | None:
        """Retrieve a specific memory by ID."""
        pass

    @abstractmethod
    async def update_memory(self, memory_id: str, entry: MemoryEntry) -> bool:
        """Update an existing memory entry."""
        pass

    @abstractmethod
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory entry."""
        pass

    @abstractmethod
    async def search_memories(self, query: MemoryQuery) -> list[MemorySearchResult]:
        """Search for memories matching the query."""
        pass

    @abstractmethod
    async def store_conversation(self, context: ConversationContext) -> str:
        """Store conversation context."""
        pass

    @abstractmethod
    async def get_conversation(self, conversation_id: str) -> ConversationContext | None:
        """Retrieve conversation context."""
        pass

    @abstractmethod
    async def update_conversation(self, context: ConversationContext) -> bool:
        """Update conversation context."""
        pass

    @abstractmethod
    async def cleanup_expired(self) -> int:
        """Remove expired memories and return count of deleted entries."""
        pass

    @abstractmethod
    async def get_stats(self) -> MemoryStats:
        """Get memory usage statistics."""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the backend and cleanup resources."""
        pass


class EmbeddingProvider(ABC):
    """Abstract base class for text embedding providers."""

    @abstractmethod
    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for text."""
        pass

    @abstractmethod
    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for multiple texts."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of embedding vectors."""
        pass


class MemoryManager(ABC):
    """Abstract base class for memory management."""

    def __init__(self, backend: MemoryBackend, embedding_provider: EmbeddingProvider | None = None):
        """Initialize the memory manager."""
        self.backend = backend
        self.embedding_provider = embedding_provider

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the memory manager and its backend."""
        pass

    @abstractmethod
    async def store(
        self,
        content: str,
        memory_type: MemoryType,
        agent_id: str,
        priority: MemoryPriority = MemoryPriority.MEDIUM,
        scope: MemoryScope = MemoryScope.AGENT_INSTANCE,
        **kwargs
    ) -> str:
        """Store a new memory entry."""
        pass

    @abstractmethod
    async def retrieve(
        self,
        query: str | MemoryQuery,
        agent_id: str,
        limit: int = 10
    ) -> list[MemorySearchResult]:
        """Retrieve memories matching the query."""
        pass

    @abstractmethod
    async def update(self, memory_id: str, **updates) -> bool:
        """Update a memory entry."""
        pass

    @abstractmethod
    async def forget(self, memory_id: str) -> bool:
        """Delete a memory entry."""
        pass

    @abstractmethod
    async def get_conversation_context(
        self,
        conversation_id: str,
        agent_id: str
    ) -> ConversationContext | None:
        """Get conversation context for managing chat history."""
        pass

    @abstractmethod
    async def update_conversation_context(
        self,
        context: ConversationContext
    ) -> bool:
        """Update conversation context."""
        pass

    @abstractmethod
    async def compress_conversation(
        self,
        conversation_id: str,
        agent_id: str
    ) -> bool:
        """Compress conversation history when context becomes too long."""
        pass

    @abstractmethod
    async def cleanup(self) -> int:
        """Clean up expired memories."""
        pass

    @abstractmethod
    async def get_statistics(self) -> MemoryStats:
        """Get memory usage statistics."""
        pass
