"""
Base agent class for all specialized agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.agents.context_manager import ContextManager
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.agents.events import EventBus, EventType, AgentEvent


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, context_manager: ContextManager, event_bus: Optional[EventBus] = None):
        self.name = name
        self.context_manager = context_manager
        self.event_bus = event_bus or EventBus()
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize the agent."""
        if not self._initialized:
            self._setup()
            self._initialized = True
            self._publish_event(EventType.AGENT_STARTED, {"agent": self.name})
    
    @abstractmethod
    def _setup(self) -> None:
        """Setup agent-specific configuration."""
        pass
    
    @abstractmethod
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute the agent's task."""
        pass
    
    def read_from_context(self, keys: list) -> Dict[str, Any]:
        """Read values from shared context."""
        result = {}
        for key in keys:
            value = self.context_manager.get(key)
            if value is not None:
                result[key] = value
        return result
    
    def write_to_context(self, updates: Dict[str, Any]) -> None:
        """Write values to shared context."""
        self.context_manager.update(updates, self.name)
        self._publish_event(EventType.CONTEXT_UPDATED, {
            "agent": self.name,
            "keys": list(updates.keys())
        })
    
    def _publish_event(self, event_type: EventType, data: Dict[str, Any]) -> None:
        """Publish an event."""
        event = AgentEvent(event_type, self.name, data)
        self.event_bus.publish(event)
    
    def handle_request(self, request: AgentRequest) -> AgentResponse:
        """Handle an agent request."""
        try:
            # Read context if needed
            if request.context_keys:
                context_data = self.read_from_context(request.context_keys)
                request.input_data.update(context_data)
            
            # Execute the task
            result = self.execute(request)
            
            # Write to context if needed
            if result.success and result.context_updates:
                self.write_to_context(result.context_updates)
            
            # Publish completion event
            self._publish_event(EventType.AGENT_COMPLETED, {
                "agent": self.name,
                "task": request.task,
                "success": result.success
            })
            
            return result
        
        except Exception as e:
            error_response = create_response(
                request,
                success=False,
                error=str(e)
            )
            self._publish_event(EventType.AGENT_FAILED, {
                "agent": self.name,
                "task": request.task,
                "error": str(e)
            })
            return error_response
    
    def get_name(self) -> str:
        """Get agent name."""
        return self.name
    
    def is_initialized(self) -> bool:
        """Check if agent is initialized."""
        return self._initialized

