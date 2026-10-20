# Changelog

All notable changes to this prompt library. Versions refer to the library as a whole; individual prompts carry their own versions.

## [2.11.0] — 2026-10-20

### Promoted — `04-process/documentation/` (8 stages, operational)

The system existed as eight 800-byte outlines and its README claimed "Operational (v1.0)". It now does what the claim said, and covers the document products the library was missing: SRS, technical design/RFC, ADR, engineer handbook, API reference, runbook, quickstart, and PDF/DOCX delivery.

- **DOC-P01 Context & products** — a fixed product vocabulary with, per product, the reader, what must and must not appear, the source of truth, the delivery format, a mechanically checkable completion test, and an owner. Hybrid "spec+design+guide" documents are split, because the client and the engineer cannot approve the same page.
- **DOC-P02 Inventory & truth audit** — existence is not truth: commands are run, links resolved, endpoints compared to the spec, and every document gets a verdict (*accurate / partially / outdated / misleading / unverifiable*) with the check that produced it. Missing documentation is expressed as a failed reader task.
- **DOC-P03 Audience & structure** — personas from evidence, jobs with completion tests, task-first structure, one canonical page per instruction, and reading paths that act as the completeness test.
- **DOC-P04 Gap analysis** — gaps typed (missing/wrong/outdated/unfindable/unusable/duplicated/unsafe) and ranked by consequence, with **S1 reserved for pages that can cause harm when followed**; the high-consequence material (runbooks, security, destructive operations) is reviewed first regardless of the request.
- **DOC-P05 Plan** — sequence by consequence and path completion, an acceptance test and an owner per deliverable, and a **maintenance mechanism per document class with its blind spot stated** (generated reference cannot catch a stale spec; a doc test cannot catch a manual step).
- **DOC-P06 Writing** — per-product authoring contracts (an SRS contains no design; a requirement is testable or it is a wish; ADRs are superseded, never edited; runbooks carry expected output and escalation). Every command is executed or explicitly labelled unverified; never document unbuilt behaviour.
- **DOC-P07 Review, export, publish** — re-execute the author's claims, walk the paths as a reader, build PDF/DOCX **from source** and inspect every page (code wrapping, table overflow, missing images, glyphs, contents/anchors), verify PDF accessibility basics, and record the approval before external publication.
- **DOC-P08 Orchestrator** — five shapes (broken page, new product, documentation debt, structure problem, delivery problem), the source-of-truth gate, the reader gate, and the publication gate.

### New scenario — `05-scenarios/live-surface-audit/` (`SURFACE-01`)

Auditing something you can only reach over the network: a URL, host, or API. Rules of engagement before the first request; baseline with TLS and headers; redirects traced hop by hop; header/cookie/CORS/disclosure checks **on the final response** (not an intermediate CDN hop); error behaviour sampled for soft-404s and leakage; API contract signals; performance and accessibility/SEO at the signal level with the tool named; every finding carrying a request/response excerpt and a confirmed/suspected label. It explicitly excludes exploitation, enumeration by wordlist, load generation, and third-party targets without permission — and routes those to `02-engineering/security-hardening/`.

### Fixed — 17 system READMEs claimed "Operational (v1.0)" over skeleton stages

The validator checked prompt overclaims but not *system* overclaims. All 17 are corrected to state their real maturity, and a new validator rule fails the build when a system README claims Operational/Production-ready while any of its own stage prompts is skeleton or draft. Verified by reverting one README and confirming the error fires.

### Result

362 Markdown files, 287 prompts: 132 operational, 6 draft, 149 skeleton. Validator 0 errors / 0 warnings.

## [2.10.0] — 2026-10-20

### New system — `04-process/feature-flags/` (5 stages, operational)

Runtime switches are branches that bypass code review, deployment approval, and version control. The library had nothing governing them: no inventory discipline, no safe-default rule, no rollout evidence standard, no removal procedure. Backlog item 1, open since the first cycle.

- **FF-P01 Inventory & risk** — reconcile three sources (code, provider console, config) and treat every disagreement as a finding; type flags by *usage site*, not name, distinguishing release, kill-switch, permission, experiment, and migration, each with a different expected lifetime; audit every kill-switch for operator, off-path effect, and exercise history; rank by consequence; state blind spots and sampling.
- **FF-P02 Design & defaults** — justify the flag against four legitimate reasons or don't add it; route entitlement gates out of the flag system into the policy layer; name for removal; make the default a safety property (what happens when the provider is unreachable); stable bucketing for percentage rollouts; owner, expiry, and removal criteria at creation; both-states and flag-mechanics tests.
- **FF-P03 Progressive rollout** — guardrail thresholds and sample-size reasoning **before** exposure; cohort ladder before percentage ladder; numeric decision rule per stage; tested reversal including data already written; confounders recorded; a 100% rollout with the flag still present is only half done.
- **FF-P04 Kill-switch use** — state the symptom as a number, predict the effect, flip once, measure against the prediction, and classify the outcome (as predicted / no effect / worse); check that the off-path does not orphan data; record the flag state you leave behind. "No effect" is the most valuable result, because it redirects the investigation.
- **FF-P05 Retirement** — evidence of permanence rather than intent; delete the losing branch, tests, fixtures, and docs (a leftover conditional silently changes behaviour); check readers before removing a writer; decide the safety property explicitly when a kill-switch dies; add a prevention mechanism or ticket.

### Changed

- `04-process/README.md` and root routing table: feature-flags row and two routing entries; the duplicate stale `code-review` skeleton row is gone.
- Coverage matrix: new row "feature flags and progressive delivery" (adequate); totals 68 adequate / 32 partial / 4 missing.
- Backlog item 1 → **Implemented**.

### Result

361 Markdown files, 286 prompts: 123 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings.

## [2.9.0] — 2026-10-20

### Changed — input declarations across the operational library (backlog item 25)

Prompts described what they needed in prose ("the repository path", "a named approver"). They now declare it: **109 of 118 operational prompts** carry an `**Inputs:**` line, and every declared name appears as a `{{PLACEHOLDER}}` in the body.

The retrofit used each prompt's own §3 as the source of truth — no invented requirements:

- A value the user supplies became a canonical name and a placeholder: "Repository path" → `{{REPO_PATH}}`; "Named approver for Category C actions" → `{{APPROVER}}`; "Change window for production-affecting changes" → `{{CHANGE_WINDOW}}`.
- An upstream artifact stayed a dependency, not an input: `.qa/QA_CONTEXT.md`, `SAFETY_NET.md`, `.db/PREFLIGHT.md` are still `Depends on`.
- Systems retrofitted: code review (6), git operations (5), testing/QA (6), release engineering (4), observability (5), dependency management (5), decommissioning (4), governance (3), privacy (3), audit (4), refactoring (7), security hardening (5), project recovery (5), feature completion (3), database (5), payments (3), cost engineering (4), AI/agentic (5), scenarios (6), workflows (3), general agent (15).

**Nine operational stages deliberately declare no inputs** — `AUDIT-P02..P05`, `AUDIT-P07`, `FC-P02`, `REC-P03`, `SEC-P03`, `QA-P03`. They consume only the previous stage's artifact; a declaration would be unused, which the convention treats as a defect. The decision is recorded in `_meta/prompt-inputs.md` and backlog item 27 so a later reviewer does not "fix" it.

### Added

- `_meta/prompt-inputs.md`: **Canonical names** table, a three-tier taxonomy of the 97 names in use (13 core, 25 cross-system, 59 system-scoped), and a rewritten migration-status section with the exact figures and the list of nine exempt stages.
- `00-core/inputs/RUN-SHEET.md`: guidance for system-scoped names, and the alias rule.
- `01-contribution/open-source/general-agent/README.md`: an Inputs table mapping `MY_DETAILS.txt` to declared names, and an honest status line replacing "Complete and ready for use".

### Backlog

- Item 25 → **Implemented**.
- Item 26 (97 names is a wide vocabulary; consolidation pass) → Discovered, P2.
- Item 27 (nine artifact-only stages) → Evaluated, justified non-implementation, P3.

### Result

355 Markdown files, 281 prompts: 118 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings. Coverage matrix 67 adequate / 32 partial / 4 missing.

## [2.8.0] — 2026-10-20

### Promoted — `04-process/code-review/` (6 stages, operational)

The highest-frequency engineering activity in the library was a skeleton: stage names with no evidence rule, no severity vocabulary, and no way to distinguish a review from a list of opinions.

- **CR-P01 Context** — intent before judgement; scope metrics; change-type taxonomy; risk surface named before reading; review depth proportional to risk.
- **CR-P02 Understanding** — three passes (structure, semantics, detail) with deletions and renames read first; diff reconciled against stated intent, recording both extra and missing scope; one real path traced; untested areas and unknowns listed.
- **CR-P03 Findings** — every finding carries a consequence and evidence; `blocker` reserved for harm (data loss, security, broken behaviour, unverifiable claims); the category checklist covers authorisation, boundaries, error paths, concurrency, data, secrets, tests, contracts, operations; tests probed by mutation; an explicit accepted list so a clean review is still credible.
- **CR-P04 Feedback** — observation → consequence → request, with nit/question/blocker markers, findings ordered by consequence, duplicates consolidated, specific praise, and a summary that states an explicit decision.
- **CR-P05 Follow-up** — fixes re-verified rather than accepted; regressions reopened; every finding ends in a state; deferrals need an owner and a ticket; reviewers concede explicitly when the author is right.
- **CR-P06 Orchestrator** — triage into trivial/standard/high-risk/unreviewable, five gates, domain routing to `SEC-*`, `PAY-*`, `DB-*`, `DEP-*`, and disclosure of unreviewed areas.

### Changed

- Coverage matrix: review row moves from partial to adequate; totals 66 adequate / 33 partial / 4 missing.
- Root routing table, `04-process/README.md`, review log updated.

### Result

281 prompts: 118 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings.

## [2.7.0] — 2026-10-20

Two gaps found by asking questions the library could not answer: "what do I do when a merge conflicts?" and "which repository is 'the target area'?"

### Added — `04-process/git-operations/` (5 stages)

Git had only ever appeared as a prohibition ("never force-push") and a publication step. The situations themselves had no procedure.

- **GIT-P01 State check** — read-only, mandatory before any destructive command: detects the five in-progress operation markers (merge, rebase, cherry-pick, bisect, revert), inventories uncommitted and unpushed work, stashes and worktrees, records a reflog snapshot with its expiry, assesses whether the branch is shared, and takes three-way backups of work at risk.
- **GIT-P02 Conflicts** — classifies conflicts by type (textual, modify/delete, both-added, rename, binary, submodule, lockfile), requires each side's intent to be stated before editing, forbids wholesale `--ours`, regenerates lockfiles rather than merging them, and searches for semantic conflicts the merge cannot see.
- **GIT-P03 History repair** — gates on whether history is shared and who authorised it; prefers a corrective commit over a rewrite; backs up before the first rebase command; uses `--force-with-lease` only; mandates **rotate the secret before purging it**, and records the old→new SHA map so dropped commits are named rather than lost.
- **GIT-P04 Recovery** — preserve evidence (`reflog` dump, `.git` copy) before diagnosing; a symptom→cause→mechanism table covering reset, deleted branch, rebase drop, stash loss, force push, detached HEAD, committed deletion; recovers to a *new* ref so recovery cannot create a second casualty; forbids `gc`/`prune` mid-recovery.
- **GIT-P05 Hygiene** — observes current practice before prescribing, picks one merge strategy, sets review gates with an enforcement mechanism per rule (or an honest "convention only"), and covers lockfiles, binaries, submodules, line endings, and secret scanning.

### Added — prompt inputs and variables

- `_meta/prompt-inputs.md` — normative convention: `**Inputs:** NAME, NAME` in metadata, `{{NAME}}` in the body, defaults and fallbacks stated in §3, `SECRET_` naming for sensitive values, and the anti-patterns ("ask the user for anything you need", inputs that duplicate what the repo already states).
- `00-core/inputs/RUN-SHEET.md` — a fill-in sheet per engagement, with a mandatory `OUT_OF_SCOPE` line, minimal sheets for six common situations, and the rule that prompts echo the sheet into their output.
- Validator: an undeclared `{{PLACEHOLDER}}` is an error, an unused declaration is a warning, malformed or lowercase names are errors, and fenced blocks are ignored so examples are never validated.
- `scripts/new_prompt.py --inputs` writes the declaration; the authoring standard, template, `AGENTS.md`, and `CONTRIBUTING.md` document the convention.

### Changed

- Coverage matrix gains two rows (version control operations: adequate; prompt input configuration: partial, because only new prompts declare inputs).
- Backlog gains eleven entries, including the inputs retrofit (P1), shallow/partial clone support (P2), LFS migration (P2), and signed-commit provenance (P2).

### Result

355 Markdown files, 281 prompts: 112 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.6.0] — 2026-10-20

### Added — `03-domains/payments/` (3 stages)

Money is the one domain where a defect is a financial loss rather than a bad experience, and it had no coverage.

- **PAY-P01 Money model** — representation inventory that flags floats and missing currency dimensions, rounding and allocation rules where the parts must sum exactly to the whole, the payment state machine including out-of-order provider events, and invariants written as runnable checks.
- **PAY-P02 Idempotency & unknown outcomes** — a failure table per money-moving flow (lost response, delayed webhook, duplicate delivery, crash mid-write), idempotency keys persisted before the call and reused on retry, webhook replay and ordering safety, concurrency guards at the database level, and the rule that "unknown" is its own state rather than being treated as failure.
- **PAY-P03 Reconciliation & change safety** — per-transaction and aggregate comparison against provider settlement, a six-class difference taxonomy (timing, missing locally, phantom success, amount, duplicate, state), repairs that never re-charge, automated daily reconciliation with alerts, fee/FX treatment, and an eight-item checklist for every future money change.

### Changed

- Coverage matrix gains a money-correctness row; totals 64 adequate / 33 partial / 4 missing.
- Root routing table and `03-domains/README.md` updated.

### Result

347 Markdown files, 276 prompts: 107 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.5.0] — 2026-10-20

### Added — library tooling

- **`scripts/find_overlaps.py`** — near-duplicate detection across all prompts using 5-word shingles after stripping metadata, code fences, and shared boilerplate sections. Reports containment (how much of the smaller prompt appears in the larger) and Jaccard similarity; `--check` fails CI at 0.55 containment. First run: no duplicated content, highest containment 0.18 inside the templated contribution skeletons (recorded as a backlog item).
- **`scripts/new_prompt.py`** — scaffolds a prompt with the correct metadata block and all ten required sections, picks the version from the requested maturity, refuses to overwrite, and prints the catalog/gallery/overlap commands.

### Changed

- CI now runs the overlap gate.
- `AGENTS.md` and `CONTRIBUTING.md` document the scaffolder and the overlap check; the authoring standard remains the reference for content.
- Backlog records fourteen newly identified engineer problems with priority and home (feature-flag lifecycle, live-API versioning, queue backpressure, environment parity, test data, build performance, payment correctness, accessibility, i18n, estimation, incident follow-through, on-call handover, prompt A/B evaluation, contribution-system overlap).

### Result

273 prompts: 104 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings; overlap check clean.

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
