# ============================================================================
# FILE: src/graph/workflow.py
# LangGraph workflow definition
# ============================================================================

from langgraph.graph import StateGraph, END
from typing import Dict
from .state import AgentState
from ..agents.orchestrator import OrchestratorAgent
from ..agents.context_collector import ContextCollectorAgent
from ..agents.error_analyzer import ErrorAnalyzerAgent
from ..agents.doc_search import DocumentationSearchAgent
from ..agents.solution_architect import SolutionArchitectAgent
from ..agents.executor import ExecutorAgent

class TerminalHeroWorkflow:
    """Main workflow orchestrating all agents"""
    
    def __init__(self):
        # Initialize agents
        self.orchestrator = OrchestratorAgent()
        self.context_collector = ContextCollectorAgent()
        self.error_analyzer = ErrorAnalyzerAgent()
        self.doc_search = DocumentationSearchAgent()
        self.solution_architect = SolutionArchitectAgent()
        self.executor = ExecutorAgent()
        
        # Build workflow graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("orchestrator", self.orchestrator.process)
        workflow.add_node("collect_context", self.context_collector.process)
        workflow.add_node("analyze_error", self.error_analyzer.process)
        workflow.add_node("search_docs", self.doc_search.process)
        workflow.add_node("generate_solutions", self.solution_architect.process)
        workflow.add_node("prepare_execution", self.executor.process)
        
        # Set entry point
        workflow.set_entry_point("orchestrator")
        
        # Add edges
        workflow.add_edge("orchestrator", "collect_context")
        workflow.add_edge("collect_context", "analyze_error")
        workflow.add_edge("analyze_error", "search_docs")
        workflow.add_edge("search_docs", "generate_solutions")
        workflow.add_edge("generate_solutions", "prepare_execution")
        
        # Conditional edges from orchestrator
        workflow.add_conditional_edges(
            "prepare_execution",
            self._should_end,
            {
                "continue": "orchestrator",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _should_end(self, state: AgentState) -> str:
        """Determine if workflow should end"""
        if state.get("current_step") == "complete":
            return "end"
        if state.get("error_occurred"):
            return "end"
        if state.get("requires_user_input"):
            return "end"
        return "continue"
    
    def run(self, user_input: str, raw_error: str) -> AgentState:
        """Execute the workflow"""
        
        # Initialize state
        initial_state: AgentState = {
            "user_input": user_input,
            "raw_error": raw_error,
            "system_info": None,
            "project_context": None,
            "error_analysis": None,
            "documentation_results": [],
            "solution_strategies": [],
            "selected_strategy": None,
            "execution_result": None,
            "agent_activity": [],
            "current_step": "start",
            "requires_user_input": False,
            "error_occurred": False
        }
        
        # Run workflow
        result = self.graph.invoke(initial_state)
        
        return result
