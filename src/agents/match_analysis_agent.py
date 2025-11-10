"""
Match Analysis Agent - Analyzes match data and extracts statistics.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.analyzers.match_analyzer import MatchAnalyzer


class MatchAnalysisAgent(BaseAgent):
    """Agent specialized in analyzing match data."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("match_analysis", context_manager, event_bus)
        self.match_analyzer = MatchAnalyzer()
    
    def _setup(self) -> None:
        """Setup match analysis agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute match analysis task."""
        try:
            # Extract input data
            matches = request.input_data.get("matches", [])
            puuid = request.input_data.get("puuid")
            
            if not matches or not puuid:
                return create_response(
                    request,
                    success=False,
                    error="Missing required input: matches or puuid"
                )
            
            # Perform analysis
            analysis = self.match_analyzer.analyze_player_matches(matches, puuid)
            
            # Prepare context updates
            context_updates = {
                "match_analysis": analysis,
                "match_count": len(matches),
                "puuid": puuid
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "analysis": analysis,
                    "match_count": len(matches)
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Match analysis failed: {str(e)}"
            )

