# Agent Context and IDE Adaptability

**Maturity: operational (v1.0.0).** Four stages for the files that tell an AI coding assistant how this repository works — `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, Copilot instructions, MCP configs, editor settings — and for proving that assistants actually obey them.

**Entry point:** [`P01-Surfaces`](P01-Surfaces/P01-Agent-Surfaces.md) to find out what already exists and what contradicts what.
**Execution mode:** diagnostic
**Per stage:** diagnostic (P01, P03), implementation (P02, P04)
**Risk class:** A → B (P02 and P04 write files; P03 runs agents in a sandbox)

## Why this system exists

Every team now maintains a second, informal specification: the instructions it gives its AI assistant. It is usually written once, by one person, and never reconciled.

- **Duplication and drift.** `AGENTS.md`, `CLAUDE.md`, and three `.cursor/rules` files say different things about the same command. Which one wins depends on the tool's load order — a decision nobody made.
- **False claims.** "Run `npm run dev`" — the script was renamed two releases ago. The agent now confidently invents a workaround.
- **No boundaries.** Nothing says *what not to do*, so an agent edits generated code, commits to a protected branch, or writes a migration by hand.
- **No verification.** Nobody has tested whether the file changes behaviour. It is treated as a control without evidence that it controls anything.
- **Permission creep.** An MCP server or tool config granted shell and network access that no human reviewed.
- **Answering the wrong question.** Ambiguity ("make it faster") is resolved by guessing and rewriting instead of asking.

This system treats agent context as **executable policy**: written once in one place, adapted per tool, mechanically checked, and behaviourally tested.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| CTX-P01 | [Surfaces](P01-Surfaces/P01-Agent-Surfaces.md) | Which tools read which files; what they claim; what is true, duplicated, dangerous, or missing | `.agent-context/SURFACES.md` |
| CTX-P02 | [Authoring](P02-Authoring/P02-Authoring-Canonical-Context.md) | One canonical file, thin per-tool adapters, commands that were executed | `AGENTS.md` + adapters + `AUTHORING.md` |
| CTX-P03 | [Adherence](P03-Adherence/P03-Adherence-Testing.md) | Probe the agent: does it follow commands, conventions, boundaries, ambiguity? | `.agent-context/ADHERENCE.md` |
| CTX-P04 | [Maintenance](P04-Maintenance/P04-Context-Maintenance.md) | Machine checks, update triggers, owner, review cadence, decay metrics | `.agent-context/MAINTENANCE.md` |

## Tool surface map

| File | Read by | Role in this system |
|------|---------|---------------------|
| `AGENTS.md` | most modern agents | **canonical source** |
| `CLAUDE.md` | Claude Code | thin adapter, points at `AGENTS.md` |
| `.cursor/rules/*.mdc` | Cursor | thin adapter; globs must match real paths |
| `.github/copilot-instructions.md` | GitHub Copilot | thin adapter |
| `.windsurf/rules`, `.clinerules`, `.roo/` | respective tools | thin adapters |
| MCP server config | agents with tool access | **reviewed as a permission grant**, not a doc |
| `.vscode/settings.json`, `tasks.json`, `launch.json` | VS Code, Cursor, Windsurf | editor behaviour; must not encode one OS |
| `.devcontainer/`, `.nvmrc`, `.tool-versions` | any environment | version parity with CI — see `05-scenarios/dev-environment/` |

## The rules

1. **One canonical source; every other file is an adapter.** ≤15 lines, no duplicated guidance.
2. **Every command is executed before it is written.**
3. **Prohibitions are concrete and paired with an alternative** — "ask before X, do Y instead".
4. **Short beats complete.** Context is a per-request cost; if it is not read, it does not exist.
5. **Describe the repository as it is**, not as it should be.
6. **Test adherence, not existence.** A file nobody obeys is worse than no file, because it manufactures confidence.
7. **An ignored clear instruction needs a machine check**, not more prose.
8. **Delete what changes no behaviour.**
9. **Human documents win conflicts.** `CONTRIBUTING.md` defines process; agent context describes it.
10. **A tool config that grants permissions is a security decision**, reviewed like any other.

## Proportionality

| Situation | Run |
|-----------|-----|
| First time setting up agent context | P01 → P02 → P03 (three probes) |
| An agent keeps doing the wrong thing | P03 with that behaviour as the probe; then P02 if the instruction is missing or vague |
| A new tool adopted by the team | P01 (one row) → P02 (one adapter) → P03 (one probe) |
| Quarterly hygiene | P04 review: checks, three probes, remove dead sections |
| Inherited repository | P01 first — you often find four conflicting files and a secret in an MCP config |

## Boundaries

- Dev environment, devcontainers, editor parity across machines: `05-scenarios/dev-environment/`.
- Documentation for humans: `04-process/documentation/`.
- Security review of the permissions an agent tool holds: `02-engineering/security-hardening/`.
- Project handover including the context file as a knowledge asset: `04-process/handover/`.

## What this system will not do

- Make a model obey. It measures whether it does, and converts the failures it can into machine checks.
- Choose your assistant. It works with whichever tools you actually use.
- Guarantee the instructions are wise — only that they are true, singular, tested, and maintained.
