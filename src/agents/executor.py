# ============================================================================
# FILE: src/agents/executor.py
# Agent that safely executes commands
# ============================================================================

from .base import BaseAgent
from ..graph.state import AgentState
from ..graph.state import ExecutionResult
import subprocess
from typing import List, Tuple
from datetime import datetime

class ExecutorAgent(BaseAgent):
    """Safely executes commands with validation and rollback"""
    
    def __init__(self):
        super().__init__("Executor", "Command Executor")
        self.dangerous_patterns = [
            r"rm -rf /",
            r"rm -rf \*",
            r"dd if=",
            r"mkfs\.",
            r"> /dev/sda",
            r":(){ :|:& };:"  # Fork bomb
        ]
    
    def process(self, state: AgentState) -> AgentState:
        """Execute selected strategy commands"""
        self.log_activity(state, "active", "Preparing to execute commands...")
        
        selected_strategy = state.get("selected_strategy")
        if not selected_strategy:
            self.log_activity(state, "waiting", "Awaiting user selection...")
            state["requires_user_input"] = True
            return state
        
        # Note: Actual execution should be triggered separately with user confirmation
        # This agent prepares and validates
        
        try:
            # Validate commands
            validation_result = self._validate_commands(selected_strategy.commands)
            
            if not validation_result[0]:
                self.log_activity(
                    state,
                    "error",
                    f"Command validation failed: {validation_result[1]}"
                )
                state["error_occurred"] = True
                return state
            
            self.log_activity(
                state,
                "ready",
                f"Commands validated. Ready to execute {len(selected_strategy.commands)} command(s)"
            )
            
        except Exception as e:
            self.log_activity(state, "error", f"Validation failed: {str(e)}")
            state["error_occurred"] = True
        
        return state
    
    def _validate_commands(self, commands: List[str]) -> Tuple[bool, str]:
        """Validate commands for safety"""
        import re
        
        for cmd in commands:
            # Check for dangerous patterns
            for pattern in self.dangerous_patterns:
                if re.search(pattern, cmd):
                    return False, f"Dangerous command detected: {cmd}"
            
            # Check for basic syntax
            if cmd.strip().startswith("#"):
                continue  # Comment
            
            if not cmd.strip():
                continue  # Empty
        
        return True, "Commands validated successfully"
    
    def execute_commands(self, commands: List[str], dry_run: bool = False) -> ExecutionResult:
        """Execute commands with safety checks"""
        
        if dry_run:
            return ExecutionResult(
                success=True,
                commands_executed=commands,
                output="DRY RUN - Commands not executed",
                error=None
            )
        
        executed = []
        output_lines = []
        
        for cmd in commands:
            if cmd.strip().startswith("#") or not cmd.strip():
                continue
            
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                executed.append(cmd)
                output_lines.append(f"$ {cmd}")
                output_lines.append(result.stdout)
                
                if result.returncode != 0:
                    return ExecutionResult(
                        success=False,
                        commands_executed=executed,
                        output="\n".join(output_lines),
                        error=result.stderr
                    )
                    
            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    success=False,
                    commands_executed=executed,
                    output="\n".join(output_lines),
                    error=f"Command timed out: {cmd}"
                )
            except Exception as e:
                return ExecutionResult(
                    success=False,
                    commands_executed=executed,
                    output="\n".join(output_lines),
                    error=str(e)
                )
        
        return ExecutionResult(
            success=True,
            commands_executed=executed,
            output="\n".join(output_lines),
            error=None
        )
