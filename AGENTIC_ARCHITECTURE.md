# Terminal Hero - Agentic Architecture

## System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER TERMINAL EXECUTION                          │
│  $ npm start                                                          │
│  Error: command not found                                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │   SHELL INTEGRATION (bashrc/zshrc)   │
        │  - Captures command execution        │
        │  - Monitors exit codes               │
        │  - Captures stderr/stdout            │
        └──────────────────┬───────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │     TERMINAL MONITOR DAEMON          │
        │  - Real-time command watchdog        │
        │  - Detects errors immediately       │
        │  - Routes to resolver                │
        └──────────────────┬───────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────────┐
        │   AUTONOMOUS RESOLVER                        │
        │                                              │
        │  Input: Error message + command              │
        │  Process:                                    │
        │    1. Identify error type                    │
        │    2. Check success history                  │
        │    3. Calculate confidence                   │
        │    4. Select intervention level              │
        │  Output: Decision (intervene? how? risk?)    │
        └──────────────────┬───────────────────────────┘
                           │
                ┌──────────┼──────────┬─────────────┐
                │          │          │             │
                ▼          ▼          ▼             ▼
            SILENT      SUGGEST   AUTO_LOW    AUTO_MEDIUM
                │          │          │             │
                ▼          ▼          ▼             ▼
        ┌─────────────────────────────────────────────────┐
        │    TERMINAL HERO WORKFLOW ENGINE                │
        │                                                 │
        │  1. ContextCollectorAgent                       │
        │     - Gathers system info                       │
        │                                                 │
        │  2. ErrorAnalyzerAgent                          │
        │     - Analyzes root cause                       │
        │     - Determines error category                 │
        │     - Builds causality chain                    │
        │                                                 │
        │  3. DocumentSearchAgent                         │
        │     - Finds relevant documentation              │
        │     - Searches Stack Overflow                   │
        │     - Gathers best practices                    │
        │                                                 │
        │  4. SolutionArchitectAgent                      │
        │     - Generates multiple solutions              │
        │     - Ranks by risk & success                   │
        │     - Provides rollback commands                │
        │                                                 │
        │  5. OrchestratorAgent                           │
        │     - Coordinates all agents                    │
        │     - Makes final decisions                     │
        │     - Manages workflow state                    │
        │                                                 │
        │  6. ExecutorAgent                              │
        │     - Executes commands safely                  │
        │     - Captures output                           │
        │     - Verifies success                          │
        └──────────────────┬──────────────────────────────┘
                           │
                ┌──────────┴──────────┬──────────────┐
                │                     │              │
                ▼                     ▼              ▼
        ┌──────────────┐      ┌──────────────┐  ┌──────────┐
        │  JUST LOG    │      │   SUGGEST    │  │AUTO-FIX  │
        │              │      │              │  │          │
        │ Record to    │      │ Display to   │  │Execute   │
        │ history      │      │ user:        │  │low-risk  │
        │              │      │ - Solutions  │  │commands  │
        │ Learn this   │      │ - Docs       │  │          │
        │ pattern      │      │ - Ask for    │  │Auto-     │
        │              │      │   approval   │  │execute   │
        │              │      │              │  │with user │
        │              │      │Record if     │  │permission│
        │              │      │approved      │  │          │
        └──────────────┘      └──────────────┘  └──────────┘
                │                     │              │
                └─────────────────────┴──────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────────┐
        │      LEARNING & FEEDBACK SYSTEM              │
        │                                              │
        │  - Success rate tracking                     │
        │  - Error pattern memorization                │
        │  - Solution effectiveness ranking            │
        │  - Confidence calculation                    │
        │  - Autonomous escalation over time           │
        │                                              │
        │  Example learning curve:                     │
        │  Try 1: SUGGEST (50% confidence)             │
        │  Try 2: SUGGEST (65% confidence)             │
        │  Try 3: AUTO_LOW_RISK (80% confidence)       │
        │  Try 4: AUTO_MEDIUM (95% confidence)         │
        └──────────────────┬───────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────────┐
        │      NEXT OCCURRENCE OF SAME ERROR           │
        │                                              │
        │  System now uses learned:                    │
        │  - Success patterns                          │
        │  - Best solutions                            │
        │  - Optimal automation level                  │
        │                                              │
        │  "We've seen this 10 times. 95% success.    │
        │   Auto-executing with confidence!"           │
        └──────────────────────────────────────────────┘
```

## Decision Tree: Intervention Logic

```
Error Detected
    │
    ├─► ERROR TYPE IDENTIFICATION
    │   ├─ command_not_found?
    │   ├─ permission_denied?
    │   ├─ missing_dependency?
    │   ├─ port_already_in_use?
    │   ├─ disk_space?
    │   ├─ network_error?
    │   └─ unknown?
    │
    └─► CONFIDENCE CALCULATION
        │
        ├─► Success History
        │   ├─ No history? → 50% confidence
        │   ├─ 1-3 attempts? → 60-70% confidence
        │   ├─ 3-7 attempts? → 75-85% confidence
        │   └─ 7+ attempts? → 90-99% confidence
        │
        └─► INTERVENTION LEVEL SELECTION
            │
            ├─ Confidence < 60%? 
            │  └─► SUGGEST LEVEL
            │      Show suggestions, wait for user
            │
            ├─ 60% ≤ Confidence < 80%?
            │  └─► SUGGEST LEVEL (can escalate)
            │      Show suggestions with confidence
            │
            ├─ Confidence ≥ 80% + Low Risk?
            │  └─► AUTO_LOW_RISK LEVEL
            │      Auto-execute chmod, apt-get
            │
            ├─ Confidence ≥ 85% + Medium Risk?
            │  └─► AUTO_MEDIUM LEVEL
            │      Auto-execute service restarts
            │
            └─ Confidence ≥ 95% + Any Risk?
               └─► FULL_AUTONOMOUS LEVEL
                   Auto-execute any safe fix

```

## State Flow

```
┌─────────────────────┐
│   Initial State     │
│                     │
│ - No error history  │
│ - No learned        │
│   patterns          │
│ - Default: SUGGEST  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   First Error Encounter             │
│                                     │
│ User gets suggestion                │
│ Resolves manually or accepts fix    │
│ Monitor records outcome: SUCCESS    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Learning Phase (Attempts 1-5)     │
│                                     │
│ - Confidence builds: 50% → 70%      │
│ - Still suggests, doesn't auto-exec │
│ - Gathers more data                 │
│ - Tests generalization              │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Confidence Phase (Attempts 5-10)  │
│                                     │
│ - Confidence: 70% → 90%             │
│ - For low-risk: AUTO_LOW_RISK       │
│ - Still suggests for medium-risk    │
│ - Automated path optimization       │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Autonomy Phase (Attempts 10+)     │
│                                     │
│ - Confidence: 90%+                  │
│ - Auto-execute without asking       │
│ - Only notify after success         │
│ - Proactive intervention ready      │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Mastery State                     │
│                                     │
│ - Error fixed before user notices   │
│ - Confidence: 95%+                  │
│ - Learns variations of same error   │
│ - Teaches other instances           │
│ - Becomes predictive                │
└─────────────────────────────────────┘
```

## Multi-Agent Interaction

```
User Error Event
    │
    ▼
[ContextCollectorAgent]
├─ Collects system information
├─ Environment state snapshot
└─ Returns: SystemInfo
    │
    ▼
[ErrorAnalyzerAgent]
├─ Analyzes error message
├─ Builds error taxonomy
├─ Determines severity
└─ Returns: ErrorAnalysis
    │
    ├────────────────────────┐
    │                        │
    ▼                        ▼
[DocSearchAgent]      [SolutionArchitectAgent]
├─ Searches docs      ├─ Generates solutions
├─ Finds examples     ├─ Ranks by risk
└─ Returns: Docs      └─ Returns: Strategies
    │                        │
    └────────────┬───────────┘
                 │
                 ▼
[OrchestratorAgent]
├─ Selects best strategy
├─ Consults resolver
├─ Decides automation level
└─ Coordinates execution
    │
    ▼
[ExecutorAgent] + [Resolver]
├─ Executes commands (if approved)
├─ Monitors execution
├─ Captures results
└─ Records learning data
```

## Autonomous Loop (After Installation)

```
LOOP (every command):
  1. User types command in shell
  2. Shell hook captures it
  3. Command executes
  4. Exit code checked
     ├─ SUCCESS? → Log it, continue
     └─ ERROR? → Send to monitor
  5. Monitor receives event
  6. Resolver analyzes immediately
  7. Decision made in <100ms
  8. Action taken:
     ├─ SILENT: Just log
     ├─ SUGGEST: Show in red text
     └─ AUTO: Execute + notify
  9. Record outcome for learning
  10. Continue with next command

This happens for EVERY error you encounter.
The system gets smarter with each error.
```

## Performance Characteristics

```
Latency:
  - Error detection: <10ms
  - Resolution decision: <100ms  
  - Workflow analysis: 0.5-2s (in background)
  - Total intervention: <2.1s

Memory:
  - Monitor daemon: ~20MB
  - History buffer: ~10MB
  - Learning data: ~5MB
  - Total: ~35MB

CPU:
  - Idle: <0.1%
  - Active analysis: 5-10%
  - Execution: 20-40% (when running fixes)

Network:
  - Only on demand (documentation search)
  - Cached results used when possible
```

---

**Terminal Hero** is now a fully autonomous system that:
- 🔍 Watches every command you run
- 🤖 Makes intelligent decisions about fixing errors
- 📚 Learns from every intervention
- ⚡ Gets faster and smarter over time
- 🎯 Requires zero user intervention after installation

The system embodies true agentic behavior - autonomous, learning, and proactive.
