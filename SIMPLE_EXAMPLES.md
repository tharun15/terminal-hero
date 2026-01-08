# Terminal Hero - Quick Examples

Quick and simple examples to test Terminal Hero.

## ⚡ 30-Second Test

```bash
# 1. Install
terminal-hero monitor --install && source ~/.bashrc

# 2. Start
terminal-hero monitor --start

# 3. Run a failing command
npm --version

# 4. Watch Terminal Hero respond!
```

---

## 📝 Code Examples

### Example 1: Use the Resolver
```python
from src.monitor import AutonomousResolver

resolver = AutonomousResolver()

# Analyze an error
decision = resolver.analyze_error(
    "npm: command not found", 
    "npm start"
)

print(decision.intervention_level)  # SUGGEST
print(decision.confidence)          # 0.7 (70%)
print(decision.suggested_actions)   # List of actions
```

### Example 2: Create a Monitor
```python
from src.monitor import TerminalMonitor, CommandEvent

monitor = TerminalMonitor()

# Handle events
def on_error(event):
    print(f"Error: {event.command}")

monitor.register_event_handler(on_error)

# Emit test event
event = CommandEvent(
    timestamp="2024-01-08T12:00:00",
    command="npm start",
    exit_code=127,
    stdout="",
    stderr="npm: command not found",
    duration=0.1,
    success=False
)

monitor.emit_event(event)  # Calls on_error()
```

### Example 3: Test Learning
```python
from src.monitor import AutonomousResolver
from src.graph.state import SolutionStrategy

resolver = AutonomousResolver()

# Create a solution
solution = SolutionStrategy(
    name="Install npm",
    description="Install Node.js and npm",
    commands=["apt-get install npm"],
    risk_level="low",
    estimated_time="2 minutes",
)

# First attempt: low confidence
d1 = resolver.analyze_error("npm: command not found", "npm start")
print(f"1st: {d1.intervention_level.name}")  # SUGGEST
resolver.record_outcome("command_not_found", True, solution)

# Second attempt: higher confidence
d2 = resolver.analyze_error("npm: command not found", "npm start")
print(f"2nd: {d2.intervention_level.name}")  # Still SUGGEST
resolver.record_outcome("command_not_found", True, solution)

# Third attempt: even higher
d3 = resolver.analyze_error("npm: command not found", "npm start")
print(f"3rd: {d3.intervention_level.name}")  # AUTO_LOW_RISK!
```

---

## 🎯 Real Terminal Tests

### Test 1: Missing Command
```bash
$ npm --version
npm: command not found

# Terminal Hero detects and suggests installation
[Terminal Hero] 🔍 Detected: command_not_found
[Terminal Hero] Suggested: apt-get install npm
```

### Test 2: Permission Error
```bash
$ echo "echo hi" > script.sh
$ ./script.sh
bash: ./script.sh: Permission denied

# Terminal Hero detects and suggests fix
[Terminal Hero] 🔍 Detected: permission_denied
[Terminal Hero] Suggested: chmod +x script.sh
```

### Test 3: Missing Module
```bash
$ python3 -c "import numpy"
ModuleNotFoundError: No module named 'numpy'

# Terminal Hero detects and suggests installation
[Terminal Hero] 🔍 Detected: missing_dependency
[Terminal Hero] Suggested: pip install numpy
```

---

## 🚀 Run All Examples

```bash
# API examples
python3 examples/api_examples.py

# Test resolver
python3 examples/api_examples.py 2

# Test learning
python3 examples/api_examples.py 3

# Test categorization
python3 examples/api_examples.py 4

# Test risk assessment
python3 examples/api_examples.py 5
```

---

## 📊 Key Components to Test

### 1. TerminalMonitor
```python
from src.monitor import TerminalMonitor

monitor = TerminalMonitor()
monitor.register_event_handler(callback)
monitor.emit_event(command_event)
```

### 2. AutonomousResolver
```python
from src.monitor import AutonomousResolver

resolver = AutonomousResolver()
decision = resolver.analyze_error(error_msg, command)
resolver.record_outcome(error_type, success, solution)
```

### 3. InterventionLevel
```python
from src.monitor import InterventionLevel

# Levels: SILENT, SUGGEST, AUTO_LOW_RISK, AUTO_MEDIUM, FULL_AUTONOMOUS
level = decision.intervention_level
```

### 4. CommandEvent
```python
from src.monitor import CommandEvent

event = CommandEvent(
    timestamp=str,
    command=str,
    exit_code=int,
    stdout=str,
    stderr=str,
    duration=float,
    success=bool
)
```

---

## 💡 What to Observe

When you run these examples, notice:

✅ **Resolver Decisions**
- How errors are categorized
- Confidence scores
- Suggested actions

✅ **Learning Progression**
- Confidence increases over time
- Intervention level escalates
- System becomes more autonomous

✅ **Risk Assessment**
- Low-risk commands: auto-execute
- Medium-risk: ask permission
- High-risk: suggest only

✅ **Real Terminal Behavior**
- Errors detected instantly
- Suggestions appear automatically
- System learns from outcomes

---

## 🎓 Understanding the Flow

```
Error Occurs
    ↓
Monitor Detects (< 10ms)
    ↓
Resolver Analyzes (< 100ms)
    ↓
Decision Made
    ├─ Type identified
    ├─ Confidence calculated
    └─ Action determined
    ↓
Action Taken
    ├─ SUGGEST: Show suggestion
    ├─ AUTO_LOW_RISK: Auto-execute
    └─ AUTO_MEDIUM: Ask permission
    ↓
Learning Updated
    ├─ Success rate recorded
    ├─ Confidence increased
    └─ Pattern learned
    ↓
Next Similar Error
    ├─ Uses learned patterns
    ├─ Higher confidence
    └─ Better action taken
```

---

## ✨ Example Output

### Resolver Example Output
```
Error: npm: command not found
  → Type: command_not_found
  → Confidence: 70%
  → Action: SUGGEST
  → First suggestion: Check spelling of the command

Error: Permission denied
  → Type: permission_denied
  → Confidence: 85%
  → Action: SUGGEST
  → First suggestion: Add execute permission: chmod +x <file>
```

### Learning Example Output
```
1st encounter: SUGGEST (confidence: 50%)
2nd encounter: SUGGEST (confidence: 65%)
3rd encounter: SUGGEST (confidence: 75%)
4th encounter: AUTO_LOW_RISK (confidence: 85%)
5th encounter: AUTO_MEDIUM (confidence: 95%)

✓ System learned: auto-execution confidence increased!
After 4 successful encounters, system shifts to AUTO_LOW_RISK level
```

---

## 🔧 Debug Tips

### Check if errors are recognized
```python
from src.monitor import AutonomousResolver
r = AutonomousResolver()
d = r.analyze_error("your error message", "command")
print(d.reason)  # Shows identified error type
```

### Check learning status
```python
from src.monitor import AutonomousResolver
r = AutonomousResolver()
status = r.get_learning_status()
print(status['success_rates'])  # Success rates per error type
print(status['learned_solutions'])  # Solutions learned
```

### Test risk assessment
```python
from src.monitor import AutonomousResolver, InterventionLevel
r = AutonomousResolver()
d = InterventionLevel.AUTO_LOW_RISK
d.confidence = 0.95
should_exec = r.should_auto_execute(d, risk_level="low")
print(should_exec)  # True for low-risk, False for medium+
```

---

## 🎉 That's It!

These simple examples show everything Terminal Hero can do:
- 🔍 Error detection
- 🤖 Intelligent decisions
- 📚 Learning system
- ⚡ Autonomous action

Start with the API examples, then test real errors!

---

**Next**: Read `TESTING_WALKTHROUGH.md` for detailed step-by-step guide
