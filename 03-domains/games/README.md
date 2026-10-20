# Game Development System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Game-Development-Orchestrator.md`](P08-Orchestrator/P08-Game-Development-Orchestrator.md)

A multi-stage system for designing and building games (or major game features) with a strong emphasis on fun, clarity, and vertical slices over premature scope expansion.

Works for:
- New game prototypes from scratch
- Major features in existing game projects
- Systems work (combat, progression, UI, tooling) inside a game codebase

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| GD-P01 | Vision & Player Fantasy | Define the core experience and audience |
| GD-P02 | Game Design | Mechanics, loop, progression, and constraints |
| GD-P03 | Technical Architecture | Engine, structure, tools, and pipelines |
| GD-P04 | Vertical Slice | Build the smallest playable proof of fun |
| GD-P05 | Core Systems | Implement supporting gameplay systems |
| GD-P06 | Content & Polish | Levels/content, UX, juice, and readability |
| GD-P07 | Playtest & Validate | Evaluate fun, clarity, and technical health |
| GD-P08 | Master Orchestrator | Coordinates the full game-dev process |

## Principles

- Prove the fun early with a vertical slice.
- Prefer tight scope and strong iteration over broad incomplete features.
- Make controls, feedback, and readability first-class.
- Separate design intent from implementation details.
- Track what is fun, confusing, or fragile during playtests.
