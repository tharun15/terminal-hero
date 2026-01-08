# 🤖 Terminal Hero

> AI-Powered Terminal Troubleshooting Agent with Sophisticated Multi-Agent Architecture

Terminal Hero is a production-grade CLI tool that uses a multi-agent AI system to diagnose and fix terminal errors instantly. Built with OpenAI's GPT-4 and LangGraph for advanced agent orchestration.

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Agent System**: 6 specialized agents working in concert
  - Orchestrator: Workflow coordination
  - Context Collector: System and project analysis
  - Error Analyzer: Root cause determination with causality graphs
  - Documentation Search: Web and docs search
  - Solution Architect: Multiple strategy generation
  - Executor: Safe command execution

- **Intelligent Analysis**
  - Pattern matching for 50+ common errors
  - Causality chain visualization
  - Confidence scoring for solutions
  - Context-aware recommendations

- **Beautiful CLI Interface**
  - Real-time agent activity dashboard
  - Interactive solution comparison
  - Syntax-highlighted command previews
  - Rich terminal UI with colors and formatting

- **Safety & Learning**
  - Command validation and safety checks
  - Undo/rollback functionality
  - Execution history tracking
  - Learning system that improves over time

### 🎨 WOW Factors

1. **Visual Agent Dashboard** - Watch agents collaborate in real-time
2. **Causality Graphs** - See how one issue led to another
3. **Solution Comparison** - Multiple strategies with risk assessment
4. **Smart Context Detection** - Understands your project type and environment
5. **Undo System** - Rollback any changes safely
6. **Memory System** - Learns from past solutions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/terminal-hero.git
cd terminal-hero

# Install dependencies
pip install -e .

# Or using Poetry
poetry install
```

### Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```
OPENAI_API_KEY=your_key_here
```

### Usage

#### Diagnose an error
```bash
terminal-hero diagnose

# Or provide error directly
terminal-hero diagnose "bash: python: command not found"
```

#### System health check
```bash
terminal-hero doctor
```

#### View history
```bash
terminal-hero history
```

#### Undo last execution
```bash
terminal-hero undo
```

## 🏗️ Architecture

### Multi-Agent Workflow

```
User Input
    ↓
Orchestrator Agent (Coordinates workflow)
    ↓
Context Collector Agent (Analyzes system & project)
    ↓
Error Analyzer Agent (Builds causality graph)
    ↓
Documentation Search Agent (Finds solutions online)
    ↓
Solution Architect Agent (Generates strategies)
    ↓
Executor Agent (Validates & executes safely)
```

### Technology Stack

- **Agent Framework**: LangGraph for sophisticated agent orchestration
- **LLM**: OpenAI GPT-4 Turbo for intelligent reasoning
- **CLI**: Typer for command-line interface
- **UI**: Rich for beautiful terminal output
- **Search**: DuckDuckGo for free documentation search
- **Storage**: SQLite for learning and history
- **Validation**: Pydantic v2 for type safety

## 📁 Project Structure

```
terminal-hero/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── base.py
│   │   ├── orchestrator.py
│   │   ├── context_collector.py
│   │   ├── error_analyzer.py
│   │   ├── doc_search.py
│   │   ├── solution_architect.py
│   │   └── executor.py
│   ├── graph/               # LangGraph workflow
│   │   ├── workflow.py
│   │   └── state.py
│   ├── cli/                 # CLI interface
│   │   ├── main.py
│   │   ├── commands.py
│   │   └── ui.py
│   ├── core/                # Core utilities
│   │   ├── system_detector.py
│   │   └── error_patterns.py
│   ├── storage/             # Storage systems
│   │   ├── memory.py
│   │   └── history.py
│   └── main.py
├── tests/
├── docs/
├── pyproject.toml
├── setup.py
├── README.md
└── .env.example
```

## 🎯 Use Cases

### For Students
- Quickly fix installation errors when learning to code
- Understand why errors occur (educational mode)
- Get step-by-step guidance

### For Developers
- Rapid troubleshooting during development
- Context-aware solutions for project-specific issues
- Save time on Stack Overflow searches

### For DevOps
- System diagnostics and health checks
- Package manager issues
- Environment configuration problems

## 🔒 Safety Features

- **Command Validation**: Blocks dangerous commands (rm -rf /, etc.)
- **Dry-run Mode**: Preview changes before execution
- **Rollback System**: Undo any changes
- **Execution History**: Track all modifications
- **User Confirmation**: Always asks before executing

## 📊 Demo Scenarios

The tool excels at handling:

1. **Missing Commands**: "command not found" errors
2. **Permission Issues**: "permission denied" errors
3. **Dependency Problems**: Missing packages or modules
4. **Configuration Errors**: PATH, environment variables
5. **Network Issues**: Connection failures, timeouts
6. **Version Conflicts**: Incompatible package versions

## 🚧 Future Enhancements

- [ ] Docker container support
- [ ] Shell integration (automatic error detection)
- [ ] Plugin system for custom agents
- [ ] Web dashboard for visualization
- [ ] Team collaboration features
- [ ] Cloud-based learning system

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [OpenAI](https://openai.com)
- UI by [Rich](https://github.com/Textualize/rich)

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/terminal-hero](https://github.com/yourusername/terminal-hero)

---

Made with ❤️ for developers who deserve better error messages
"""

# ============================================================================
# FILE: CONTRIBUTING.md
# ============================================================================

"""
# Contributing to Terminal Hero

Thank you for your interest in contributing! Here's how you can help:

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/terminal-hero.git`
3. Install dependencies: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature`

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Run `ruff` for linting
- Run `mypy` for type checking

## Testing

```bash
pytest tests/
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Agent Development

When adding new agents:

1. Inherit from `BaseAgent`
2. Implement `process(state) -> state`
3. Add logging with `log_activity()`
4. Update workflow in `graph/workflow.py`
5. Document agent purpose and behavior

## Questions?

Open an issue or reach out to maintainers.