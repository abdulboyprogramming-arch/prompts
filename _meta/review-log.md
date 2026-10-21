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

### `04-process/handover/` — 5 stages (new, operational)
- **2026-10-20 · mixed · 87/100 · operational**
- Problem: the library had an excellent *stage* handoff contract and no procedure for handing a whole project to another owner. That gap is where production access stays with leavers and where a receiver inherits a system they cannot deploy.
- Design: acceptance criteria are capabilities, not documents; P03 is class D because ownership plus revocation is the highest-consequence operation outside data deletion, and it demands proof of denial rather than a checkbox; P04 is performed by the receiver, so the documentation is tested by use rather than by review; P05 refuses "accepted with issues" without conditions, owners, and dates.
- Deductions: legal assignment of contracts is out of scope (recorded as a blocking dependency); on-call shift handover is still backlog item 12 and P02's operational brief is only a partial answer.
- Follow-up: a worked example of an agency→client transfer, including the vendor-console ownership matrix, would make P03 concrete.

### `07-workflows/HANDOFF-CONTRACT.md` — draft → operational (v1.1.0)
- **2026-10-20 · process · 88/100 · operational**
- The contract was already substantive (84 lines, all ten sections) but carried a draft label that made every stage's handover provisional. Promoted after adding the four-failure table, receiver verification duty, repository-based staleness rule, and the machine-readable form for agent receivers.

### `05-scenarios/hackathon-sprint/` — new scenario (HACK-01)
- **2026-10-20 · autonomous-completion · 86/100 · operational**
- Problem: the library assumed time to be careful. A hackathon inverts the constraint — the deliverable is four minutes in front of judges, and the failure mode is a beautiful unfinished thing that cannot be demoed or submitted.
- Design: the rubric is the specification, the demo script is the build order, cut lines are declared before they are needed, the last 15% of time is reserved for freeze/rehearsal/submission, and every mock is disclosed. The credential section exists because a public repo plus a rushed `git commit -a` is the most common security incident in student and startup hackathons.
- Deductions: no team-coordination guidance beyond a freeze rule (parallel work in a 24-hour event is its own problem); judging-rubric inference is named but not modelled.
- Follow-up: a worked example of a rubric-to-demo-moment table would make step 1 concrete.

### Licensing
- **2026-10-20 · meta · operational** — MIT for code, CC BY 4.0 for content, with the endorsement boundary stated. Resolves the blocking decision in `_meta/publication-checklist.md`.

### `05-scenarios/deployment-target/` — DEPLOY-01 + platform profiles
- **2026-10-20 · implementation · 87/100 · operational**
- Problem: the library covered release process but never *provisioning a target*. Vercel/Netlify/Railway/Fly/Cloud Run appeared zero times; the provider was invisible, so every platform-specific trap was rediscovered by the user.
- Design: the platform is `{{DEPLOY_PLATFORM}}` and its specifics live in a referenced profile, so the prompt stays honest across providers. The three-scope env-var split is the core insight — most "works locally, fails deployed" incidents are a build-time secret or a missing runtime var.
- Deductions: no IaC (Terraform/Pulumi) guidance; profiles are hand-maintained and will drift with provider changes — the file says so and tells the reader to verify.

### `05-scenarios/platform-migration/` — HOSTMIG-01
- **2026-10-20 · implementation · 88/100 · operational (class D)**
- Problem: host moves are where teams discover MX records, OAuth callbacks, and duplicate cron the hard way. The library had nothing between "deploy" and "decommission".
- Design: reversibility first; TTL lowering as the defining constraint; the old host's jobs disabled at cutover; retention past the TTL rather than same-day teardown.
- Deductions: no provider-specific DNS API commands (registrars differ too much); database engine moves are routed to `03-domains/database/`.

### `04-process/agent-context/` — CTX-P01..P04 (new system)
- **2026-10-20 · mixed · 86/100 · operational**
- Problem: `AGENTS.md` mentioned in the repo only as something to *read*; nothing taught authoring, reconciling, or testing it. Teams now maintain a second specification without version control discipline.
- Design: P03 is the differentiator — adherence probes with a four-cause diagnosis, and the rule that an ignored clear instruction needs a machine check rather than more prose. P02's size budget and adapter pattern prevent the common failure of five drifting files.
- Deductions: per-vendor format details change fast; the system teaches conservative adapters and verification against current docs rather than memorising formats.

### `05-scenarios/dev-environment/` — DEVENV-01
- **2026-10-20 · implementation · 85/100 · operational**
- Problem: setup instructions are prose claims; nothing measured whether a clean machine could follow them. Onboarding cost and CI drift both trace here.
- Design: baseline-first (measure the gap before fixing), pinned runtimes over documented ones, one entry point, and per-OS claims only where tested.

### `05-scenarios/on-call-handover/` — ONCALL-01
- **2026-10-20 · specialised · 87/100 · operational**
- Problem: backlog item 12 since 2.1.0. Shift handover was covered only indirectly by the stage handoff block, which carries task state, not operational state.
- Design: state from systems, silences as decisions with owners and expiry, known-noise named, and the "if this pages you tonight" section that survives contact with 03:00.

### `00-core/prompt-engineering/PROMPT-FORGE.md` — GEN-P01
- **2026-10-20 · specialised · 91/100 · operational**
- Problem: the library could judge a prompt but not generate one. The scaffolder emits an empty skeleton; the rubric scores; neither converts "I want something that audits my Terraform" into a runnable artifact.
- Design: five modes with distinct exit conditions; routing against existing coverage *before* drafting (prevents a competing source of truth); risk class derived from consequence rather than phrasing; verification must be a table a person can execute; self-score with the two weakest dimensions named; provenance marks output `draft` so generation is never mistaken for validation.
- Deductions: quality still depends on the operator's answer to the interview questions; the self-score is self-assessment, not evidence (GEN-P02 is the evidence path).

### `00-core/prompt-engineering/PROMPT-REGRESSION.md` — GEN-P02
- **2026-10-20 · continuous-improvement · 86/100 · operational**
- Problem: only one prompt in the library had ever been executed (`DBG-01`). Prose review cannot detect a rewrite that reads better and behaves worse.
- Design: fixtures frozen before results; two runs per case; trace-level grading; separate design score and behavioural grade; defect classification (missing / ambiguous / ignored / fixture / tool limitation) that determines the fix rather than inviting more prose.
- Deductions: small-n by nature; no automated runner yet — the protocol is manual first, tooled later.

### `03-domains/web3/` — CHAIN-P01..P04
- **2026-10-20 · mixed · 88/100 · operational**
- Problem: zero coverage. `reentrancy`, `gas fee`, `EVM` appeared nowhere; the only Web3 material was a contribution skeleton. Value-moving code with no review, custody, upgrade, or incident procedure.
- Design: P01 ranks by profit-to-attacker rather than cleverness; P02 makes authority the design object (tiers, thresholds, drilled rotation); P03 enforces append-only storage with a fork rehearsal and a declared rollback position; P04 orders containment before explanation, and adds "re-review before resume" because exploits cluster.
- Deductions: no formal verification, no MEV strategy, no token-economics review; the fork rehearsal depends on archive RPC access the user must supply.

### `03-domains/mobile/` — MOB-P01..P03
- **2026-10-20 · mixed · 85/100 · operational (new domain)**
- Problem: no system at all. Store review, staged rollout, symbolication, and version skew were absent while `mobile` was flagged missing in the coverage matrix since 2.9.0.
- Design: halt criterion written before rollout; rollback levers enumerated and tested because unpublishing is impossible; crash ranking by affected users and critical path; compatibility as a contract with per-version fixtures.
- Deductions: platform-specific console details age quickly; device-farm testing is assumed, not provided.

### `03-domains/embedded-iot/` — IOT-P01..P02
- **2026-10-20 · mixed · 87/100 · operational (new domain)**
- Problem: `firmware` appeared only in a backlog row. OTA without rollback is the classic fleet-bricking mistake, and silence-as-failure had no procedure.
- Design: power-cut as the default test; atomic slot write with readback; trial boot with automatic confirmation (no human in the loop); cohort rollout with pre-declared abandonment; fleet triage that checks the server before the device and classifies silence by cohort.
- Deductions: no RTOS/safety-critical certification coverage; recovery cost is quantified but not solved.

### `03-domains/games/P09`, `P10` — GD-P09, GD-P10
- **2026-10-20 · implementation / diagnostic · 84/100 · operational**
- Problem: 8 design skeletons and nothing about the two failures that generate refunds: destroyed saves and unfair-feeling multiplayer.
- Design: forward-only versioned saves with real historical fixtures and atomic writes; netcode diagnosis aligning three clocks and measuring against a budget before changing code.
- Deductions: the remaining seven stages are still skeletons, so the system is mixed, not operational.

### `03-domains/ai-agentic/P06`, `P07` — AI-P06, AI-P07
- **2026-10-20 · audit-remediation · 88/100 · operational**
- Problem: retrieval was chosen but never measured; the engineering agent's permissions were never audited as a whole.
- Design: P06 separates retrieval metrics from groundedness, mandates ≥30% unanswerable questions, and tests ACL leakage as a security case. P07 judges capability rather than intent across six axes, treats unpinned `npx` as a supply-chain gap, and requires the tightened configuration to survive daily use.
- Deductions: neither covers model selection or hosting; both assume the operator can read their own configuration files.

### `02-engineering/tenancy-audit/` — TENANCY-01
- **2026-10-20 · diagnostic · 89/100 · operational**
- Problem: no prompt anywhere addressed cross-tenant leakage, the highest-severity defect class in B2B software. `tenant`, `multi-tenant`, `IDOR` returned no prompt coverage.
- Design: store inventory before code review, enforcement classified as database / query-layer / convention, seven named leak patterns including caches and background jobs, two-synthetic-tenant regression suite, existence-disclosure as a distinct finding class.
- Deductions: no automated scanner (deliberate — the valuable checks are cross-request); admin-tool scoping is covered procedurally, not tested.

### `02-engineering/secrets-rotation/` — SEC-ROT-01
- **2026-10-20 · implementation · 88/100 · operational**
- Problem: rotation appeared only as "rotate first" inside incident remediation. Nothing covered inventory by consumer, overlap strategy, or the drilled proof that the old credential is dead.
- Design: rotation treated as a capability demonstrated by a drill; the 03:00 cron as the test that matters; revoke-first ordering for compromise; short-lived credentials preferred to rotation.
- Deductions: vendor-specific CLI commands are intentionally absent; the drill assumes an environment equivalent to production exists.

### `05-scenarios/background-jobs/` — JOBS-01
- **2026-10-20 · diagnostic · 87/100 · operational**
- Problem: `cron`, `idempotent`, `dead-letter` appear only inside other systems' procedures; no prompt treated background work as a correctness surface in its own right.
- Design: job table before diagnosis, "assume it runs twice" as the organising rule, visibility-timeout-versus-p99 as a concrete duplicate-delivery cause, UTC scheduling with an explicit DST test.
- Deductions: queue-backend specifics are named but not exhaustively mapped; reconciliation of already-duplicated effects is routed rather than performed.

### `05-scenarios/email-deliverability/` — EMAIL-01
- **2026-10-20 · diagnostic · 86/100 · operational**
- Problem: SPF/DKIM/DMARC appeared in zero prompts. The failure — a provider returning 202 while mail is discarded — is invisible to every existing diagnostic.
- Design: DNS as the source of truth over the provider UI, alignment explained as the thing DMARC actually enforces, stream separation framed as reputation isolation, SMTP response code required before any change.
- Deductions: reputation remediation (blocklist removal) is described but not proceduralised; provider-specific APIs vary too much to script.

### `04-process/accessibility-audit/` — A11Y-01
- **2026-10-20 · diagnostic · 87/100 · operational**
- Problem: `SURFACE-01` checked alt text and heading order; WCAG 2.2 AA conformance needs rendering, keyboard operation, assistive technology, reflow and the four 2.2 additions. Backlog #32 since 2.11.0.
- Design: explicit ordering by yield (keyboard → screen reader → scanner), contrast measured on rendered output, states tested that demos never show, and a mandatory statement of what was not tested.
- Deductions: no automated harness; the automatable third is not the difficult third, and the prompt says so.

### `03-domains/data-engineering/` — DE-P01, DE-P02
- **2026-10-20 · mixed · 88/100 · operational (new domain)**
- Problem: backlog #71 and a coverage-matrix "Missing" row since 2.9.0 — `data-ml-ai` conflated pipelines with modelling, so ingestion, freshness, backfills and reconciliation had nowhere to live.
- Design: DE-P01 asserts on output rather than task status and treats volume anomalies as failures; DE-P02 treats a backfill as a migration with consumers (snapshot, full-scale dry run, per-partition atomicity, value-level reconciliation). `data-ml-ai` now states the boundary.
- Deductions: no orchestration-tool-specific guidance; warehouse cost is routed to `cost-engineering`.

### Library capability — README overclaim rule (2.16.0)
- **2026-10-20 · tooling · n/a**
- Change: `README_CLAIM` now matches `**Maturity: operational` as well as `**Status:** Operational`; a second rule flags prose "Operational" claims when more than half a system's stages are skeleton and the README does not declare itself mixed.
- Evidence: three real hits on the first run — `01-contribution/web` and `01-contribution/web3` (genuine overclaims, rewritten to skeleton), `03-domains/games` (false positive, exempted because it declares "Mixed"). The rule was verified against real cases, not fixtures; backlog #82 records that gap.

### `05-scenarios/disaster-recovery/` — DR-01
- **2026-10-20 · implementation · 90/100 · operational**
- Problem: `disaster recovery` appeared in **zero** files. The library could recover one deleted table and one failed deploy, but had nothing on losing a region, an account, or the backup system itself. This was the highest-consequence untested assumption in the repository.
- Design: the drill is the deliverable — restore from the real backup in an isolated environment, measure every phase, verify the *application* against restored data (sequences, extensions, migrations), and state RTO/RPO in minutes against targets. Account-loss is a separate class with separate preparation.
- Deductions: business-continuity planning (staff, premises) is out of scope; cost of a drill environment is assumed available.

### `02-engineering/time-correctness/` — TIME-01
- **2026-10-20 · diagnostic · 88/100 · operational**
- Problem: DST, month arithmetic, and naive timestamps were handled incidentally (`JOBS-01` mentions UTC), never audited. Off-by-one-day defects are silent and reach reports, billing, and scheduling.
- Design: classify every field as instant / wall-clock / date before fixing; eight named anti-patterns; boundary tests at DST transitions and month-end; frozen clocks so tests are reproducible.
- Deductions: timezone database updates are an ops concern; product definitions of "day" must be supplied by the product.

### `05-scenarios/third-party-integration/` — INTEG-01
- **2026-10-20 · implementation · 88/100 · operational**
- Problem: no prompt treated a vendor as an external dependency with its own failure modes. `DEPLOY-01` mentioned egress; nothing covered error-in-200, webhook duplication, or timeout ambiguity.
- Design: eight-mode failure matrix; validate the body not the status; outbound idempotency keys stable across retries; webhook signature verification on the raw body; degradation defined before the outage.
- Deductions: vendor-specific SDKs are not catalogued; commercial negotiation is out of scope.

### `05-scenarios/file-uploads/` — UPLOAD-01
- **2026-10-20 · implementation · 86/100 · operational**
- Problem: uploads are simultaneously a security surface (malware, XSS, SSRF), a cost surface (orphans, egress), and a privacy surface (documents not covered by deletion). None appeared in the library.
- Design: limits enforced at three layers; magic-byte validation; re-encode images; generated keys; private bucket with signed URLs; lifecycle rules for orphans and multipart parts; object keys tied to owning entities so deletion is queryable.
- Deductions: media transcoding pipelines and CDN tuning are out of scope.

### `05-scenarios/localization/` — I18N-01
- **2026-10-20 · implementation · 85/100 · operational**
- Problem: translation of *documents* was covered; localisation *correctness* (plurals, concatenation, RTL, expansion, locale sorting) was not. English-shaped code fails silently in every other language.
- Design: eliminate fragment concatenation; ICU plural categories rather than `count === 1`; pseudo-localisation before translation; logical CSS properties for RTL; per-locale screenshot evidence.
- Deductions: translation quality requires a native reviewer and is routed, not performed.

### `05-scenarios/infrastructure-as-code/` — IAC-01
- **2026-10-20 · audit-remediation · 87/100 · operational**
- Problem: backlog #57. `DEPLOY-01` provisions; nothing established whether the code matches the estate, or how to adopt hand-built infrastructure without re-creating it.
- Design: provider API as ground truth, provenance per resource, every plan destroy/replace treated as a decision, state posture, import-verify-no-change loop, pipeline as the only path.
- Deductions: applies are explicitly out of scope for the prompt's own execution.

### `05-scenarios/performance-budget/` — PERF-BUDGET-01
- **2026-10-20 · implementation · 85/100 · operational**
- Problem: backlog #52. Performance existed as an investigation (`performance-investigation`) but never as a gate; regressions accumulate undetected.
- Design: p75 baselines on mid-tier mobile; budgets from perceptible thresholds plus a separate regression ceiling; deterministic CI gate; per-route attribution on pull requests; third-party budgets.
- Deductions: implementation techniques remain in the `frontend` skeleton.

### `05-scenarios/monorepo/` — MONO-01
- **2026-10-20 · audit-remediation · 86/100 · operational**
- Problem: backlog #54. Everything in the library assumed a single package; monorepo failures (affected detection, boundaries, cache invalidation) had no home.
- Design: import graph over manifests; deep imports as violations; tasks must declare inputs to be cacheable; affected-only demonstrated by a leaf change; contracts imported from one source.
- Deductions: tool migrations are out of scope.

### `03-domains/backend/P09` — API-VER-01
- **2026-10-20 · planning · 88/100 · operational**
- Problem: backlogs #53 and #81. `MOB-P03` covered installed clients; nothing covered the public/partner API contract, deprecation, or sunset.
- Design: consumer inventory before scheme; change classification table; schema artifact in CI with contract tests; deprecation with traffic thresholds; two concurrent majors as the ceiling.
- Deductions: GraphQL-specific federation concerns are noted, not solved.

### `03-domains/desktop-cli/` — DESK-P01, DESK-P02
- **2026-10-20 · implementation · 87/100 · operational (new domain)**
- Problem: the last **Missing** row in the coverage matrix. Distribution is a trust boundary and the terminal contract is an API that tools break silently.
- Design: P01 treats the updater as a signature-verified code-execution channel and requires clean-machine install evidence; P02 specifies exit codes, stream separation, TTY detection, signals, and `NO_COLOR`.
- Deductions: GUI desktop packaging and platform notarisation services are out of scope.

### Library capability — validator regression suite (2.17.0)
- **2026-10-20 · tooling · n/a**
- Change: `scripts/test_validator.py`, six fixtures covering both claim forms, the prose rule, the mixed exemption, and a clean system; wired into CI before the validator itself runs.
- Finding: writing the tests immediately exposed a real defect — the 2.16.0 regex matched `**Status:** Operational` but **not** `**Maturity: operational (v1.0.0).**`, the form used by most READMEs in this repository. It was silently checking almost nothing. Fixed, and the suite now pins both forms.

### `04-process/licence-compliance/` — LIC-01
- **2026-10-20 · implementation · 89/100 · operational**
- Problem: licence posture appeared as one bullet inside `DEP-P01` ("flag for the owner"). Nothing produced the obligations, the attribution file, or a gate. The distinction that matters — what you are *obliged to do* when you distribute — had no home.
- Design: distribution perimeter first (every judgement depends on it), obligation families rather than labels, outbound/inbound compatibility in the direction people forget, notices generated from the resolved graph, disposition with owner and expiry, CI gate.
- Deductions: legal conclusions are explicitly routed, not performed; patent review out of scope.

### `04-process/standards-conformance/` — STD-01
- **2026-10-20 · audit-remediation · 88/100 · operational**
- Problem: `GOV-P01..P03` map organisation-level controls; nothing assessed a *project* against a named standard with per-requirement evidence. The compliance question was answerable only by an auditor.
- Design: claimed / practised / evidenced / enforced as four distinct levels; only the last two count; periodic controls checked by **last occurrence date**; unknown rows preserved rather than rounded up; maintainability model (which rows automate).
- Deductions: certification is not performed; legal interpretation routed.

### `07-workflows/compliance-readiness.md` — WF-COMPLY
- **2026-10-20 · orchestration · 87/100 · operational**
- Problem: the library had components of a compliance response and no sequence. The workflow adds entry conditions, four gates, ordering rules (evidence capture before remediation), and an evidence-pack specification with dates.
- Design: the pack table names the minimum per section; failure routing covers unavailable standard text, architectural scope gaps, and deadlines shorter than remediation.

### `05-scenarios/automation/` — AUTO-01
- **2026-10-20 · implementation · 88/100 · operational**
- Problem: the direct answer to "does it cover automating a described task" was no. The library described how to *build* software; it did not describe how to convert a manually-performed procedure into something that runs.
- Design: four step classes (deterministic / fragile / judgement / blocked), idempotency proven by a double run, the silent-no-op guard, outcome verification rather than exit codes, four recorded proofs before the schedule is enabled.
- Deductions: orchestration platforms and workflow engines are not evaluated.

### `05-scenarios/client-secrets/` — SECRET-CLIENT-01
- **2026-10-20 · audit-remediation · 90/100 · operational**
- Problem: backlog #86. `SEC-ROT-01` rotates server credentials; a key inlined into a bundle is published forever and rotation alone cannot fix it. The severity question ("what can a holder do") was nowhere.
- Design: scan the built artifact, not the source; framework inlining mechanisms enumerated by name; capability-based severity table; replacement architecture per capability; revocation ordered before removal because artifacts are archived.
- Deductions: provider console configuration is described, not performed.

### `05-scenarios/supply-chain/` — SUPPLY-01
- **2026-10-20 · audit-remediation · 87/100 · operational**
- Problem: dependency management chose versions; nothing asked whether the artifact you deployed is the artifact you built.
- Design: chain with evidence per link; install-time execution as the pre-scanner blind spot; dependency confusion as a naming problem; digest pinning; provenance verified once; SBOM queried while nothing is on fire.
- Deductions: build-infrastructure hardening beyond CI trust boundaries is out of scope.

### `05-scenarios/data-residency/` — RESIDENCY-01
- **2026-10-20 · audit-remediation · 86/100 · operational**
- Problem: backlog #90. Residency was a phrase inside three prompts and a map nowhere.
- Design: six location kinds (storage, replicas, processing, observability, support access, third parties), configuration as evidence, client-side SDK flows, transfer register with a named mechanism and confirmer, enforcement control proven by a deliberate violation.
- Deductions: legal adequacy analysis routed; data itself never copied into the map.

### `05-scenarios/feature-sunset/` — SUNSET-01
- **2026-10-20 · planning · 87/100 · operational**
- Problem: backlog #85. `decommissioning` retires systems; removing one feature — with contracts, machine clients, shared tables, and a data decision — had no procedure.
- Design: usage by account/workflow/concentration rather than page views; blind spots (machine clients, scheduled jobs, support tooling); a reversible sequence that names the last reversible point; data retention as part of the sunset, not a follow-up.
- Deductions: the decision to sunset is product's; compensation and contract renegotiation routed.

### `05-scenarios/incident-communications/` — INC-COMMS-01
- **2026-10-20 · specialised · 85/100 · operational**
- Problem: `INC-01` restores service and `OBS-P05` writes the postmortem. Nobody owned the customer update, and the rules that prevent damage (no cause speculation, no duration promises, no unverified "your data is safe") were unstated.
- Design: facts sheet citing incident-channel messages; announced cadence; four-state vocabulary; audience separation; append-only log that makes every external claim attributable.
- Deductions: disclosure decisions belong to legal; PR strategy out of scope.

### `05-scenarios/operational-readiness/` — OPS-01
- **2026-10-20 · audit-remediation · 88/100 · operational**
- Problem: `REL-P01` gates a release; nothing tested whether a *service* is operable at 03:00 by someone who did not build it. Alert triage and the runbook outsider test were absent.
- Design: four failure classes (silence, saturation, dependency, partial), page/ticket/remove triage, dated proof of rollback and restore, on-call access confirmed today, one timed exercise.
- Deductions: architecture redesign routed to `architecture-review`.

### `05-scenarios/build-performance/` — BUILD-01
- **2026-10-20 · diagnostic · 85/100 · operational**
- Problem: build and CI time was invisible. `PERF-BUDGET-01` covers runtime budgets; the loop engineers wait on twenty times a day had no prompt.
- Design: phase timings before any fix; three loops with different budgets; work reduced before cached; cache hit rate measured; before/after with the same method including cold cache.
- Deductions: runner purchasing decisions routed.

### `05-scenarios/ai-output-verification/` — AIVERIFY-01
- **2026-10-20 · diagnostic · 91/100 · operational**
- Problem: the library instructs agents extensively and had no prompt for verifying an agent's claims. `WF-VERIFY` covers human work; the agent-specific failure modes (test-count regression, "verified" by reading, narrowed requirement, silenced checks) were unaddressed.
- Design: claims verbatim, clean-state reproduction, revert-and-fail as the only proof a test works, diff accounting, and an explicit `unverifiable` verdict that may never be rounded up.
- Deductions: fixing is deliberately out of scope — fixing destroys independence.


### `05-scenarios/data-migration/` — DATA-MIG-01
- **2026-10-20 · specialised · 88/100 · operational**
- Problem: backlog #93. Schema migration (`DB-P01..P05`) and host migration (`05-scenarios/platform-migration/`) both existed; moving *records* between systems, where meaning changes in transit, had no procedure. The characteristic failure is not the job erroring — it is the job succeeding with truncated strings and lost timezone offsets.
- Design: field mapping with an explicit loss register and affected-row counts; identity decided before loading so reruns upsert rather than append; resumable load with checkpoints and reject files; reconciliation on hashes and aggregates rather than counts; two rehearsals; cutover with a named rollback expiry.
- Deductions: target schema design and application rewrites are out of scope.

### `04-process/privacy-requests/P04` — PRIV-P04
- **2026-10-20 · audit-remediation · 90/100 · operational**
- Problem: backlog #95. `PRIV-P02` deletes and marks the request complete. The places where deletion is claimed and never checked — warehouse, logs, search index, queue, backups, vendor — were unexamined, and a restore could resurrect a deleted subject.
- Design: per-location definition of what "deleted" can even mean (immutable logs age out; backups expire); multiple identifiers including hashes; verification queries tested against a known-positive record; resurrection paths examined; a synthetic canary through the real path.
- Notes: this is the adversarial half of deletion — it assumes P02 was incomplete and looks for the proof. Promoted the system README to v1.1.0.

### `02-engineering/access-review/` — ACCESS-01
- **2026-10-20 · audit-remediation · 89/100 · operational**
- Problem: backlog #97. Access control was covered as a review *topic* and never as a recurring *procedure*. Tenants of this gap: reviews run against the roster rather than the identity provider, reviewed people instead of entitlements, and removals recorded in a document rather than executed in the system.
- Design: inventory from providers and reconciled to the roster; consequence classification; non-human access (CI identities, long-lived tokens, vendor impersonation, break-glass); decisions of keep/narrow/remove/escalate with reasons; removals verified by denial; exceptions with owners and expiry.
- Deductions: authentication design and incident containment are separate; removing access is class D because it can stop production or lock out the only administrator.


### `05-scenarios/environment-parity/` — ENVPARITY-01
- **2026-10-20 · audit-remediation · 88/100 · operational**
- Problem: backlog-level gap in §8 of the coverage matrix ("no environment-parity prompt"). Reproducibility covered *setup*; nothing explained **behaviour differences** between local, CI, staging and production, which is the more common and more expensive question.
- Design: nine layers ranked by how often each is the cause; config diffed mechanically including **missing** keys, because absence means a code default; data compared by shape and volume; service gaps enumerated; cause proven by a single-variable experiment rather than argued; config contract plus a CI parity check that compares keys, never secret values.
- Deductions: building environments and performance-only differences are routed elsewhere.

### `05-scenarios/capacity-planning/` — CAPACITY-01
- **2026-10-20 · planning · 87/100 · operational**
- Problem: backlog #96. `cost-engineering` optimises spend and `operational-readiness` tests alerts, but nothing computed *when* a resource hits its ceiling. The failures that hurt are the non-obvious ones: connection pools, sequence headroom, quotas with reset windows, and certificate expiry — capacity with a date and no growth.
- Design: peak rather than average; date-to-ceiling **and** date-to-headroom, with the earliest date named as the bottleneck; specific failure behaviour per resource; autoscaler metric, cooldown and maximum interrogated; four plan forms (scale / shed / eliminate / accept); expiries in the same table as capacity.
- Deductions: purchasing decisions routed; disaster-recovery capacity is a different problem.

### `05-scenarios/vendor-due-diligence/` — VENDOR-01
- **2026-10-20 · research · 86/100 · operational**
- Problem: backlog #94. `STD-01` answers questionnaires sent *to* you; `INTEG-01` handles a vendor misbehaving *after* adoption. Nothing assessed a supplier *before* the dependency existed.
- Design: dependency class sets the depth (accessory / degrading / critical path / data processor); "claimed by vendor" is a third evidence category, weaker than verified; reliability read from incident history rather than an uptime figure; SLA compared against your own promise; lock-in quantified in switching days; exit plan written before adoption.
- Deductions: contract negotiation and security testing of the vendor are out of scope.

### `05-scenarios/abuse-prevention/` — ABUSE-01
- **2026-10-20 · audit-remediation · 89/100 · operational**
- Problem: backlog #102. Abuse had no home: hardening covers auth weaknesses, tenancy covers isolation, and nothing covered the endpoint that is *working as designed* while being used for something else.
- Design: abuse economics first; the limiting dimension table (credential stuffing limited per account rather than per IP; scraping limited by coverage rather than rate; cost-based abuse limited by cost units); uniform responses before rate limits; four-stage rollout with a measured false-positive budget; exemption path for server traffic and an appeal path tested once.
- Deductions: network-level DDoS is the provider's responsibility; confirmed attacks go to `security-incident`.

### Library capability — duplicate detection (2.19.0)
- **2026-10-20 · tooling · n/a**
- Change: `find_overlaps.py` gained vocabulary containment, structure similarity, and their product as a combined metric, plus `--metric` selection with per-metric floors and CI bars. `scripts/test_overlaps.py` pins 13 cases.
- Finding: the combined metric immediately ranked the `01-contribution` parallel variants highest (0.68) — shingle containment had reported them at 0.11–0.18 and made them look unremarkable. Backlog #100 records the consolidation decision that has not been made.
- Limitation, stated in the module: all four signals are lexical. A paraphrase with genuinely different vocabulary is still invisible, and the tool's job is to shorten the reading list, not to replace the reading.

### Library capability — evidence levels (2.19.0)
- **2026-10-20 · tooling · n/a**
- Change: `_meta/evidence.json` is the registry of executions that actually happened; `scripts/evidence_report.py` validates it against the catalog and the filesystem and generates `_meta/evidence-levels.md`, which CI checks for staleness.
- Why: every release note quotes the operational count, and that number reads as a quality claim. The generated report states the measured alternative — **1 of 201 operational prompts (0.5%)** has a recorded execution — and cannot be edited without editing the registry.

### `00-core/inputs/RUN-SHEET-EXAMPLE.md`
- **2026-10-20 · documentation · n/a**
- Problem: backlog #99. The run sheet defined a form; composition between systems was asserted rather than shown.
- Design: one filled sheet across two systems and six stages, with the artifact chain, the three properties that make it work (paste once, artifacts rather than transcripts, inputs ≠ dependencies), a system-scoped input block, and a recorded amendment. Also states what the example does **not** show (a refused gate, a failed stage, a multi-agent run) and points at backlog #101 for the first.


### `05-scenarios/usage-metering/` — METER-01
- **2026-10-20 · audit-remediation · 90/100 · operational**
- Problem: backlog #105. Money movement (`PAY-P01..P03`) and infrastructure spend (`COST-P01..P04`) were covered; **the quantity you bill** was not. Metering fails silently in both directions — uncounted usage is revenue loss, duplicated usage is a dispute — and the first detector is usually a customer with a spreadsheet.
- Design: the billable unit as a contract with exclusions; one metering point per unit with its blind spot written down; immutable, idempotent events with corrections as new events; fail-open versus fail-closed chosen and logged; period boundary, timezone and late-event rules; plan-change/proration rules; **enforcement separated from accounting**; monthly reconciliation against an independent source; dispute reconstruction from stored events alone.
- Deductions: invoicing, tax, and collection remain with `payments`.

### `05-scenarios/test-data/` — TESTDATA-01
- **2026-10-20 · audit-remediation · 87/100 · operational**
- Problem: backlog #103. `testing-qa` P04 contains one bullet on test data strategy; the risks (a committed fixture with a real address, a staging database copied from production, a screenshot in a pull request) had no procedure. Test data is the least-governed copy of production data and the only one that ships with the repository.
- Design: inventory including cassettes, base64 blobs and attached evidence; four states (synthetic / anonymised / pseudonymised / real copy) with different remediation; a test that "anonymised" is actually irreversible; generators that produce awkward data deliberately, because tidy test data hides bugs; isolation as structure rather than discipline; a CI guard demonstrated failing.
- Deductions: retention and subject rights stay with `privacy-requests`.

### `07-workflows/failure-examples.md` — WF-FAILURE
- **2026-10-20 · specialised · 86/100 · operational**
- Problem: backlog #101. Every workflow defines gates and failure routing; none demonstrated them. `RUN-SHEET-EXAMPLE.md` closed this for the success path in 2.19.0; this closes the failure path.
- Design: four scenarios — a refused gate after work was already done, a stage blocked by an upstream artifact, an agent claim refuted by verification (test count down from 87 to 84), and a mitigation that made the incident worse. Each names the wrong response, because that is what readers do by default, and the artifact that changes.
- Deductions: these are reconstructed examples, not transcripts of named incidents; the file states that.

### Library capability — prose lint (2.20.0)
- **2026-10-20 · tooling · n/a**
- Change: `scripts/lint_prose.py` flags unactionable qualifiers (`as appropriate`, `if necessary`, `etc.`), empty intensifiers when the sentence contains no concrete instruction, and sentences over 55 words. `scripts/test_prose_lint.py` pins 12 cases including the false positives that would make it unusable.
- Adoption: **a ratchet, not a gate** — `--check` fails only when findings exceed `_meta/prose-lint-baseline.json`. Baseline is 171 across 112 files (68 of them `etc.`, concentrated in the 16-stage open-source agent). Non-zero baselines are honest debt; a gate at zero would have blocked every change on day one, and a lint nobody adopts catches nothing.
- Limit: lexical only. It cannot see that a sentence is ambiguous in a way that uses none of these words.

### `01-contribution/VARIANTS.md` — the duplication decision (#100)
- **2026-10-20 · decision record · n/a**
- Finding: the combined duplicate metric puts the three contribution variants at 0.63–0.68 — the highest in the library — where shingles reported 0.06–0.18.
- Decision: keep three, and require every overlapping stage to state its domain difference or be deleted. Promotion stays blocked until it does; the differentiation work is backlog #107, deliberately ordered *one stage across all three variants* rather than one system at a time, because a single-author bulk rewrite would reproduce the same text with different nouns.
- Why recorded as a file: the next agent to "clean up duplication" needs to know the risk model and approval model differ, not just the vocabulary.


### `00-core/conversational/` — CHAT-MODE, CHAT-REVIEW, CHAT-DEBUG, CHAT-DESIGN
- **2026-10-20 · specialised · 88–90/100 · operational (new family)**
- Problem, stated by the maintainer as a question: *do these prompts have a chatbot version?* They did not. All 358 assumed an agent that can read files, run commands, and observe results. Nothing in the library said what survives when those are removed, and a fluent answer about an unseen repository is the most dangerous output this library can produce.
- Decision: answer the question with a mechanism rather than a disclaimer. **`CHAT-MODE` adapts any prompt**, and the adaptation is a three-row capability table (discovery → interrogation, execution → the user runs it, verification → labelled claims) plus a paste protocol, a state ledger for long sessions, and a closing self-audit where `cannot verify in chat` is a first-class verdict.
- Design detail worth keeping: the evidence vocabulary. `verified` is reserved for the case where the user pasted the command *and* its output *and* they match the claim; everything else is `observed`, `reported`, `inferred`, or `unknown`. Without that rule a chat run silently inherits the authority of an agent run.
- Three chat-native prompts were written because they are the tasks people actually do in a chat window and they need different wording: `CHAT-REVIEW` (bounded review with a not-assessed list), `CHAT-DEBUG` (one discriminating experiment per turn, with a ledger), `CHAT-DESIGN` (ADR with rejected options and a reopening condition).
- Deductions: no attempt to model a specific vendor's features; context-window behaviour is described generically.


### `00-core/conversational/CHAT-DEBUG.md` — first execution (v1.1.0)
- **2026-10-20 · specialised · 89/100 · operational (re-review after execution)**
- Method: `_meta/empirical-evaluation-02.md`. A constructed fixture — a nightly sync failing with `sqlite3.OperationalError: database is locked` at `db.commit()` — where the pasted function contains **no defect** and a second, uncommitted connection in code the user never sent holds the lock. The prompt's steps were followed as written, with the user turns written by the evaluator. A tabletop, not a live session, and recorded as such.
- Finding 1 (the important one): the prompt inherited the assumption that the bug is in the paste. It had no instruction to ask what else touches the same resource, so its natural next move was to critique a correct loop. Added workflow step 2b and a failure-handling rule: *"this function is fine, and something else holds the lock" is a valid answer.*
- Finding 2: the evidence ledger had no slot for a finding located outside the paste, so the discovery of the second connection would have stayed `OPEN` forever and looked unresolved. Ledger gained `CONTRADICTION:` and `OUT OF SCOPE (needs access):`.
- Finding 3: no rule for a user claim that conflicts with evidence ("we bumped nothing", while a version differs). Added: a contradiction is evidence — record both and test the difference rather than accepting the reassuring account.
- Also learned about the stop rule: escalation here is not a count of failed experiments but a **scope change** — the search moved outside what the user can paste. Recorded in the write-up as a partial gap; the prompt's stop rule is still count-based.
- Deduction: this is the author evaluating the author's prompt, so the run demonstrates followability and defect discovery, not effectiveness. `CHAT-MODE`, `CHAT-REVIEW`, `CHAT-DESIGN` remain unexecuted.

### `00-core/conversational/CHAT-SELECT.md`, `CHAT-HANDOFF.md` — the problems after the first success
- **2026-10-21 · specialised · 88/100 · operational (new)**
- Problem: two gaps that only appear once chat mode works. Selection still assumed a human who knows the library, and continuity assumed the conversation would stay open. A chat model can do neither: it cannot read 364 files, and it cannot remember beyond the window.
- `CHAT-SELECT` decision worth keeping: **the label is the honesty mechanism.** A route is `observed` only when the user pasted `TASKS.md` or `GALLERY.md`; otherwise it is `inferred` and says so on the card. Without that, a plausible-sounding route inherits the authority of the index it never read. It also returns **one** prompt with a falsifier ("if the job also fails when run alone, this is `DBG-01`, not `FLAKE-01`") rather than a menu, because a menu returns the work to the person who asked.
- `CHAT-HANDOFF` decision worth keeping: **a summary is the wrong artifact.** Summaries keep conclusions and drop disproved hypotheses, so the next conversation re-proposes an eliminated theory with fresh confidence and the user pays for the same dead end twice. The packet carries the eliminations, the label on every fact, the rejected decisions with reasons, the redaction statement, and a mandatory restatement from the receiving conversation before work resumes.
- Design detail: the sixty-line bound is a truncation guard, not a style preference — a long packet is truncated from the bottom, which silently deletes the constraints, so the constraints go at the top.
- Deductions: neither prompt has been executed. `CHAT-SELECT` is the cheaper of the two to test (two people, the same situation, compare the routing cards); that is the next evidence entry.

### Library capability — the prose lint closes (2.22.0)
- **2026-10-21 · tooling · n/a**
- Change: 171 findings to 0. `_meta/prose-lint-baseline.json` now records `0`, so `--check` is a hard gate rather than a ratchet, and the script's own docstring says so.
- Method worth recording: every replacement named items instead of gesturing at them, and the 24 long sentences were split at clause boundaries rather than abbreviated. A burndown that shortens by deleting content would have lowered the number and raised the ambiguity, which is the failure the lint exists to catch.
- Lesson from the first pass: replacing `where possible` with another hedge (`where the platform allows`) would have passed the lint and changed nothing. The rule that kept it honest was reading each line's meaning before editing it — the find-and-replace version of this job is a way to score zero badly.

### Library capability — task index (2.22.0)
- **2026-10-21 · tooling · n/a**
- Change: `scripts/generate_task_index.py` generates `TASKS.md` from 21 task definitions, and CI fails when a prompt belongs to no task or the file is stale. `scripts/test_task_index.py` pins 15 cases, including the prefix rule that must not match a sibling directory and the "unrouted prompt is reported, not dropped" property.
- Finding: the first run reported **13 prompts with no home**, including all five `observability-reliability` stages. A hand-written index would have left them out silently; the coverage check is what made the gap visible, which is the argument for generating the index rather than curating it.
- Limitation, stated in the file: homes are directory prefixes, so routing is coarse — a prompt is assigned by where it lives, not by what it says. The test pins the matching rules, and the falsifier is a mis-routed prompt a reader notices.

### `01-contribution/*/P06` — the first differentiation pass (#107)
- **2026-10-21 · specialised · 89/100 · operational (3 stages promoted)**
- Problem: `VARIANTS.md` ruled that an overlapping stage must state its domain difference or be deleted, and blocked promotion until it did. Seven stages in each of three systems were the same file with different nouns.
- Method: one stage across all three variants, as the record prescribes. `P06 Validation` was chosen because the difference is sharpest there and because validation is where a wrong evidence standard does the most damage.
- Design detail worth keeping: **each file names the characteristic failure it exists to catch** — *works in the author's browser*, *works in the test suite and drains the contract*, *works here and breaks a consumer's build*. Naming the failure is what makes three files non-interchangeable, more than any amount of domain vocabulary.
- Measurement, and the honest reading of it: pairwise vocabulary overlap went 0.20–0.28 → 0.22–0.27, with one pair rising. The `P06` outlines were two paragraphs each, so they were never the source of the 0.63–0.68 similarity at the top of `VARIANTS.md`; rewriting an outline into a developed prompt also multiplies the denominator. The pass is justified by what the files now require, not by the metric. That distinction is written into `VARIANTS.md` so the next pass is not judged by a number that cannot see it.
- Deductions: none of the three has been executed. They are `operational` in the library's sense — structurally reviewed with evidence rules — and the review log says plainly that no run exists.

### `07-workflows/multi-agent-worked-example.md` — a run where every suite was green (#109)
- **2026-10-21 · documentation · n/a · `WF-MULTIAGENT` promoted to v1.1.0**
- Problem: the orchestration workflow required frozen interfaces and an interference audit, and demonstrated neither. A rule with no worked failure behind it is a formality.
- Design of the example: the drift is **a required field added under a `done` report**. Deliberately chosen because it passes every check an individual agent can run — A's suite asserts the field exists, B's asserts the frozen payload renders — and fails only at the seam. The seam test asserts on the *rendered email body*, not on event delivery, because an event-arrived assertion would have passed and shipped blank emails.
- Decision worth keeping: recovery **versions** the interface rather than reverting it. The consumer already depended on v1; a revert would have been a second unreviewed break. The fixing agent built its test from the producer's serialised payload, not from the plan text — a copy of the schema is where drift lives.
- Honest detail kept in the file: the audit that would have caught the change in twelve minutes was **defined and skipped**, because both agents reported done. That is the real mechanism, and softening it would have produced a tutorial instead of a record.
- Deductions: constructed run, not an observed incident; two agents only, and it says so. Three-agent drift is worse and is not shown.
