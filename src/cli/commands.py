# ============================================================================
# FILE: src/cli/commands.py
# CLI commands using Typer
# ============================================================================

import typer
from typing import Optional
from pathlib import Path
from .ui import TerminalHeroUI, console
from ..graph.workflow import TerminalHeroWorkflow
from ..storage.memory import MemorySystem
from ..storage.history import CommandHistory
from ..agents.executor import ExecutorAgent
from ..monitor.terminal_monitor import TerminalMonitor
import sys
import os
import platform
from rich.table import Table
from rich import box

app = typer.Typer(
    name="terminal-hero",
    help="AI-Powered Terminal Troubleshooting Agent",
    add_completion=False
)

ui = TerminalHeroUI()
workflow = TerminalHeroWorkflow()
memory = MemorySystem()
history = CommandHistory()

@app.command()
def diagnose(
    error: Optional[str] = typer.Argument(None, help="Error message or description")
):
    """Diagnose and fix a terminal error"""
    
    ui.print_banner()
    
    # Get error input
    if not error:
        console.print("[cyan]Paste your error message or describe the issue:[/cyan]")
        error = console.input("[bold]> [/bold]")
    
    if not error.strip():
        ui.print_error("No error provided. Exiting.")
        raise typer.Exit(1)
    
    console.print()
    console.print("[bold green]🔍 Analyzing your issue...[/bold green]")
    console.print()
    
    # Run workflow
    try:
        result = workflow.run(
            user_input=error,
            raw_error=error
        )
        
        # Display agent activity
        ui.print_agent_dashboard(result["agent_activity"])
        
        # Display error analysis
        if result.get("error_analysis"):
            ui.print_causality_graph(result["error_analysis"])
        
        # Display documentation
        if result.get("documentation_results"):
            ui.print_documentation_results(result["documentation_results"][:3])
        
        # Display solutions
        if result.get("solution_strategies"):
            strategies = result["solution_strategies"]
            ui.print_solution_strategies(strategies)
            
            # Prompt for selection
            while True:
                choice = ui.prompt_strategy_selection(strategies)
                
                if choice.lower() == 'q':
                    console.print("[yellow]Exiting without executing.[/yellow]")
                    raise typer.Exit(0)
                elif choice.lower() == 'd':
                    # Show detailed comparison
                    continue
                else:
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(strategies):
                            selected = strategies[idx]
                            break
                    except:
                        pass
                
                ui.print_error("Invalid choice. Please try again.")
            
            # Show execution preview
            ui.print_execution_preview(selected)
            
            # Confirm execution
            if ui.prompt_execution_confirmation():
                executor = ExecutorAgent()
                exec_result = executor.execute_commands(selected.commands)
                
                if exec_result.success:
                    ui.print_success("Commands executed successfully!")
                    console.print("\n[bold]Output:[/bold]")
                    console.print(exec_result.output)
                    
                    # Record in history
                    history.add_execution(
                        commands=selected.commands,
                        rollback_commands=selected.rollback_commands,
                        description=selected.name
                    )
                    
                    # Record in memory
                    if result.get("error_analysis"):
                        memory.record_solution_attempt(
                            error_type=result["error_analysis"].error_type,
                            error_category=result["error_analysis"].error_category,
                            raw_error=error[:500],
                            solution=str(selected.commands),
                            success=True
                        )
                else:
                    ui.print_error("Execution failed!")
                    if exec_result.error:
                        console.print(f"\n[red]Error:[/red] {exec_result.error}")
            else:
                console.print("[yellow]Execution cancelled.[/yellow]")
        else:
            ui.print_error("No solutions found. Manual investigation required.")
            
    except Exception as e:
        ui.print_error(f"Workflow failed: {str(e)}")
        raise typer.Exit(1)

@app.command()
def doctor():
    """Run a health check on your system"""
    ui.print_banner()
    console.print("[bold cyan]🏥 Running system health check...[/bold cyan]")
    console.print()
    
    from ..core.system_detector import SystemDetector
    
    info = SystemDetector.collect_all()
    
    table = Table(title="System Information", box=box.ROUNDED)
    table.add_column("Property", style="cyan bold")
    table.add_column("Value", style="white")
    
    table.add_row("Operating System", f"{info.os_type} {info.os_version}")
    table.add_row("Shell", info.shell)
    table.add_row("Python", info.python_version or "Not found")
    table.add_row("Node.js", info.node_version or "Not found")
    table.add_row("Package Managers", ", ".join(info.package_managers))
    
    console.print(table)
    console.print()
    
    ui.print_success("System check complete!")

@app.command()
def undo(
    last: bool = typer.Option(True, help="Undo last execution")
):
    """Undo the last executed command"""
    
    if last:
        exec_entry = history.get_last_execution()
    else:
        # TODO: Allow selecting specific execution
        exec_entry = history.get_last_execution()
    
    if not exec_entry:
        ui.print_error("No executions to undo.")
        raise typer.Exit(1)
    
    console.print(f"[bold]Undoing:[/bold] {exec_entry['description']}")
    console.print()
    
    if exec_entry.get("rollback_commands"):
        ui.print_info("Executing rollback commands...")
        
        executor = ExecutorAgent()
        result = executor.execute_commands(exec_entry["rollback_commands"])
        
        if result.success:
            ui.print_success("Rollback successful!")
        else:
            ui.print_error("Rollback failed!")
            console.print(result.error)
    else:
        ui.print_error("No rollback commands available for this execution.")

@app.command()
def history_cmd(
    count: int = typer.Option(10, help="Number of recent executions to show")
):
    """Show execution history"""
    
    recent = history.list_recent(count)
    
    if not recent:
        console.print("[yellow]No execution history found.[/yellow]")
        return
    
    table = Table(title="Execution History", box=box.ROUNDED)
    table.add_column("ID", style="cyan")
    table.add_column("Timestamp", style="dim")
    table.add_column("Description")
    table.add_column("Commands", style="green")
    
    for entry in recent:
        table.add_row(
            str(entry["id"]),
            entry["timestamp"][:19],
            entry["description"],
            f"{len(entry['commands'])} command(s)"
        )
    
    console.print(table)

@app.command()
def monitor(
    install: bool = typer.Option(False, help="Install shell integration"),
    uninstall: bool = typer.Option(False, help="Remove shell integration"),
    start: bool = typer.Option(False, help="Start monitoring daemon"),
    stop: bool = typer.Option(False, help="Stop monitoring daemon"),
    auto_fix: bool = typer.Option(True, help="Enable autonomous fixes"),
    status: bool = typer.Option(False, help="Show monitor status"),
):
    """
    Autonomous terminal monitoring and interference.
    Watch your terminal commands and autonomously fix errors.
    """
    
    ui.print_banner()
    
    monitor_instance = TerminalMonitor(workflow)
    
    # Install mode
    if install:
        console.print("[bold cyan]Installing Terminal Hero autonomous monitor...[/bold cyan]")
        
        shell_type = "zsh" if "zsh" in os.getenv("SHELL", "") else "bash"
        console.print(f"Detected shell: {shell_type}")
        
        if monitor_instance.install_shell_integration(shell_type):
            ui.print_success("Monitor installed successfully!")
            console.print("\n[cyan]To activate, run:[/cyan]")
            console.print(f"  source ~/.{shell_type}rc")
            console.print("\n[cyan]To uninstall later, run:[/cyan]")
            console.print("  terminal-hero monitor --uninstall")
        else:
            ui.print_error("Failed to install monitor")
            raise typer.Exit(1)
        
        return
    
    # Uninstall mode
    if uninstall:
        console.print("[bold yellow]Removing Terminal Hero autonomous monitor...[/bold yellow]")
        
        shell_type = "zsh" if "zsh" in os.getenv("SHELL", "") else "bash"
        
        if monitor_instance.uninstall_shell_integration(shell_type):
            ui.print_success("Monitor uninstalled successfully!")
            console.print("\n[cyan]To complete removal, run:[/cyan]")
            console.print(f"  source ~/.{shell_type}rc")
        else:
            ui.print_error("Failed to uninstall monitor")
            raise typer.Exit(1)
        
        return
    
    # Status mode
    if status:
        console.print("[bold cyan]Monitor Status[/bold cyan]\n")
        
        monitor_status = monitor_instance.get_status()
        
        table = Table(box=box.ROUNDED)
        table.add_column("Property", style="cyan bold")
        table.add_column("Value", style="white")
        
        table.add_row("Status", "🟢 Active" if monitor_status["is_monitoring"] else "🔴 Inactive")
        table.add_row("Auto-fix Enabled", "✓ Yes" if monitor_status["auto_fix_enabled"] else "✗ No")
        
        console.print(table)
        
        return
    
    # Start daemon
    if start:
        console.print("[bold cyan]Starting Terminal Hero autonomous monitor daemon...[/bold cyan]")
        monitor_instance.auto_fix_enabled = auto_fix
        monitor_instance.start_daemon()
        
        ui.print_success("Monitor daemon started!")
        console.print("\n[cyan]The monitor is now watching your commands for errors.[/cyan]")
        console.print("[cyan]When an error is detected, Terminal Hero will:[/cyan]")
        console.print("  1. 🔍 Analyze the error")
        console.print("  2. 💡 Generate solutions")
        console.print("  3. 🤖 Suggest or auto-fix (based on risk level)")
        
        return
    
    # Stop daemon
    if stop:
        console.print("[bold yellow]Stopping Terminal Hero monitor...[/bold yellow]")
        monitor_instance.stop_daemon()
        ui.print_success("Monitor stopped!")
        return
    
    # Default: show help
    console.print("[cyan]Terminal Hero Autonomous Monitor[/cyan]\n")
    console.print("Usage examples:")
    console.print("  terminal-hero monitor --install        # Install shell integration")
    console.print("  terminal-hero monitor --start          # Start monitoring daemon")
    console.print("  terminal-hero monitor --status         # Check monitor status")
    console.print("  terminal-hero monitor --stop           # Stop monitoring")
    console.print("  terminal-hero monitor --uninstall      # Remove monitor")

if __name__ == "__main__":
    app()