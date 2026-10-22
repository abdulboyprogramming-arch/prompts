# Game Development System

**Status:** Operational — ten stages (`GD-P01`–`GD-P10`). The system is sequenced so that nothing gets content before it has a playable slice: vision writes the fantasy and the falsifiers, design turns it into a loop with a cycle time, architecture sets the tuning pipeline and the frame budget, the slice proves the loop end to end on target hardware, the core systems are built one at a time with their numbers in data, content is produced against a manifest, and the playtest judges the falsifiers with observations rather than opinions. `GD-P09` and `GD-P10` cover the two failures that cost players their progress and their fairness perception. **No stage has been executed against a real game project**, so the system is a supervised checklist, not a proven procedure; [`_meta/release-readiness.md`](../../_meta/release-readiness.md) records that gap.
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
