#!/usr/bin/env python3
"""
Terminal Hero - Simple Test Examples
Demonstrates the autonomous resolver in action
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.monitor import AutonomousResolver

def test_resolver():
    """Test the autonomous resolver with sample errors"""
    
    resolver = AutonomousResolver()
    
    print("=" * 60)
    print("Terminal Hero - Autonomous Resolver Test")
    print("=" * 60)
    print()
    
    # Test cases
    test_errors = [
        {
            "command": "npm start",
            "error": "npm: command not found",
            "description": "Missing package manager"
        },
        {
            "command": "./deploy.sh",
            "error": "bash: ./deploy.sh: Permission denied",
            "description": "File not executable"
        },
        {
            "command": "python3 -c 'import requests'",
            "error": "ModuleNotFoundError: No module named 'requests'",
            "description": "Missing Python dependency"
        },
        {
            "command": "npm start",
            "error": "listen EADDRINUSE: address already in use :::3000",
            "description": "Port already in use"
        },
        {
            "command": "git clone repo.git",
            "error": "fatal: unable to access 'https://...': Could not resolve host",
            "description": "Network error"
        },
    ]
    
    for i, test_case in enumerate(test_errors, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"  Command: {test_case['command']}")
        print(f"  Error: {test_case['error']}")
        print()
        
        # Analyze the error
        decision = resolver.analyze_error(test_case['error'], test_case['command'])
        
        print(f"  Resolver Analysis:")
        print(f"    ✓ Should Intervene: {decision.should_intervene}")
        print(f"    ✓ Confidence: {decision.confidence:.0%}")
        print(f"    ✓ Intervention Level: {decision.intervention_level.name}")
        print(f"    ✓ Reason: {decision.reason}")
        print(f"    ✓ Suggested Actions:")
        for action in decision.suggested_actions:
            print(f"      - {action}")
        print()
        print("-" * 60)
        print()
    
    # Show learning status
    print("Learning Status After Analysis:")
    print()
    status = resolver.get_learning_status()
    print(f"  Total Interventions: {status['total_interventions']}")
    print(f"  Error Types Learned: {status['error_types_learned']}")
    print(f"  Success Rates: {status['success_rates']}")
    print()


def test_monitor_events():
    """Test the terminal monitor event system"""
    
    from src.monitor import TerminalMonitor, CommandEvent
    from datetime import datetime
    
    print("=" * 60)
    print("Terminal Hero - Monitor Event Test")
    print("=" * 60)
    print()
    
    monitor = TerminalMonitor()
    
    # Register an event handler
    def on_command_event(event: CommandEvent):
        print(f"  Event Handler Called!")
        print(f"    Command: {event.command}")
        print(f"    Exit Code: {event.exit_code}")
        print(f"    Success: {event.success}")
    
    monitor.register_event_handler(on_command_event)
    
    # Emit test events
    print("Creating test command events...")
    print()
    
    # Success event
    event1 = CommandEvent(
        timestamp=datetime.now().isoformat(),
        command="echo 'Hello World'",
        exit_code=0,
        stdout="Hello World",
        stderr="",
        duration=0.1,
        success=True
    )
    
    print("Event 1: Successful Command")
    print(f"  Command: {event1.command}")
    print(f"  Exit Code: {event1.exit_code}")
    monitor.emit_event(event1)
    print()
    
    # Error event
    event2 = CommandEvent(
        timestamp=datetime.now().isoformat(),
        command="npm start",
        exit_code=127,
        stdout="",
        stderr="npm: command not found",
        duration=0.2,
        success=False
    )
    
    print("Event 2: Failed Command")
    print(f"  Command: {event2.command}")
    print(f"  Exit Code: {event2.exit_code}")
    print(f"  Error: {event2.stderr}")
    monitor.emit_event(event2)
    print()


def demonstrate_learning():
    """Demonstrate the learning system"""
    
    from src.monitor import AutonomousResolver
    from src.graph.state import SolutionStrategy
    
    print("=" * 60)
    print("Terminal Hero - Learning System Demonstration")
    print("=" * 60)
    print()
    
    resolver = AutonomousResolver()
    
    error_type = "command_not_found"
    solution = SolutionStrategy(
        name="Install missing command",
        description="Install the missing package using apt-get",
        commands=["apt-get install npm"],
        risk_level="low",
        estimated_time="30 seconds",
    )
    
    print(f"Simulating repeated encounters with: {error_type}")
    print()
    
    # Simulate 5 encounters
    for attempt in range(1, 6):
        # Record a successful outcome
        resolver.record_outcome(error_type, success=True, solution=solution)
        
        success_rate = resolver.success_patterns.get(error_type, 0)
        
        print(f"Attempt {attempt}:")
        print(f"  Success Rate: {success_rate:.0%}")
        
        # Show what would happen next time
        decision = resolver.analyze_error(
            "command: command not found",
            "command arg1"
        )
        print(f"  Next Intervention: {decision.intervention_level.name}")
        print(f"  Confidence: {decision.confidence:.0%}")
        print()
    
    print("Learning Progression:")
    print("  Attempt 1: SUGGEST (50%) → Show suggestion")
    print("  Attempt 2: SUGGEST (67%) → Show suggestion")
    print("  Attempt 3: SUGGEST (77%) → Show suggestion")
    print("  Attempt 4: AUTO_LOW_RISK (84%) → Auto-execute")
    print("  Attempt 5: AUTO_MEDIUM (88%) → Auto-execute")
    print()
    print("✓ System learned the pattern and increased automation!")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test = sys.argv[1]
        if test == "resolver":
            test_resolver()
        elif test == "monitor":
            test_monitor_events()
        elif test == "learning":
            demonstrate_learning()
        else:
            print(f"Unknown test: {test}")
            print("Available tests: resolver, monitor, learning")
    else:
        # Run all tests
        try:
            test_resolver()
            print("\n\n")
            test_monitor_events()
            print("\n\n")
            demonstrate_learning()
        except Exception as e:
            print(f"Error running tests: {e}")
            print("\nMake sure you're running from the project root:")
            print("  cd ~/projects/terminal-hero")
            print("  python3 examples/test_simple.py")
