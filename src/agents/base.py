# ============================================================================
# FILE: src/agents/base.py
# Base agent class with common functionality
# ============================================================================

from abc import ABC, abstractmethod
from datetime import datetime
from openai import OpenAI
import os
from typing import Any
from pathlib import Path
from dotenv import load_dotenv
from ..graph.state import AgentState

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"
        
    def log_activity(self, state: AgentState, status: str, message: str):
        """Log agent activity to shared state"""
        if "agent_activity" not in state:
            state["agent_activity"] = []
        
        state["agent_activity"].append({
            "agent": self.name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """Call OpenAI API with error handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    @abstractmethod
    def process(self, state: AgentState) -> AgentState:
        """Process the state and return updated state"""
        pass