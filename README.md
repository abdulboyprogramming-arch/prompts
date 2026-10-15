# Supercharged Prompt Archive

**The most complete, organized, and powerful collection of professional software-engineering prompt systems.**

This monorepo is designed to become the definitive archive of high-quality, multi-stage, production-grade prompt sets that software professionals can use across virtually any situation they encounter:

- Contributing to open-source or private projects
- Designing or extending programming languages
- Building or improving web, web3, game, mobile, systems, and infrastructure projects
- Deep codebase audits, architecture reviews, and rewrites
- Research & development, pattern invention, and systems thinking
- Full project creation from scratch
- Day-to-day scenario prompts (debugging, performance, security, migrations, etc.)
- Interactive prompts that intelligently gather missing context

## Philosophy

1. **Depth over shallowness** — Prefer complete multi-stage systems with clear handovers, validation gates, and recovery logic over one-shot prompts.
2. **Evidence and professionalism** — Prompts must produce work that a competent human engineer would be proud to submit.
3. **Safety and authorization boundaries** — Clear action categories, secret handling, and respect for project governance.
4. **Durable state** — Multi-stage systems maintain artifacts so work can be resumed across sessions.
5. **Extensibility** — The taxonomy is designed to grow to hundreds of thousands of prompts without becoming chaotic.
6. **Practicality** — Every prompt set should be immediately usable by a capable coding agent.

## Top-Level Structure

```
prompts/
├── _meta/                          # Taxonomy, templates, quality standards
├── 00-core/                        # Foundational system & orchestration prompts
├── 01-contribution/                # All contribution workflows
│   ├── open-source/
│   │   └── general-agent/          # ← Full 16-prompt Open-Source Contribution Agent (ready)
│   ├── language-design/
│   ├── packages-libraries/
│   ├── web/
│   ├── web3/
│   └── ...
├── 02-engineering/                 # Core engineering activities
│   ├── codebase-audit/
│   ├── architecture-review/
│   ├── refactoring/
│   ├── rewriting-migration/
│   ├── feature-design-suggestion/
│   ├── from-scratch/
│   ├── patterns-strategies-methods/
│   └── ...
├── 03-domains/                     # Domain-specific deep prompts
│   ├── frontend/
│   ├── backend/
│   ├── devops-infra/
│   ├── web3/
│   ├── games/
│   └── ...
├── 04-process/                     # Methodology & process
│   ├── research-and-development/
│   ├── systems-building-improvement/
│   ├── testing-qa/
│   └── ...
├── 05-scenarios/                   # Quick / situational prompts
├── 06-interactive/                 # Prompts that collect extra user context
├── 99-misc/                        # Temporary holding area
└── archive/                        # Historical / legacy content
```

## Currently Available High-Quality Systems

| Location | Description | Status |
|----------|-------------|--------|
| `01-contribution/open-source/general-agent/` | Complete 16-prompt autonomous open-source contribution agent (P01–P16) | **Production-ready** |
| `01-contribution/web/general/` | General Web Contribution system (8 stages + orchestrator) | **Operational** |
| `01-contribution/web3/general/` | General Web3 Contribution system (8 stages + orchestrator) | **Operational** |
| `01-contribution/packages-libraries/` | Package & Library Contribution system (8 stages + orchestrator) | **Operational** |
| `01-contribution/language-design/` | Language Design & Invention system (8 stages + orchestrator) | **Operational** |
| `04-process/testing-qa/` | Testing & QA Process system (7 stages + orchestrator) | **Operational** |
| `04-process/code-review/` | Code Review process system (6 stages + orchestrator) | **Operational** |
| `04-process/documentation/` | Documentation process system (8 stages + orchestrator) | **Operational** |
| `06-interactive/` | Interactive Context Collectors & System Selector Wizard | **Operational** |
| `05-scenarios/` | Scenario & Quick-Prompt collections (Debugging, Onboarding, Quick-Fix, Legacy) | **Operational** |
| `02-engineering/codebase-audit/` | Deep Codebase Audit & Analysis system (9 stages + orchestrator) | **Operational** |
| `02-engineering/from-scratch/` | From-Scratch Project system (8 stages + orchestrator) | **Operational** |
| `02-engineering/refactoring/` | Safe Refactoring system (7 stages + orchestrator) | **Operational** |
| `02-engineering/feature-design-suggestion/` | Feature Design & Suggestion system (7 stages + orchestrator) | **Operational** |
| `02-engineering/rewriting-migration/` | Rewriting & Language Migration system (8 stages + orchestrator) | **Operational** |
| `02-engineering/architecture-review/` | Architecture Review system (7 stages + orchestrator) | **Operational** |
| `02-engineering/patterns-strategies-methods/` | Patterns, Strategies & Methods system (7 stages + orchestrator) | **Operational** |
| `02-engineering/performance/` | Performance Analysis & Optimization system (7 stages + orchestrator) | **Operational** |
| `02-engineering/security-hardening/` | Security Hardening system (7 stages + orchestrator) | **Operational** |

## How to Use

1. Choose the prompt system that matches your situation.
2. Start with the highest-level orchestrator prompt in that folder (usually named `...-Orchestrator.md` or `README.md`).
3. Provide the required context (repository, `MY_DETAILS.txt`, project description, etc.).
4. Let the agent follow the staged process, maintaining the durable artifacts it creates.

## Adding New Prompt Sets

See `_meta/` for templates and quality standards. Every major prompt set should include:

- Clear identity and version
- Role definition
- Prerequisites and required tools
- Explicit workflow with decision gates
- Validation and failure handling
- Security / authorization constraints
- Completion criteria and handover notes

## Roadmap (High Level)

- Expand contribution systems for languages, packages, web, and web3
- Full codebase audit & architecture review systems
- From-scratch project generation systems (multiple stacks)
- Game development prompt systems
- Interactive context-collection wizards
- Large library of scenario-specific quick prompts
- Continuous quality improvement of existing systems

---

**This is the beginning of the widest, deepest, and most professional prompt archive for software work.**
