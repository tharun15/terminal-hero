# Terminal Hero - Autonomous Terminal Monitoring

Terminal Hero can now autonomously watch your terminal commands and fix errors in real-time. This is true agentic behavior - the system proactively monitors your environment and intervenes without explicit user prompts.

## Quick Start

### 1. Install Shell Integration

The first step is to install Terminal Hero into your shell configuration:

```bash
terminal-hero monitor --install
```

This will add a monitoring function to your `~/.bashrc` or `~/.zshrc` that:
- Captures every command you execute
- Monitors exit codes and error output
- Sends errors to Terminal Hero for autonomous analysis

### 2. Start the Monitor Daemon

```bash
terminal-hero monitor --start
```

This starts a background daemon that:
- 🔍 Analyzes errors in real-time
- 💡 Generates solutions autonomously
- 🤖 Can auto-execute low-risk fixes
- 📚 Learns from past interventions

### 3. Watch It Work

Now when you run a command that fails:

```bash
$ docker run --port 8080 my-app
docker: command not found
[Terminal Hero] 🔍 Detected error in command: docker run --port 8080 my-app
[Terminal Hero] Exit code: 127
[Terminal Hero] 🤖 Autonomously analyzing...
[Terminal Hero] Root cause: Docker not installed or not in PATH
[Terminal Hero] 💡 Solution: Install Docker
[Terminal Hero] Description: Docker is not installed. Please install Docker Desktop or Docker Engine.
[Terminal Hero] Auto-fixing would require: apt-get install docker.io
```

## How It Works

### Autonomous Error Detection

When a command fails, Terminal Hero:

1. **Detects the error** - Captures exit code and stderr
2. **Identifies error type** - Maps to known error categories (missing dependency, permission denied, etc.)
3. **Analyzes root cause** - Uses AI to understand what went wrong
4. **Generates solutions** - Creates multiple fix strategies
5. **Decides intervention level** - Based on risk and success history
6. **Takes action** - Auto-executes low-risk fixes or prompts you

### Intervention Levels

Terminal Hero can operate at different automation levels:

- **SUGGEST** (default) - Analyzes and shows you suggestions
- **AUTO_LOW_RISK** - Auto-executes only "chmod", "install package" type fixes
- **AUTO_MEDIUM** - Auto-fixes medium-risk issues like restarting services
- **FULL_AUTONOMOUS** - Executes any fix (use with caution!)

### Learning System

Terminal Hero learns from successes:

- Tracks success rate for each error type
- Remembers the best solution for each error
- Increases confidence over time
- Automatically escalates to higher automation as confidence grows

Example: First time you get a missing dependency, it asks. After 3 successful auto-fixes for the same dependency, it starts auto-executing.

## Commands Reference

### Monitor Installation

```bash
# Install for your current shell
terminal-hero monitor --install

# Remove the monitor
terminal-hero monitor --uninstall
```

### Monitor Control

```bash
# Start monitoring daemon
terminal-hero monitor --start

# Stop the daemon
terminal-hero monitor --stop

# Check status
terminal-hero monitor --status

# Start with auto-fix disabled (suggest only)
terminal-hero monitor --start --no-auto-fix
```

## Configuration

Create `~/.terminal-hero/config.json` to customize behavior:

```json
{
  "intervention_level": "AUTO_LOW_RISK",
  "auto_fix_enabled": true,
  "confidence_threshold": 0.7,
  "risk_tolerance": "medium",
  "max_execution_time": 30,
  "auto_approve_commands": ["apt-get install", "pip install"],
  "auto_block_commands": ["rm -rf"]
}
```

## Safety Features

Terminal Hero includes multiple safety mechanisms:

1. **Risk Assessment** - Every command is assessed for danger level
2. **Confirmation Required** - Medium/high risk changes ask for approval
3. **Dry Run Mode** - Preview changes before executing
4. **Rollback Capability** - Remembers how to undo changes
5. **Command Whitelisting** - Only auto-execute approved command types
6. **Audit Trail** - Full history of all interventions

## Example Scenarios

### Scenario 1: Missing Package

```bash
$ npm install
npm: command not found

[Terminal Hero] Detected npm not installed
[Terminal Hero] Auto-executing: apt-get install npm
[Terminal Hero] ✓ npm installed successfully
$ npm install  # Automatically re-runs the original command
```

### Scenario 2: Permission Issue

```bash
$ ./deploy.sh
bash: ./deploy.sh: Permission denied

[Terminal Hero] Detected permission issue
[Terminal Hero] Suggesting: chmod +x deploy.sh
[Terminal Hero] Execute? (y/n): y
[Terminal Hero] ✓ Fixed! Re-running...
$ ./deploy.sh
Deployment started...
```

### Scenario 3: Port Already in Use

```bash
$ npm start
Error: listen EADDRINUSE: address already in use :::3000

[Terminal Hero] Detected port 3000 in use
[Terminal Hero] Process: node (PID: 1234)
[Terminal Hero] Suggesting: Kill process and retry
[Terminal Hero] Risk level: medium
[Terminal Hero] Auto-fix disabled for medium-risk. Need approval?
```

## Performance Considerations

The monitor runs as a lightweight daemon and only activates on errors:

- Memory overhead: ~20MB
- CPU usage: <1% idle
- Latency added: <100ms per command
- All processing is async and non-blocking

## Troubleshooting

### Monitor not detecting errors

1. Verify installation: `grep TERMINAL_HERO ~/.bashrc`
2. Reload shell: `source ~/.bashrc`
3. Check daemon: `terminal-hero monitor --status`

### Too many false positives

Adjust intervention level:
```bash
terminal-hero monitor --start --no-auto-fix
```

### Monitor is too aggressive

Configure auto-blocking commands in config.json

## Advanced Usage

### Programmatic API

```python
from terminal_hero.monitor import TerminalMonitor, CommandEvent

monitor = TerminalMonitor()

def on_error(event: CommandEvent):
    print(f"Error detected: {event.command}")
    # Custom handling

monitor.register_event_handler(on_error)
monitor.start_daemon()
```

### Metrics and Analytics

View Terminal Hero's learning progress:

```bash
terminal-hero monitor --stats
```

Shows:
- Total interventions
- Error types learned
- Success rates by error type
- Most common errors
- Auto-fix success rate

## Future Enhancements

Planned features:
- [ ] Team mode - Share learned solutions across team
- [ ] Predictive mode - Prevent errors before they happen
- [ ] IDE integration - Works in VS Code terminal
- [ ] GPU acceleration - Faster error analysis
- [ ] Custom patterns - Define your own error types
- [ ] Webhook integration - Alert external systems

---

Terminal Hero makes your terminal smarter. It watches, learns, and fixes problems autonomously.
