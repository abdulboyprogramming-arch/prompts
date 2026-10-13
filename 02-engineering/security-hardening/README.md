# Security Hardening System

**Status:** Operational (v1.0)  
**Entry Point:** [`P07-Orchestrator/P07-Security-Hardening-Orchestrator.md`](P07-Orchestrator/P07-Security-Hardening-Orchestrator.md)

A practical, multi-stage system for identifying security weaknesses and applying focused, high-value hardening improvements to an existing system.

This system emphasizes responsible analysis, prioritization by risk, and safe implementation. It is not a replacement for a full professional penetration test or formal audit.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| SEC-P01 | Context & Scope | Understand the system and define hardening goals |
| SEC-P02 | Lightweight Threat Modeling | Identify key assets, threats, and trust boundaries |
| SEC-P03 | Security Surface Analysis | Examine entry points, auth, data handling, dependencies |
| SEC-P04 | Findings & Risk Prioritization | Consolidate and prioritize issues |
| SEC-P05 | Hardening Plan | Design concrete, prioritized improvements |
| SEC-P06 | Implementation & Validation | Apply changes and verify |
| SEC-P07 | Master Orchestrator | Coordinates the full hardening process |

## Principles

- Focus on high-impact, realistic risks.
- Prefer secure defaults and simple, proven controls.
- Never weaken security to make tests pass.
- Handle sensitive findings responsibly.
- Make trade-offs (usability, complexity, performance) explicit.
- Document residual risks honestly.
