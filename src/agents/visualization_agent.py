"""
Visualization Agent - Creates charts and visualizations.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.generators.visualizations import VisualizationGenerator


class VisualizationAgent(BaseAgent):
    """Agent specialized in creating visualizations."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("visualization", context_manager, event_bus)
        self.viz_generator = VisualizationGenerator()
    
    def _setup(self) -> None:
        """Setup visualization agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute visualization generation task."""
        try:
            # Get required data from context or input
            matches = request.input_data.get("matches", [])
            puuid = request.input_data.get("puuid")
            match_analysis = request.input_data.get("match_analysis")
            
            # Try to get from context if not in input
            if not matches:
                matches = self.context_manager.get("matches", [])
            if not puuid:
                puuid = self.context_manager.get("puuid")
            if not match_analysis:
                match_analysis = self.context_manager.get("match_analysis", {})
            
            # If still missing, try to get from context keys
            if request.context_keys:
                context_data = self.read_from_context(request.context_keys)
                if not matches and "matches" in context_data:
                    matches = context_data["matches"]
                if not puuid and "puuid" in context_data:
                    puuid = context_data["puuid"]
                if not match_analysis and "match_analysis" in context_data:
                    match_analysis = context_data["match_analysis"]
            
            if not matches or not puuid:
                return create_response(
                    request,
                    success=False,
                    error="Missing required input: matches or puuid"
                )
            
            # Generate visualizations
            visualizations = {}
            
            try:
                visualizations["win_rate_chart"] = self.viz_generator.generate_win_rate_chart(matches, puuid)
            except Exception as e:
                print(f"Error generating win rate chart: {e}")
            
            try:
                visualizations["kda_trend"] = self.viz_generator.generate_kda_trend(matches, puuid)
            except Exception as e:
                print(f"Error generating KDA trend: {e}")
            
            try:
                champion_stats = match_analysis.get("champion_stats", {})
                visualizations["champion_performance"] = self.viz_generator.generate_champion_performance(champion_stats)
            except Exception as e:
                print(f"Error generating champion performance: {e}")
            
            try:
                role_stats = match_analysis.get("role_stats", {})
                visualizations["role_performance"] = self.viz_generator.generate_role_performance(role_stats)
            except Exception as e:
                print(f"Error generating role performance: {e}")
            
            # Prepare context updates
            context_updates = {
                "visualizations": visualizations
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "visualizations": visualizations
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Visualization generation failed: {str(e)}"
            )

