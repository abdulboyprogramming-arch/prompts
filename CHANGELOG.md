# Changelog

All notable changes to this prompt library. Versions refer to the library as a whole; individual prompts carry their own versions.

## [2.4.0] — 2026-10-20

Two capabilities that had no coverage at all, both chosen because they cost real money or create legal exposure when improvised.

### Added — `03-domains/cost-engineering/` (4 stages)

- **COST-P01 Visibility** — period, currency, and discount treatment stated; spend broken down by service, environment, owner, and cost type; the unattributed percentage reported as a headline figure rather than a footnote.
- **COST-P02 Waste diagnosis** — findings classified by mechanism (idle, over-provisioned, always-on non-production, egress topology, storage growth, log ingestion, query scans, duplication, licensing, chatty calls), each sized in money with its calculation and its protecting dependency named.
- **COST-P03 Optimisation** — one change at a time per service, reliability tolerance agreed beforehand, health metrics and cost signal both verified, and a saving not treated as real until a billing cycle confirms it.
- **COST-P04 Guardrails** — unit economics with a three-month trend, thresholds with owners and responses, tagging enforced in IaC, lifecycle and scheduling controls, and standing exemptions for reliability and security.

### Added — `04-process/privacy-requests/` (3 stages)

- **PRIV-P01 Data inventory** — identifier variants, ten system classes including the ones usually forgotten (warehouse, search index, queues, APM payloads, vendor copies, backups), per-system queries and hit counts, and an explicit completeness statement.
- **PRIV-P02 Execution** — identity verification, legal-hold clearance, export scoped and redacted, deletion in dependency order verified by fresh queries, backups described honestly with an age-out date, blocked systems escalated rather than skipped.
- **PRIV-P03 Retention** — data classes with a stated basis and period, deletion enforced by mechanism (TTL, lifecycle, rotation) rather than intention, a request path sized to volume, and a verification job that alerts when deletion silently stops working.

### Changed

- Coverage matrix: two new dimension rows (cost / FinOps, privacy / subject rights); totals now 63 adequate / 33 partial / 4 missing.
- Root routing table, section READMEs, roadmap, and gallery updated.

### Result

343 Markdown files, 273 prompts: 104 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.3.0] — 2026-10-20

### Added / promoted — safe refactoring (7 stages, operational)

`02-engineering/refactoring/` was the largest remaining skeleton and covers the most frequently performed risky change in software.

- **REF-P01 Assessment** — refuses to start without a measurable target ("one place to change the tax rule instead of four"), classifies the request as refactor / rewrite / repair / optimisation / feature-in-disguise, and records stop conditions before any code moves.
- **REF-P02 Strategy** — technique chosen against the deployment constraint (preparatory, branch-by-abstraction, strangler, parallel run, or explicitly-treated-as-rewrite), slices that keep the trunk green, seams introduced before moves, reversal points, and an estimate sized against the stop conditions.
- **REF-P03 Safety net** — characterisation tests that assert current behaviour (including behaviour that looks wrong), golden-master corpora, contract tests at seams, and a **mutation probe per important test**; a net that has not been shown to catch breakage blocks execution.
- **REF-P04 Execution** — one mechanical transformation per commit, green after each, diff size checked against the budget, behaviour changes excluded and logged.
- **REF-P05 Validation** — golden-master diff including hold-out inputs, contract-surface diff, post-move mutation probe, differential or shadow comparison, performance delta, and a measurement of the P01 target.
- **REF-P06 Cleanup** — observation window before removal, three-signal evidence of non-use, removal in dependency order (flag last), documentation and diagrams updated, follow-ups routed.
- **REF-P07 Orchestrator** — gates with artifacts, failure routing (red net → revert slice; behaviour change → separate; target unmet → reassess, not re-execute), and scope-drift protection.

### Changed

- Coverage matrix: technical debt and maintenance rows move to adequate; dimension totals now 61 adequate / 33 partial / 4 missing.
- Roadmap marks refactoring complete; backend is now the highest-value remaining skeleton.

### Result

266 prompts: 97 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.2.0] — 2026-10-20

### Added

- **`GALLERY.md`** — a single index of every prompt (266) with a direct link and one line describing when to use it, grouped by area and system, with maturity and risk class per row, plus the seven `00-core` reference documents. Generated from the prompt files, so it cannot drift from them.
- **`scripts/generate_gallery.py`** — builds the gallery. Purpose text comes from the prompt's `Gallery:` metadata line if present, otherwise from the first usable line of its objective (role prose and prohibitions are skipped), otherwise its `Produces:` value. `--write` regenerates; `--check` fails when the file is stale.
- **CI gate**: the workflow now runs `--check`, so adding or renaming a prompt without regenerating the gallery fails the build.

### Changed

- Five scenario skeletons (`quick-fixes`, `performance-investigation`, `legacy-code`, `onboarding`, `pr-authoring`) had ad-hoc headers (`**Version:**`, `**Type:**`, `**Use when:**`) and were invisible to the catalog and gallery. They now carry standard metadata with identifiers `QUICK-01`, `PERF-01`, `LEGACY-01`, `ONBOARD-01`, `PR-01`, maturity `skeleton`, version `0.1.0`.
- Validator: `_meta/` is no longer counted as prompts (the template is tooling, not a prompt), and any new Markdown file that is neither a prompt nor an allowed document now fails validation with an actionable message — closing the hole that hid those five files.
- `AGENTS.md`, `CONTRIBUTING.md`, and `_meta/prompt-authoring-standard.md` document the gallery step, the optional `Gallery:` field, and the `<!-- not-a-prompt -->` marker.

### Result

334 Markdown files, 266 prompts: 90 operational, 6 draft, 170 skeleton. Validator 0 errors / 0 warnings.

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
- `07-workflows/cross-layer-integration.md` — contract reconciliation before wiring, seam table with auth and failure contracts, transport/config diffs, end-to-end journey, per-seam failure injection, explicit unproven list.
- `04-process/decommissioning/` (4 stages) — consumer discovery that does not accept "no traffic" as evidence, notice periods derived from constraints, staged reversible shutdown with a quiescence window, and per-asset retirement with verified archives and revoked identities.
- `04-process/governance-compliance/` (3 stages) — claim-to-mechanism control map, evidence testing with population/sample sizes and mechanism bypass attempts, and a readiness decision offering fix/instrument/accept/stop-claiming per gap.
- `07-workflows/multi-agent-orchestration.md` — decomposing work across agents: interface freezing before fan-out, single ownership of shared files, fixed status-report form, per-task verification before dependents unblock, and independent verification of the merged result.

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
- 4 dimension scenarios remain missing (data engineering, mobile, embedded, desktop/CLI); no critical workflow is unprocedured, though five remain partial.

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
