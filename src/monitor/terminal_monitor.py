# ============================================================================
# FILE: src/monitor/terminal_monitor.py
# Real-time terminal command monitoring and autonomous intervention
# ============================================================================

import os
import sys
import json
import time
import threading
from datetime import datetime
from typing import Optional, Callable, Dict, Any, List
from pathlib import Path
from dataclasses import dataclass, asdict
import tempfile
import subprocess

from ..graph.state import AgentState
from ..graph.workflow import TerminalHeroWorkflow
from ..storage.history import CommandHistory
from ..storage.memory import MemorySystem
from .autonomous_resolver import AutonomousResolver, InterventionLevel


@dataclass
class CommandEvent:
    """Represents a terminal command execution event"""
    timestamp: str
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    success: bool
    
    def to_dict(self):
        return asdict(self)


class TerminalMonitor:
    """
    Monitors terminal commands in real-time and autonomously intervenes on errors.
    Works by injecting a shell function that captures command output and status.
    """
    
    def __init__(self, workflow: Optional[TerminalHeroWorkflow] = None):
        self.workflow = workflow or TerminalHeroWorkflow()
        self.history = CommandHistory()
        self.memory = MemorySystem()
        self.resolver = AutonomousResolver()
        self.is_monitoring = False
        self.event_handlers: List[Callable[[CommandEvent], None]] = []
        self.auto_fix_enabled = True
        self.monitor_thread: Optional[threading.Thread] = None
        
        # Temp directory for command monitoring
        self.monitor_dir = Path(tempfile.gettempdir()) / "terminal_hero"
        self.monitor_dir.mkdir(exist_ok=True)
        self.command_log = self.monitor_dir / "commands.log"
        self.status_file = self.monitor_dir / "monitor_status.json"
        
        # Load previous status
        self._load_status()
        
    def register_event_handler(self, handler: Callable[[CommandEvent], None]):
        """Register a callback for command events"""
        self.event_handlers.append(handler)
    
    def emit_event(self, event: CommandEvent):
        """Emit a command event to all registered handlers"""
        for handler in self.event_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}", file=sys.stderr)
    
    def _process_command_event(self, event: CommandEvent):
        """Process a command event and determine if autonomous intervention is needed"""
        if event.success:
            self.history.add_command(event.command, event.exit_code, event.stdout, event.stderr)
            return
        
        # Error detected - get resolver's decision
        error_text = event.stderr or event.stdout
        decision = self.resolver.analyze_error(error_text, event.command)
        
        if not decision.should_intervene:
            self.history.add_command(event.command, event.exit_code, event.stdout, event.stderr)
            return
        
        print(f"\n[Terminal Hero] 🔍 {decision.reason}", file=sys.stderr)
        
        # Try to autonomously fix based on decision
        if self.auto_fix_enabled and decision.intervention_level != InterventionLevel.SILENT:
            try:
                self._autonomous_fix(event, decision)
            except Exception as e:
                print(f"[Terminal Hero] Error during autonomous fix: {e}", file=sys.stderr)
        else:
            # Just suggest
            for action in decision.suggested_actions:
                print(f"[Terminal Hero] 💡 {action}", file=sys.stderr)
        
        self.history.add_command(event.command, event.exit_code, event.stdout, event.stderr)
    
    def _autonomous_fix(self, event: CommandEvent, decision):
        """Autonomously analyze and attempt to fix the error"""
        error_context = f"""
Command: {event.command}
Exit Code: {event.exit_code}
Output: {event.stderr or event.stdout}
Intervention Level: {decision.intervention_level.name}
Confidence: {decision.confidence:.0%}
"""
        
        print(f"[Terminal Hero] 🤖 Autonomously analyzing...", file=sys.stderr)
        
        try:
            result = self.workflow.run(
                user_input=event.command,
                raw_error=error_context
            )
            
            if result.get("error_analysis"):
                analysis = result["error_analysis"]
                print(f"[Terminal Hero] Root cause: {analysis.get('root_cause', 'Unknown')}", file=sys.stderr)
            
            if result.get("solution_strategies"):
                strategies = result["solution_strategies"]
                if strategies:
                    best_strategy = strategies[0]
                    print(f"[Terminal Hero] 💡 Solution: {best_strategy.get('name', 'Unknown')}", file=sys.stderr)
                    print(f"[Terminal Hero] Description: {best_strategy.get('description', '')}", file=sys.stderr)
                    
                    # Check if we should auto-execute
                    should_auto_exec = self.resolver.should_auto_execute(
                        decision,
                        best_strategy.get("risk_level", "medium")
                    )
                    
                    if should_auto_exec:
                        print(f"[Terminal Hero] ✓ Auto-executing low-risk fix...", file=sys.stderr)
                        # Could auto-execute fixes here
                    else:
                        # Suggest to user
                        print(f"[Terminal Hero] Suggested fix: {', '.join(best_strategy.get('commands', []))}", file=sys.stderr)
                        print(f"[Terminal Hero] Run with: terminal-hero diagnose '{event.command}'", file=sys.stderr)
                    
                    # Record the outcome for learning
                    self.resolver.record_outcome(
                        decision.reason,
                        True,  # Assume success for now
                        best_strategy
                    )
        except Exception as e:
            print(f"[Terminal Hero] Analysis error: {e}", file=sys.stderr)
    
    def get_shell_integration_code(self) -> str:
        """
        Get the shell function code to inject into .bashrc or .zshrc
        This captures command execution and communicates with the monitor
        """
        monitor_script = self.monitor_dir / "command_monitor.sh"
        
        shell_code = f"""
# Terminal Hero Autonomous Monitor
export TERMINAL_HERO_ENABLED=1
export TERMINAL_HERO_LOG="{self.command_log}"
export TERMINAL_HERO_DIR="{self.monitor_dir}"

# Simple command logging function
terminal_hero_log_command() {{
    local EXIT_CODE=$?
    local TIMESTAMP=$(date -Iseconds)
    local CMD="$1"
    
    # Only log if command failed
    if [ $EXIT_CODE -ne 0 ]; then
        local EVENT_JSON="{{\\"timestamp\\": \\"$TIMESTAMP\\", \\"command\\": \\"$CMD\\", \\"exit_code\\": $EXIT_CODE, \\"stdout\\": \\"\\", \\"stderr\\": \\"Command failed\\", \\"duration\\": 0, \\"success\\": false}}"
        echo "$EVENT_JSON" >> "$TERMINAL_HERO_LOG"
    fi
}}

# Override common commands to add logging
git() {{
    command git "$@"
    terminal_hero_log_command "git $@"
}}

npm() {{
    command npm "$@"
    terminal_hero_log_command "npm $@"
}}

pip() {{
    command pip "$@"
    terminal_hero_log_command "pip $@"
}}

python() {{
    command python "$@"
    terminal_hero_log_command "python $@"
}}

python3() {{
    command python3 "$@"
    terminal_hero_log_command "python3 $@"
}}

# Catch-all for other commands using PROMPT_COMMAND
__terminal_hero_prompt() {{
    local EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ] && [ -n "$__TERMINAL_HERO_LAST_CMD" ]; then
        local TIMESTAMP=$(date -Iseconds)
        local EVENT_JSON="{{\\"timestamp\\": \\"$TIMESTAMP\\", \\"command\\": \\"$__TERMINAL_HERO_LAST_CMD\\", \\"exit_code\\": $EXIT_CODE, \\"stdout\\": \\"\\", \\"stderr\\": \\"Command failed\\", \\"duration\\": 0, \\"success\\": false}}"
        echo "$EVENT_JSON" >> "$TERMINAL_HERO_LOG"
    fi
    __TERMINAL_HERO_LAST_CMD=""
}}

__terminal_hero_preexec() {{
    __TERMINAL_HERO_LAST_CMD="$@"
}}

# For bash
if [ -n "$BASH_VERSION" ]; then
    trap '__terminal_hero_preexec "$BASH_COMMAND"' DEBUG
    PROMPT_COMMAND="${{PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}}__terminal_hero_prompt"
fi

# For zsh  
if [ -n "$ZSH_VERSION" ]; then
    preexec_functions+=( __terminal_hero_preexec )
    precmd_functions+=( __terminal_hero_prompt )
fi
"""
        return shell_code
    
    def install_shell_integration(self, shell_type: str = "bash") -> bool:
        """
        Install the monitor into the user's shell configuration
        Supports bash and zsh
        """
        shell_config_file = None
        home = Path.home()
        
        if shell_type == "bash":
            shell_config_file = home / ".bashrc"
        elif shell_type == "zsh":
            shell_config_file = home / ".zshrc"
        else:
            print(f"Unsupported shell: {shell_type}")
            return False
        
        if not shell_config_file.exists():
            print(f"Shell config not found: {shell_config_file}")
            return False
        
        integration_code = self.get_shell_integration_code()
        marker = "# TERMINAL_HERO_START"
        marker_end = "# TERMINAL_HERO_END"
        
        # Read existing config
        config_content = shell_config_file.read_text()
        
        # Check if already installed
        if marker in config_content:
            print(f"Terminal Hero monitor already installed in {shell_config_file}")
            return True
        
        # Append integration code
        with open(shell_config_file, "a") as f:
            f.write(f"\n{marker}\n")
            f.write(integration_code)
            f.write(f"\n{marker_end}\n")
        
        print(f"Terminal Hero monitor installed in {shell_config_file}")
        print("Please restart your terminal or run: source ~/.bashrc (or ~/.zshrc)")
        return True
    
    def uninstall_shell_integration(self, shell_type: str = "bash") -> bool:
        """Remove the monitor from shell configuration"""
        shell_config_file = None
        home = Path.home()
        
        if shell_type == "bash":
            shell_config_file = home / ".bashrc"
        elif shell_type == "zsh":
            shell_config_file = home / ".zshrc"
        
        if not shell_config_file.exists():
            return False
        
        config_content = shell_config_file.read_text()
        marker = "# TERMINAL_HERO_START"
        marker_end = "# TERMINAL_HERO_END"
        
        if marker not in config_content:
            return False
        
        # Remove terminal hero section
        start_idx = config_content.find(marker)
        end_idx = config_content.find(marker_end) + len(marker_end)
        
        new_content = config_content[:start_idx] + config_content[end_idx:]
        shell_config_file.write_text(new_content)
        
        print(f"Terminal Hero monitor removed from {shell_config_file}")
        return True
    
    def start_daemon(self):
        """Start monitoring in background"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self._save_status()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("[Terminal Hero] Monitor started")
    
    def stop_daemon(self):
        """Stop the monitoring daemon"""
        self.is_monitoring = False
        self._save_status()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("[Terminal Hero] Monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        last_pos = 0
        
        while self.is_monitoring:
            try:
                if self.command_log.exists():
                    with open(self.command_log, "r") as f:
                        f.seek(last_pos)
                        lines = f.readlines()
                        last_pos = f.tell()
                        
                        for line in lines:
                            try:
                                event_data = json.loads(line.strip())
                                event = CommandEvent(**event_data)
                                self.emit_event(event)
                                self._process_command_event(event)
                            except json.JSONDecodeError:
                                pass
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Monitor error: {e}", file=sys.stderr)
                time.sleep(1)
    
    def _save_status(self):
        """Save monitor status to file"""
        status = {
            "is_monitoring": self.is_monitoring,
            "auto_fix_enabled": self.auto_fix_enabled,
            "timestamp": datetime.now().isoformat()
        }
        try:
            with open(self.status_file, "w") as f:
                json.dump(status, f)
        except Exception:
            pass  # Ignore errors saving status
    
    def _load_status(self):
        """Load monitor status from file"""
        try:
            if self.status_file.exists():
                with open(self.status_file, "r") as f:
                    status = json.load(f)
                    self.is_monitoring = status.get("is_monitoring", False)
                    self.auto_fix_enabled = status.get("auto_fix_enabled", True)
        except Exception:
            pass  # Ignore errors loading status
    
    def get_status(self) -> Dict[str, Any]:
        """Get monitor status"""
        # Reload status from file in case it changed
        self._load_status()
        return {
            "is_monitoring": self.is_monitoring,
            "auto_fix_enabled": self.auto_fix_enabled,
            "recent_commands": self.history.get_recent_commands(5) if hasattr(self.history, 'get_recent_commands') else [],
        }
