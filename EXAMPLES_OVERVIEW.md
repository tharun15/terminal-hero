# Testing & Examples - Overview

Complete guide to testing Terminal Hero's autonomous monitoring system.

## 📂 Files in `examples/` Directory

### 1. **test_simple.py** - Programmatic API Tests
Three test modes:
- `python3 examples/test_simple.py resolver` - Test error analysis
- `python3 examples/test_simple.py monitor` - Test event system  
- `python3 examples/test_simple.py learning` - Test learning system

### 2. **api_examples.py** - Complete Component Examples
Five detailed examples:
- `python3 examples/api_examples.py 1` - Basic monitoring setup
- `python3 examples/api_examples.py 2` - Resolver decision making
- `python3 examples/api_examples.py 3` - Learning system progression
- `python3 examples/api_examples.py 4` - Error categorization
- `python3 examples/api_examples.py 5` - Risk assessment
- `python3 examples/api_examples.py` - Run all at once

### 3. **practical_tests.sh** - Real Terminal Tests
Interactive guide to test with actual failing commands:
```bash
bash examples/practical_tests.sh
```

---

## 📖 Documentation Files

### 1. **SIMPLE_EXAMPLES.md** ⭐ START HERE
Quick examples (5 min read):
- 30-second quick test
- Simple code examples
- Real terminal tests
- Key components overview

### 2. **EXAMPLES.md**
Comprehensive examples (20 min read):
- API examples with code
- Real terminal testing
- Component testing
- Performance testing
- Troubleshooting

### 3. **TESTING_WALKTHROUGH.md**
Step-by-step guide (90 min total):
- Part 1: Run API examples (5 min)
- Part 2: Test resolver (10 min)
- Part 3: Install & start (5 min)
- Part 4: Real error detection (15 min)
- Part 5: Learning system (20 min)
- Part 6: Error categories (15 min)
- Part 7: Monitor stats (5 min)
- Part 8: Cleanup (3 min)

---

## 🎯 Quick Start Paths

### Path 1: "I Want to Code" (15 min)
1. Read: `SIMPLE_EXAMPLES.md`
2. Run: `python3 examples/api_examples.py`
3. Code: Check the examples and modify

### Path 2: "I Want to Test Real Errors" (30 min)
1. Read: `SIMPLE_EXAMPLES.md`
2. Run: `terminal-hero monitor --install && source ~/.bashrc`
3. Run: `terminal-hero monitor --start`
4. Execute: The failing commands from `SIMPLE_EXAMPLES.md`
5. Observe: Terminal Hero's responses

### Path 3: "I Want Everything" (90 min)
1. Read: `TESTING_WALKTHROUGH.md`
2. Follow: All 8 parts step-by-step
3. Execute: Every code example
4. Test: Every scenario
5. Verify: All components work

---

## 🚀 Fastest Testing

**Absolute minimum to see it work:**

```bash
# 1. Run API example (shows it works)
python3 examples/api_examples.py

# 2. Install monitor (30 seconds)
terminal-hero monitor --install && source ~/.bashrc

# 3. Start daemon (5 seconds)
terminal-hero monitor --start

# 4. Trigger an error (5 seconds)
npm --version

# 5. Done! Watch Terminal Hero respond
```

**Total time: ~2 minutes**

---

## 📋 Example Categories

### Programmatic Examples
Files:
- `examples/test_simple.py`
- `examples/api_examples.py`

What they test:
- Resolver component
- Monitor component
- Learning system
- Error categorization
- Risk assessment

### Real Terminal Examples
Files:
- `examples/practical_tests.sh`
- From SIMPLE_EXAMPLES.md
- From EXAMPLES.md

What they test:
- Real command execution
- Actual error detection
- Shell integration
- Daemon behavior
- Learning progression

### Walkthrough Examples
Files:
- `TESTING_WALKTHROUGH.md`

What it covers:
- Complete end-to-end setup
- 8 detailed test parts
- Expected outputs
- Troubleshooting

---

## 📊 Error Types to Test

Terminal Hero recognizes and handles:

1. **command_not_found**
   ```bash
   npm --version
   ```

2. **permission_denied**
   ```bash
   echo "hi" > script.sh && ./script.sh
   ```

3. **missing_dependency**
   ```bash
   python3 -c "import nonexistent"
   ```

4. **port_already_in_use**
   ```bash
   python3 -c "import socket; s = socket.socket(); s.bind(('127.0.0.1', 8080))"
   ```

5. **disk_space**
   (Requires full disk, skip in testing)

6. **network_error**
   ```bash
   ping 192.0.2.1
   ```

---

## ✅ Verification Checklist

- [ ] Can run `python3 examples/api_examples.py`
- [ ] Can run `python3 examples/test_simple.py`
- [ ] Can run `terminal-hero monitor --install`
- [ ] Can run `terminal-hero monitor --start`
- [ ] Can run failing commands and see responses
- [ ] Can check `terminal-hero monitor --status`
- [ ] Can run `terminal-hero monitor --stop`

All checks pass = Everything works! ✨

---

## 🎓 Learning Path

**Beginner:**
1. Read: SIMPLE_EXAMPLES.md
2. Run: `python3 examples/api_examples.py`
3. Understand: How components work

**Intermediate:**
1. Read: EXAMPLES.md
2. Run: All examples
3. Test: Real errors
4. Understand: Full system

**Advanced:**
1. Read: TESTING_WALKTHROUGH.md
2. Run: Step-by-step tests
3. Observe: Learning progression
4. Master: All components

**Expert:**
1. Review: Source code
2. Modify: Examples
3. Extend: Add custom patterns
4. Contribute: Improvements

---

## 🔍 What Each Example Shows

### api_examples.py - Example 1
**Shows**: Basic monitoring setup
**Demonstrates**: Event registration and emission
**Key Insight**: How monitor handles command events

### api_examples.py - Example 2
**Shows**: Resolver decision making
**Demonstrates**: Error analysis and action selection
**Key Insight**: How resolver categorizes errors

### api_examples.py - Example 3
**Shows**: Learning system in action
**Demonstrates**: Confidence progression
**Key Insight**: How system gets smarter over time

### api_examples.py - Example 4
**Shows**: Error categorization
**Demonstrates**: All 6 error types
**Key Insight**: How errors are identified

### api_examples.py - Example 5
**Shows**: Risk-based execution
**Demonstrates**: Risk level impact
**Key Insight**: How safety is maintained

---

## 💾 Files Created for Testing

- `examples/test_simple.py` - Simple component tests
- `examples/api_examples.py` - Five detailed examples
- `examples/practical_tests.sh` - Real terminal tests
- `SIMPLE_EXAMPLES.md` - Quick reference
- `EXAMPLES.md` - Comprehensive guide
- `TESTING_WALKTHROUGH.md` - Step-by-step walkthrough
- `EXAMPLES_OVERVIEW.md` - This file

---

## 🎉 Expected Results

### When you run examples:
✅ System identifies error types correctly
✅ Confidence scores are calculated
✅ Intervention levels are chosen
✅ Learning progression is shown
✅ Risk assessment works

### When you test real errors:
✅ Errors are detected automatically
✅ Suggestions appear
✅ System learns from outcomes
✅ Confidence increases
✅ Automation escalates

### When you monitor stats:
✅ Total errors tracked
✅ Success rates shown
✅ Learning level displayed
✅ Most common errors listed

---

## 🚨 Troubleshooting Examples

### Python import errors?
```bash
# Make sure you're in project root
cd ~/projects/terminal-hero

# Verify imports work
python3 -c "from src.monitor import TerminalMonitor; print('✓')"
```

### Monitor not installing?
```bash
# Check shell config
grep TERMINAL_HERO ~/.bashrc

# Manual install
pip install -e .
terminal-hero monitor --install
```

### Examples not running?
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Check dependencies
pip list | grep -E "langchain|openai|pydantic"

# Run simpler example
python3 examples/test_simple.py resolver
```

---

## 📝 Next Steps

1. **Read** `SIMPLE_EXAMPLES.md` (5 min)
2. **Run** `python3 examples/api_examples.py` (5 min)
3. **Install** `terminal-hero monitor --install` (1 min)
4. **Test** real errors (10 min)
5. **Explore** `TESTING_WALKTHROUGH.md` (optional)

---

**All examples are self-contained and can run independently.**

Start with whichever you prefer: 
- API examples for understanding components
- Real tests for hands-on experience
- Walkthrough for complete guidance

**Enjoy testing Terminal Hero!** 🚀
