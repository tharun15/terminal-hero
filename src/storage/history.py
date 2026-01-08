# ============================================================================
# FILE: src/storage/history.py
# Command history and undo functionality
# ============================================================================

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

class CommandHistory:
    """Tracks executed commands for undo functionality"""
    
    def __init__(self, history_file: str = "~/.terminal_hero/history.json"):
        self.history_file = Path(history_file).expanduser()
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.history_file.exists():
            self._save_history([])
    
    def _load_history(self) -> List[Dict]:
        """Load command history"""
        try:
            with open(self.history_file) as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save command history"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def add_execution(
        self,
        commands: List[str],
        rollback_commands: List[str],
        description: str
    ):
        """Add an execution to history"""
        history = self._load_history()
        
        entry = {
            "id": len(history) + 1,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "commands": commands,
            "rollback_commands": rollback_commands
        }
        
        history.append(entry)
        self._save_history(history)
    
    def get_last_execution(self) -> Dict:
        """Get the last execution"""
        history = self._load_history()
        return history[-1] if history else None
    
    def get_execution_by_id(self, exec_id: int) -> Dict:
        """Get specific execution by ID"""
        history = self._load_history()
        for entry in history:
            if entry["id"] == exec_id:
                return entry
        return None
    
    def list_recent(self, count: int = 10) -> List[Dict]:
        """List recent executions"""
        history = self._load_history()
        return history[-count:] if history else []