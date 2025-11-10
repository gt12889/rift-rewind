"""
Agent communication protocol and message formats.
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Message types for agent communication."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class AgentMessage(BaseModel):
    """Standardized message format for agent communication."""
    message_id: str
    message_type: MessageType
    from_agent: str
    to_agent: Optional[str] = None
    task: str
    payload: Dict[str, Any]
    timestamp: str
    context_version: Optional[int] = None
    
    class Config:
        use_enum_values = True


class AgentRequest(BaseModel):
    """Request message from orchestrator to agent."""
    request_id: str
    agent_name: str
    task: str
    input_data: Dict[str, Any]
    context_keys: Optional[List[str]] = None  # Keys to read from context
    output_keys: Optional[List[str]] = None  # Keys to write to context
    timestamp: str = datetime.now().isoformat()


class AgentResponse(BaseModel):
    """Response message from agent to orchestrator."""
    request_id: str
    agent_name: str
    task: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    context_updates: Optional[Dict[str, Any]] = None
    timestamp: str = datetime.now().isoformat()


def create_request(agent_name: str, task: str, input_data: Dict[str, Any], 
                   context_keys: Optional[List[str]] = None,
                   output_keys: Optional[List[str]] = None) -> AgentRequest:
    """Create a standardized agent request."""
    import uuid
    return AgentRequest(
        request_id=str(uuid.uuid4()),
        agent_name=agent_name,
        task=task,
        input_data=input_data,
        context_keys=context_keys,
        output_keys=output_keys
    )


def create_response(request: AgentRequest, success: bool, 
                   result: Optional[Dict[str, Any]] = None,
                   error: Optional[str] = None,
                   context_updates: Optional[Dict[str, Any]] = None) -> AgentResponse:
    """Create a standardized agent response."""
    return AgentResponse(
        request_id=request.request_id,
        agent_name=request.agent_name,
        task=request.task,
        success=success,
        result=result,
        error=error,
        context_updates=context_updates
    )

