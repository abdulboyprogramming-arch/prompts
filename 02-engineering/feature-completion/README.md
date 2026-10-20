# Feature Completion Across Layers

**Maturity: operational (v1.0.0).** Four stages for finishing a feature that "looks done" but is not.

**Entry point:** [`P01-Contract/P01-Completion-Contract.md`](P01-Contract/P01-Completion-Contract.md)
**Execution mode:** implementation
**Risk class:** B — application code and tests; deployment is Category C

## The failure this system prevents

An agent or engineer implements what is visible: the form, the button, the endpoint that returns 200. Then the feature is reported complete, and production reveals that:

- the write path bypasses the authorisation check the read path has,
- the new field is stored but never validated, so bad data enters silently,
- the list view has no empty state and crashes on zero results,
- the background job that should act on the record was never registered,
- the audit log, notification, and export all ignore the new state,
- the index required by the new query does not exist, so the page is fast with 40 rows and unusable with 400,000,
- the feature works for the admin who tested it, and returns 403 for normal users.

None of these are exotic. They are **layers left unimplemented**, and they are invisible to the demo that produced the completion claim.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| FC-P01 | [Completion contract](P01-Contract/P01-Completion-Contract.md) | Define what "done" means across every layer before writing code | `.feature/COMPLETION_CONTRACT.md` |
| FC-P02 | [Layer inventory & gap map](P02-Layer-Map/P02-Layer-Gap-Map.md) | Locate every implementation point and mark present/missing | `.feature/LAYER_MAP.md` |
| FC-P03 | [Implementation](P03-Implementation/P03-Layer-Implementation.md) | Fill the gaps in end-to-end increments | commits, `.feature/IMPLEMENTATION_LOG.md` |
| FC-P04 | [Acceptance](P04-Acceptance/P04-End-to-End-Acceptance.md) | Prove it works for every role, state, and volume — from clean state | `.feature/ACCEPTANCE.md` |

## The layer checklist (the heart of this system)

A feature is not complete until each applicable layer has been considered. "Not applicable" is a valid answer — but it must be written down with a reason.

| Layer | Question |
|-------|----------|
| Interface | Does the user-facing surface exist for every state: loading, empty, populated, error, permission-denied? |
| Validation | Is input validated at the boundary, with messages the user can act on? |
| API / contract | Is the operation exposed, typed, documented, and consistent with its siblings? |
| Business rules | Is the logic in the right place, and does it handle the edge cases (duplicates, concurrency, partial failure)? |
| Authorisation | Is it enforced for *this* operation, at object level, for every role? |
| Persistence | Schema, migration, constraints, indexes for the access pattern, and nullability that matches reality? |
| Asynchrony | Jobs, queues, webhooks, or scheduled work registered, idempotent, retried, and monitored? |
| Integration | Third-party calls authenticated, timeouts set, failures handled, retries bounded? |
| Side effects | Notifications, emails, audit logs, analytics, search index, caches — all updated? |
| Config | New settings declared, defaulted, documented, and safe in every environment? |
| Observability | Can you tell whether it worked or failed in production? |
| Accessibility & i18n | Keyboard, labels, contrast, error announcement; strings externalised? |
| Tests | Unit for logic, integration for the seam, one end-to-end for the journey, negative cases? |
| Documentation | User docs, API docs, changelog, and any runbook? |

## Boundaries

- Designing a new feature from scratch: `02-engineering/feature-design-suggestion/` (skeleton) — this system assumes the design intent exists or is trivially clear.
- Broad codebase assessment: `02-engineering/codebase-audit/`.
- Completing an entire abandoned project: `02-engineering/project-recovery/` — this system is for one feature.
- Verifying someone else's completion claim: `07-workflows/independent-verification.md`.

## What this system will not do

- Invent product requirements you have not agreed. If the contract is ambiguous, it stops at FC-P01 and asks.
- Guarantee the feature is *wanted*. It guarantees the feature is *finished*.
