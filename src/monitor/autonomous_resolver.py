# ============================================================================
# FILE: src/monitor/autonomous_resolver.py
# Autonomous problem resolution with decision making
# ============================================================================

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re
from enum import Enum

from ..graph.state import ErrorAnalysis, SolutionStrategy


class InterventionLevel(Enum):
    """Levels of autonomous intervention"""
    SILENT = 0  # Just log, don't suggest
    SUGGEST = 1  # Suggest solutions, ask for confirmation
    AUTO_LOW_RISK = 2  # Auto-execute low-risk fixes
    AUTO_MEDIUM = 3  # Auto-execute medium-risk fixes
    FULL_AUTONOMOUS = 4  # Auto-execute any fix


@dataclass
class InterventionDecision:
    """Decision about how to intervene on an error"""
    should_intervene: bool
    intervention_level: InterventionLevel
    confidence: float
    reason: str
    suggested_actions: List[str]


class AutonomousResolver:
    """
    Makes intelligent decisions about when and how to intervene on errors.
    Learns from successful past interventions.
    """
    
    def __init__(self):
        self.intervention_history: List[Dict] = []
        self.success_patterns: Dict[str, float] = {}  # error_type -> success_rate
        self.learned_solutions: Dict[str, SolutionStrategy] = {}  # error_type -> best_solution
        
        # Common error patterns and auto-fix rules
        self.auto_fixable_errors = {
            "command_not_found": {
                "patterns": [
                    r"command not found",
                    r"No such file or directory",
                    r"not found in",
                ],
                "risk_level": "low",
                "intervention_level": InterventionLevel.AUTO_LOW_RISK,
            },
            "permission_denied": {
                "patterns": [
                    r"Permission denied",
                    r"permission denied",
                    r"Operation not permitted",
                ],
                "risk_level": "medium",
                "intervention_level": InterventionLevel.SUGGEST,
            },
            "missing_dependency": {
                "patterns": [
                    r"ModuleNotFoundError",
                    r"No module named",
                    r"cannot find -l",
                    r"pkg-config",
                ],
                "risk_level": "low",
                "intervention_level": InterventionLevel.SUGGEST,
            },
            "port_already_in_use": {
                "patterns": [
                    r"Address already in use",
                    r"port [0-9]+ is already in use",
                    r"EADDRINUSE",
                ],
                "risk_level": "medium",
                "intervention_level": InterventionLevel.SUGGEST,
            },
            "disk_space": {
                "patterns": [
                    r"No space left on device",
                    r"disk full",
                    r"out of space",
                ],
                "risk_level": "high",
                "intervention_level": InterventionLevel.SUGGEST,
            },
            "network_error": {
                "patterns": [
                    r"Connection refused",
                    r"Connection reset",
                    r"Network unreachable",
                    r"Temporary failure in name resolution",
                ],
                "risk_level": "low",
                "intervention_level": InterventionLevel.SUGGEST,
            },
        }
    
    def analyze_error(self, error_text: str, command: str) -> InterventionDecision:
        """
        Analyze an error and decide on intervention strategy.
        Returns a decision about how to handle the error.
        """
        
        # Identify error type
        error_type = self._identify_error_type(error_text)
        
        if error_type not in self.auto_fixable_errors:
            # Unknown error type
            return InterventionDecision(
                should_intervene=True,
                intervention_level=InterventionLevel.SUGGEST,
                confidence=0.5,
                reason=f"Unknown error type: {error_type}",
                suggested_actions=["Run 'terminal-hero diagnose' for analysis"]
            )
        
        error_config = self.auto_fixable_errors[error_type]
        
        # Check success history
        success_rate = self.success_patterns.get(error_type, 0.0)
        
        # Determine intervention level
        if success_rate > 0.9:
            # High confidence from past successes
            intervention_level = InterventionLevel.AUTO_LOW_RISK
            confidence = 0.95
        elif success_rate > 0.7:
            # Medium confidence
            intervention_level = error_config["intervention_level"]
            confidence = 0.80
        else:
            # Low confidence or no history
            config_level = error_config["intervention_level"]
            intervention_level = config_level if config_level.value >= InterventionLevel.SUGGEST.value else InterventionLevel.SUGGEST
            confidence = 0.6
        
        return InterventionDecision(
            should_intervene=True,
            intervention_level=intervention_level,
            confidence=confidence,
            reason=f"Detected {error_type} error (confidence: {confidence:.0%})",
            suggested_actions=self._get_suggested_actions(error_type, command)
        )
    
    def _identify_error_type(self, error_text: str) -> Optional[str]:
        """Identify the type of error from error text"""
        error_text_lower = error_text.lower()
        
        for error_type, config in self.auto_fixable_errors.items():
            for pattern in config["patterns"]:
                if re.search(pattern, error_text_lower, re.IGNORECASE):
                    return error_type
        
        return None
    
    def _get_suggested_actions(self, error_type: str, command: str) -> List[str]:
        """Get suggested actions for an error type"""
        
        suggestions: Dict[str, List[str]] = {
            "command_not_found": [
                "Check spelling of the command",
                "Ensure the program is installed",
                "Verify the program is in your PATH",
                "Try 'which <command>' to locate it",
            ],
            "permission_denied": [
                "Add execute permission: chmod +x <file>",
                "Run with sudo (if appropriate)",
                "Check file ownership",
            ],
            "missing_dependency": [
                "Install the missing dependency",
                "Check package manager (npm, pip, apt, etc.)",
                "Verify installation completed successfully",
            ],
            "port_already_in_use": [
                "Use a different port number",
                "Kill the process using the port",
                "Check for zombie processes",
            ],
            "disk_space": [
                "Clean up temporary files",
                "Check disk usage with 'df -h'",
                "Remove old build artifacts",
            ],
            "network_error": [
                "Check internet connection",
                "Verify the target server is running",
                "Check DNS resolution",
                "Look for proxy/firewall issues",
            ],
        }
        
        return suggestions.get(error_type, ["Run 'terminal-hero diagnose' for detailed analysis"])
    
    def record_outcome(self, error_type: str, success: bool, solution: SolutionStrategy):
        """Record the outcome of an intervention"""
        
        self.intervention_history.append({
            "error_type": error_type,
            "success": success,
            "solution": solution,
        })
        
        # Update success rate
        if error_type not in self.success_patterns:
            self.success_patterns[error_type] = 1.0 if success else 0.0
        else:
            # Moving average with decay
            old_rate = self.success_patterns[error_type]
            new_rate = (old_rate * 0.7) + (1.0 if success else 0.0) * 0.3
            self.success_patterns[error_type] = new_rate
        
        # Remember best solution
        if success:
            self.learned_solutions[error_type] = solution
    
    def should_auto_execute(self, 
                           decision: InterventionDecision,
                           risk_level: str) -> bool:
        """
        Determine if a solution should be auto-executed based on decision and risk.
        """
        
        risk_scores = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        risk_score = risk_scores.get(risk_level, 2)
        
        if decision.intervention_level == InterventionLevel.AUTO_LOW_RISK:
            return risk_score == 0
        elif decision.intervention_level == InterventionLevel.AUTO_MEDIUM:
            return risk_score <= 1
        elif decision.intervention_level == InterventionLevel.FULL_AUTONOMOUS:
            return True
        
        return False
    
    def get_quick_fix(self, error_type: str) -> Optional[str]:
        """Get a quick fix command for common errors"""
        
        quick_fixes: Dict[str, str] = {
            "permission_denied": "chmod +x",
            "port_already_in_use": "lsof -i :<port>",
            "disk_space": "df -h && du -sh *",
        }
        
        return quick_fixes.get(error_type)
    
    def get_learning_status(self) -> Dict:
        """Get the resolver's learning status"""
        return {
            "total_interventions": len(self.intervention_history),
            "error_types_learned": len(self.success_patterns),
            "success_rates": self.success_patterns,
            "learned_solutions": list(self.learned_solutions.keys()),
        }
