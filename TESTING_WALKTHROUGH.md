# Terminal Hero - Step-by-Step Testing Walkthrough

A hands-on guide to test Terminal Hero's autonomous monitoring system.

## Prerequisites

- Linux/WSL system
- Python 3.7+
- Terminal Hero installed (from setup instructions)

## Part 1: Run API Examples (5 minutes)

These examples show how Terminal Hero's components work.

```bash
cd ~/projects/terminal-hero

# Run all examples
python3 examples/api_examples.py
```

**What you'll see:**
- Basic monitoring setup demo
- Resolver making decisions
- Learning system in action
- Error categorization
- Risk assessment logic

---

## Part 2: Test the Autonomous Resolver (10 minutes)

Test how Terminal Hero identifies and responds to errors.

### Step 1: Create a test script
```bash
cat > test_resolver.py << 'EOF'
from src.monitor import AutonomousResolver

resolver = AutonomousResolver()

# Test different errors
errors = [
    "npm: command not found",
    "Permission denied",
    "ModuleNotFoundError: No module named 'flask'",
]

for error in errors:
    decision = resolver.analyze_error(error, "some_command")
    print(f"\nError: {error}")
    print(f"  Decision: {decision.intervention_level.name}")
    print(f"  Confidence: {decision.confidence:.0%}")
    print(f"  Action: {decision.suggested_actions[0]}")
EOF
```

### Step 2: Run it
```bash
python3 test_resolver.py
```

**Expected output:**
```
Error: npm: command not found
  Decision: SUGGEST
  Confidence: 70%
  Action: Check spelling of the command

Error: Permission denied
  Decision: SUGGEST
  Confidence: 80%
  Action: Add execute permission: chmod +x <file>

Error: ModuleNotFoundError: No module named 'flask'
  Decision: SUGGEST
  Confidence: 75%
  Action: Install the missing dependency
```

---

## Part 3: Install & Start Monitoring (5 minutes)

Set up autonomous monitoring.

### Step 1: Install shell integration
```bash
terminal-hero monitor --install
```

**Expected output:**
```
Installing Terminal Hero autonomous monitor...
Detected shell: bash
✓ Monitor installed successfully!

To activate, run:
  source ~/.bashrc
```

### Step 2: Reload shell
```bash
source ~/.bashrc
```

### Step 3: Start daemon
```bash
terminal-hero monitor --start
```

**Expected output:**
```
[Terminal Hero] Monitor started
```

### Step 4: Verify it's running
```bash
terminal-hero monitor --status
```

**Expected output:**
```
Monitor Status

Property               Value
──────────────────────────────
Status                 🟢 Active
Auto-fix Enabled       ✓ Yes
```

---

## Part 4: Test Real Error Detection (15 minutes)

Now Terminal Hero should be watching your terminal. Let's trigger some errors.

### Test 1: Command Not Found

```bash
# This should fail
npm --version
```

**Expected Terminal Hero response:**
```
[Terminal Hero] 🔍 Detected: command_not_found (confidence: 70%)
[Terminal Hero] 🤖 Autonomously analyzing...
[Terminal Hero] Root cause: npm not installed or not in PATH
[Terminal Hero] 💡 Solution: Install npm
[Terminal Hero] Description: Node Package Manager not found...
```

### Test 2: Permission Denied

```bash
# Create a script without execute permission
echo "echo hello" > test_script.sh

# Try to run it
./test_script.sh
```

**Expected Terminal Hero response:**
```
[Terminal Hero] 🔍 Detected: permission_denied (confidence: 85%)
[Terminal Hero] Root cause: File not executable
[Terminal Hero] 💡 Suggested: chmod +x test_script.sh
[Terminal Hero] Risk: Low
```

### Test 3: Missing Python Package

```bash
# Try importing a non-existent package
python3 -c "import nonexistent_module"
```

**Expected Terminal Hero response:**
```
[Terminal Hero] 🔍 Detected: missing_dependency (confidence: 80%)
[Terminal Hero] Root cause: Python package not installed
[Terminal Hero] 💡 Solution: pip install nonexistent-module
```

### Test 4: Network Error (Optional)

```bash
# Try reaching unreachable host
ping 192.0.2.1
```

Press Ctrl+C after a few attempts.

**Expected Terminal Hero response:**
```
[Terminal Hero] 🔍 Detected: network_error (confidence: 60%)
[Terminal Hero] 💡 Suggested: Check internet connection
```

---

## Part 5: Watch the Learning System (20 minutes)

See Terminal Hero get smarter with repeated errors.

### Step 1: Trigger the same error multiple times

```bash
# First time
npm start
# -> SUGGEST level

# Second time (same error)
npm start
# -> Confidence increased

# Third time
npm start
# -> Higher confidence

# Fourth time
npm start
# -> AUTO_LOW_RISK - may auto-execute

# Fifth+ time
npm start
# -> FULL_AUTONOMOUS - fixes it automatically
```

### Step 2: Monitor the learning progress

```bash
# Check real-time learning (if available)
tail -f ~/.terminal-hero/logs

# Or check after multiple tests
terminal-hero monitor --status
```

### Step 3: Observe progression

Watch how Terminal Hero:
1. **1st encounter**: 50% confidence, SUGGEST level
2. **2nd encounter**: 65% confidence, SUGGEST level
3. **3rd encounter**: 75% confidence, starts AUTO_LOW_RISK
4. **4th+ encounter**: 90%+ confidence, FULL_AUTONOMOUS

---

## Part 6: Test Different Error Categories (15 minutes)

Terminal Hero recognizes 6 error categories. Test them all:

```bash
#!/bin/bash
# test_all_categories.sh

echo "Testing all error categories..."
echo ""

echo "1. command_not_found:"
npm --version 2>/dev/null || echo "  ✓ Error triggered"
echo ""

echo "2. permission_denied:"
touch test.sh
./test.sh 2>/dev/null || echo "  ✓ Error triggered"
echo ""

echo "3. missing_dependency:"
python3 -c "import nonexistent" 2>/dev/null || echo "  ✓ Error triggered"
echo ""

echo "4. port_already_in_use:"
python3 -c "import socket; s = socket.socket(); s.bind(('127.0.0.1', 22)); s.close()" 2>/dev/null || echo "  ✓ Error triggered"
echo ""

echo "5. disk_space:"
# This won't fail unless disk full, skip for now
echo "  (Only fails when disk is full)"
echo ""

echo "6. network_error:"
python3 -c "import socket; s = socket.socket(); s.connect(('192.0.2.1', 80))" 2>/dev/null || echo "  ✓ Error triggered"
echo ""

echo "All categories tested!"
```

Save and run:
```bash
chmod +x test_all_categories.sh
./test_all_categories.sh
```

---

## Part 7: Check Monitor Statistics (5 minutes)

View what Terminal Hero learned.

```bash
terminal-hero monitor --status
```

**You should see:**
- Monitor is active
- Number of errors detected
- Success rate for each error type
- Most common errors
- Learning level (BEGINNER → INTERMEDIATE → ADVANCED)

---

## Part 8: Stop and Verify (3 minutes)

Stop the monitoring daemon.

```bash
# Stop watching
terminal-hero monitor --stop

# Verify it stopped
terminal-hero monitor --status
```

**Expected output:**
```
Status: 🔴 Inactive
```

---

## Summary Checklist

- [ ] Ran API examples successfully
- [ ] Tested resolver with sample errors
- [ ] Installed shell integration
- [ ] Started monitoring daemon
- [ ] Triggered "command not found" error
- [ ] Triggered "permission denied" error
- [ ] Triggered "missing dependency" error
- [ ] Triggered "network error"
- [ ] Watched learning system improve
- [ ] Checked monitor status
- [ ] Stopped daemon

---

## What You've Tested

✅ **Architecture**
- Multi-agent workflow
- Autonomous resolver
- Terminal monitor

✅ **Functionality**
- Error detection
- Decision making
- Learning system

✅ **Features**
- Real-time monitoring
- Error categorization
- Risk assessment
- Confidence scoring

✅ **Real-world Usage**
- Command execution tracking
- Autonomous intervention
- System learning

---

## Next Steps

1. **Explore the Code**
   ```bash
   # Main components
   cat src/monitor/terminal_monitor.py
   cat src/monitor/autonomous_resolver.py
   ```

2. **Customize Behavior**
   ```bash
   # Edit configuration
   vim ~/.terminal-hero/config.json
   ```

3. **Extend with Custom Patterns**
   ```bash
   # Add your own error types to resolver
   vim src/monitor/autonomous_resolver.py
   ```

4. **Integrate with Your Workflow**
   - Use in your daily terminal work
   - Watch it learn your patterns
   - Contribute improvements

---

## Troubleshooting

### Monitor not detecting errors
```bash
# Verify shell integration installed
grep TERMINAL_HERO ~/.bashrc

# Verify daemon running
terminal-hero monitor --status

# Reinstall if needed
terminal-hero monitor --uninstall
terminal-hero monitor --install
source ~/.bashrc
terminal-hero monitor --start
```

### Errors not showing suggestions
```bash
# Make sure monitor is running
terminal-hero monitor --status

# Check if error matches known patterns
python3 -c "from src.monitor import AutonomousResolver; \
            r = AutonomousResolver(); \
            d = r.analyze_error('your error here', 'command'); \
            print(f'Identified: {d.reason}')"
```

### Want to disable auto-fix temporarily
```bash
terminal-hero monitor --stop
terminal-hero monitor --start --no-auto-fix
```

---

**That's it! You've now tested Terminal Hero's complete autonomous system.** 🎉

---

**Time Estimate**: 90 minutes total for complete walkthrough
**Difficulty**: Beginner (just run commands, watch results)
**Outcome**: Full understanding of how Terminal Hero works
