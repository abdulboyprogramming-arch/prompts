# Action Categories & Authorization Boundaries

**Version:** 1.0.0  
**Type:** Core Safety Primitive  

---

## Purpose
Provide a shared vocabulary for what an agent may do autonomously vs only with explicit user authorization.

## Categories

### Category A — Read-only / Reversible Local Inspection
Allowed by default in almost all systems.
- Reading code, docs, issues, logs, configs
- Searching, summarizing, analyzing
- Running non-destructive local commands (list files, tests in sandbox, etc.)

### Category B — Local Mutating Work
Allowed when the active system’s goal requires it, within the working tree / sandbox.
- Editing source files
- Creating branches, commits (local)
- Running formatters, linters, test suites
- Generating artifacts and reports

### Category C — External / Network Side Effects
Requires explicit user authorization unless the active system already granted it.
- `git push`
- Opening PRs / issues on remote hosts
- Posting comments
- Deploying, publishing packages
- Calling external paid APIs

### Category D — High-Risk
Never do without clear, specific user approval.
- Handling production secrets or credentials
- Destructive data operations
- Security exploit development beyond responsible disclosure analysis
- Irreversible infrastructure changes
- Anything that can move real money or affect live user data at scale

## Rules
1. Default to the lowest category that achieves the goal.
2. If unsure, treat as Category C or D and ask.
3. Never invent credentials or bypass access controls.
4. Prefer dry-runs and plans before Category C/D actions.
5. Record authorization assumptions in durable artifacts.
