# ============================================================================
# FILE: src/agents/error_analyzer.py
# Agent that analyzes errors and determines root causes
# ============================================================================

from .base import BaseAgent
from ..graph.state import AgentState
from ..graph.state import ErrorAnalysis
from ..core.error_patterns import ErrorPatterns
import json

class ErrorAnalyzerAgent(BaseAgent):
    """Analyzes errors and builds causality chains"""
    
    def __init__(self):
        super().__init__("ErrorAnalyzer", "Diagnostician")
    
    def process(self, state: AgentState) -> AgentState:
        """Analyze error and determine root cause"""
        self.log_activity(state, "active", "Building causality graph...")
        
        try:
            error_text = state["raw_error"]
            system_info = state.get("system_info")
            
            # Quick pattern matching
            pattern_match = ErrorPatterns.match_error(error_text)
            
            # Deep analysis with LLM
            analysis = self._deep_analysis(error_text, system_info, pattern_match)
            
            state["error_analysis"] = analysis
            
            self.log_activity(
                state,
                "complete",
                f"Identified {analysis.error_category} error with {analysis.confidence:.0%} confidence"
            )
            
        except Exception as e:
            self.log_activity(state, "error", f"Analysis failed: {str(e)}")
            state["error_occurred"] = True
        
        return state
    
    def _deep_analysis(self, error_text: str, system_info, pattern_match) -> ErrorAnalysis:
        """Perform deep error analysis using LLM"""
        
        system_prompt = """You are an expert system diagnostician. Analyze terminal errors and provide:
1. Error type and category
2. Root cause (not just symptoms)
3. Causality chain (how one issue led to another)
4. Affected components
5. Severity level

Respond in JSON format with these exact keys:
{
  "error_type": "string",
  "error_category": "permission|not_found|dependency|config|network|unknown",
  "severity": "low|medium|high|critical",
  "root_cause": "string",
  "affected_components": ["list"],
  "causality_chain": ["list of steps from root cause to visible error"],
  "confidence": 0.95
}"""
        
        system_context = ""
        if system_info:
            system_context = f"\n\nSystem Context:\n- OS: {system_info.os_type}\n- Package Managers: {', '.join(system_info.package_managers)}"
        
        pattern_context = ""
        if pattern_match:
            pattern_name, pattern_info = pattern_match
            pattern_context = f"\n\nPattern Match: {pattern_name} ({pattern_info['category']})"
        
        user_prompt = f"""Error to analyze:
{error_text}
{system_context}
{pattern_context}

Provide detailed analysis in JSON format."""
        
        response = self.call_llm(system_prompt, user_prompt, temperature=0.3)
        
        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            
            data = json.loads(json_str)
            return ErrorAnalysis(**data)
        except:
            # Fallback to pattern match or default
            if pattern_match:
                _, info = pattern_match
                return ErrorAnalysis(
                    error_type=pattern_match[0],
                    error_category=info["category"],
                    severity=info["severity"],
                    root_cause="Pattern-based detection",
                    causality_chain=[error_text[:100]],
                    confidence=0.7
                )
            else:
                return ErrorAnalysis(
                    error_type="unknown",
                    error_category="unknown",
                    severity="medium",
                    root_cause="Unable to determine",
                    causality_chain=[error_text[:100]],
                    confidence=0.5
                )