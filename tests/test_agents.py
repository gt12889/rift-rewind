"""
Tests for multi-agent system.
"""
import pytest
from src.agents.context_manager import ContextManager
from src.agents.registry import AgentRegistry
from src.agents.orchestrator import Orchestrator
from src.agents.match_analysis_agent import MatchAnalysisAgent
from src.agents.insights_agent import InsightsAgent
from src.agents.messages import create_request


def test_context_manager():
    """Test context manager functionality."""
    context = ContextManager()
    
    # Test set and get
    context.set("test_key", "test_value")
    assert context.get("test_key") == "test_value"
    
    # Test has
    assert context.has("test_key") is True
    assert context.has("nonexistent") is False
    
    # Test update
    context.update({"key1": "value1", "key2": "value2"})
    assert context.get("key1") == "value1"
    assert context.get("key2") == "value2"
    
    # Test versioning
    initial_version = context.get_version()
    context.set("new_key", "new_value")
    assert context.get_version() == initial_version + 1


def test_agent_registry():
    """Test agent registry."""
    context = ContextManager()
    registry = AgentRegistry()
    
    # Register agent
    agent = MatchAnalysisAgent(context)
    registry.register(agent)
    
    # Test retrieval
    retrieved = registry.get("match_analysis")
    assert retrieved is not None
    assert retrieved.get_name() == "match_analysis"
    
    # Test listing
    assert "match_analysis" in registry.list_agents()
    
    # Test health check
    assert registry.health_check("match_analysis") is True


def test_match_analysis_agent():
    """Test match analysis agent."""
    context = ContextManager()
    agent = MatchAnalysisAgent(context)
    agent.initialize()
    
    # Create test request
    request = create_request(
        "match_analysis",
        "analyze_matches",
        {
            "matches": [],
            "puuid": "test_puuid"
        }
    )
    
    # Execute agent
    response = agent.handle_request(request)
    
    # Should succeed even with empty matches
    assert response.success is True
    assert response.agent_name == "match_analysis"


def test_orchestrator():
    """Test orchestrator."""
    context = ContextManager()
    registry = AgentRegistry()
    orchestrator = Orchestrator(context, registry)
    
    # Register agents
    registry.register(MatchAnalysisAgent(context))
    registry.register(InsightsAgent(context))
    
    # Test delegation
    response = orchestrator.delegate(
        "match_analysis",
        "analyze_matches",
        {"matches": [], "puuid": "test"}
    )
    
    assert response.agent_name == "match_analysis"
    
    # Cleanup
    orchestrator.shutdown()

