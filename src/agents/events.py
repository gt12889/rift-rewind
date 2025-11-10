"""
Event-driven communication system for agents.
"""
from typing import Callable, Dict, List, Any
from enum import Enum
from datetime import datetime
import uuid


class EventType(str, Enum):
    """Event types for agent communication."""
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    CONTEXT_UPDATED = "context_updated"
    TASK_DELEGATED = "task_delegated"
    RESULT_READY = "result_ready"


class AgentEvent:
    """Event for agent communication."""
    
    def __init__(self, event_type: EventType, source: str, data: Dict[str, Any] = None):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.source = source
        self.data = data or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp
        }


class EventBus:
    """Event bus for agent communication."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._event_history: List[AgentEvent] = []
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            if handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
    
    def publish(self, event: AgentEvent) -> None:
        """Publish an event."""
        self._event_history.append(event)
        
        if event.event_type in self._subscribers:
            for handler in self._subscribers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def get_history(self) -> List[AgentEvent]:
        """Get event history."""
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """Clear event history."""
        self._event_history.clear()

