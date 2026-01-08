# Terminal Hero - Component Overview

## System Modules

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          TERMINAL HERO SYSTEM                            │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ MONITORING LAYER (src/monitor/)                                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐      ┌──────────────────────────────────┐  │
│  │   TerminalMonitor        │      │   AutonomousResolver             │  │
│  ├──────────────────────────┤      ├──────────────────────────────────┤  │
│  │ • Watches shell commands │      │ • Identifies error types         │  │
│  │ • Captures stderr/stdout │      │ • Calculates confidence          │  │
│  │ • Detects errors         │      │ • Selects intervention level     │  │
│  │ • Runs daemon            │      │ • Tracks success patterns        │  │
│  │ • Installs/uninstalls    │      │ • Makes decisions                │  │
│  │ • Event handling         │      │ • Learns from outcomes           │  │
│  │ • Shell integration      │      │ • Provides suggestions           │  │
│  └──────────────────────────┘      └──────────────────────────────────┘  │
│           │                                        │                      │
│           │ CommandEvent                          │ InterventionDecision │
│           └────────────────────────┬───────────────┘                      │
│                                    │                                      │
│                        Processes error autonomously                       │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ WORKFLOW ENGINE (src/graph/ & src/agents/)                               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │  Context         │  │  Error           │  │  Doc Search      │       │
│  │  Collector       │  │  Analyzer        │  │  Agent           │       │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤       │
│  │ • System info    │  │ • Root cause     │  │ • Search web     │       │
│  │ • Environment    │  │ • Error category │  │ • Find examples  │       │
│  │ • Shell state    │  │ • Severity       │  │ • Gather docs    │       │
│  │ • Installed      │  │ • Confidence     │  │                  │       │
│  │   packages       │  │ • Chain analysis │  │                  │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
│           │                     │                     │                    │
│           └─────────────────────┼─────────────────────┘                   │
│                                 │                                         │
│                         ┌───────▼────────┐                               │
│                         │ Orchestrator   │                               │
│                         ├────────────────┤                               │
│                         │ • Coordinates  │                               │
│                         │ • Makes final  │                               │
│                         │   decisions    │                               │
│                         │ • Selects      │                               │
│                         │   strategy     │                               │
│                         └───────┬────────┘                               │
│                                 │                                         │
│                         ┌───────▼────────┐                               │
│                         │ Solution       │                               │
│                         │ Architect      │                               │
│                         ├────────────────┤                               │
│                         │ • Generates    │                               │
│                         │   solutions    │                               │
│                         │ • Ranks fixes  │                               │
│                         │ • Provides     │                               │
│                         │   rollbacks    │                               │
│                         └───────┬────────┘                               │
│                                 │                                         │
│                         ┌───────▼────────┐                               │
│                         │ Executor       │                               │
│                         ├────────────────┤                               │
│                         │ • Executes     │                               │
│                         │   commands     │                               │
│                         │ • Captures     │                               │
│                         │   output       │                               │
│                         │ • Verifies     │                               │
│                         │   success      │                               │
│                         └────────────────┘                               │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ STORAGE LAYER (src/storage/)                                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────┐         ┌──────────────────────────┐           │
│  │   Command History    │         │   Memory System          │           │
│  ├──────────────────────┤         ├──────────────────────────┤           │
│  │ • All executed cmds  │         │ • Success patterns       │           │
│  │ • Exit codes         │         │ • Error categorization   │           │
│  │ • Output captured    │         │ • Solution effectiveness │           │
│  │ • Timestamp          │         │ • Confidence scores      │           │
│  │ • Queryable          │         │ • Learned solutions      │           │
│  └──────────────────────┘         └──────────────────────────┘           │
│           │                               │                               │
│           └───────────────┬───────────────┘                               │
│                           │                                               │
│                  Provides feedback loop                                   │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ SHELL INTEGRATION (Bash/Zsh)                                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  ~/.bashrc / ~/.zshrc                                              │  │
│  │                                                                      │  │
│  │  export TERMINAL_HERO_ENABLED=1                                    │  │
│  │  export TERMINAL_HERO_LOG=/tmp/terminal_hero/commands.log          │  │
│  │                                                                      │  │
│  │  __terminal_hero_preexec() {                                       │  │
│  │      __TERMINAL_HERO_COMMAND="${@}"                               │  │
│  │      __TERMINAL_HERO_START_TIME=$(date +%s%N)                      │  │
│  │  }                                                                   │  │
│  │                                                                      │  │
│  │  __terminal_hero_postexec() {                                      │  │
│  │      # Capture exit code and duration                             │  │
│  │      # Log to command file                                        │  │
│  │      # Trigger monitor if error                                   │  │
│  │  }                                                                   │  │
│  │                                                                      │  │
│  │  trap '__terminal_hero_preexec' DEBUG  # For bash                 │  │
│  │  preexec_functions+=( __terminal_hero_preexec )  # For zsh       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ CLI INTERFACE (src/cli/commands.py)                                        │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Commands:                                                                 │
│  ├─ diagnose    [ERROR]     → Diagnose error interactively               │
│  ├─ doctor                  → System health check                         │
│  ├─ undo                    → Undo last command                           │
│  ├─ history     [--count N] → Show command history                       │
│  └─ monitor [OPTIONS]       → Autonomous monitoring                       │
│     ├─ --install            → Install shell integration                   │
│     ├─ --uninstall          → Remove shell integration                    │
│     ├─ --start              → Start monitoring daemon                     │
│     ├─ --stop               → Stop monitoring daemon                      │
│     ├─ --status             → Check monitor status                        │
│     └─ --auto-fix / --no-auto-fix → Control behavior                      │
│                                                                             │
└───────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│  User Types │
│   Command   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Shell Execute   │
└──────┬───────────┘
       │ (via trap/preexec)
       ▼
┌──────────────────────────────────┐
│  Shell Hook Captures:            │
│  - Command text                  │
│  - Exit code                     │
│  - Start/end time                │
│  - Stdout/stderr                 │
└──────┬───────────────────────────┘
       │
       ├─ SUCCESS? ──→ Log & Continue
       │
       └─ ERROR? ──→ Log to CommandEvent
                      │
                      ▼
              ┌────────────────────┐
              │ Monitor Daemon     │
              │ (polling loop)     │
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────────────┐
              │ AutonomousResolver         │
              │ analyze_error()            │
              │                            │
              │ Returns:                   │
              │ - Error Type               │
              │ - Confidence Score         │
              │ - Intervention Level       │
              │ - Suggested Actions        │
              └────────┬───────────────────┘
                       │
           ┌───────────┼───────────┐
           │           │           │
           ▼           ▼           ▼
       SILENT       SUGGEST      AUTO
        │             │           │
        │             │           ▼
        │             │      [Execute]
        │             │           │
        │             ▼           │
        │         [Show User]     │
        │             │           │
        └─────────────┼───────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ Terminal Hero Workflow     │
         │ (if detailed analysis      │
         │  needed or requested)      │
         │                            │
         │ 1. ContextCollector        │
         │ 2. ErrorAnalyzer           │
         │ 3. DocSearch               │
         │ 4. SolutionArchitect       │
         │ 5. Executor                │
         │ 6. Orchestrator            │
         └────────┬───────────────────┘
                  │
                  ▼
         ┌────────────────────────────┐
         │ Record Outcome             │
         │ - Success/failure          │
         │ - Time taken               │
         │ - Solution used            │
         │ - Error type               │
         └────────┬───────────────────┘
                  │
                  ▼
         ┌────────────────────────────┐
         │ Update Learning System     │
         │ - Success rates            │
         │ - Confidence scores        │
         │ - Learned patterns         │
         │ - Future decisions         │
         └────────────────────────────┘
```

## Intervention Decision Tree

```
Error Detected
    │
    ├─► Classification
    │   └─► Error Type & Severity
    │
    ├─► Historical Analysis
    │   ├─ First time? → 50% confidence
    │   ├─ Seen 2-3x? → 65% confidence
    │   ├─ Seen 5-10x? → 85% confidence
    │   └─ Seen 10+x? → 95% confidence
    │
    ├─► Risk Assessment
    │   ├─ Low risk (chmod, apt-get)
    │   ├─ Medium risk (restart service)
    │   └─ High risk (system config, rm -rf)
    │
    └─► Decision Selection
        │
        ├─ Low confidence (< 60%)
        │  └─ Action: SUGGEST
        │
        ├─ Medium confidence (60-80%) + Low Risk
        │  └─ Action: SUGGEST (escalate to AUTO on repeat)
        │
        ├─ High confidence (80-90%) + Low Risk
        │  └─ Action: AUTO_LOW_RISK
        │
        ├─ High confidence (90%+) + Medium Risk
        │  └─ Action: AUTO_MEDIUM (with notification)
        │
        └─ Very high confidence (95%+) + Any Risk
           └─ Action: FULL_AUTONOMOUS
```

## Learning Feedback Loop

```
                ┌──────────────────┐
                │   New Error      │
                │   Encountered    │
                └────────┬─────────┘
                         │
                ┌────────▼──────────┐
                │  Resolver        │
                │  Analyzes Error  │
                │  Decision Made   │
                └────────┬─────────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
    AUTO-EXECUTE    SUGGEST TO      JUST LOG
           │         USER             │
           │             │             │
           ▼             ▼             ▼
    ┌────────────┐ ┌──────────┐ ┌──────────┐
    │  Execute   │ │  Ask for │ │  Record  │
    │  Command   │ │Approval  │ │   Only   │
    └──────┬─────┘ └─────┬────┘ └──────┬───┘
           │             │             │
           │        USER DECIDES       │
           │        YES / NO           │
           │             │             │
           │      ┌──────▼─────┐      │
           │      │  Execute   │      │
           │      └──────┬─────┘      │
           │             │             │
           └─────────────┼─────────────┘
                         │
                ┌────────▼──────────────┐
                │ Record Outcome:       │
                │ - Success or Failure  │
                │ - Time Taken          │
                │ - Error Type          │
                │ - Solution Used       │
                └────────┬──────────────┘
                         │
                ┌────────▼──────────────────┐
                │ Update Success Patterns:  │
                │ error_type => success%    │
                │ confidence = 70% → 75%    │
                └────────┬──────────────────┘
                         │
                ┌────────▼──────────────────┐
                │ Next Time Same Error:     │
                │ Uses updated confidence   │
                │ & success history         │
                │ → Better decision!        │
                └──────────────────────────┘
```

## Memory/State Structures

```
CommandEvent {
  - timestamp: ISO datetime
  - command: str
  - exit_code: int
  - stdout: str
  - stderr: str
  - duration: float
  - success: bool
}

InterventionDecision {
  - should_intervene: bool
  - intervention_level: Enum
  - confidence: float (0-1)
  - reason: str
  - suggested_actions: List[str]
}

AgentState {
  - user_input: str
  - raw_error: str
  - system_info: SystemInfo
  - error_analysis: ErrorAnalysis
  - documentation_results: List[DocumentationResult]
  - solution_strategies: List[SolutionStrategy]
  - execution_result: ExecutionResult
  - agent_activity: List[Dict]
  - current_step: str
  - requires_user_input: bool
  - error_occurred: bool
}
```

---

This is the complete agentic system. Every component works together to create autonomous error detection and resolution.
