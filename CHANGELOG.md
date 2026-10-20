# Changelog

All notable changes to this prompt library. Versions refer to the library as a whole; individual prompts carry their own versions.

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
- `PROJECT-STATUS.md` — continuation checkpoint.
- `AGENTS.md` — repository-level instructions for AI agents working in this repository.

### Rewritten to operational depth

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

- 172 prompts remain `skeleton`. They outline a defensible sequence but cannot run unsupervised. See the backlog.
- No prompt in this library has been empirically tested against a real repository and recorded. All `operational` labels are structural reviews.
- No CI workflow runs the validator yet.
