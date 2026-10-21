# 01-Contribution

Prompt systems for adding value to existing projects (open-source or private): choosing what to contribute, understanding the target, implementing safely, and communicating with maintainers.

> **System maturity is not uniform.** Only `open-source/general-agent/` is developed to the library standard. The four other systems in this folder are **stage skeletons**: they outline a sensible sequence but do not yet contain the verification, evidence, and failure-handling rules required before an agent should run them unsupervised. See `_meta/prompt-authoring-standard.md` and `_meta/ROADMAP-AND-BACKLOG.md`.

## Systems

| Path | What it does | Stages | Maturity |
|------|--------------|-------:|----------|
| [`open-source/general-agent/`](open-source/general-agent/README.md) | End-to-end autonomous open-source contribution: bootstrap → recon → architecture → opportunity discovery → implementation → QA → publication → PR communication → recovery | 16 | **Operational** |
| [`packages-libraries/`](packages-libraries/README.md) | Contributing to packages and libraries where API compatibility matters | 8 | Skeleton |
| [`web/general/`](web/general/README.md) | Contributing to web projects (framework-agnostic) | 8 | Skeleton |
| [`web3/general/`](web3/general/README.md) | Contributing to web3 projects | 8 | Skeleton |
| [`language-design/`](language-design/README.md) | Designing or extending a programming language | 8 | Skeleton |

## Why three near-identical systems exist

`web/general/`, `web3/general/`, and `packages-libraries/` share a stage sequence and differ in risk model, definition of done, and approval requirements. That duplication is measured, decided, and bounded — read [`VARIANTS.md`](VARIANTS.md) before consolidating, deleting, or promoting any of them. Short version: keep three, and any stage that cannot state what differs in its domain is a duplicate to delete rather than maintain.

## Choosing a system

- **You have a specific repository and want the agent to find and land a contribution** → `open-source/general-agent/` (start at `P16` orchestrator, or `P03` if you only want reconnaissance).
- **The value you add is an API surface others depend on** → `packages-libraries/`.
- **The change is UI/browser-facing** → `web/general/`, but read the skeleton warning first.
- **The work is language/semantics design** → `language-design/`.

## What "skeleton" means in practice

A skeleton system can still be useful as a *checklist for a human-driven session*: it names the stages and the artifacts. It is not safe to hand to an autonomous agent expecting it to know when to stop, what evidence to produce, or how to verify its own work. If you use one, pair it with `00-core/system-prompts/BASE-ENGINEERING-AGENT.md` and expect to supervise closely.

## Relationship to other folders

- Deep technology-specific work belongs in `03-domains/` (backend, frontend, mobile, AI).
- Audits, refactors, and migrations of *your own* codebase belong in `02-engineering/`.
- Multi-stage compositions that span folders live in `07-workflows/`.
