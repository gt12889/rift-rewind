"""
Social Content Agent - Generates shareable social media content.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.generators.social_content import SocialContentGenerator


class SocialContentAgent(BaseAgent):
    """Agent specialized in generating social media content."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("social_content", context_manager, event_bus)
        self.social_generator = SocialContentGenerator()
    
    def _setup(self) -> None:
        """Setup social content agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute social content generation task."""
        try:
            content_type = request.input_data.get("content_type", "year-end")
            
            # Get insights from context
            insights = self.context_manager.get("insights", {})
            year_summary = self.context_manager.get("year_summary")
            
            if content_type == "year-end" and year_summary:
                # Generate year-end card
                content = self.social_generator.generate_year_end_card(year_summary)
            elif content_type == "insights" and insights:
                # Generate insight card
                content = self.social_generator.generate_insight_card(insights)
            else:
                return create_response(
                    request,
                    success=False,
                    error=f"Content type '{content_type}' not supported or missing data"
                )
            
            # Prepare context updates
            context_updates = {
                "social_content": content,
                "content_type": content_type
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "content": content,
                    "content_type": content_type
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Social content generation failed: {str(e)}"
            )

