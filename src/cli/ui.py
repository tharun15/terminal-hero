# ============================================================================
# FILE: src/cli/ui.py
# Rich UI components for beautiful terminal output
# ============================================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.tree import Tree
from rich.syntax import Syntax
from rich import box
from typing import List, Dict
from ..graph.state import ErrorAnalysis, SolutionStrategy, DocumentationResult

console = Console()

class TerminalHeroUI:
    """Rich UI components for Terminal Hero"""
    
    @staticmethod
    def print_banner():
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🤖  TERMINAL HERO  🤖                                ║
║                                                              ║
║         AI-Powered Terminal Troubleshooting Agent           ║
║         Multi-Agent System for Instant Problem Solving      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
    
    @staticmethod
    def print_agent_dashboard(agent_activity: List[Dict]):
        """Print real-time agent activity dashboard"""
        
        status_symbols = {
            "active": "[yellow]●[/yellow]",
            "complete": "[green]✓[/green]",
            "error": "[red]✗[/red]",
            "waiting": "[blue]○[/blue]",
            "ready": "[green]✓[/green]"
        }
        
        table = Table(
            title="🤖 Agent Activity Dashboard",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Agent", style="cyan", width=20)
        table.add_column("Status", width=10)
        table.add_column("Activity", style="white")
        
        # Track latest status for each agent
        agent_status = {}
        for activity in agent_activity:
            agent = activity["agent"]
            agent_status[agent] = activity
        
        # Display all agents
        all_agents = [
            "Orchestrator",
            "ContextCollector",
            "ErrorAnalyzer",
            "DocSearch",
            "SolutionArchitect",
            "Executor"
        ]
        
        for agent in all_agents:
            if agent in agent_status:
                activity = agent_status[agent]
                status = activity["status"]
                message = activity["message"]
                table.add_row(
                    agent,
                    status_symbols.get(status, "○"),
                    message
                )
            else:
                table.add_row(agent, "[dim]○[/dim]", "[dim]Waiting...[/dim]")
        
        console.print(table)
        console.print()
    
    @staticmethod
    def print_causality_graph(error_analysis: ErrorAnalysis):
        """Print error causality chain as a tree"""
        console.print(
            Panel.fit(
                "🔍 Error Chain Analysis",
                style="bold yellow"
            )
        )
        
        tree = Tree("🎯 Root Cause Analysis", guide_style="bold bright_blue")
        
        # Build causality chain
        current = tree
        for i, step in enumerate(error_analysis.causality_chain):
            if i == len(error_analysis.causality_chain) - 1:
                current = current.add(f"[red]⚠️  {step}[/red]")
            else:
                current = current.add(f"[yellow]↓ {step}[/yellow]")
        
        console.print(tree)
        console.print()
        
        # Additional info
        info_table = Table(box=box.SIMPLE, show_header=False)
        info_table.add_column("Key", style="cyan bold")
        info_table.add_column("Value")
        
        info_table.add_row("Error Type", error_analysis.error_type)
        info_table.add_row("Category", error_analysis.error_category.upper())
        info_table.add_row("Severity", f"[{'red' if error_analysis.severity == 'critical' else 'yellow'}]{error_analysis.severity.upper()}[/]")
        info_table.add_row("Confidence", f"{error_analysis.confidence:.0%}")
        
        console.print(info_table)
        console.print()
    
    @staticmethod
    def print_solution_strategies(strategies: List[SolutionStrategy]):
        """Print solution strategies with comparison"""
        console.print(
            Panel.fit(
                "💡 Solution Strategies",
                style="bold green"
            )
        )
        
        for i, strategy in enumerate(strategies, 1):
            # Risk color
            risk_colors = {
                "low": "green",
                "medium": "yellow",
                "high": "red"
            }
            risk_color = risk_colors.get(strategy.risk_level, "white")
            
            # Create strategy panel
            strategy_content = f"""
[bold]{strategy.name}[/bold]
{strategy.description}

[cyan]Commands:[/cyan]
"""
            for cmd in strategy.commands:
                strategy_content += f"  $ {cmd}\n"
            
            strategy_content += f"""
[cyan]Details:[/cyan]
  • Risk Level: [{risk_color}]{strategy.risk_level.upper()}[/{risk_color}]
  • Confidence: {strategy.confidence:.0%}
  • Estimated Time: {strategy.estimated_time}
"""
            
            if strategy.prerequisites:
                strategy_content += f"\n[cyan]Prerequisites:[/cyan]\n"
                for prereq in strategy.prerequisites:
                    strategy_content += f"  • {prereq}\n"
            
            if strategy.side_effects:
                strategy_content += f"\n[yellow]⚠️  Potential Side Effects:[/yellow]\n"
                for effect in strategy.side_effects:
                    strategy_content += f"  • {effect}\n"
            
            panel = Panel(
                strategy_content,
                title=f"Strategy {i}",
                border_style=risk_color,
                box=box.ROUNDED
            )
            
            console.print(panel)
            console.print()
    
    @staticmethod
    def print_documentation_results(docs: List[DocumentationResult]):
        """Print documentation search results"""
        if not docs:
            return
        
        console.print(
            Panel.fit(
                "📚 Relevant Documentation",
                style="bold blue"
            )
        )
        
        for i, doc in enumerate(docs, 1):
            console.print(f"[bold cyan]{i}. {doc.title}[/bold cyan]")
            console.print(f"   [dim]{doc.url}[/dim]")
            console.print(f"   {doc.snippet[:200]}...")
            console.print(f"   [green]Relevance: {doc.relevance_score:.0%}[/green]")
            console.print()
    
    @staticmethod
    def print_execution_preview(strategy: SolutionStrategy):
        """Print execution preview"""
        console.print(
            Panel.fit(
                "🚀 Execution Preview",
                style="bold green"
            )
        )
        
        console.print("[cyan]The following commands will be executed:[/cyan]\n")
        
        for i, cmd in enumerate(strategy.commands, 1):
            syntax = Syntax(cmd, "bash", theme="monokai", line_numbers=False)
            console.print(f"  {i}. ", end="")
            console.print(syntax)
        
        console.print()
        
        if strategy.side_effects:
            console.print("[yellow]⚠️  Warning: This will:[/yellow]")
            for effect in strategy.side_effects:
                console.print(f"   • {effect}")
            console.print()
    
    @staticmethod
    def prompt_strategy_selection(strategies: List[SolutionStrategy]) -> int:
        """Prompt user to select a strategy"""
        console.print("[bold]Select a strategy to execute:[/bold]")
        console.print("  [1-{}] Choose strategy number".format(len(strategies)))
        console.print("  [d] Show detailed comparison")
        console.print("  [q] Quit without executing")
        console.print()
        
        choice = console.input("[bold cyan]Your choice: [/bold cyan]")
        return choice
    
    @staticmethod
    def prompt_execution_confirmation() -> bool:
        """Prompt for execution confirmation"""
        console.print()
        response = console.input(
            "[bold yellow]Execute these commands? [y/N]: [/bold yellow]"
        )
        return response.lower() in ['y', 'yes']
    
    @staticmethod
    def print_success(message: str):
        """Print success message"""
        console.print(
            Panel.fit(
                f"✅ {message}",
                style="bold green"
            )
        )
    
    @staticmethod
    def print_error(message: str):
        """Print error message"""
        console.print(
            Panel.fit(
                f"❌ {message}",
                style="bold red"
            )
        )
    
    @staticmethod
    def print_info(message: str):
        """Print info message"""
        console.print(
            Panel.fit(
                f"ℹ️  {message}",
                style="bold blue"
            )
        )
