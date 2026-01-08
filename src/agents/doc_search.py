# ============================================================================
# FILE: src/agents/doc_search.py
# Agent that searches documentation and online resources
# ============================================================================

from .base import BaseAgent
from ..graph.state import AgentState
from ..graph.state import DocumentationResult
from duckduckgo_search import DDGS
from typing import List
import json

class DocumentationSearchAgent(BaseAgent):
    """Searches documentation and Stack Overflow for solutions"""
    
    def __init__(self):
        super().__init__("DocSearch", "Researcher")
        self.ddgs = DDGS()
    
    def process(self, state: AgentState) -> AgentState:
        """Search for relevant documentation and solutions"""
        self.log_activity(state, "active", "Searching documentation...")
        
        try:
            error_analysis = state.get("error_analysis")
            if not error_analysis:
                state["documentation_results"] = []
                return state
            
            # Generate search queries
            queries = self._generate_search_queries(error_analysis, state)
            
            # Search and aggregate results
            all_results = []
            for query in queries[:3]:  # Limit to 3 queries
                results = self._search_web(query)
                all_results.extend(results)
            
            # Rank and filter results
            ranked_results = self._rank_results(all_results, error_analysis)
            state["documentation_results"] = ranked_results[:5]  # Top 5
            
            self.log_activity(
                state,
                "complete",
                f"Found {len(state['documentation_results'])} relevant resources"
            )
            
        except Exception as e:
            self.log_activity(state, "error", f"Search failed: {str(e)}")
            state["documentation_results"] = []
        
        return state
    
    def _generate_search_queries(self, error_analysis, state) -> List[str]:
        """Generate targeted search queries"""
        queries = []
        
        # Base query from error type
        queries.append(f"{error_analysis.error_type} fix")
        
        # Add system-specific query
        system_info = state.get("system_info")
        if system_info:
            queries.append(f"{error_analysis.error_type} {system_info.os_type}")
        
        # Add Stack Overflow query
        queries.append(f"site:stackoverflow.com {error_analysis.error_type}")
        
        # Project-specific query
        project_context = state.get("project_context", {})
        if project_context.get("project_type"):
            queries.append(f"{project_context['project_type']} {error_analysis.error_type}")
        
        return queries
    
    def _search_web(self, query: str) -> List[DocumentationResult]:
        """Perform web search using DuckDuckGo"""
        try:
            results = self.ddgs.text(query, max_results=3)
            
            return [
                DocumentationResult(
                    source="web",
                    url=r["href"],
                    title=r["title"],
                    snippet=r["body"],
                    relevance_score=0.8  # Default score
                )
                for r in results
            ]
        except Exception as e:
            return []
    
    def _rank_results(self, results: List[DocumentationResult], error_analysis) -> List[DocumentationResult]:
        """Rank results by relevance using LLM"""
        if not results:
            return []
        
        # For now, simple ranking by source priority
        priority = {
            "stackoverflow.com": 1.0,
            "github.com": 0.9,
            "docs.python.org": 1.0,
            "docs.npmjs.com": 1.0,
            "doc.rust-lang.org": 1.0
        }
        
        for result in results:
            base_score = 0.5
            for domain, score in priority.items():
                if domain in result.url:
                    base_score = score
                    break
            result.relevance_score = base_score
        
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
