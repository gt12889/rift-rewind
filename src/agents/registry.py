"""
Agent registry for agent discovery and management.
"""
from typing import Dict, Optional, List
from src.agents.base_agent import BaseAgent


class AgentRegistry:
    """Registry for managing agents."""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_health: Dict[str, bool] = {}
    
    def register(self, agent: BaseAgent) -> None:
        """Register an agent."""
        agent.initialize()
        self._agents[agent.get_name()] = agent
        self._agent_health[agent.get_name()] = True
    
    def get(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self._agents.get(agent_name)
    
    def get_all(self) -> Dict[str, BaseAgent]:
        """Get all registered agents."""
        return self._agents.copy()
    
    def list_agents(self) -> List[str]:
        """List all registered agent names."""
        return list(self._agents.keys())
    
    def is_registered(self, agent_name: str) -> bool:
        """Check if an agent is registered."""
        return agent_name in self._agents
    
    def health_check(self, agent_name: str) -> bool:
        """Perform health check on an agent."""
        if agent_name not in self._agents:
            return False
        
        agent = self._agents[agent_name]
        try:
            # Check if agent is initialized
            if not agent.is_initialized():
                self._agent_health[agent_name] = False
                return False
            
            self._agent_health[agent_name] = True
            return True
        except Exception:
            self._agent_health[agent_name] = False
            return False
    
    def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all agents."""
        results = {}
        for agent_name in self._agents.keys():
            results[agent_name] = self.health_check(agent_name)
        return results
    
    def get_health_status(self, agent_name: str) -> bool:
        """Get cached health status."""
        return self._agent_health.get(agent_name, False)
    
    def unregister(self, agent_name: str) -> None:
        """Unregister an agent."""
        if agent_name in self._agents:
            del self._agents[agent_name]
        if agent_name in self._agent_health:
            del self._agent_health[agent_name]

