# Frontend Domain System

**Status:** Operational — 8 developed stages (`FE-P01` … `FE-P08`). Each stage states its inputs, decision rules, verification, failure handling and handover. None of these eight has been executed against a real application yet: they are developed to the standard, not empirically tested — see [`_meta/evidence.json`](../../_meta/evidence.json) for the prompts that have run.
**Entry Point:** [`P08-Orchestrator/P08-Frontend-Orchestrator.md`](P08-Orchestrator/P08-Frontend-Orchestrator.md)

A multi-stage system for building, improving, or extending frontend applications with strong attention to UX, architecture, state, accessibility, and quality.

Works for:
- New frontend features or pages
- Frontend-heavy product work
- Refactors of UI architecture within an existing app
- Design-system-aligned implementation

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| FE-P01 | Context & Stack | Understand product, users, and frontend stack |
| FE-P02 | UX & Interaction Goals | Define flows, states, and interaction quality |
| FE-P03 | Frontend Architecture | Structure components, routing, and boundaries |
| FE-P04 | Implementation | Build UI with project conventions |
| FE-P05 | State & Data | Handle client state, server data, and caching |
| FE-P06 | Quality & Accessibility | Tests, a11y, responsiveness, performance basics |
| FE-P07 | Polish & Handoff | Visual polish, edge cases, and review readiness |
| FE-P08 | Master Orchestrator | Coordinates the full frontend process |

## What each stage gates on

`FE-P01` records the stack as installed and the render mode per route, because both
decide where state may live. `FE-P02` writes a state matrix with no blank cells — loading,
empty, error, partial, permission-denied, success, offline — because an undesigned state
is improvised in code. `FE-P03` assigns exactly one owner to every piece of state and a
boundary to every failure region. `FE-P04` implements the matrix cell by cell and logs
every deviation. `FE-P05` makes the cache honest: keys that carry their parameters,
invalidation per mutation, races handled, and a session boundary that is cleared on
logout. `FE-P06` produces checks with artifacts — automated scanning is the floor, not the
result. `FE-P07` runs the long-string, translation, zoom and slow-network passes, then
writes the honest note about what was not tested.

Two related prompts live outside this system and are cited rather than duplicated:
[`A11Y-01`](../../04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) for a formal
WCAG 2.2 AA conformance audit, and
[`PERF-BUDGET-01`](../../05-scenarios/performance-budget/PERFORMANCE-BUDGET.md) for a
standing performance budget and CI gate.

## Principles

- Start from user flows and states, not from components in isolation.
- Prefer composition and clear boundaries over deep inheritance or spaghetti state.
- Accessibility and responsiveness are part of done, not polish-only extras.
- Match existing design system and project conventions.
- Keep loading, empty, error, and success states explicit.
