# Terminal Hero - Agentic Terminal Monitoring

## What's New: True Autonomous Behavior

Terminal Hero is now a truly agentic system that autonomously monitors your terminal and fixes errors without requiring explicit user prompts. Here's what's been implemented:

## Architecture Overview

```
Terminal Input
      ↓
Shell Integration (captures commands)
      ↓
Command Monitor (watches for errors)
      ↓
Autonomous Resolver (decides intervention level)
      ↓
Terminal Hero Workflow (analyzes & fixes)
      ↓
Autonomous Action (execute, suggest, or learn)
```

## Core Components

### 1. **Terminal Monitor** (`src/monitor/terminal_monitor.py`)
- Watches shell commands in real-time
- Detects errors automatically
- Invokes autonomous fixes without user prompts
- Learns from intervention outcomes
- **Key Class**: `TerminalMonitor`

### 2. **Autonomous Resolver** (`src/monitor/autonomous_resolver.py`)
- Analyzes errors and decides intervention strategy
- Maintains success history for each error type
- Escalates automation as confidence grows
- Handles 6 common error categories:
  - Command not found
  - Permission denied
  - Missing dependencies
  - Port already in use
  - Disk space issues
  - Network errors
- **Key Class**: `AutonomousResolver`

### 3. **CLI Integration** (`src/cli/commands.py`)
- New `monitor` command for installation and control
- Commands:
  - `terminal-hero monitor --install` - Install shell hooks
  - `terminal-hero monitor --start` - Start watching
  - `terminal-hero monitor --stop` - Stop daemon
  - `terminal-hero monitor --status` - Check status
  - `terminal-hero monitor --uninstall` - Remove hooks

## How It Works

### Installation
```bash
$ terminal-hero monitor --install
Installing Terminal Hero autonomous monitor...
Detected shell: bash
✓ Monitor installed successfully!

To activate, run:
  source ~/.bashrc
```

### Running
```bash
$ terminal-hero monitor --start
[Terminal Hero] Monitor started
```

### In Action
```bash
$ docker run my-app
docker: command not found

[Terminal Hero] 🔍 Detected command_not_found error (confidence: 60%)
[Terminal Hero] 🤖 Autonomously analyzing...
[Terminal Hero] Root cause: Docker not installed or not in PATH
[Terminal Hero] 💡 Solution: Install Docker
[Terminal Hero] Description: Docker is not installed. Please install Docker Desktop or Docker Engine.
```

## Autonomous Decision Making

### Intervention Levels

The system operates at 5 automation levels:

1. **SILENT** - Just logs, no intervention
2. **SUGGEST** (default) - Shows suggestions, waits for user
3. **AUTO_LOW_RISK** - Auto-executes low-risk fixes
4. **AUTO_MEDIUM** - Auto-executes medium-risk fixes  
5. **FULL_AUTONOMOUS** - Executes any fix

### How It Decides

For each error, the resolver:

1. **Identifies error type** - Matches against known patterns
2. **Checks success history** - Has this fix worked before?
3. **Calculates confidence** - How sure are we about the fix?
4. **Selects intervention level** - Based on risk × confidence
5. **Takes action** - Auto-execute, suggest, or learn

Example:
- First time seeing missing dependency → SUGGEST level
- After 3 successes → AUTO_LOW_RISK level
- After 10 successes → AUTO_MEDIUM level

## Learning System

The `AutonomousResolver` learns from every intervention:

- **Success Tracking**: Records which fixes work for which errors
- **Confidence Growth**: Increases automation as success rate grows
- **Pattern Memory**: Remembers best solutions for each error type
- **Adaptive Behavior**: Becomes more autonomous over time

```python
# The resolver learns:
resolver.record_outcome(
    error_type="missing_dependency",
    success=True,
    solution=solution_strategy
)

# Success rates improve:
resolver.success_patterns["missing_dependency"] = 0.95
```

## File Structure

```
src/monitor/
├── __init__.py                  # Module exports
├── terminal_monitor.py          # Main monitoring engine (305 lines)
├── autonomous_resolver.py       # Decision making AI (350 lines)
└── command_event.py            # Event data structures

src/cli/
└── commands.py                 # Updated with monitor command

AUTONOMOUS_MONITORING.md        # Full user guide
```

## Key Features

✅ **Real-time Monitoring** - Watches every command as you type
✅ **Autonomous Intervention** - Fixes errors without asking
✅ **Learning System** - Gets smarter with each fix
✅ **Risk Assessment** - Won't auto-execute dangerous commands
✅ **Safe Execution** - Rolls back if something goes wrong
✅ **Command Whitelist** - Approve which commands auto-execute
✅ **Audit Trail** - Full history of all interventions
✅ **Non-intrusive** - Minimal overhead, only acts on errors

## Usage Examples

### Example 1: Missing Command
```bash
$ npm start
npm: command not found

[Terminal Hero] Detected command_not_found (60% confidence)
[Terminal Hero] Analyzing...
[Terminal Hero] Root cause: npm not installed
[Terminal Hero] Suggested: apt-get install npm
[Terminal Hero] Execute? y/n: y
[Terminal Hero] ✓ npm installed
[Terminal Hero] Re-running: npm start
```

### Example 2: Permission Issue
```bash
$ ./deploy.sh
bash: ./deploy.sh: Permission denied

[Terminal Hero] Detected permission_denied (80% confidence)
[Terminal Hero] Analyzing...
[Terminal Hero] Root cause: File not executable
[Terminal Hero] Auto-fix: chmod +x deploy.sh
[Terminal Hero] ✓ Fixed! Re-executing...
./deploy.sh
Deployment started...
```

### Example 3: Learning in Action
```bash
# First time with this error:
$ pip install requirements.txt
ERROR: Directory not a package

[Terminal Hero] Confidence: 50%
[Terminal Hero] Suggested: pip install -r requirements.txt

# After fixing once:
$ pip install requirements.txt
ERROR: Directory not a package

[Terminal Hero] Confidence: 75%
[Terminal Hero] Suggested: pip install -r requirements.txt

# After fixing 5 times:
$ pip install requirements.txt
ERROR: Directory not a package

[Terminal Hero] Confidence: 95%
[Terminal Hero] Auto-executing: pip install -r requirements.txt
```

## Advanced Configuration

Create `~/.terminal-hero/config.json`:

```json
{
  "intervention_level": "AUTO_LOW_RISK",
  "auto_fix_enabled": true,
  "confidence_threshold": 0.7,
  "risk_tolerance": "medium",
  "max_execution_time": 30,
  "auto_approve_commands": [
    "apt-get install",
    "pip install",
    "npm install"
  ],
  "auto_block_commands": [
    "rm -rf",
    "sudo",
    "shutdown"
  ]
}
```

## Next Steps

To make Terminal Hero even more agentic:

1. **Predictive Mode** - Predict errors before they happen based on commands
2. **Team Learning** - Share learned solutions across team members
3. **Custom Patterns** - Define your own error recognition patterns
4. **IDE Integration** - Works in VS Code, PyCharm terminals
5. **Webhook Support** - Alert other systems when errors occur
6. **GPU Acceleration** - Faster analysis with local LLM

## Starting the Autonomous Monitor

Quick start:
```bash
# Install once
terminal-hero monitor --install

# Reload your shell
source ~/.bashrc

# Start monitoring
terminal-hero monitor --start

# Watch Terminal Hero fix your errors!
```

---

Terminal Hero is now **truly agentic** - it watches your terminal autonomously, detects errors in real-time, and fixes them without you asking. The more you use it, the smarter it gets.
