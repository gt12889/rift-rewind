"""
FastAPI application main file.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from pydantic import BaseModel
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from config.settings import settings
from src.services.riot_api import RiotAPIClient
from src.services.aws_bedrock import BedrockService
from src.services.aws_comprehend import ComprehendService
from src.analyzers.match_analyzer import MatchAnalyzer
from src.analyzers.year_summary import YearSummaryGenerator
from src.analyzers.rank_comparison import RankComparisonAnalyzer
from src.generators.visualizations import VisualizationGenerator
from src.generators.social_content import SocialContentGenerator
from src.agents.context_manager import ContextManager
from src.agents.registry import AgentRegistry
from src.agents.orchestrator import Orchestrator
from src.agents.match_analysis_agent import MatchAnalysisAgent
from src.agents.insights_agent import InsightsAgent
from src.agents.visualization_agent import VisualizationAgent
from src.agents.social_content_agent import SocialContentAgent
from src.agents.year_summary_agent import YearSummaryAgent
from src.agents.comparison_agent import ComparisonAgent


app = FastAPI(
    title="Rift Rewind API",
    description="AI-powered League of Legends coaching agent",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
riot_client = RiotAPIClient()
bedrock_service = BedrockService()
comprehend_service = ComprehendService()
match_analyzer = MatchAnalyzer()
year_summary_gen = YearSummaryGenerator()
rank_comparison = RankComparisonAnalyzer()
viz_generator = VisualizationGenerator()
social_generator = SocialContentGenerator()

# Initialize multi-agent system
context_manager = ContextManager()
agent_registry = AgentRegistry()
orchestrator = Orchestrator(context_manager, agent_registry)

# Register agents
agent_registry.register(MatchAnalysisAgent(context_manager))
agent_registry.register(InsightsAgent(context_manager))
agent_registry.register(VisualizationAgent(context_manager))
agent_registry.register(SocialContentAgent(context_manager))
agent_registry.register(YearSummaryAgent(context_manager))
agent_registry.register(ComparisonAgent(context_manager))


# Request/Response Models
class PlayerInsightsResponse(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    trends: str
    unexpected_insights: List[str]
    recommendations: List[str]
    key_metrics: dict
    rank_info: Optional[dict] = None
    rank_comparisons: Optional[dict] = None
    visualizations: Optional[dict] = None


class YearSummaryResponse(BaseModel):
    year: int
    summary: dict
    highlights: List[dict]
    strengths: List[str]
    weaknesses: List[str]
    growth_areas: List[str]
    ai_generated_summary: str
    shareable_content: dict


class MatchAnalysisResponse(BaseModel):
    match_id: str
    analysis: str
    key_moments: List[str]
    recommendations: List[str]


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    response: str
    message_id: Optional[str] = None


# Serve static files - Angular app takes priority
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
angular_dir = os.path.join(static_dir, "angular", "browser")  # Angular 17+ outputs to "browser" subdirectory

# Debug logging
logger.info(f"Static dir: {static_dir}")
logger.info(f"Angular dir: {angular_dir}")
logger.info(f"Static dir exists: {os.path.exists(static_dir)}")
logger.info(f"Angular dir exists: {os.path.exists(angular_dir)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/player/{summoner_name}/insights", response_model=PlayerInsightsResponse)
async def get_player_insights(
    summoner_name: str,
    region: str = Query(default="na1", description="League region"),
    match_count: int = Query(default=50, ge=1, le=100, description="Number of matches to analyze")
):
    """Get personalized insights for a player."""
    logger.info(f"API route hit: /api/player/{summoner_name}/insights")
    logger.info(f"Summoner name: {summoner_name}, Region: {region}, Match count: {match_count}")
    try:
        # Get summoner info
        summoner = riot_client.get_summoner_by_name(summoner_name, region)
        puuid = summoner.get("puuid")
        
        if not puuid:
            raise HTTPException(status_code=404, detail="Summoner not found")
        
        # Get match history
        match_ids = riot_client.get_match_history(puuid, count=match_count)
        matches = [riot_client.get_match_details(mid) for mid in match_ids[:match_count]]
        
        # Get player-specific match data
        player_matches = []
        for match in matches:
            player_data = riot_client.get_player_match_data(match, puuid)
            if player_data:
                player_matches.append(player_data)
        
        # Use multi-agent system to generate insights
        result = orchestrator.get_player_insights_workflow(matches, puuid, player_matches[:20])
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("details", "Agent workflow failed"))
        
        # Extract results from context
        analysis = result.get("match_analysis", {})
        insights = result.get("insights", {})
        visualizations = result.get("visualizations", {})
        
        # Get rank info if available (optional)
        rank_info = None
        rank_tier = None
        try:
            # Try to get rank info from Riot API (optional, may not be available)
            rank_info = riot_client.get_rank_info(puuid, region) if hasattr(riot_client, 'get_rank_info') else None
            if rank_info and rank_info.get("solo_queue"):
                rank_tier = rank_info["solo_queue"].get("tier", "GOLD")
        except Exception:
            # Rank info is optional, continue without it
            pass
        
        # Calculate rank comparisons
        rank_comparisons = None
        if rank_tier and matches:
            try:
                player_metrics = result.get("key_metrics", {})
                player_kda = player_metrics.get("avg_kda", 0)
                
                # KDA comparison
                kda_comparison = rank_comparison.compare_kda(player_kda, rank_tier)
                
                # CS/min comparison
                player_cs_per_min = rank_comparison.calculate_player_cs_per_min(matches, puuid)
                cs_comparison = rank_comparison.compare_cs_per_min(player_cs_per_min, rank_tier)
                
                # Champion win rate comparison (use most played champion)
                most_played_champ = rank_comparison.get_most_played_champion(matches, puuid)
                champ_win_rate_comparison = None
                if most_played_champ:
                    champ_win_rate = rank_comparison.get_champion_win_rate(matches, puuid, most_played_champ)
                    if champ_win_rate is not None:
                        champ_win_rate_comparison = rank_comparison.compare_champion_win_rate(
                            champ_win_rate, most_played_champ, rank_tier
                        )
                
                rank_comparisons = {
                    "kda_vs_rank": kda_comparison,
                    "cs_per_min_vs_rank": cs_comparison,
                    "champion_win_rate": champ_win_rate_comparison
                }
            except Exception as e:
                # Comparison is optional, continue without it
                pass
        
        return PlayerInsightsResponse(
            strengths=insights.get("strengths", analysis.get("strengths", [])),
            weaknesses=insights.get("weaknesses", analysis.get("weaknesses", [])),
            trends=insights.get("trends", ""),
            unexpected_insights=insights.get("unexpected_insights", []),
            recommendations=insights.get("recommendations", []),
            key_metrics=result.get("key_metrics", {}),
            rank_info=rank_info,
            rank_comparisons=rank_comparisons,
            visualizations=visualizations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/player/{summoner_name}/year-summary", response_model=YearSummaryResponse)
async def get_year_summary(
    summoner_name: str,
    year: int = Query(default=2024, ge=2020, le=2025, description="Year to analyze"),
    region: str = Query(default="na1", description="League region")
):
    """Get year-end summary for a player."""
    try:
        # Get summoner info
        summoner = riot_client.get_summoner_by_name(summoner_name, region)
        puuid = summoner.get("puuid")
        
        if not puuid:
            raise HTTPException(status_code=404, detail="Summoner not found")
        
        # Get full year matches
        matches = riot_client.get_full_year_matches(puuid, year)
        
        # Use multi-agent system to generate year summary
        result = orchestrator.get_year_summary_workflow(matches, puuid, year)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("details", "Agent workflow failed"))
        
        # Extract results
        year_summary = result.get("year_summary", {})
        ai_summary = result.get("ai_summary", "")
        shareable = result.get("social_content", {})
        
        return YearSummaryResponse(
            year=year,
            summary=year_summary.get("summary", {}),
            highlights=year_summary.get("highlights", []),
            strengths=year_summary.get("strengths", []),
            weaknesses=year_summary.get("weaknesses", []),
            growth_areas=year_summary.get("growth_areas", []),
            ai_generated_summary=ai_summary,
            shareable_content=shareable
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/match/{match_id}/analysis", response_model=MatchAnalysisResponse)
async def get_match_analysis(
    match_id: str,
    puuid: str = Query(description="Player PUUID")
):
    """Get detailed analysis for a specific match."""
    try:
        match = riot_client.get_match_details(match_id)
        player_data = riot_client.get_player_match_data(match, puuid)
        
        if not player_data:
            raise HTTPException(status_code=404, detail="Player not found in match")
        
        # Generate AI analysis
        analysis = bedrock_service.generate_match_analysis(match, player_data)
        
        # Use Comprehend for additional insights
        comprehend_analysis = comprehend_service.analyze_match_commentary(analysis)
        
        return MatchAnalysisResponse(
            match_id=match_id,
            analysis=analysis,
            key_moments=comprehend_analysis.get("insights", {}).get("focus_areas", []),
            recommendations=[]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/player/{summoner_name}/compare")
async def compare_players(
    summoner_name: str,
    friend_name: str = Query(description="Friend's summoner name"),
    region: str = Query(default="na1", description="League region")
):
    """Compare two players."""
    try:
        # Get both players' info
        player1 = riot_client.get_summoner_by_name(summoner_name, region)
        player2 = riot_client.get_summoner_by_name(friend_name, region)
        
        puuid1 = player1.get("puuid")
        puuid2 = player2.get("puuid")
        
        if not puuid1 or not puuid2:
            raise HTTPException(status_code=404, detail="One or both summoners not found")
        
        # Get match histories
        matches1 = riot_client.get_match_history(puuid1, count=50)
        matches2 = riot_client.get_match_history(puuid2, count=50)
        
        # Prepare player data
        player1_data = {
            "name": summoner_name,
            "puuid": puuid1,
            "matches": [riot_client.get_match_details(mid) for mid in matches1[:20]]
        }
        player2_data = {
            "name": friend_name,
            "puuid": puuid2,
            "matches": [riot_client.get_match_details(mid) for mid in matches2[:20]]
        }
        
        # Use multi-agent system for comparison
        result = orchestrator.get_comparison_workflow(player1_data, player2_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("details", "Agent workflow failed"))
        
        comparison_data = result.get("comparison", {})
        
        return {
            "player1": comparison_data.get("player1", {}),
            "player2": comparison_data.get("player2", {}),
            "comparison": comparison_data.get("comparison_text", ""),
            "shareable_content": comparison_data.get("shareable_content", "")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/player/{summoner_name}/social-content")
async def get_social_content(
    summoner_name: str,
    content_type: str = Query(default="year-end", description="Type of content: year-end, insights, achievements"),
    region: str = Query(default="na1", description="League region")
):
    """Get shareable social media content."""
    try:
        summoner = riot_client.get_summoner_by_name(summoner_name, region)
        puuid = summoner.get("puuid")
        
        if content_type == "year-end":
            matches = riot_client.get_full_year_matches(puuid, 2024)
            result = orchestrator.get_year_summary_workflow(matches, puuid, 2024)
            if "error" in result:
                raise HTTPException(status_code=500, detail=result.get("details", "Agent workflow failed"))
            return result.get("social_content", {})
        
        elif content_type == "insights":
            match_ids = riot_client.get_match_history(puuid, count=50)
            matches = [riot_client.get_match_details(mid) for mid in match_ids[:50]]
            
            player_matches = []
            for match in matches:
                player_data = riot_client.get_player_match_data(match, puuid)
                if player_data:
                    player_matches.append(player_data)
            
            result = orchestrator.get_player_insights_workflow(matches, puuid, player_matches[:20])
            if "error" in result:
                raise HTTPException(status_code=500, detail=result.get("details", "Agent workflow failed"))
            
            # Generate social content from insights
            insights = result.get("insights", {})
            social_response = orchestrator.delegate(
                "social_content",
                "generate_content",
                {"content_type": "insights"},
                context_keys=["insights"],
                output_keys=["social_content"]
            )
            
            if social_response.success:
                return social_response.result.get("content", {})
            else:
                return social_generator.generate_insight_card(insights)
        
        else:
            raise HTTPException(status_code=400, detail="Invalid content type")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: ChatRequest):
    """Chat with the AI agent using Amazon Bedrock."""
    try:
        # Convert conversation history to the format expected by BedrockService
        conversation_history = None
        if chat_request.conversation_history:
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.conversation_history
            ]
        
        # Get response from Bedrock
        response = bedrock_service.chat(
            user_message=chat_request.message,
            context=chat_request.context,
            conversation_history=conversation_history
        )
        
        return ChatResponse(
            response=response,
            message_id=None
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get response from agent: {str(e)}")


# Serve Angular app static files and handle routing (must be last, after all API routes)
# This allows Angular routing to work on the client side
if os.path.exists(angular_dir):
    index_path = os.path.join(angular_dir, "index.html")
    logger.info(f"Angular index.html exists: {os.path.exists(index_path)}")
    logger.info(f"Angular index.html path: {index_path}")
    if os.path.exists(index_path):
        logger.info("Serving Angular app")
    else:
        logger.warning("Angular directory exists but index.html not found")
    
    # Root endpoint - serve Angular app
    @app.get("/")
    async def root():
        """Root endpoint - serve Angular app."""
        index_path = os.path.join(angular_dir, "index.html")
        logger.info(f"Root endpoint called - checking index.html at: {index_path}")
        logger.info(f"Index.html exists: {os.path.exists(index_path)}")
        if os.path.exists(index_path):
            logger.info("Serving Angular index.html")
            return FileResponse(index_path)
        logger.warning("Angular index.html not found, returning error message")
        return {"message": "Angular app not found. Run 'npm run build' in the frontend directory."}
    
    # Serve Angular static files (JS, CSS, etc.) from root path
    # Since base-href is "/", we mount at root with html=True for SPA routing
    # IMPORTANT: This must be AFTER all API routes are defined
    app.mount("/", StaticFiles(directory=angular_dir, html=True), name="angular_static")
else:
    logger.info("Angular directory not found, using legacy static files")
    # Fallback to legacy static files
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    async def root():
        """Root endpoint - serve legacy UI."""
        ui_path = os.path.join(static_dir, "index.html")
        logger.info(f"Root endpoint called - serving legacy UI from: {ui_path}")
        logger.info(f"Legacy index.html exists: {os.path.exists(ui_path)}")
        if os.path.exists(ui_path):
            logger.info("Serving legacy index.html")
            return FileResponse(ui_path)
        logger.warning("Legacy index.html not found")
        return {
            "message": "Rift Rewind API",
            "version": "1.0.0",
            "status": "operational",
            "ui": "Build Angular app with 'npm run build' or use legacy UI at /static/index.html"
        }


if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=settings.app_debug
    )

