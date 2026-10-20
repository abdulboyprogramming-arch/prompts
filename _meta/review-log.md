# Review Log

Records quality reviews that justify a maturity label. Format: `ID · date · tier · score · label`, then the reason and follow-up.

**Independence status:** the reviews below are *author assessments* by the agent that wrote the prompts. They are not independent third-party reviews. A prompt labelled `operational` has been checked against `_meta/quality-rubric.md` and passes the validator; it has not been empirically tested on a real repository unless explicitly stated.

---

## 2026-10-20 — Library-wide baseline

**Scope:** all 293 Markdown files.
**Method:** structural audit, link check, metadata migration, per-file maturity assessment against the standard.
**Outcome:** 172 files demoted to `skeleton`; 1 pre-existing `operational` system retained (open-source general-agent, 16 prompts); adoption of metadata blocks across 235 prompt files.

Notable findings:

- Exactly one system met the pre-existing quality bar; the other multi-stage systems were 5–9 KB of 20-line outlines while their READMEs claimed "Operational" or "Production-ready".
- Two system READMEs advertised operational status with eight skeleton stages each (`01-contribution/web/general`, `01-contribution/web3/general`); corrected.
- No broken relative links existed, and all 201 declared identifiers were unique — the structural hygiene was better than the content depth.
- 111 files were under 800 bytes; median file size was 869 bytes.

---

## System reviews

### `01-contribution/open-source/general-agent` — 16 prompts
- **2026-10-20 · autonomous · 86/100 · operational (retained)**
- Reason: substantive stages with evidence rules, artifacts, and handover; P01 establishes a constitution, P13 gates publication, P16 orchestrates. Depth is real (4.6–13.4 KB per prompt).
- Deductions: identifiers are bare (`P03`) rather than system-namespaced, which weakens cross-library uniqueness as the library grows; no verification section distinguishes "check ran" from "check could not run"; P16 lacks an explicit failure-routing table per stage.
- Follow-up: namespace identifiers in a future major version; add a check-ran/not-run distinction shared across systems.

### `02-engineering/codebase-audit` — 9 stages
- **2026-10-20 · autonomous · 91/100 · operational**
- Reason: complete audit chain with a shared evidence standard, a five-level severity model with required evidence, and an adversarial synthesis gate (P07) that deletes unsupported findings. P01 fixes the commit and sampling policy; P08 requires risk-of-inaction and a confidence statement.
- Deductions: severity calibration examples are thin for non-web systems; P05 depends on network access for vulnerability scanning and degrades (documented).
- Follow-up: add worked findings examples; consider a stage for licence/SBOM.

### `04-process/testing-qa` — 7 stages
- **2026-10-20 · implementation-remediation · 89/100 · operational**
- Reason: risk-first prioritisation (R1–R4), explicit coverage rule rejecting percentage-chasing, mutation spot checks in P06 that force the verifier to test the tests, and a mandatory human checkpoint after the plan.
- Deductions: tool-specific examples (pytest/Jest) are minimal; contract-testing guidance is one paragraph.
- Follow-up: add per-stack appendices; extend contract testing after backend system upgrade.

### `02-engineering/project-recovery` — 7 stages
- **2026-10-20 · autonomous · 90/100 · operational**
- Reason: containment-before-modification, preservation of uncommitted work, intent reconstruction from evidence, three explicit prohibitions, and an acceptance stage that grades `partial`/`not-achieved` honestly. Addresses the most common real-world starting condition the library previously ignored.
- Deductions: no monorepo variant; P02 struggles when history is absent (documented, but the fallback is generic).
- Follow-up: add a monorepo variant and a worked example.

### `07-workflows` — 5 workflows + contract
- **2026-10-20 · orchestration · 78/100 · draft**
- Reason: stages, gates, failure routing, and acceptance criteria are defined per workflow; the handoff contract makes composition concrete.
- Deductions: not yet exercised end to end; cross-system artifact names are reconciled by convention, not by tooling; the multi-agent orchestration workflow is missing.
- Follow-up: run one workflow against a real repository and record the result; add multi-agent coordination.

### `04-process/observability-reliability` — 5 stages
- **2026-10-20 · specialised · 85/100 · operational**
- Reason: signals → SLOs → alerts → runbooks → postmortem chain; burn-rate alerting with rationale; runbook sections that force an action and a verification signal; postmortem caps actions at five and requires owners.
- Deductions: vendor-neutral, so stack-specific implementation (OTel collectors, Prometheus rules) is left to the reader; P03 query validation depends on tooling availability.
- Follow-up: add a Prometheus/OpenTelemetry appendix.

### `03-domains/ai-agentic` — 5 stages
- **2026-10-20 · specialised · 84/100 · operational**
- Reason: covers the three failure modes that make LLM features different (non-determinism, untrusted inputs, fluent wrongness); evaluation before optimisation; explicit statement that the system prompt is not a security boundary; release process for non-code artifacts.
- Deductions: model/provider guidance is deliberately generic; no worked RAG example; judge calibration is described but not demonstrated.
- Follow-up: add a worked evaluation example and a retrieval-tuning stage.

### `04-process/release-engineering` — 4 stages
- **2026-10-20 · audit-remediation · 82/100 · operational**
- Reason: readiness verdict with verifiable conditions, bidirectional changelog truthfulness check, expand/contract migration sequencing, three-layer rollback with honest irreversibility handling, post-release verification against pre-defined criteria.
- Deductions: no per-platform deployment examples; SBOM/provenance is not yet covered.
- Follow-up: add artifact-signing and provenance guidance.

### `05-scenarios/debugging`, `incident-response`, `flaky-tests`
- **2026-10-20 · diagnostic/specialised · 87 / 88 / 86 · operational**
- Reason: hypothesis-driven debugging with minimal reproduction and revert-to-prove; incident response with strict restore-first ordering and data-integrity verification; flake triage that forbids retry-as-fix and requires a denominator.
- Deductions: debugging assumes runnable environment; incident response assumes telemetry exists (degradation documented).
- Follow-up: none urgent.

---

## Pending reviews

All systems listed as `skeleton` in `_meta/CATALOG.md` are unreviewed. Review order follows `_meta/ROADMAP-AND-BACKLOG.md` P1.

### `02-engineering/security-hardening` — 7 stages
- **2026-10-20 · audit-remediation · 88/100 · operational**
- Reason: authorisation gate precedes assessment; threat model requires concrete abuse cases with expected controls; P03 builds an ingress enforcement matrix so a missing control on one route is visible; P04 permits S1/S2 only for `confirmed` findings and forbids payloads; P06 requires a failing-before test and a route × role authorisation matrix, and forbids weakening controls to make tests pass.
- Deductions: framework-specific examples are absent; supply-chain review is one section rather than a stage; compliance mapping is out of scope by design.
- Follow-up: add worked examples for one ORM and one middleware framework; add SBOM/signing guidance.

---

## 2026-10-20 — Addendum cycle (2.1.0)

**Trigger:** independent gap-discovery pass against a 12-dimension coverage matrix (`_meta/coverage-matrix.md`), not against the existing roadmap.

### `03-domains/database` — 5 stages
- **2026-10-20 · audit-remediation · 90/100 · operational**
- Reason: the only routine change that can destroy unrecoverable value. P01 establishes schema truth (live vs migrations vs models) before anything is designed; P02 requires a compatibility matrix proving both old and new code run against every phase; P03 makes the migration fail on a staged copy, demands a *performed* restore drill, and measures lock duration under load; P04 enforces reconciliation with numbers; P05 states when rollback stops being possible.
- Deductions: engine-neutral, so PostgreSQL/MySQL specifics are notes rather than procedures; no drift-detection tooling ships with it.
- Follow-up: add per-engine appendices; add a data-corruption recovery prompt (identified as a missing scenario).

### `04-process/dependency-management` — 5 stages
- **2026-10-20 · audit-remediation · 87/100 · operational**
- Reason: closes the highest-frequency missing workflow. Distinguishes security/unsupported/blocking/planned upgrades; requires each breaking change to be matched to code usage with counts; forbids hand-edited lockfiles and one-commit-everything upgrades; verification includes mutation probing and an independent lockfile audit; P05 converts episodic upgrades into policy with owners and dates.
- Deductions: no per-ecosystem codemod catalogue; supply-chain integrity measures are listed but not fully procedural (no SBOM stage).
- Follow-up: add SBOM/signing guidance when the release system gains provenance support.

### `02-engineering/feature-completion` — 4 stages
- **2026-10-20 · implementation · 88/100 · operational**
- Reason: targets a specific, observable failure mode — features finished at the visible layer only. The 14-layer checklist makes "not applicable" an explicit decision, the layer map requires an analogue and evidence of absence, and acceptance requires testing as each role with direct endpoint access rather than through the UI.
- Deductions: assumes the design intent exists; a genuinely ambiguous feature stops at P01 (by design, but it means the system cannot resolve product questions).
- Follow-up: add a worked example using a CRUD feature.

### `07-workflows/independent-verification.md`
- **2026-10-20 · diagnostic · 90/100 · operational**
- Reason: the library previously asked agents to grade their own work. This workflow makes verification adversarial in a useful way: claims extraction including implicit claims, clean-state reproduction, mutation probing of new tests, and a diff audit for undeclared scope, weakened tests, and dependency changes. It is the missing control for an ecosystem where agents report completion.
- Deductions: cannot verify what it cannot run; verdict ceiling is `verified with gaps` in that case (stated).
- Follow-up: pair it with the empirical test harness when that exists.

### `05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md`
- **2026-10-20 · diagnostic · 87/100 · operational**
- Reason: addresses the repeated-patching spiral with an attempt ledger, a failure classification (wrong model / wrong reproduction / wrong layer / untested assumption / incomplete / regression), and a decision to revert, re-scope, narrow, or escalate. Reverting is legitimised, which is the behaviour most agents lack.
- Deductions: depends on an accurate attempt history; when that is missing, the ledger is reconstructed from git and is partial.
- Follow-up: none urgent.

### Library-level reassessment
- Coverage matrix created with 12 dimensions, 97 dimension rows and 14 workflow rows, each with an evidence pointer. Current honest totals: 52 adequate / 38 partial / 7 missing (dimensions), 7 adequate / 5 partial / 2 missing (workflows).
- Nine new opportunities discovered this cycle are recorded in `_meta/ROADMAP-AND-BACKLOG.md` §"Discovered in 2.1.0", including three rejected ideas with reasons.
- **Still not done:** no empirical execution of any prompt against a real repository. This remains the single largest credibility gap and is now item P0 in the backlog.

### `05-scenarios/data-loss/DATA-LOSS-RECOVERY.md`
- **2026-10-20 · specialised · 89/100 · operational**
- Reason: the highest-consequence scenario in the matrix. Enforces containment before diagnosis, evidence preservation before cleanup, restore to a side instance instead of over live data, merge that preserves post-incident legitimate writes, and a loss statement that separates recovered / lost / uncertain. Distinguishes loss types (deletion, overwrite, corruption, migration damage, hardware, malicious) because each has a different route.
- Deductions: engine-neutral, so PITR mechanics are described procedurally rather than as commands; legal notification is flagged, not resolved (correctly out of scope).
- Follow-up: pair with an engine-specific appendix if demand appears.

### `05-scenarios/security-incident/SECURITY-INCIDENT.md`
- **2026-10-20 · specialised · 90/100 · operational**
- Reason: closes a real gap — the library had assessment/remediation (`SEC-P01..P07`) but nothing for an active compromise, where the correct first move (preserve evidence) is the opposite of the availability playbook. Includes the containment-strategy trade-off table, persistence search, access-vs-exfiltration discipline, eradication against a known-good baseline, rotation verification, and a disclosure decision record that stops short of legal advice.
- Deductions: no forensic tooling detail by design (tool-specific depth ages badly); insider case handled as an escalation, not a procedure.
- Follow-up: add an evidence-collection appendix per platform if the library gains platform appendices.

### Coverage movement (2.1.x)
- Dimension rows: 55 adequate / 36 partial / 6 missing (from 52/38/7 at the start of the cycle).
- Workflows: 7 adequate / 5 partial / 2 missing — unchanged by this batch.
- Remaining missing: decommissioning, enterprise readiness, data engineering, mobile, embedded, desktop/CLI, cross-layer integration, prototype discipline, and (outside the table) the empirical test harness.

### Empirical evaluation 01 (`DBG-01`, v1.1.0 → v1.2.0)
- **2026-10-20 · first executed prompt · 20 min · synthetic fixture · evaluator = prompt author**
- Method: fixture with a mutable-default-argument state leak and a green test suite; protocol followed step by step; every step produced something.
- Outcome: defect reproduced in 2 min, cause proven by instrumentation (not code reading), fix verified by reverting it, regression test red→green. Three weaknesses found and fixed: (1) a green suite while a defect exists is now treated as evidence that the tests encode the buggy behaviour; (2) localisation now requires varying invocation context, and step 5 gains an ordered hypothesis-class list led by shared mutable state; (3) a new step requires explaining why the existing tests missed the defect.
- Honest limits: one defect, one language, one evaluator who knew the fixture. Not a validation study, and no claim of superiority over unprompted debugging.
- Follow-up: fixture set + scoring sheet; fixtures authored by someone other than the prompt author.

### `07-workflows/cross-layer-integration.md`
- **2026-10-20 · specialised · 88/100 · operational**
- Reason: the characteristic failure it targets — every layer "done", product broken — was invisible in the library. Reconciles the contract before wiring infrastructure (where most time is wasted), enforces a seam table with auth and failure columns, tests through the transport rather than the function, and requires per-seam failure injection plus a "not proven" list.
- Deductions: no language-specific client-generation recipes; assumes the layers can be composed locally if no integration environment exists.
- Follow-up: add a worked example with a generated client.

### `04-process/decommissioning/` — 4 stages
- **2026-10-20 · specialised · 88/100 · operational**
- Reason: the library covered construction exhaustively and removal not at all, despite removal being irreversible. P01 rejects "no traffic in the logs" as proof and enumerates consumer classes that leave no trace (batch jobs, partners, pipelines, BI). P02 derives the notice period from constraints instead of defaulting to 90 days. P03 stages shutdown with reversal at every step and a quiescence window. P04 decides per asset, with archive verified by restore and identities revoked and confirmed dead.
- Deductions: no platform-specific teardown commands (by design); legal retention is escalated, not decided.
- Follow-up: link P04's asset inventory to `03-domains/database`'s destructive register.

### Coverage movement after integration + decommissioning
- Dimension rows: 57 adequate / 36 partial / 5 missing.
- Workflow rows: 8 adequate / 5 partial / 1 missing.
- Remaining missing: enterprise readiness (dimension + workflow), data engineering, mobile, embedded, desktop/CLI, plus prototype discipline and duplicate detection outside the table.

### `04-process/governance-compliance/` — 3 stages
- **2026-10-20 · audit-remediation · 86/100 · operational**
- Reason: enterprise obligations were the last workflow-level missing scenario. P01 separates the claim from the mechanism and from the evidence (a policy document is a claim about a mechanism, not a control). P02 tests operations with population/sample sizes, mechanism bypass attempts, and a quiet-failure checklist (approvals after merge, self-approval, skipped CI, alerts routing nowhere). P03 forces one of four responses per gap and produces per-claim readiness statements in questionnaire language, explicitly refusing to certify.
- Deductions: no framework clause mapping (SOC 2/ISO tables age badly and encourage mapping theatre); legal interpretation escalated rather than answered.
- Follow-up: add a worked evidence index example.

### `07-workflows/multi-agent-orchestration.md`
- **2026-10-20 · orchestration · 88/100 · operational**
- Reason: the master brief asked for multi-agent patterns, and the library's orchestration content covered single-run fan-out only. This workflow starts with "should you parallelise at all", freezes interfaces before fan-out, assigns one owner per shared file (the rule that prevents most multi-agent breakage), forbids agents negotiating interfaces pairwise, and requires per-task verification before dependents unblock plus independent verification of the merged result.
- Deductions: no tool-specific agent APIs (deliberate); assumes separate branches/worktrees are possible.
- Follow-up: pair with `independent-verification.md` as the default verification step in the worked example.

### Coverage movement (integration, decommissioning, governance, orchestration)
- Dimension rows: 59 adequate / 35 partial / 4 missing. Workflow rows: 9 adequate / 5 partial / 0 missing.
- Remaining missing dimensions: data engineering, mobile, embedded, desktop/CLI. Every critical workflow now has a procedure.

### Prompt gallery (`GALLERY.md`, `scripts/generate_gallery.py`)
- **2026-10-20 · library capability · generated index**
- Reason: the catalog lists metadata for tooling; nothing answered "which prompt do I want for this situation?" without opening files. The gallery adds a purpose line per prompt, extracted from the prompt's own objective so it cannot go stale.
- Extraction is deliberately conservative: `Gallery:` metadata wins; otherwise the first usable objective line, skipping role prose ("You are…") and prohibitions ("Do not…"), then the first bullet, then `Produces:`, then a title-based fallback for orchestrator prompts. Two prompts needed an explicit `Gallery:` line because their objectives are structural rather than situational (`DATALOSS-01`, `WF-IMPROVE`).
- **Found and fixed while building it:** five scenario skeleton prompts had no identifier and were therefore absent from both the catalog and the gallery. They now carry standard metadata, and the validator fails on any future unindexed Markdown file, so the gap cannot reopen silently.
- Known limitation: the extracted sentence is the prompt's own wording, so rows vary in tone; authors who want better wording add a `Gallery:` line.

### `02-engineering/refactoring/` — 7 stages promoted (skeleton → operational)
- **2026-10-20 · mixed · 88/100 · operational**
- Reason: the most frequently performed risky change in software was the largest remaining skeleton, and the old outlines had no defensible verification. The system now refuses the work without a measurable target (P01), forces a technique chosen against the deployment constraint rather than taste (P02), and treats the safety net as unproven until a mutation probe shows it catches breakage (P03).
- Distinctive decisions: behaviour change is banned from refactoring commits and must be separated; P05 measures the *target*, so a clean refactor that missed its purpose is reported as a failure; P06 forbids leaving two structures in place and requires the observation window before removal.
- Deductions: language-agnostic, so the mechanical-refactoring catalogue is named rather than tool-specific; no automated codemod integration.
- Follow-up: a worked example (extract-a-service or replace-conditional) would help reviewers recognise a good slice plan.

### `03-domains/cost-engineering/` — 4 stages (new)
- **2026-10-20 · audit-remediation · 86/100 · operational**
- Reason: cloud spend was the largest engineering metric with no coverage at all. The system refuses to recommend anything unquantified (P02 requires unit × quantity × time), separates mechanical savings from decisions that trade reliability, and treats a saving as unreal until a billing cycle confirms it (P03). P04 converts the win into guardrails, because optimisation without enforcement decays within a quarter.
- Deductions: no provider-specific pricing or tooling (ages badly, and prices are per-contract); commitments/reserved capacity are treated as financial decisions, not engineering fixes.
- Follow-up: a worked example of `unit cost` for a request-driven service.

### `04-process/privacy-requests/` — 3 stages (new)
- **2026-10-20 · specialised · 88/100 · operational**
- Reason: subject access and deletion requests are recurring, legally bounded, and fail predictably — the warehouse copy, the APM payload, the support ticket, the backup. P01 forces an explicit inventory with queries and a completeness statement; P02 forbids executing on an incomplete map, verifies per system, and refuses to pretend backups were edited. P03 makes retention structural and verifies that deletions actually happen.
- Deductions: legal validity, exemptions, and notification obligations are escalated, not decided; no vendor-specific deletion procedures.
- Follow-up: a self-service design appendix for teams handling high request volume.

### Tooling — overlap detection and scaffolding
- **2026-10-20 · library capability · measured, not asserted**
- `find_overlaps.py` compares every prompt with 5-word shingles after stripping metadata, code fences, and the boilerplate sections all prompts share. It reports containment (share of the smaller prompt found in the larger) and Jaccard.
- **Finding:** no duplicated content exists today. The highest containment is 0.18, between `packages-libraries` and `web3` P02 discovery prompts; the next five pairs are all within the web/web3/packages contribution skeletons. That is a real but mild signal: those three systems are near-variants of one template, and promoting them without differentiation would produce three copies of the same advice. Recorded in the backlog.
- CI runs `--check` at a 0.55 containment bar so genuine duplication fails the build while shared vocabulary does not.
- `new_prompt.py` writes the metadata block plus all ten sections, choosing `0.1.0` for skeletons and `1.0.0` otherwise, refusing to overwrite, and printing the three regeneration commands. Verified by scaffolding a throwaway prompt, validating it cleanly, then removing it.

### `03-domains/payments/` — 3 stages (new)
- **2026-10-20 · specialised · 89/100 · operational**
- Reason: money is the domain where a defect is a loss, not a bad experience, and the library had nothing. P01 treats representation as the first-order problem (floats, missing currency dimension, rounding allocation) and requires invariants that can be run as queries. P02 is built around the failure everyone gets wrong: the *unknown* outcome, which must be a state rather than being treated as failure (double charge) or success (lost payment), with idempotency keys persisted before the call and verified under concurrency. P03 automates reconciliation against the provider, classifies every difference (timing, missing locally, phantom success, amount, duplicate, state), forbids repairing by re-charging, and installs an eight-item change-safety checklist.
- Deductions: provider-agnostic, so API-specific idempotency semantics are cited rather than specified; tax and revenue recognition are explicitly out of scope.
- Follow-up: a worked failure table for a card charge with a lost response would make P02's core artifact easier to copy.

### `04-process/git-operations/` — 5 stages (new)
- **2026-10-20 · mixed · 89/100 · operational**
- Reason: git is the substrate every other prompt runs on, and the library offered only prohibitions. The specific failure this closes: an agent resolving a conflict by taking "ours" across a file, or rewriting shared history because it was technically possible.
- Design: P01 is read-only and mandatory before any destructive command (it checks the five in-progress marker files, unpushed commits, stashes, worktrees, and shared status, and takes three-way backups of uncommitted work). P02 requires stating each side's intent before editing and separates lockfile regeneration from hand-merging. P03 gates on `SHARED_HISTORY`/`APPROVER`, forbids plain `--force`, mandates rotate-before-purge for secrets, and requires an old→new SHA map. P04 acts before it investigates (evidence preservation first) and recovers to a *new* ref. P05 records an observed-then-chosen convention with an enforcement mechanism per rule.
- Deductions: no platform-specific commands (GitHub/GitLab reflog APIs are named, not scripted); LFS migration and signed-commit setup are recorded as backlog rather than written.
- Follow-up: a worked example of a force-push recovery, since that is the case users search for by name.

### Prompt inputs and variables (library capability)
- **2026-10-20 · convention + validator + template**
- Investigation: `{{`/`**Inputs:**`/`REPLACE_ME` occurrences across the library were **zero**; only the general-agent system had an ad-hoc `MY_DETAILS.txt`. Prompts referred to "the user", "the target area", "the repository" in prose, which is exactly what an agent guesses at.
- Implemented: `_meta/prompt-inputs.md` (declaration syntax, placeholder rules, defaults, sensitive inputs, anti-patterns), `00-core/inputs/RUN-SHEET.md` (fill-in sheet with a mandatory `OUT_OF_SCOPE` line and minimal sheets per situation), an optional `Inputs` metadata key, validator rules (undeclared placeholder = error, unused declaration = warning, malformed/lowercase = error, fenced blocks ignored), `--inputs` on the scaffolder, and the authoring standard, template, AGENTS and CONTRIBUTING updated.
- Honest limit: enforcement applies to prompts that declare inputs; the existing library still uses prose and is retrofitted as touched. Recorded as backlog item 25 rather than claimed as complete.

### `04-process/code-review/` — 6 stages promoted (skeleton → operational)
- **2026-10-20 · mixed · 87/100 · operational**
- Reason: the highest-frequency engineering activity in the library was a skeleton with no evidence rule and no severity vocabulary, so a review could not be distinguished from an opinion list.
- Design: P01 forces intent before judgement and makes depth proportional to risk; P02 reads deletions and renames first and reconciles the diff against the stated intent (extra scope and missing scope both recorded); P03 requires a consequence per finding, reserves "blocker" for harm, probes the tests on the main path, and demands an accepted list so an empty review is still credible; P04 uses observation → consequence → request with nit/question/blocker markers; P05 re-verifies fixes rather than accepting "fixed" and requires every finding to end in a state; P06 triages depth and routes domain-specific changes to the domain systems instead of pretending one review covers a migration and a payment path.
- Deductions: no platform-specific API usage (review is described, not scripted); tone guidance is principled rather than exemplified.
- Follow-up: an example review of a 40-line auth change would make the evidence standard concrete.

### Input retrofit — 109 operational prompts
- **2026-10-20 · metadata · 78/100 · operational**
- What changed: `**Inputs:**` plus `{{PLACEHOLDER}}` usage in 109 prompts, sourced from each prompt's existing §3 rather than from new requirements.
- Why it matters: a prompt that says "the repository path" is only runnable by a human reading it. A prompt that declares `{{REPO_PATH}}` can be composed, validated, and replayed.
- What was deliberately not done: nine artifact-only stages were left without declarations; forcing an input there would have produced unused declarations and taught the wrong lesson.
- Deductions: 97 names is more vocabulary than the library needs; some names will merge (item 26). No prompt was executed with a filled run sheet, so "declared" is verified and "runnable end to end" is not.

### `04-process/feature-flags/` — 5 stages (new, operational)
- **2026-10-20 · mixed · 86/100 · operational**
- Problem: the library treated deploys as the unit of risk, but most production behaviour is changed by toggles that never pass through a deploy review.
- Design: P01 forces typing by usage site (a permission gate living in a console is a security finding, not a flag); P02 makes the unreachable-provider default a design decision instead of an accident; P03 requires sample-size arithmetic before exposure, which is where most rollout plans are dishonest; P04 makes the *prediction* the record, so a flip with no effect is evidence rather than a story; P05 treats removal as the stage that reduces complexity and refuses to delete a writer whose readers still exist.
- Deductions: no provider-specific API detail (evaluation semantics differ per vendor); the interaction between flags and mobile clients pinned to old versions is named as a blocker rather than solved.
- Follow-up: a worked example of a 3-stage rollout with the arithmetic would make P03's standard concrete.

### `04-process/documentation/` — 8 stages promoted (skeleton → operational)
- **2026-10-20 · mixed · 88/100 · operational**
- Reason: the system was eight outlines ~800 bytes each while its README said "Operational (v1.0)" — the exact claim/artifact gap this library exists to close. It also lacked the document products people actually ask for (SRS, design doc, handbook) and any export discipline.
- Design: truth is a gate (no document without a source of truth, no command unexecuted, no unbuilt behaviour documented); products have separate contracts so an SRS cannot smuggle in design; gaps are ranked by what happens to a reader, with S1 for pages that harm when followed; maintenance mechanisms are named with their blind spots rather than asserted; exports are built from source and every page is opened.
- Deductions: no localisation or docs-site-specific guidance; the accessibility checks are signal-level, not WCAG conformance, and the prompt says so.
- Follow-up: a worked SRS example and a pandoc/LaTeX failure catalogue would make P06/P07 concrete.

### `05-scenarios/live-surface-audit/` — new scenario (SURFACE-01)
- **2026-10-20 · diagnostic · 85/100 · operational**
- Problem: the library could only audit systems whose source it could read. The common request — "look at this site/API" — had no procedure, while a naive procedure is either useless (headers only) or an unauthorised attack.
- Design: rules of engagement first; observation-only evidence with reproduction; no enumeration, no exploitation, no load; consequences ranked by exposure; coverage statement separating observed from inferred.
- Deductions: no vendor-specific tooling detail (Lighthouse, OWASP ZAP stay named, not scripted); authenticated testing is out of scope by design.

### Tooling — system-README overclaim gate
- **2026-10-20 · tooling · operational**
- 17 READMEs claimed Operational over skeleton stages. Fixed, and `check_system_readmes()` now fails the build on the class. Fixture-tested by reintroducing the claim in `02-engineering/performance/`.
