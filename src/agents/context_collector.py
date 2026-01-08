# ============================================================================
# FILE: src/agents/context_collector.py
# Agent that collects system context
# ============================================================================

import json
import os
from pathlib import Path
from typing import Optional, Dict
from .base import BaseAgent
from ..graph.state import AgentState
from ..core.system_detector import SystemDetector

class ContextCollectorAgent(BaseAgent):
    """Collects comprehensive system and project context"""
    
    def __init__(self):
        super().__init__("ContextCollector", "System Detective")
    
    def process(self, state: AgentState) -> AgentState:
        """Collect system and project context"""
        self.log_activity(state, "active", "Analyzing system state...")
        
        try:
            # Collect system info
            system_info = SystemDetector.collect_all()
            state["system_info"] = system_info
            
            # Detect project context
            project_context = self._detect_project_context()
            state["project_context"] = project_context
            
            self.log_activity(
                state, 
                "complete", 
                f"Detected {system_info.os_type} system with {len(system_info.package_managers)} package managers"
            )
            
        except Exception as e:
            self.log_activity(state, "error", f"Context collection failed: {str(e)}")
            state["error_occurred"] = True
        
        return state
    
    def _detect_project_context(self) -> Dict:
        """Detect project type and relevant files"""
        context = {
            "project_type": None,
            "config_files": [],
            "dependencies": []
        }
        
        cwd = Path.cwd()
        
        # Check for common project files
        project_indicators = {
            "package.json": "node",
            "requirements.txt": "python",
            "Pipfile": "python",
            "pyproject.toml": "python",
            "Cargo.toml": "rust",
            "go.mod": "go",
            "pom.xml": "java",
            "Gemfile": "ruby"
        }
        
        for filename, proj_type in project_indicators.items():
            file_path = cwd / filename
            if file_path.exists():
                context["project_type"] = proj_type
                context["config_files"].append(str(file_path))
                
                # Try to read dependencies
                if filename == "package.json":
                    context["dependencies"] = self._read_package_json(file_path)
                elif filename == "requirements.txt":
                    context["dependencies"] = self._read_requirements_txt(file_path)
        
        return context
    
    def _read_package_json(self, path: Path) -> list:
        """Read dependencies from package.json"""
        try:
            with open(path) as f:
                data = json.load(f)
                deps = []
                if "dependencies" in data:
                    deps.extend(data["dependencies"].keys())
                if "devDependencies" in data:
                    deps.extend(data["devDependencies"].keys())
                return deps
        except:
            return []
    
    def _read_requirements_txt(self, path: Path) -> list:
        """Read dependencies from requirements.txt"""
        try:
            with open(path) as f:
                lines = f.readlines()
                return [line.split("==")[0].strip() for line in lines if line.strip() and not line.startswith("#")]
        except:
            return []