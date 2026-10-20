# Game Development System

**Status:** Mixed — 7 skeleton stage outlines plus **2 operational stages** (GD-P09 save migration, GD-P10 netcode). The skeletons name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`; the two operational stages target the failures that cost players their progress and their fairness perception. See [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
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
| GD-P09 | **Save Migration** (operational) | Versioned saves, forward-only migration, atomic writes, real old saves as fixtures |
| GD-P10 | **Netcode & Determinism** (operational) | Latency reproduction, three-clock alignment, desync and rollback diagnosis |

## Operational stages added in 2.15.0

The eight skeletons describe *how to build* a game. The two failures that actually end players' relationships with a shipped game were unrepresented:

- **Save data** — an unversioned format, a non-atomic write, or a migration tested only on fresh saves destroys hundreds of hours of progress and generates refunds. `GD-P09` treats real historical saves as the test fixture set.
- **Netcode** — "I shot first and died" is a clock and reconciliation problem, not a balance problem. `GD-P10` aligns server tick, client tick, and input timestamp before changing any code, and measures against a latency budget rather than a feeling.

## Principles

- Prove the fun early with a vertical slice.
- Prefer tight scope and strong iteration over broad incomplete features.
- Make controls, feedback, and readability first-class.
- Separate design intent from implementation details.
- Track what is fun, confusing, or fragile during playtests.
