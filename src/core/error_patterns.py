# ============================================================================
# FILE: src/core/error_patterns.py
# Error pattern matching library
# ============================================================================

import re
from typing import Optional, Tuple

class ErrorPatterns:
    """Library of common error patterns and their categorization"""
    
    PATTERNS = {
        "command_not_found": {
            "regex": r"(command not found|not recognized as an internal or external command)",
            "category": "not_found",
            "severity": "medium"
        },
        "permission_denied": {
            "regex": r"(permission denied|access denied|EACCES)",
            "category": "permission",
            "severity": "medium"
        },
        "module_not_found": {
            "regex": r"(ModuleNotFoundError|ImportError|cannot find module)",
            "category": "dependency",
            "severity": "high"
        },
        "package_not_found": {
            "regex": r"(package not found|E: Unable to locate package|No matching distribution)",
            "category": "dependency",
            "severity": "high"
        },
        "port_in_use": {
            "regex": r"(address already in use|port.*already in use|EADDRINUSE)",
            "category": "config",
            "severity": "medium"
        },
        "network_error": {
            "regex": r"(network.*error|connection.*refused|timeout|unable to connect)",
            "category": "network",
            "severity": "medium"
        },
        "syntax_error": {
            "regex": r"(SyntaxError|syntax error)",
            "category": "config",
            "severity": "low"
        },
        "missing_dependency": {
            "regex": r"(missing.*dependency|required.*not found|needs.*to be installed)",
            "category": "dependency",
            "severity": "high"
        },
        "version_conflict": {
            "regex": r"(version.*conflict|incompatible.*version|version.*mismatch)",
            "category": "dependency",
            "severity": "high"
        },
        "disk_space": {
            "regex": r"(no space left|disk.*full|out of disk space)",
            "category": "config",
            "severity": "critical"
        }
    }
    
    @classmethod
    def match_error(cls, error_text: str) -> Optional[Tuple[str, dict]]:
        """Match error text against known patterns"""
        error_lower = error_text.lower()
        
        for pattern_name, pattern_info in cls.PATTERNS.items():
            if re.search(pattern_info["regex"], error_lower, re.IGNORECASE):
                return pattern_name, pattern_info
        
        return None