"""
Shared context manager for multi-agent system.
Provides centralized context storage with thread-safe operations.
"""
from typing import Dict, Any, Optional
from threading import Lock
from datetime import datetime
import uuid


class ContextManager:
    """Manages shared context for agent collaboration."""
    
    def __init__(self):
        self._context: Dict[str, Any] = {}
        self._lock = Lock()
        self._version = 0
        self._session_id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._history: list = []
    
    def set(self, key: str, value: Any, agent_name: Optional[str] = None) -> None:
        """Set a value in the shared context."""
        with self._lock:
            self._context[key] = value
            self._version += 1
            self._history.append({
                "version": self._version,
                "key": key,
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "action": "set"
            })
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the shared context."""
        with self._lock:
            return self._context.get(key, default)
    
    def has(self, key: str) -> bool:
        """Check if a key exists in the context."""
        with self._lock:
            return key in self._context
    
    def update(self, updates: Dict[str, Any], agent_name: Optional[str] = None) -> None:
        """Update multiple values in the context."""
        with self._lock:
            self._context.update(updates)
            self._version += 1
            self._history.append({
                "version": self._version,
                "updates": list(updates.keys()),
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "action": "update"
            })
    
    def get_all(self) -> Dict[str, Any]:
        """Get all context data."""
        with self._lock:
            return self._context.copy()
    
    def clear(self) -> None:
        """Clear all context data."""
        with self._lock:
            self._context.clear()
            self._version += 1
    
    def get_version(self) -> int:
        """Get current context version."""
        with self._lock:
            return self._version
    
    def get_session_id(self) -> str:
        """Get session ID."""
        return self._session_id
    
    def get_history(self) -> list:
        """Get context change history."""
        with self._lock:
            return self._history.copy()
    
    def cache_result(self, agent_name: str, task: str, result: Any) -> None:
        """Cache an agent's result."""
        cache_key = f"agent_result:{agent_name}:{task}"
        self.set(cache_key, {
            "result": result,
            "agent": agent_name,
            "task": task,
            "timestamp": datetime.now().isoformat()
        }, agent_name)
    
    def get_cached_result(self, agent_name: str, task: str) -> Optional[Any]:
        """Get a cached agent result."""
        cache_key = f"agent_result:{agent_name}:{task}"
        cached = self.get(cache_key)
        if cached:
            return cached.get("result")
        return None

