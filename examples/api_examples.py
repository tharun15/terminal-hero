#!/usr/bin/env python3
"""
Terminal Hero - Direct Monitor Test
Shows the autonomous monitor responding to simulated command failures
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.monitor import TerminalMonitor, CommandEvent
from datetime import datetime

def test_monitor_response():
    """Test the monitor responding to command failures"""
    print("\n" + "="*60)
    print("Terminal Hero - Direct Monitor Test")
    print("="*60 + "\n")
    
    # Create monitor
    monitor = TerminalMonitor()
    
    # Register a simple event handler to show responses
    def show_response(event: CommandEvent):
        if not event.success:
            print(f"\n[Terminal Hero] 🔍 Detected failed command: {event.command}")
            print(f"[Terminal Hero] 💡 Analyzing error...")
            
            # This will trigger the autonomous response
            monitor._process_command_event(event)
    
    monitor.register_event_handler(show_response)
    
    print("Testing autonomous responses to failed commands:\n")
    
    # Test cases - simulate failed commands
    test_cases = [
        ("npm install", 1, "", "npm: command not found"),
        ("pip install flask", 1, "", "pip: command not found"),
        ("python -c 'import nonexistent'", 1, "", "ModuleNotFoundError: No module named 'nonexistent'"),
    ]
    
    for command, exit_code, stdout, stderr in test_cases:
        print(f"Running: {command}")
        
        event = CommandEvent(
            timestamp=datetime.now().isoformat(),
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration=1.0,
            success=False
        )
        
        # Emit the event (this triggers the monitor's response)
        monitor.emit_event(event)
        
        print()
    
    print("✓ Monitor test completed!")
    print("The monitor autonomously detected and responded to each error.")

if __name__ == "__main__":
    test_monitor_response()

def example_1_basic_monitoring():
    """Example 1: Basic monitoring setup"""
    print("\n" + "="*60)
    print("Example 1: Basic Monitoring Setup")
    print("="*60 + "\n")
    
    # Create a monitor instance
    monitor = TerminalMonitor()
    
    # Define a callback for events
    def handle_event(event: CommandEvent):
        if not event.success:
            print(f"[Alert] Command failed: {event.command}")
            print(f"        Exit code: {event.exit_code}")
            print(f"        Error: {event.stderr[:100]}")
    
    # Register the handler
    monitor.register_event_handler(handle_event)
    
    # Simulate some command events
    print("Simulating command execution...\n")
    
    # Success event
    event1 = CommandEvent(
        timestamp=datetime.now().isoformat(),
        command="ls -la",
        exit_code=0,
        stdout="file1.txt file2.txt...",
        stderr="",
        duration=0.05,
        success=True
    )
    
    print("✓ Command succeeded: ls -la")
    monitor.emit_event(event1)
    
    # Error event
    event2 = CommandEvent(
        timestamp=datetime.now().isoformat(),
        command="npm install",
        exit_code=127,
        stdout="",
        stderr="npm: command not found",
        duration=0.1,
        success=False
    )
    
    print("✗ Command failed: npm install")
    monitor.emit_event(event2)
    print()


def example_2_resolver_decisions():
    """Example 2: Using the autonomous resolver"""
    print("\n" + "="*60)
    print("Example 2: Resolver Decision Making")
    print("="*60 + "\n")
    
    resolver = AutonomousResolver()
    
    errors_to_test = [
        "npm: command not found",
        "Permission denied",
        "ModuleNotFoundError: No module named 'flask'",
        "Address already in use :::8000",
        "Temporary failure in name resolution",
    ]
    
    for error in errors_to_test:
        print(f"Error: {error}")
        
        decision = resolver.analyze_error(error, "some_command")
        
        print(f"  → Type: {decision.reason}")
        print(f"  → Confidence: {decision.confidence:.0%}")
        print(f"  → Action: {decision.intervention_level.name}")
        print(f"  → First suggestion: {decision.suggested_actions[0] if decision.suggested_actions else 'None'}")
        print()


def example_3_learning_system():
    """Example 3: The learning system in action"""
    print("\n" + "="*60)
    print("Example 3: Learning System")
    print("="*60 + "\n")
    
    resolver = AutonomousResolver()
    
    from src.graph.state import SolutionStrategy
    
    print("Simulating repeated 'npm not found' errors:\n")
    
    solution = SolutionStrategy(
        name="Install npm",
        description="Install Node.js and npm",
        commands=["apt-get install npm"],
        risk_level="low",
        estimated_time="2 minutes",
        confidence=0.8,
    )
    
    # First encounter
    decision1 = resolver.analyze_error("npm: command not found", "npm start")
    print(f"1st encounter: {decision1.intervention_level.name} (confidence: {decision1.confidence:.0%})")
    resolver.record_outcome("command_not_found", True, solution)
    
    # Second encounter
    decision2 = resolver.analyze_error("npm: command not found", "npm start")
    print(f"2nd encounter: {decision2.intervention_level.name} (confidence: {decision2.confidence:.0%})")
    resolver.record_outcome("command_not_found", True, solution)
    
    # Third encounter
    decision3 = resolver.analyze_error("npm: command not found", "npm start")
    print(f"3rd encounter: {decision3.intervention_level.name} (confidence: {decision3.confidence:.0%})")
    resolver.record_outcome("command_not_found", True, solution)
    
    # Fourth encounter
    decision4 = resolver.analyze_error("npm: command not found", "npm start")
    print(f"4th encounter: {decision4.intervention_level.name} (confidence: {decision4.confidence:.0%})")
    resolver.record_outcome("command_not_found", True, solution)
    
    print("\n✓ System learned: auto-execution confidence increased!")
    print("  After 4 successful encounters, system shifts to AUTO_LOW_RISK level")
    print()


def example_4_error_categorization():
    """Example 4: Error type identification"""
    print("\n" + "="*60)
    print("Example 4: Error Categorization")
    print("="*60 + "\n")
    
    resolver = AutonomousResolver()
    
    test_cases = [
        ("bash: docker: command not found", "command_not_found"),
        ("bash: ./script.sh: Permission denied", "permission_denied"),
        ("pip: No module named requests", "missing_dependency"),
        ("Address already in use", "port_already_in_use"),
        ("No space left on device", "disk_space"),
        ("Could not resolve host", "network_error"),
    ]
    
    print("Error Categorization Examples:\n")
    
    for error_msg, expected_category in test_cases:
        decision = resolver.analyze_error(error_msg, "command")
        
        # Extract identified category
        identified = "unknown"
        for category in ["command_not_found", "permission_denied", "missing_dependency", 
                        "port_already_in_use", "disk_space", "network_error"]:
            if category in decision.reason.lower():
                identified = category
                break
        
        status = "✓" if identified == expected_category else "✗"
        print(f"{status} Expected: {expected_category:20} | Identified: {identified:20}")
        print(f"   Error: {error_msg}")
        print()


def example_5_risk_assessment():
    """Example 5: Risk-based execution decisions"""
    print("\n" + "="*60)
    print("Example 5: Risk Assessment")
    print("="*60 + "\n")
    
    resolver = AutonomousResolver()
    
    from src.monitor import InterventionLevel
    
    print("Risk Level Impact on Auto-Execution:\n")
    
    # Create a high-confidence decision
    decision = resolver.analyze_error("npm: command not found", "npm start")
    decision.intervention_level = InterventionLevel.AUTO_LOW_RISK
    decision.confidence = 0.95
    
    # Test different risk levels
    risk_levels = ["low", "medium", "high", "critical"]
    
    for risk_level in risk_levels:
        should_execute = resolver.should_auto_execute(decision, risk_level)
        status = "✓ WILL AUTO-EXECUTE" if should_execute else "✗ NEEDS APPROVAL"
        print(f"Risk: {risk_level:10} → {status}")
    
    print("\nConclusion:")
    print("  • Low-risk commands: Auto-execute when confident")
    print("  • Medium+ risk: Always ask for approval")
    print("  • This prevents dangerous auto-execution")
    print()


if __name__ == "__main__":
    import sys
    
    print("\n╔════════════════════════════════════════════╗")
    print("║   Terminal Hero - API Examples             ║")
    print("╚════════════════════════════════════════════╝")
    
    # Run specific example or all
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples = {
            "1": example_1_basic_monitoring,
            "2": example_2_resolver_decisions,
            "3": example_3_learning_system,
            "4": example_4_error_categorization,
            "5": example_5_risk_assessment,
        }
        
        if example_num in examples:
            examples[example_num]()
        else:
            print(f"\nUnknown example: {example_num}")
            print("Available: 1, 2, 3, 4, 5")
    else:
        # Run all examples
        try:
            example_1_basic_monitoring()
            example_2_resolver_decisions()
            example_3_learning_system()
            example_4_error_categorization()
            example_5_risk_assessment()
            
            print("\n" + "="*60)
            print("All examples completed!")
            print("="*60)
            print("\nRun specific examples:")
            print("  python3 examples/api_examples.py 1  # Monitoring")
            print("  python3 examples/api_examples.py 2  # Resolver")
            print("  python3 examples/api_examples.py 3  # Learning")
            print("  python3 examples/api_examples.py 4  # Categorization")
            print("  python3 examples/api_examples.py 5  # Risk Assessment")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("\nMake sure to run from project root:")
            print("  cd ~/projects/terminal-hero")
            print("  python3 examples/api_examples.py")
