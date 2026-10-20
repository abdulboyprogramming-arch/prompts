# 05-Scenarios — Single-Purpose Prompts

High-utility prompts for a specific situation, usable in one session. Lighter than the multi-stage systems, but held to the same standards: evidence, verification, completion criteria.

## Available

| Prompt | Use when | Maturity |
|--------|----------|----------|
| [`debugging/SYSTEMATIC-DEBUGGING.md`](debugging/SYSTEMATIC-DEBUGGING.md) | A defect resists normal debugging; you want reproduction, hypotheses, and a proven cause | **operational** |
| [`incident-response/PRODUCTION-INCIDENT.md`](incident-response/PRODUCTION-INCIDENT.md) | Production is broken now; restore first, understand second | **operational** |
| [`flaky-tests/FLAKY-TEST-TRIAGE.md`](flaky-tests/FLAKY-TEST-TRIAGE.md) | A test passes and fails without code changes | **operational** |
| [`failed-fix/FAILED-FIX-ESCALATION.md`](failed-fix/FAILED-FIX-ESCALATION.md) | Two or more fix attempts have failed and you need to break the loop | **operational** |
| [`data-loss/DATA-LOSS-RECOVERY.md`](data-loss/DATA-LOSS-RECOVERY.md) | Data has been deleted, corrupted, or overwritten and you need it back without losing more | **operational** |
| [`security-incident/SECURITY-INCIDENT.md`](security-incident/SECURITY-INCIDENT.md) | A compromise is suspected or confirmed: preserve evidence, contain, scope, disclose | **operational** |
| [`live-surface-audit/LIVE-SURFACE-AUDIT.md`](live-surface-audit/LIVE-SURFACE-AUDIT.md) | You can only see a system from outside — a URL, host, or API — and need an evidence-backed assessment | **operational** |
| [`hackathon-sprint/HACKATHON-SPRINT.md`](hackathon-sprint/HACKATHON-SPRINT.md) | A hard deadline, judges, and a demo — build backwards from the four minutes | **operational** |
| [`deployment-target/DEPLOY-TO-PLATFORM.md`](deployment-target/DEPLOY-TO-PLATFORM.md) | Put an app on Vercel, Netlify, Render, Railway, Fly, Cloud Run, or a VPS — without the classic misconfigurations | **operational** |
| [`platform-migration/PLATFORM-MIGRATION.md`](platform-migration/PLATFORM-MIGRATION.md) | Move a running service between hosts without an outage you cannot undo | **operational** |
| [`dev-environment/DEV-ENVIRONMENT.md`](dev-environment/DEV-ENVIRONMENT.md) | "Clone and run" is false — make one command work on every machine and editor | **operational** |
| [`on-call-handover/ONCALL-HANDOVER.md`](on-call-handover/ONCALL-HANDOVER.md) | Shift change, and the next responder must inherit the real state of the system | **operational** |
| [`quick-fixes/SAFE-QUICK-FIX.md`](quick-fixes/SAFE-QUICK-FIX.md) | A small, contained fix with minimal blast radius | skeleton |
| [`performance-investigation/PERFORMANCE-INVESTIGATION.md`](performance-investigation/PERFORMANCE-INVESTIGATION.md) | Something is slow and you need a diagnosis, not an optimisation project | skeleton |
| [`legacy-code/WORKING-WITH-LEGACY.md`](legacy-code/WORKING-WITH-LEGACY.md) | Changing code nobody understands, without a rewrite | skeleton |
| [`onboarding/CODEBASE-ONBOARDING.md`](onboarding/CODEBASE-ONBOARDING.md) | You have just been handed an unfamiliar codebase | skeleton |
| [`pr-authoring/WRITE-STRONG-PR.md`](pr-authoring/WRITE-STRONG-PR.md) | Preparing a change for review | skeleton |

The five skeleton prompts have useful structure but no verification or failure handling. Treat them as scaffolds for a supervised session.

## Scenario or system?

| Situation | Use |
|-----------|-----|
| One question, one session, contained change | a scenario prompt |
| Ordered stages, artifacts that persist, decisions between stages | a system in `02-engineering/`, `04-process/`, etc. |
| Multiple systems in sequence | a workflow in `07-workflows/` |

If a scenario prompt keeps needing stages, handoffs, or durable artifacts, it should be promoted into a system rather than growing into a badly organised one.

## Design principles

- Fast to start: no required intake ritual.
- Evidence over guessing; explicit `verified` / `inferred` / `unknown`.
- Safe defaults: do not make things worse to make progress.
- Clear stopping point and completion criteria.
- Composable as a precursor to a deeper system (e.g. debugging → refactoring, incident → postmortem).
