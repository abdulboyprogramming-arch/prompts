# Changelog

All notable changes to this prompt library. Versions refer to the library as a whole; individual prompts carry their own versions.

## [2.1.0] — 2026-10-20

Gap-discovery cycle driven by a new coverage matrix rather than the existing roadmap. Five systems and one workflow were added; three missing scenarios in the previous audit are closed.

### Added

- `_meta/coverage-matrix.md` — 12-dimension coverage assessment (97 dimension rows, 14 workflow rows) with a status and evidence pointer per row, an end-to-end assessment of 14 critical workflows, and a computed summary. A scenario counts as adequate only when a prompt addresses its distinctive verification and failure handling.
- `03-domains/database/` (5 stages) — schema truth, migration design with an old/new code compatibility matrix, pre-flight validation on a realistic copy with a performed restore drill, execution with reconciliation, rollback and post-verification.
- `04-process/dependency-management/` (5 stages) — dependency inventory and risk, breaking-change assessment matched to actual code usage, one-family-per-commit execution with lockfile discipline, verification with mutation probing, and a written update policy.
- `02-engineering/feature-completion/` (4 stages) — a 14-layer completion checklist, layer gap map against an analogue, end-to-end implementation, and acceptance tested per role with direct endpoint access.
- `07-workflows/independent-verification.md` — adversarial verification of another agent's completion claims: claim extraction, clean-state reproduction, mutation probing, diff audit for undeclared scope and weakened tests.
- `05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md` — attempt ledger, failure classification, and a decision to revert, re-scope, narrow, or escalate instead of patching again.
- `05-scenarios/data-loss/DATA-LOSS-RECOVERY.md` — freeze writes, preserve evidence, bound the window, restore to a side instance and merge, with a loss statement separating recovered / lost / uncertain.
- `05-scenarios/security-incident/SECURITY-INCIDENT.md` — evidence-first response for an active compromise: containment strategy trade-offs, persistence search, verified eradication against a baseline, disclosure decision record.

### Changed

- `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md` → v1.2.0, after the library's first empirical execution (`_meta/empirical-evaluation-01.md`): treat a green suite as evidence it encodes the bug, vary invocation context when localising, ordered hypothesis classes led by shared mutable state, and a required explanation of why the existing tests missed the defect.

- Root README routing table extended with verification, failed-fix, database, dependency, and feature-completion entries.
- `_meta/ROADMAP-AND-BACKLOG.md` restructured: completed items marked, and a new "Discovered in 2.1.0" section with nine opportunities, their priority, and five rejected/deferred ideas with reasons.
- `_meta/coverage-matrix.md` summary counts are computed from the tables, not estimated.
- Validator: risk-class heuristic no longer flags descriptive mentions of deployment; backticked repository paths are checked for existence.

### Fixed

- Four `06-interactive` prompts had no metadata block and were invisible to the catalog; migrated.

### Known limitations

- 165 prompts remain `skeleton`.
- No prompt has been empirically executed against a real repository; structural validation is not empirical validation.
- 6 dimension scenarios and 2 workflows remain missing, listed by priority in the coverage matrix.

## [2.0.0] — 2026-10-20

This release reconciles the library's claims with its artifacts, establishes enforceable standards, and adds the systems that were most conspicuously missing. It is a breaking change for anyone who trusted the previous status tables: most systems are now labelled `skeleton` because that is what they are.

### Added

- `_meta/prompt-authoring-standard.md` — metadata schema, four maturity levels, nine execution modes, twelve required sections, writing rules, definition of done.
- `_meta/quality-rubric.md` — 100-point rubric with band anchors, three mode-specific weightings, nine critical failure conditions, review-record format.
- `scripts/validate_library.py` — validates metadata, identifiers, maturity/version consistency, required sections, links (Markdown and backticked repo paths), empty sections, risk-class honesty, and status overclaims; generates `_meta/CATALOG.md`.
- `07-workflows/` — five composed workflows (`recover-abandoned-project`, `audit-to-remediation`, `production-incident`, `greenfield-delivery`, `continuous-improvement`) plus `HANDOFF-CONTRACT.md`.
- `02-engineering/project-recovery/` — seven-stage system for inherited, interrupted, or broken projects (containment → intent → completeness → integration → plan → execution → acceptance).
- `04-process/observability-reliability/` — five stages: assessment, instrumentation, SLOs/alerting, on-call/runbooks, postmortem.
- `04-process/release-engineering/` — four stages: readiness, versioning/changelog, deployment/rollback, post-release verification.
- `03-domains/ai-agentic/` — five stages: context/risk, architecture, evaluation, safety/guardrails, production operations.
- `05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md`.
- `.github/workflows/validate-library.yml` — runs the validator and fails if the generated catalog is stale.
- `PROJECT-STATUS.md` — continuation checkpoint.
- `AGENTS.md` — repository-level instructions for AI agents working in this repository.

### Rewritten to operational depth

- `02-engineering/security-hardening/` — all seven stages rebuilt around an authorisation gate, concrete abuse cases, an ingress-by-ingress enforcement matrix, triage that admits only confirmed S1/S2 findings, and remediation proven by failing-before tests and a route × role matrix.
- `02-engineering/codebase-audit/` — all nine stages rebuilt with a shared evidence standard, severity model with required evidence per level, finding schema, adversarial synthesis gate, and a report structure that includes risk of inaction and coverage limits.
- `04-process/testing-qa/` — all seven stages rebuilt with R1–R4 risk prioritisation, a coverage rule that rejects percentage-chasing, mutation spot checks, and a mandatory plan checkpoint.
- `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md` — reproduction, minimisation, explicit hypotheses, fix-proven-by-revert, regression test.
- `05-scenarios/incident-response/PRODUCTION-INCIDENT.md` — restore-first ordering, timeline discipline, data-integrity verification, postmortem handoff.

### Changed

- All 235 prompt files now carry a metadata block (`Identifier`, `System`, `Version`, `Maturity`, `Execution mode`, `Risk class`, `Depends on`, `Produces`).
- Versions of skeleton prompts reset to `0.1.0`; `1.x` is reserved for reviewed prompts.
- Root `README.md`, `CONTRIBUTING.md`, and section READMEs rewritten around actual maturity and discovery paths.
- `_meta/taxonomy.md` extended with `07-workflows`, `scripts`, the maturity axis, and rules preventing empty folders.
- `00-core/prompt-engineering/STAGE-PROMPT-TEMPLATE.md` reduced to a pointer to the single canonical standard.
- `04-process/README.md`, `05-scenarios/README.md`, `06-interactive/README.md` corrected and extended.

### Fixed

- Two system READMEs advertised `Operational` while all their stages were 20-line outlines.
- Root README claimed "the most complete ... archive" and "production-ready" systems that did not exist; replaced with a status table that states maturity.
- Empty "Planned / Future" sections removed; plans moved to `_meta/ROADMAP-AND-BACKLOG.md`.

### Removed

- Competing prompt template in `00-core/` (now a pointer), eliminating two divergent definitions of a valid prompt.

### Known limitations

- 165 prompts remain `skeleton`. They outline a defensible sequence but cannot run unsupervised. See the backlog.
- No prompt in this library has been empirically tested against a real repository and recorded. All `operational` labels are structural reviews.
