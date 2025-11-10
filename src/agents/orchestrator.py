"""
Orchestrator Agent - Central coordinator that manages workflow and delegates tasks.
"""
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.agents.context_manager import ContextManager
from src.agents.registry import AgentRegistry
from src.agents.messages import AgentRequest, AgentResponse, create_request
from src.agents.events import EventBus, EventType, AgentEvent


class Orchestrator:
    """Orchestrator for managing multi-agent workflows."""
    
    def __init__(self, context_manager: ContextManager, agent_registry: AgentRegistry, event_bus: Optional[EventBus] = None):
        self.context_manager = context_manager
        self.agent_registry = agent_registry
        self.event_bus = event_bus or EventBus()
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    def delegate(self, agent_name: str, task: str, input_data: Dict[str, Any],
                 context_keys: Optional[List[str]] = None,
                 output_keys: Optional[List[str]] = None) -> AgentResponse:
        """Delegate a task to a specific agent."""
        agent = self.agent_registry.get(agent_name)
        if not agent:
            return AgentResponse(
                request_id="",
                agent_name=agent_name,
                task=task,
                success=False,
                error=f"Agent '{agent_name}' not found in registry"
            )
        
        # Create request
        request = create_request(agent_name, task, input_data, context_keys, output_keys)
        
        # Publish delegation event
        event = AgentEvent(EventType.TASK_DELEGATED, "orchestrator", {
            "agent": agent_name,
            "task": task
        })
        self.event_bus.publish(event)
        
        # Execute agent
        response = agent.handle_request(request)
        
        return response
    
    def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a workflow of agent tasks."""
        results = {}
        
        for step in workflow:
            agent_name = step.get("agent")
            task = step.get("task")
            input_data = step.get("input_data", {})
            context_keys = step.get("context_keys")
            output_keys = step.get("output_keys")
            parallel = step.get("parallel", False)
            
            if parallel:
                # Execute in parallel with other parallel steps
                continue
            
            response = self.delegate(agent_name, task, input_data, context_keys, output_keys)
            results[f"{agent_name}_{task}"] = response
        
        return results
    
    def execute_parallel(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple agent tasks in parallel."""
        futures = {}
        results = {}
        
        for task_config in tasks:
            agent_name = task_config.get("agent")
            task = task_config.get("task")
            input_data = task_config.get("input_data", {})
            context_keys = task_config.get("context_keys")
            output_keys = task_config.get("output_keys")
            
            # Submit task to executor
            future = self.executor.submit(
                self.delegate,
                agent_name,
                task,
                input_data,
                context_keys,
                output_keys
            )
            futures[future] = f"{agent_name}_{task}"
        
        # Collect results
        for future in as_completed(futures):
            task_key = futures[future]
            try:
                response = future.result()
                results[task_key] = response
            except Exception as e:
                results[task_key] = AgentResponse(
                    request_id="",
                    agent_name="",
                    task="",
                    success=False,
                    error=str(e)
                )
        
        return results
    
    def get_player_insights_workflow(self, matches: List[Dict], puuid: str, player_matches: List[Dict]) -> Dict[str, Any]:
        """Get workflow for player insights generation."""
        # Clear context for new workflow
        self.context_manager.clear()
        
        # Store initial data in context
        self.context_manager.set("matches", matches)
        self.context_manager.set("puuid", puuid)
        self.context_manager.set("player_matches", player_matches)
        
        # Execute sequential workflow
        # Step 1: Match Analysis
        match_analysis_response = self.delegate(
            "match_analysis",
            "analyze_matches",
            {"matches": matches, "puuid": puuid},
            output_keys=["match_analysis", "match_count", "puuid"]
        )
        
        if not match_analysis_response.success:
            return {"error": "Match analysis failed", "details": match_analysis_response.error}
        
        # Step 2: Insights Generation (depends on match analysis)
        insights_response = self.delegate(
            "insights_generation",
            "generate_insights",
            {"player_matches": player_matches},
            context_keys=["match_analysis"],
            output_keys=["insights", "strengths", "weaknesses", "unexpected_insights", "recommendations"]
        )
        
        # Step 3: Visualization (can run in parallel with insights, but we'll do it sequentially for now)
        viz_response = self.delegate(
            "visualization",
            "generate_visualizations",
            {"matches": matches, "puuid": puuid},
            context_keys=["match_analysis"],
            output_keys=["visualizations"]
        )
        
        # Aggregate results
        match_analysis = self.context_manager.get("match_analysis", {})
        insights = self.context_manager.get("insights", {})
        visualizations = self.context_manager.get("visualizations", {})
        
        return {
            "success": True,
            "match_analysis": match_analysis,
            "insights": insights,
            "visualizations": visualizations,
            "key_metrics": match_analysis.get("key_metrics", {})
        }
    
    def get_year_summary_workflow(self, matches: List[Dict], puuid: str, year: int) -> Dict[str, Any]:
        """Get workflow for year-end summary generation."""
        # Clear context for new workflow
        self.context_manager.clear()
        
        # Store initial data
        self.context_manager.set("matches", matches)
        self.context_manager.set("puuid", puuid)
        self.context_manager.set("year", year)
        
        # Execute year summary agent
        response = self.delegate(
            "year_summary",
            "generate_year_summary",
            {"matches": matches, "puuid": puuid, "year": year},
            output_keys=["year_summary", "year", "ai_summary"]
        )
        
        if not response.success:
            return {"error": "Year summary generation failed", "details": response.error}
        
        # Get social content
        social_response = self.delegate(
            "social_content",
            "generate_content",
            {"content_type": "year-end"},
            context_keys=["year_summary"],
            output_keys=["social_content", "content_type"]
        )
        
        # Aggregate results
        year_summary = self.context_manager.get("year_summary", {})
        ai_summary = self.context_manager.get("ai_summary", "")
        social_content = self.context_manager.get("social_content", {})
        
        return {
            "success": True,
            "year_summary": year_summary,
            "ai_summary": ai_summary,
            "social_content": social_content
        }
    
    def get_comparison_workflow(self, player1_data: Dict, player2_data: Dict) -> Dict[str, Any]:
        """Get workflow for player comparison."""
        # Clear context for new workflow
        self.context_manager.clear()
        
        response = self.delegate(
            "player_comparison",
            "compare_players",
            {"player1": player1_data, "player2": player2_data},
            output_keys=["comparison"]
        )
        
        if not response.success:
            return {"error": "Player comparison failed", "details": response.error}
        
        comparison = self.context_manager.get("comparison", {})
        
        return {
            "success": True,
            "comparison": comparison
        }
    
    def shutdown(self) -> None:
        """Shutdown the orchestrator."""
        self.executor.shutdown(wait=True)

