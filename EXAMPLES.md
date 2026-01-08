# Terminal Hero - Examples & Testing

Quick examples to test and understand Terminal Hero's autonomous monitoring.

## 1️⃣ Simple API Examples

Run the programmatic examples:

```bash
# Run all examples
python3 examples/api_examples.py

# Run specific example
python3 examples/api_examples.py 1  # Monitoring setup
python3 examples/api_examples.py 2  # Resolver decisions
python3 examples/api_examples.py 3  # Learning system
python3 examples/api_examples.py 4  # Error categorization
python3 examples/api_examples.py 5  # Risk assessment
```

### Example 1: Basic Monitoring
```python
from src.monitor import TerminalMonitor, CommandEvent

monitor = TerminalMonitor()

# Register an event handler
def on_error(event: CommandEvent):
    print(f"Error detected: {event.command}")

monitor.register_event_handler(on_error)

# Emit test events
event = CommandEvent(..., success=False, ...)
monitor.emit_event(event)  # Handler gets called
```

### Example 2: Resolver Decisions
```python
from src.monitor import AutonomousResolver

resolver = AutonomousResolver()

# Analyze an error
decision = resolver.analyze_error("npm: command not found", "npm start")

print(decision.intervention_level)  # SUGGEST
print(decision.confidence)          # 0.7
print(decision.suggested_actions)   # ["Install npm..."]
```

### Example 3: Learning System
```python
# First encounter
decision1 = resolver.analyze_error(error, command)
resolver.record_outcome(error_type, success=True, solution)

# Second encounter - confidence increased
decision2 = resolver.analyze_error(error, command)
print(decision2.confidence)  # Higher than before
```

### Example 4: Error Categorization
```python
# System automatically identifies:
"npm: command not found" → command_not_found
"Permission denied" → permission_denied
"ModuleNotFoundError" → missing_dependency
"Address already in use" → port_already_in_use
"No space left on device" → disk_space
"Could not resolve host" → network_error
```

### Example 5: Risk Assessment
```python
# Auto-execute based on risk level
should_execute = resolver.should_auto_execute(decision, risk_level="low")

# Low-risk: Can auto-execute if confident
# Medium-risk: Always ask for approval
# High-risk: Never auto-execute
```

---

## 2️⃣ Real Terminal Testing

Test Terminal Hero with actual commands:

### Test 1: Missing Command
```bash
# This will fail with "command not found"
npm --version

# Terminal Hero output:
# [Terminal Hero] 🔍 Detected: command_not_found
# [Terminal Hero] Confidence: 70%
# [Terminal Hero] Solution: apt-get install npm
```

### Test 2: Permission Error
```bash
# Create a script without execute permission
echo "echo hello" > test.sh
./test.sh

# Terminal Hero output:
# [Terminal Hero] 🔍 Detected: permission_denied
# [Terminal Hero] Confidence: 90%
# [Terminal Hero] Solution: chmod +x test.sh
```

### Test 3: Missing Python Package
```bash
# Try importing a package that doesn't exist
python3 -c "import nonexistent_package"

# Terminal Hero output:
# [Terminal Hero] 🔍 Detected: missing_dependency
# [Terminal Hero] Confidence: 80%
# [Terminal Hero] Solution: pip install nonexistent_package
```

### Test 4: Network Error
```bash
# Try to reach an unreachable host
ping 192.0.2.1

# Terminal Hero output:
# [Terminal Hero] 🔍 Detected: network_error
# [Terminal Hero] Confidence: 60%
# [Terminal Hero] Suggestions: Check internet connection
```

---

## 3️⃣ Monitoring Setup Test

```bash
# Install
terminal-hero monitor --install
source ~/.bashrc

# Start
terminal-hero monitor --start

# Check status
terminal-hero monitor --status

# Now run some commands that will fail
npm --version        # command not found
./script.sh          # permission denied
python3 -c "import flask"  # missing dependency

# Watch Terminal Hero respond automatically!
```

---

## 4️⃣ Learning System Demonstration

Run commands multiple times to see learning in action:

```bash
# First time (SUGGEST level)
$ npm start
npm: command not found
[Terminal Hero] Suggesting: apt-get install npm

# After installation (or second attempt)
$ npm start
npm: command not found
[Terminal Hero] Confidence increased: 75%
[Terminal Hero] Still suggesting...

# After 3-4 attempts
$ npm start
npm: command not found
[Terminal Hero] Confidence: 90%
[Terminal Hero] AUTO_LOW_RISK activated
[Terminal Hero] Auto-executing: apt-get install npm
```

---

## 5️⃣ Component Testing

### Test Resolver Component
```python
from src.monitor import AutonomousResolver

resolver = AutonomousResolver()

# Test error identification
errors = [
    "npm: command not found",
    "Permission denied",
    "ModuleNotFoundError: No module named 'requests'"
]

for error in errors:
    decision = resolver.analyze_error(error, "command")
    print(f"{error}")
    print(f"  → {decision.intervention_level.name}")
    print(f"  → {decision.confidence:.0%} confidence")
```

### Test Monitor Component
```python
from src.monitor import TerminalMonitor, CommandEvent
from datetime import datetime

monitor = TerminalMonitor()

# Create test events
success_event = CommandEvent(
    timestamp=datetime.now().isoformat(),
    command="ls -la",
    exit_code=0,
    stdout="...",
    stderr="",
    duration=0.1,
    success=True
)

error_event = CommandEvent(
    timestamp=datetime.now().isoformat(),
    command="npm start",
    exit_code=127,
    stdout="",
    stderr="npm: command not found",
    duration=0.1,
    success=False
)

# Emit events
monitor.emit_event(success_event)  # Logged
monitor.emit_event(error_event)    # Analyzed
```

---

## 6️⃣ Full Integration Test

Complete end-to-end test:

```bash
#!/bin/bash

# 1. Install
echo "Installing Terminal Hero..."
terminal-hero monitor --install
source ~/.bashrc

# 2. Start
echo "Starting monitor..."
terminal-hero monitor --start
sleep 2

# 3. Run test commands
echo "Running test commands..."

# These should trigger Terminal Hero
npm --version 2>/dev/null || true
docker --version 2>/dev/null || true
python3 -c "import nonexistent" 2>/dev/null || true

# 4. Check results
echo "Checking monitor status..."
terminal-hero monitor --status

# 5. View learning
echo "System learning progress..."
terminal-hero monitor --stats

# 6. Clean up
echo "Stopping monitor..."
terminal-hero monitor --stop
```

---

## 7️⃣ Performance Testing

Check Terminal Hero's performance:

```bash
# Monitor daemon memory usage
ps aux | grep "terminal-hero"

# Expected: ~35MB memory
# Expected: <1% CPU when idle

# Test latency
# Time from error to detection should be < 100ms

# Run high-volume commands
for i in {1..100}; do
    npm --version 2>/dev/null || true
done

# Monitor should handle all without slowdown
```

---

## Expected Output Examples

### Example 1: First Error (SUGGEST level)
```
$ docker run my-app
docker: command not found

[Terminal Hero] 🔍 Detected error
[Terminal Hero] Type: command_not_found (confidence: 70%)
[Terminal Hero] Suggested: apt-get install docker
[Terminal Hero] Would you like me to: install | skip
```

### Example 2: Repeated Error (AUTO level)
```
$ docker run my-app
docker: command not found

[Terminal Hero] 🔍 Detected error
[Terminal Hero] Type: command_not_found (confidence: 95%)
[Terminal Hero] 🤖 Auto-executing: apt-get install docker
[Terminal Hero] ✓ Docker installed successfully
$ docker run my-app
# Now runs successfully
```

### Example 3: Learning Progress
```
$ terminal-hero monitor --stats

Monitor Statistics:
  Total Errors Detected: 15
  Errors Fixed: 12 (80%)
  
Error Categories:
  - command_not_found: 5 occurrences, 100% success
  - permission_denied: 4 occurrences, 75% success
  - missing_dependency: 6 occurrences, 67% success

Learning Level: INTERMEDIATE
  confidence_avg: 78%
  automation_level: AUTO_LOW_RISK
```

---

## Troubleshooting Tests

### Test: Monitor Not Detecting Errors
```bash
# Verify installation
grep TERMINAL_HERO ~/.bashrc

# Verify daemon running
terminal-hero monitor --status

# Try installing again
terminal-hero monitor --install
source ~/.bashrc
terminal-hero monitor --start
```

### Test: Too Many False Positives
```bash
# Disable auto-fix, use suggestions only
terminal-hero monitor --stop
terminal-hero monitor --start --no-auto-fix
```

### Test: Performance Issues
```bash
# Check memory usage
ps aux | grep terminal-hero

# Check if daemon is stuck
terminal-hero monitor --status

# Restart if needed
terminal-hero monitor --stop
terminal-hero monitor --start
```

---

## Next Steps

1. **Run examples**: `python3 examples/api_examples.py`
2. **Test monitoring**: `terminal-hero monitor --install && terminal-hero monitor --start`
3. **Try commands**: Run commands that fail and watch Terminal Hero respond
4. **Monitor learning**: `terminal-hero monitor --status` and `terminal-hero monitor --stats`
5. **Explore code**: Review `src/monitor/` to understand implementation

---

**All examples are designed to be simple and educational.**

Start with the API examples, then test real monitoring, then explore the full system!
