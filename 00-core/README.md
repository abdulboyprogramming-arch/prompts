# 00-Core — Foundational Prompt Infrastructure

Shared primitives used across the archive: safety rules, orchestration patterns, system-level agent instructions, and prompt-engineering standards.

These are not end-user task systems. They are the common substrate that specialized systems build on.

## Contents

| Path | Purpose |
|------|---------|
| `safety-and-security/` | Action categories, secret handling, authorization boundaries |
| `agent-orchestration/` | Multi-stage coordination, handovers, recovery, progress tracking |
| `system-prompts/` | Base operating personas and durable agent contracts |
| `prompt-engineering/` | Templates, quality bars, and anti-patterns |

## Usage

Specialized systems (contribution, engineering, process, domains) should reference these primitives rather than redefining safety or orchestration rules from scratch.
