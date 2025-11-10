"""
Year-End Summary Agent - Creates comprehensive year-end retrospectives.
"""
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.messages import AgentRequest, AgentResponse, create_response
from src.analyzers.year_summary import YearSummaryGenerator
from src.services.aws_bedrock import BedrockService


class YearSummaryAgent(BaseAgent):
    """Agent specialized in generating year-end summaries."""
    
    def __init__(self, context_manager, event_bus=None):
        super().__init__("year_summary", context_manager, event_bus)
        self.year_summary_gen = YearSummaryGenerator()
        self.bedrock_service = BedrockService()
    
    def _setup(self) -> None:
        """Setup year-end summary agent."""
        pass
    
    def execute(self, request: AgentRequest) -> AgentResponse:
        """Execute year-end summary generation task."""
        try:
            # Extract input data
            matches = request.input_data.get("matches", [])
            puuid = request.input_data.get("puuid")
            year = request.input_data.get("year", 2024)
            
            if not matches or not puuid:
                return create_response(
                    request,
                    success=False,
                    error="Missing required input: matches or puuid"
                )
            
            # Generate year summary
            year_summary = self.year_summary_gen.generate_year_summary(matches, puuid, year)
            
            # Generate AI summary using Bedrock
            ai_summary = self.bedrock_service.generate_year_end_summary(
                year_summary.get("summary", {}),
                year_summary.get("highlights", [])
            )
            
            # Prepare context updates
            context_updates = {
                "year_summary": year_summary,
                "year": year,
                "ai_summary": ai_summary
            }
            
            return create_response(
                request,
                success=True,
                result={
                    "year_summary": year_summary,
                    "ai_summary": ai_summary
                },
                context_updates=context_updates
            )
        
        except Exception as e:
            return create_response(
                request,
                success=False,
                error=f"Year-end summary generation failed: {str(e)}"
            )

