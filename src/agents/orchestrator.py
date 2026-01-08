# ============================================================================
# FILE: src/agents/orchestrator.py
# Main orchestrator that coordinates all agents
# ============================================================================

from .base import BaseAgent
from ..graph.state import AgentState
from typing import Dict, Callable

class OrchestratorAgent(BaseAgent):
    """Coordinates the multi-agent workflow"""
    
    def __init__(self):
        super().__init__("Orchestrator", "Workflow Manager")
    
    def process(self, state: AgentState) -> AgentState:
        """Determine next steps in the workflow"""
        self.log_activity(state, "active", "Orchestrating workflow...")
        
        # Determine current stage and next action
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            state["current_step"] = "collect_context"
        elif current_step == "collect_context":
            state["current_step"] = "analyze_error"
        elif current_step == "analyze_error":
            state["current_step"] = "search_docs"
        elif current_step == "search_docs":
            state["current_step"] = "generate_solutions"
        elif current_step == "generate_solutions":
            state["current_step"] = "await_user_selection"
            state["requires_user_input"] = True
        elif current_step == "await_user_selection":
            state["current_step"] = "execute"
        elif current_step == "execute":
            state["current_step"] = "complete"
        
        return state
    
    def should_continue(self, state: AgentState) -> str:
        """Determine if workflow should continue or branch"""
        
        if state.get("error_occurred"):
            return "error"
        
        if state.get("requires_user_input"):
            return "wait_user"
        
        current_step = state.get("current_step", "start")
        
        step_routing = {
            "start": "collect_context",
            "collect_context": "analyze_error",
            "analyze_error": "search_docs",
            "search_docs": "generate_solutions",
            "generate_solutions": "await_user_selection",
            "await_user_selection": "execute",
            "execute": "complete",
            "complete": "end"
        }
        
        return step_routing.get(current_step, "end")