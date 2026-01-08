# ============================================================================
# FILE: src/core/system_detector.py
# System detection utilities
# ============================================================================

import platform
import subprocess
import os
import shutil
from typing import List, Dict, Optional
from ..graph.state import SystemInfo

class SystemDetector:
    """Detects system information for context"""
    
    @staticmethod
    def get_os_info() -> Dict[str, str]:
        """Get operating system information"""
        return {
            "os_type": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "platform": platform.platform()
        }
    
    @staticmethod
    def get_shell() -> str:
        """Detect current shell"""
        shell = os.environ.get("SHELL", "")
        if shell:
            return os.path.basename(shell)
        return "unknown"
    
    @staticmethod
    def get_python_version() -> Optional[str]:
        """Get Python version"""
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except:
            return None
    
    @staticmethod
    def get_node_version() -> Optional[str]:
        """Get Node.js version"""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except:
            return None
    
    @staticmethod
    def detect_package_managers() -> List[str]:
        """Detect available package managers"""
        managers = []
        candidates = ["apt", "yum", "dnf", "pacman", "brew", "pip", "npm", "cargo"]
        
        for manager in candidates:
            if shutil.which(manager):
                managers.append(manager)
        
        return managers
    
    @staticmethod
    def get_path() -> List[str]:
        """Get PATH environment variable as list"""
        path = os.environ.get("PATH", "")
        return path.split(os.pathsep) if path else []
    
    @staticmethod
    def get_relevant_env_vars() -> Dict[str, str]:
        """Get relevant environment variables"""
        relevant_vars = [
            "PATH", "HOME", "USER", "SHELL", 
            "PYTHONPATH", "NODE_PATH", "VIRTUAL_ENV",
            "CONDA_DEFAULT_ENV"
        ]
        
        return {
            var: os.environ.get(var, "")
            for var in relevant_vars
            if os.environ.get(var)
        }
    
    @classmethod
    def collect_all(cls) -> SystemInfo:
        """Collect all system information"""
        os_info = cls.get_os_info()
        
        return SystemInfo(
            os_type=os_info["os_type"],
            os_version=os_info["os_version"],
            shell=cls.get_shell(),
            python_version=cls.get_python_version(),
            node_version=cls.get_node_version(),
            package_managers=cls.detect_package_managers(),
            env_vars=cls.get_relevant_env_vars(),
            path=cls.get_path()
        )