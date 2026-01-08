# ============================================================================
# FILE: src/storage/memory.py
# Memory and learning system
# ============================================================================

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class MemorySystem:
    """Stores error patterns and solutions for learning"""
    
    def __init__(self, db_path: str = "~/.terminal_hero/memory.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                error_category TEXT NOT NULL,
                raw_error TEXT NOT NULL,
                solution_used TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solution_success_rate (
                solution_hash TEXT PRIMARY KEY,
                total_attempts INTEGER DEFAULT 0,
                successful_attempts INTEGER DEFAULT 0,
                last_used DATETIME
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_solution_attempt(
        self,
        error_type: str,
        error_category: str,
        raw_error: str,
        solution: str,
        success: bool
    ):
        """Record a solution attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Record pattern
        cursor.execute("""
            INSERT INTO error_patterns (error_type, error_category, raw_error, solution_used, success)
            VALUES (?, ?, ?, ?, ?)
        """, (error_type, error_category, raw_error[:500], solution, success))
        
        # Update success rate
        solution_hash = str(hash(solution))
        cursor.execute("""
            INSERT INTO solution_success_rate (solution_hash, total_attempts, successful_attempts, last_used)
            VALUES (?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(solution_hash) DO UPDATE SET
                total_attempts = total_attempts + 1,
                successful_attempts = successful_attempts + ?,
                last_used = CURRENT_TIMESTAMP
        """, (solution_hash, 1 if success else 0, 1 if success else 0))
        
        conn.commit()
        conn.close()
    
    def get_similar_cases(self, error_type: str, limit: int = 5) -> List[Dict]:
        """Get similar past cases"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT error_type, solution_used, success, COUNT(*) as occurrences
            FROM error_patterns
            WHERE error_type = ?
            GROUP BY solution_used
            ORDER BY occurrences DESC
            LIMIT ?
        """, (error_type, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "error_type": r[0],
                "solution": r[1],
                "success": bool(r[2]),
                "occurrences": r[3]
            }
            for r in results
        ]
    
    def get_solution_confidence(self, solution: str) -> float:
        """Get confidence score for a solution based on history"""
        solution_hash = str(hash(solution))
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_attempts, successful_attempts
            FROM solution_success_rate
            WHERE solution_hash = ?
        """, (solution_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result or result[0] == 0:
            return 0.5  # Default confidence
        
        total, successful = result
        return successful / total