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
| [`background-jobs/BACKGROUND-JOBS.md`](background-jobs/BACKGROUND-JOBS.md) | Jobs duplicate, overlap, or silently stop — make retries safe | **operational** |
| [`email-deliverability/EMAIL-DELIVERABILITY.md`](email-deliverability/EMAIL-DELIVERABILITY.md) | "I never got the reset link" — SPF/DKIM/DMARC alignment, streams, bounces | **operational** |
| [`third-party-integration/THIRD-PARTY-INTEGRATION.md`](third-party-integration/THIRD-PARTY-INTEGRATION.md) | A vendor API: slow, wrong, duplicated, or silently changed | **operational** |
| [`file-uploads/FILE-UPLOADS.md`](file-uploads/FILE-UPLOADS.md) | Uploads that must not become an unindexed copy of the customer database | **operational** |
| [`localization/LOCALIZATION.md`](localization/LOCALIZATION.md) | Correct in another language, not just translated | **operational** |
| [`infrastructure-as-code/INFRA-AS-CODE.md`](infrastructure-as-code/INFRA-AS-CODE.md) | Is the code the truth, or a plausible fiction about the console? | **operational** |
| [`performance-budget/PERFORMANCE-BUDGET.md`](performance-budget/PERFORMANCE-BUDGET.md) | "The site feels slow" turned into a number that fails a build | **operational** |
| [`monorepo/MONOREPO.md`](monorepo/MONOREPO.md) | Slow, fragile, or quietly coupled packages | **operational** |
| [`disaster-recovery/DISASTER-RECOVERY.md`](disaster-recovery/DISASTER-RECOVERY.md) | The region, account, or data is gone — prove the restore, measure RTO/RPO | **operational** |
| [`automation/AUTOMATE-TASK.md`](automation/AUTOMATE-TASK.md) | "Every Monday we do this by hand" — turn it into a script that is idempotent, verified, and heard from when it fails | **operational** |
| [`client-secrets/CLIENT-SIDE-SECRETS.md`](client-secrets/CLIENT-SIDE-SECRETS.md) | A key shipped in a bundle, app, or CLI — find it, state what it can do, replace the design | **operational** |
| [`supply-chain/SUPPLY-CHAIN.md`](supply-chain/SUPPLY-CHAIN.md) | Can you prove the artifact you deployed is the one you built, and would a compromised dependency reach production? | **operational** |
| [`data-residency/DATA-RESIDENCY.md`](data-residency/DATA-RESIDENCY.md) | A contract or regulator says data must stay in a region — find where it actually goes | **operational** |
| [`data-migration/DATA-MIGRATION.md`](data-migration/DATA-MIGRATION.md) | Records must move between systems — field mapping, loss register, idempotent load, value-level reconciliation | **operational** |
| [`feature-sunset/FEATURE-SUNSET.md`](feature-sunset/FEATURE-SUNSET.md) | Retire a feature customers use: usage evidence, notice, reversible switch-off, data decision | **operational** |
| [`incident-communications/INCIDENT-COMMUNICATIONS.md`](incident-communications/INCIDENT-COMMUNICATIONS.md) | Someone must write the customer update on a cadence, without speculation | **operational** |
| [`operational-readiness/OPERATIONAL-READINESS.md`](operational-readiness/OPERATIONAL-READINESS.md) | Would the on-call engineer survive this service at 03:00? | **operational** |
| [`build-performance/BUILD-PERFORMANCE.md`](build-performance/BUILD-PERFORMANCE.md) | CI takes 40 minutes and people skip tests — measure the loop before optimising | **operational** |
| [`ai-output-verification/AI-OUTPUT-VERIFICATION.md`](ai-output-verification/AI-OUTPUT-VERIFICATION.md) | An agent says it is done — verify what is true before anyone trusts it | **operational** |
| [`environment-parity/ENVIRONMENT-PARITY.md`](environment-parity/ENVIRONMENT-PARITY.md) | "Works locally, fails in staging" — find the difference that changes behaviour, by experiment | **operational** |
| [`capacity-planning/CAPACITY-PLANNING.md`](capacity-planning/CAPACITY-PLANNING.md) | What runs out first, when, and what you will do about it — pools, quotas, sequences, expiries | **operational** |
| [`vendor-due-diligence/VENDOR-DUE-DILIGENCE.md`](vendor-due-diligence/VENDOR-DUE-DILIGENCE.md) | Before you depend on a supplier: data exposure, reliability, lock-in, exit plan | **operational** |
| [`abuse-prevention/ABUSE-PREVENTION.md`](abuse-prevention/ABUSE-PREVENTION.md) | Credential stuffing, scraping, enumeration, signup spam — limit the dimension the abuse consumes | **operational** |
| [`test-data/TEST-DATA.md`](test-data/TEST-DATA.md) | The fixture holding a real customer, the staging database copied from production | **operational** |
| [`usage-metering/USAGE-METERING.md`](usage-metering/USAGE-METERING.md) | You bill by usage, seat, or request — make the number defensible | **operational** |
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
| Ordered stages, artifacts that persist, decisions between stages | a multi-stage system in `02-engineering/` or `04-process/` |
| Multiple systems in sequence | a workflow in `07-workflows/` |

If a scenario prompt keeps needing stages, handoffs, or durable artifacts, it should be promoted into a system rather than growing into a badly organised one.

## Design principles

- Fast to start: no required intake ritual.
- Evidence over guessing; explicit `verified` / `inferred` / `unknown`.
- Safe defaults: do not make things worse to make progress.
- Clear stopping point and completion criteria.
- Composable as a precursor to a deeper system (e.g. debugging → refactoring, incident → postmortem).
