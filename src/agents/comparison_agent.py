"""
Player Comparison Agent - Compares two players and generates insights.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.analyzers.match_analyzer import MatchAnalyzer
from src.services.aws_bedrock import BedrockService
from src.generators.social_content import SocialContentGenerator


class ComparisonAgent(BaseAgent):
    """Agent specialized in comparing players."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("player_comparison", context_manager, event_bus)
        self.match_analyzer = MatchAnalyzer()
        self.bedrock_service = BedrockService()
        self.social_generator = SocialContentGenerator()
    
    def _setup(self) -> None:
        """Setup player comparison agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute player comparison task."""
        try:
            # Extract input data
            player1_data = request.input_data.get("player1")
            player2_data = request.input_data.get("player2")
            
            if not player1_data or not player2_data:
                return create_response(
                    request,
                    success=False,
                    error="Missing required input: player1 or player2 data"
                )
            
            # Analyze both players
            matches1 = player1_data.get("matches", [])
            puuid1 = player1_data.get("puuid")
            matches2 = player2_data.get("matches", [])
            puuid2 = player2_data.get("puuid")
            
            analysis1 = self.match_analyzer.analyze_player_matches(matches1, puuid1)
            analysis2 = self.match_analyzer.analyze_player_matches(matches2, puuid2)
            
            # Generate comparison using Bedrock
            comparison = self.bedrock_service.generate_social_comparison(
                analysis1.get("key_metrics", {}),
                analysis2.get("key_metrics", {})
            )
            
            # Generate shareable content
            player1_name = player1_data.get("name", "Player 1")
            player2_name = player2_data.get("name", "Player 2")
            shareable = self.social_generator.generate_comparison_post(
                player1_name,
                player2_name,
                comparison
            )
            
            # Prepare context updates
            context_updates = {
                "comparison": {
                    "player1": {
                        "name": player1_name,
                        "stats": analysis1.get("key_metrics", {})
                    },
                    "player2": {
                        "name": player2_name,
                        "stats": analysis2.get("key_metrics", {})
                    },
                    "comparison_text": comparison,
                    "shareable_content": shareable
                }
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "player1_stats": analysis1.get("key_metrics", {}),
                    "player2_stats": analysis2.get("key_metrics", {}),
                    "comparison": comparison,
                    "shareable_content": shareable
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Player comparison failed: {str(e)}"
            )

