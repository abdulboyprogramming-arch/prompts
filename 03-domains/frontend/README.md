# Frontend Domain System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
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

## Principles

- Start from user flows and states, not from components in isolation.
- Prefer composition and clear boundaries over deep inheritance or spaghetti state.
- Accessibility and responsiveness are part of done, not polish-only extras.
- Match existing design system and project conventions.
- Keep loading, empty, error, and success states explicit.
