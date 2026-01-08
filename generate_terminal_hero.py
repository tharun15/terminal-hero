#!/usr/bin/env python3
"""
Terminal Hero - Quick Test Version (Single File)
A simplified version to test the concept immediately

Usage:
1. pip install openai rich python-dotenv
2. export OPENAI_API_KEY=your_key_here  (or create .env file)
3. python terminal_hero_quick_test.py
"""

import os
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich import box
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

console = Console()

class QuickTerminalHero:
    """Simplified Terminal Hero for quick testing"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[red]❌ Error: OPENAI_API_KEY not found[/red]")
            console.print("Set it with: export OPENAI_API_KEY=your_key_here")
            console.print("Or create a .env file with: OPENAI_API_KEY=your_key_here")
            exit(1)
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
    
    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║         🤖  TERMINAL HERO - QUICK TEST  🤖                   ║
║         AI-Powered Terminal Troubleshooting                  ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
    
    def analyze_error(self, error_text: str) -> dict:
        """Analyze error using GPT-4"""
        console.print("\n[yellow]🔍 Analyzing error...[/yellow]")
        
        system_prompt = """You are an expert system diagnostician. Analyze terminal errors and provide:
1. Error type and category
2. Root cause
3. Causality chain (how one issue led to another)
4. Severity level

Respond in JSON format with these keys:
{
  "error_type": "string",
  "error_category": "permission|not_found|dependency|config|network|unknown",
  "severity": "low|medium|high|critical",
  "root_cause": "string",
  "causality_chain": ["step1", "step2", "step3"],
  "confidence": 0.95
}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this error:\n{error_text}"}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            
            # Extract JSON
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            return json.loads(result)
            
        except Exception as e:
            console.print(f"[red]Error in analysis: {e}[/red]")
            return None
    
    def generate_solutions(self, error_analysis: dict) -> list:
        """Generate solution strategies"""
        console.print("[yellow]💡 Generating solution strategies...[/yellow]")
        
        system_prompt = """You are a senior DevOps engineer. Generate 3 solution strategies:
1. Quick Fix
2. Proper Solution
3. Alternative Approach

For each strategy provide:
- name: Short name
- description: What it does
- commands: List of exact shell commands
- risk_level: low/medium/high
- estimated_time: e.g., "2 minutes"

Respond ONLY in JSON format as an array of strategy objects."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate solutions for:\n{json.dumps(error_analysis, indent=2)}"}
                ],
                temperature=0.7
            )
            
            result = response.choices[0].message.content
            
            # Extract JSON
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            return json.loads(result)
            
        except Exception as e:
            console.print(f"[red]Error generating solutions: {e}[/red]")
            return []
    
    def display_causality_graph(self, analysis: dict):
        """Display causality chain"""
        console.print(Panel.fit("🔍 Error Chain Analysis", style="bold yellow"))
        
        tree = Tree("🎯 Root Cause Analysis", guide_style="bold bright_blue")
        
        current = tree
        for i, step in enumerate(analysis.get("causality_chain", [])):
            if i == len(analysis["causality_chain"]) - 1:
                current = current.add(f"[red]⚠️  {step}[/red]")
            else:
                current = current.add(f"[yellow]↓ {step}[/yellow]")
        
        console.print(tree)
        console.print()
        
        # Info table
        info_table = Table(box=box.SIMPLE, show_header=False)
        info_table.add_column("Key", style="cyan bold")
        info_table.add_column("Value")
        
        info_table.add_row("Error Type", analysis.get("error_type", "Unknown"))
        info_table.add_row("Category", analysis.get("error_category", "unknown").upper())
        info_table.add_row("Severity", f"[yellow]{analysis.get('severity', 'unknown').upper()}[/]")
        info_table.add_row("Confidence", f"{analysis.get('confidence', 0):.0%}")
        
        console.print(info_table)
        console.print()
    
    def display_solutions(self, solutions: list):
        """Display solution strategies"""
        console.print(Panel.fit("💡 Solution Strategies", style="bold green"))
        
        risk_colors = {"low": "green", "medium": "yellow", "high": "red"}
        
        for i, strategy in enumerate(solutions, 1):
            risk_color = risk_colors.get(strategy.get("risk_level", "medium"), "white")
            
            content = f"""[bold]{strategy.get('name', 'Solution')}[/bold]
{strategy.get('description', '')}

[cyan]Commands:[/cyan]
"""
            for cmd in strategy.get("commands", []):
                content += f"  $ {cmd}\n"
            
            content += f"""
[cyan]Details:[/cyan]
  • Risk Level: [{risk_color}]{strategy.get('risk_level', 'unknown').upper()}[/{risk_color}]
  • Estimated Time: {strategy.get('estimated_time', 'N/A')}
"""
            
            panel = Panel(content, title=f"Strategy {i}", border_style=risk_color, box=box.ROUNDED)
            console.print(panel)
            console.print()
    
    def run(self, error_text: str):
        """Run the complete workflow"""
        self.print_banner()
        
        console.print(f"\n[bold]Error to analyze:[/bold] {error_text}\n")
        
        # Step 1: Analyze error
        analysis = self.analyze_error(error_text)
        if not analysis:
            console.print("[red]❌ Analysis failed[/red]")
            return
        
        console.print("[green]✓ Analysis complete[/green]\n")
        
        # Display causality graph
        self.display_causality_graph(analysis)
        
        # Step 2: Generate solutions
        solutions = self.generate_solutions(analysis)
        if not solutions:
            console.print("[red]❌ Solution generation failed[/red]")
            return
        
        console.print("[green]✓ Solutions generated[/green]\n")
        
        # Display solutions
        self.display_solutions(solutions)
        
        # Summary
        console.print(Panel.fit(
            "✅ Analysis Complete! In the full version, you can select and execute these solutions.",
            style="bold green"
        ))

def main():
    """Main entry point"""
    hero = QuickTerminalHero()
    
    # Demo errors
    demo_errors = [
        "bash: python: command not found",
        "npm ERR! code EACCES permission denied, access '/usr/local/lib/node_modules'",
        "ModuleNotFoundError: No module named 'requests'",
        "Error: listen EADDRINUSE: address already in use :::3000",
    ]
    
    console.print("\n[bold cyan]Select a demo error or enter your own:[/bold cyan]")
    for i, error in enumerate(demo_errors, 1):
        console.print(f"  {i}. {error}")
    console.print("  5. Enter custom error")
    console.print()
    
    choice = console.input("[bold]Your choice (1-5): [/bold]")
    
    if choice in ['1', '2', '3', '4']:
        error_text = demo_errors[int(choice) - 1]
    else:
        error_text = console.input("[bold]Enter your error: [/bold]")
    
    if error_text.strip():
        hero.run(error_text)
    else:
        console.print("[red]No error provided[/red]")

if __name__ == "__main__":
    main()