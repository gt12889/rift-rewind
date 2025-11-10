"""
Insights Generation Agent - Generates AI-powered insights from analyzed data.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.services.aws_bedrock import BedrockService


class InsightsAgent(BaseAgent):
    """Agent specialized in generating AI-powered insights."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("insights_generation", context_manager, event_bus)
        self.bedrock_service = BedrockService()
    
    def _setup(self) -> None:
        """Setup insights generation agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute insights generation task."""
        try:
            # Get match analysis from context or input
            match_analysis = request.input_data.get("match_analysis")
            if not match_analysis:
                # Try to get from context
                match_analysis = self.context_manager.get("match_analysis")
            
            if not match_analysis:
                return create_response(
                    request,
                    success=False,
                    error="Match analysis not found in input or context"
                )
            
            # Get player match data
            player_matches = request.input_data.get("player_matches", [])
            key_metrics = match_analysis.get("key_metrics", {})
            
            # Generate insights using Bedrock
            ai_insights = self.bedrock_service.generate_insights(
                player_matches[:20] if player_matches else [],
                key_metrics
            )
            
            # Prepare context updates
            context_updates = {
                "insights": ai_insights,
                "strengths": ai_insights.get("strengths", []),
                "weaknesses": ai_insights.get("weaknesses", []),
                "unexpected_insights": ai_insights.get("unexpected_insights", []),
                "recommendations": ai_insights.get("recommendations", [])
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "insights": ai_insights
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Insights generation failed: {str(e)}"
            )

