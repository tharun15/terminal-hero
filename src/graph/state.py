"""
Terminal Hero - AI-Powered Terminal Troubleshooting Agent
A sophisticated multi-agent system for resolving terminal issues
"""

# ============================================================================
# FILE: src/graph/state.py
# Shared state management for all agents
# ============================================================================

from typing import TypedDict, List, Dict, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class SystemInfo(BaseModel):
    """System information collected by Context Collector Agent"""
    os_type: str
    os_version: str
    shell: str
    python_version: Optional[str] = None
    node_version: Optional[str] = None
    package_managers: List[str] = Field(default_factory=list)
    env_vars: Dict[str, str] = Field(default_factory=dict)
    path: List[str] = Field(default_factory=list)

class ErrorAnalysis(BaseModel):
    """Error analysis from Error Analyzer Agent"""
    error_type: str
    error_category: Literal["permission", "not_found", "dependency", "config", "network", "unknown"]
    severity: Literal["low", "medium", "high", "critical"]
    root_cause: str
    affected_components: List[str] = Field(default_factory=list)
    causality_chain: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)

class DocumentationResult(BaseModel):
    """Documentation search results"""
    source: str
    url: str
    title: str
    snippet: str
    relevance_score: float = Field(ge=0.0, le=1.0)

class SolutionStrategy(BaseModel):
    """A solution strategy with metadata"""
    name: str
    description: str
    commands: List[str]
    risk_level: Literal["low", "medium", "high"]
    estimated_time: str
    confidence: float = Field(ge=0.0, le=1.0)
    prerequisites: List[str] = Field(default_factory=list)
    side_effects: List[str] = Field(default_factory=list)
    rollback_commands: List[str] = Field(default_factory=list)

class ExecutionResult(BaseModel):
    """Result of command execution"""
    success: bool
    commands_executed: List[str]
    output: str
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentState(TypedDict):
    """Shared state passed between agents in the workflow"""
    # Input
    user_input: str
    raw_error: str
    
    # Context
    system_info: Optional[SystemInfo]
    project_context: Optional[Dict[str, any]]
    
    # Analysis
    error_analysis: Optional[ErrorAnalysis]
    
    # Research
    documentation_results: List[DocumentationResult]
    
    # Solutions
    solution_strategies: List[SolutionStrategy]
    selected_strategy: Optional[SolutionStrategy]
    
    # Execution
    execution_result: Optional[ExecutionResult]
    
    # Metadata
    agent_activity: List[Dict[str, str]]
    current_step: str
    requires_user_input: bool
    error_occurred: bool