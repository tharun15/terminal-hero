# ============================================================================
# FILE: src/agents/solution_architect.py
# Agent that generates multiple solution strategies
# ============================================================================

from .base import BaseAgent
from ..graph.state import AgentState
from ..graph.state import SolutionStrategy
import json
from typing import List

class SolutionArchitectAgent(BaseAgent):
    """Generates multiple solution strategies with risk assessment"""
    
    def __init__(self):
        super().__init__("SolutionArchitect", "Solution Designer")
    
    def process(self, state: AgentState) -> AgentState:
        """Generate solution strategies"""
        self.log_activity(state, "active", "Designing solution strategies...")
        
        try:
            error_analysis = state.get("error_analysis")
            system_info = state.get("system_info")
            docs = state.get("documentation_results", [])
            
            if not error_analysis:
                state["solution_strategies"] = []
                return state
            
            # Generate multiple strategies
            strategies = self._generate_strategies(error_analysis, system_info, docs)
            state["solution_strategies"] = strategies
            
            self.log_activity(
                state,
                "complete",
                f"Generated {len(strategies)} solution strategies"
            )
            
        except Exception as e:
            self.log_activity(state, "error", f"Strategy generation failed: {str(e)}")
            state["solution_strategies"] = []
        
        return state
    
    def _generate_strategies(self, error_analysis, system_info, docs) -> List[SolutionStrategy]:
        """Generate multiple solution approaches using LLM"""
        
        system_prompt = """You are a senior DevOps engineer. Given an error analysis, generate 3 different solution strategies:
1. Quick Fix - Fast but may have limitations
2. Proper Solution - Best practice approach
3. Alternative - Different method entirely

For each strategy provide:
- name: Short name
- description: What it does
- commands: List of exact shell commands
- risk_level: low/medium/high
- estimated_time: e.g., "2 minutes"
- confidence: 0.0 to 1.0
- prerequisites: What's needed first
- side_effects: Potential issues
- rollback_commands: How to undo

Respond ONLY in JSON format as an array of strategy objects."""

        # Build context
        doc_context = ""
        if docs:
            doc_context = "\n\nRelevant Documentation:\n"
            for doc in docs[:3]:
                doc_context += f"- {doc.title}: {doc.snippet[:200]}\n"
        
        system_context = ""
        if system_info:
            system_context = f"""
System Info:
- OS: {system_info.os_type} {system_info.os_version}
- Shell: {system_info.shell}
- Package Managers: {', '.join(system_info.package_managers)}
"""
        
        user_prompt = f"""Error Analysis:
- Type: {error_analysis.error_type}
- Category: {error_analysis.error_category}
- Root Cause: {error_analysis.root_cause}
- Severity: {error_analysis.severity}
{system_context}
{doc_context}

Generate 3 solution strategies in JSON array format."""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.7)
        
        # Parse strategies
        try:
            # Extract JSON
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            
            data = json.loads(json_str)
            strategies = [SolutionStrategy(**s) for s in data]
            return strategies
        except Exception as e:
            # Fallback strategy
            return self._generate_fallback_strategy(error_analysis, system_info)
    
    def _generate_fallback_strategy(self, error_analysis, system_info) -> List[SolutionStrategy]:
        """Generate a basic fallback strategy"""
        
        # Simple heuristics based on error category
        if error_analysis.error_category == "not_found":
            if system_info and "apt" in system_info.package_managers:
                commands = ["sudo apt-get update", "sudo apt-get install <package>"]
            elif system_info and "brew" in system_info.package_managers:
                commands = ["brew install <package>"]
            else:
                commands = ["# Install the missing package using your package manager"]
        elif error_analysis.error_category == "permission":
            commands = ["sudo <your-command>"]
        elif error_analysis.error_category == "dependency":
            commands = ["# Install missing dependencies"]
        else:
            commands = ["# Manual investigation required"]
        
        return [
            SolutionStrategy(
                name="Basic Fix",
                description=f"Address the {error_analysis.error_category} issue",
                commands=commands,
                risk_level="medium",
                estimated_time="5 minutes",
                confidence=0.6,
                prerequisites=[],
                side_effects=["May require system-level changes"],
                rollback_commands=[]
            )
        ]