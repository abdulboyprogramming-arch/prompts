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
