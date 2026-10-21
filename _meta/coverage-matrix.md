# Coverage Matrix

**Version:** 1.3.0 · **Last assessed:** 2026-10-20 (post-2.19.0 reassessment) · **Method:** evidence review of every prompt file; a scenario counts as covered only when an existing prompt addresses its distinctive requirements, constraints, and verification — not because a related prompt exists.

**Status vocabulary**

| Status | Meaning |
|--------|---------|
| **Adequate** | A dedicated prompt covers the scenario's distinctive requirements, including verification and failure handling |
| **Partial** | Covered, but a material element (a stage, a verification, a failure path) is missing or only outlined |
| **Indirect** | Only reachable through a prompt designed for a different purpose; usable with effort |
| **Missing** | No prompt addresses it; the user must improvise |
| **Defective** | An existing prompt would actively mislead or under-verify |
| **N/A** | Not applicable to a prompt library, with justification |

Legend for evidence: `[system:stage]` refers to identifiers in `_meta/CATALOG.md`.

---

## 1. Lifecycle coverage

| Stage | Status | Evidence / gap |
|-------|--------|----------------|
| Discovery / reconnaissance | Adequate | `AUDIT-P01..P03`, `REC-P02`, open-source `P03–P05` |
| Requirements | Partial | Authoring is covered (`DOC-P01` product contract, `DOC-P06` testable requirements with verification methods); recovery by `REC-P02`. Still missing: requirements **change** management and traceability maintenance across releases |
| Design / architecture | Partial | `AUDIT-P03` recovers; `AI-P02` designs. `architecture-review`, `feature-design-suggestion` are skeletons |
| Planning | Adequate | `REC-P05`, `QA-P04`, `SEC-P05`, `AI-P03`, workflow gates |
| Implementation | Adequate | `REC-P06`, `SEC-P06`, `QA-P05`, `AI-P04/P05`, contribution agent `P11` |
| Verification | Adequate | `QA-P06`, `SEC-P06`, `REL-P04`, `WF-VERIFY` |
| Release | Adequate | `REL-P01..P04` |
| Operation | Adequate | `OBS-P01..P05`, `INC-01` |
| Maintenance / improvement | Adequate | `REF-P01..P07` for structural work, `WF-IMPROVE` (draft) for the loop itself |
| Modernisation | Partial | `rewriting-migration` skeleton; DB change covered by `DB-P01..P05`, but no language/platform modernisation procedure |
| Retirement / decommissioning | **Adequate** | `DEC-P01..P04` (new) — consumer discovery by class with positive evidence, derived notice period, staged reversible shutdown with a quiescence window, asset-by-asset retirement decisions |

## 2. Task coverage

| Task | Status | Evidence / gap |
|------|--------|----------------|
| Creation | Partial | `from-scratch` skeleton; `WF-GREENFIELD` (draft) |
| Completion of incomplete work | Adequate | `project-recovery` whole system |
| Review | **Adequate** | `CR-P01..P06` (new) for code review; `WF-VERIFY` for verifying claims. Different jobs, both covered |
| Diagnosis | Adequate | `DBG-01`, `FIXFAIL-01`, `AUDIT-*`, `FLAKE-01` |
| Correction | Adequate | `SEC-P06`, `REC-P06`, debugging fix stage |
| Optimisation | Partial | `performance` skeleton |
| Migration (code) | Partial | `rewriting-migration` skeleton |
| Migration (data/schema) | Adequate | `DB-P01..P05` (schema, in place) and `DATA-MIG-01` (records between systems: field mapping, loss register, idempotent upsert, value-level reconciliation, cutover and rollback expiry) |
| Recovery | Adequate | `project-recovery`, `INC-01`, `DB-P05` |
| Integration | **Adequate** | `WF-INTEGRATE` (new) — contract reconciliation before wiring, seam table, transport and config diffs, end-to-end journey, failure paths per seam |
| Feature completion across layers | **Adequate** | `FC-P01..P04` (new) — contract, layer map, implementation, acceptance |
| Independent verification of others' work | **Adequate** | `WF-VERIFY` (new) — claims audit, clean-state reproduction, mutation probing, undeclared-change audit |
| Failed-fix escalation | **Adequate** | `FIXFAIL-01` (new) — attempt ledger, failure classification, decision to revert/re-scope/escalate |
| Continuous improvement | Partial | `WF-IMPROVE` draft; no measurement harness |
| Automating a described manual task | **Adequate** | `AUTO-01`: step classification (deterministic / fragile / judgement / blocked), idempotency proof by double-run, input-shape guard against the silent no-op, outcome verification, failure channel, and four recorded proofs before enabling the schedule |
| Verifying another agent's output | **Adequate** | `AIVERIFY-01`: claims enumerated verbatim, clean-state reproduction, test-count comparison against base, revert-and-fail proof, diff accounting including silenced checks, one-sentence verdict. Complements `WF-VERIFY`, which verifies human work |

## 3. System maturity

| Maturity | Status | Evidence / gap |
|----------|--------|----------------|
| Prototype / spike | Partial | No prompt for time-boxed prototyping with explicit "throw it away" discipline |
| MVP | Partial | `greenfield-delivery` draft; `from-scratch` skeleton |
| Growing product | Adequate | audit, testing, release, observability systems |
| Enterprise system | **Adequate** | `GOV-P01..P03` (new) — claim-to-mechanism map, evidence testing with mechanism bypass tests, readiness decision with four-way responses |
| Legacy system | Partial | `legacy-code` skeleton; audit + recovery cover much of the need |
| Production-critical platform | Partial | release/observability adequate; no capacity planning or DR exercise prompt |

## 4. Project state

| State | Status | Evidence / gap |
|-------|--------|----------------|
| Healthy | Adequate | audit, QA, release, observability |
| Incomplete | Adequate | `project-recovery` |
| Broken | Adequate | `project-recovery` + `DBG-01` |
| Abandoned | Adequate | `project-recovery` P01–P03 |
| Undocumented | Partial | `REC-P02` reconstructs intent; no README-reconstruction prompt |
| Partially migrated | Partial | `REC-P04` detects; no prompt for completing a half-applied migration |
| Conflicting (multiple implementations) | Partial | `REC-P02` surfaces contradictions; resolution is unspecified |
| Inherited (new owner) | Adequate | `project-recovery` + `PROJECT-STATUS`-style checkpoint pattern |

## 5. Failure severity

| Severity | Status | Evidence / gap |
|----------|--------|----------------|
| Routine defect | Adequate | `DBG-01`, `FLAKE-01` |
| Regression | Adequate | `QA-P06` mutation checks, `REL-P04` |
| Service outage | Adequate | `INC-01`, `OBS-P05` |
| Security incident | **Adequate** | `SECINC-01` (new) — evidence preservation before remediation, verified containment, access-vs-exfiltration scoping, baseline eradication, disclosure decision record |
| Data integrity failure | **Adequate** | `DB-P04/P05` for migration-caused damage; `DATALOSS-01` for corruption and overwrites of any origin |
| Data loss | **Adequate** | `DATALOSS-01` (new) — freeze writes, preserve evidence, bound the window, restore to a side instance, merge and reconcile, quantify what is gone |
| Cascading/multi-service failure | Partial | `INC-01` mentions shared dependencies; no distributed-systems incident procedure |

## 6. Technical breadth

| Area | Status | Evidence / gap |
|------|--------|----------------|
| Frontend | Partial | `03-domains/frontend` skeleton; `A11Y-01` provides the accessibility conformance method, `PERF-BUDGET-01` the performance gate, `I18N-01` the localisation correctness method |
| Backend / APIs | Partial | `backend` skeleton except `API-VER-01` (versioning, contracts, sunset); cross-cutting backend failures covered by `TENANCY-01`, `JOBS-01`, `EMAIL-01`, `TIME-01`, `INTEG-01` |
| Databases | Adequate | `DB-P01..P05` (schema truth, migration design, pre-flight drills, execution/reconciliation, rollback and verification) |
| Infrastructure | Partial | `devops-infra` skeleton; `IAC-01` provides drift detection and adoption, `05-scenarios/deployment-target/` the provisioning path |
| Security | Adequate | `security-hardening` (assessment/remediation), `SEC-ROT-01` (rotation as a drilled capability) |
| Testing | Adequate | `testing-qa` |
| AI / LLM | Adequate | `ai-agentic` `AI-P01..P07`; P06 adds grounded retrieval with ACL-leakage and abstention measurement, P07 adds the engineering agent's own permission surface (MCP servers, shell, egress, credential inheritance) |
| Data engineering | **Adequate** | `DE-P01..P02` (new) — pipeline inventory, seven failure modes, data tests and freshness/volume contracts, atomic per-partition backfills with value-level reconciliation. `data-ml-ai` now starts after trustworthy data |
| Cost / FinOps | **Adequate** | `COST-P01..P04` (new) — attribution, waste diagnosis sized in money, safe optimisation, guardrails and unit economics |
| Privacy / subject rights | **Adequate** | `PRIV-P01..P04` — cross-system subject data inventory, verified export/deletion, enforced retention, and deletion **verification** across warehouses, logs, indices, queues, backups and vendors, including whether a restore could resurrect a deleted subject |
| Money correctness | **Adequate** | `PAY-P01..P03` (new) — representation and invariants, idempotency and unknown outcomes, provider reconciliation and change-safety checklist |
| Version control operations | **Adequate** | `GIT-P01..P05` (new) — state check before destructive commands, conflict resolution by intent, history repair with a shared-history gate, reflog-based recovery, written conventions. Previously only prohibitions existed |
| Distributed systems | Partial | architecture/audit cover analysis; no design or failure-mode prompt |
| Mobile | **Adequate** | `MOB-P01..P03` (new) — store release with a pre-declared halt criterion, crash triage with symbolication and consequence ranking, client-version compatibility and deprecation schedule |
| Embedded / firmware | **Adequate** | `IOT-P01..P02` (new) — atomic OTA with trial boot and automatic rollback, power-cut testing, fleet silence classification and bounded recovery ladder |
| Desktop / CLI | **Adequate** | `DESK-P01..P02` (new) — distribution as a trust boundary, signed updates, terminal contract (exit codes, streams, signals, TTY) |
| Games | Partial | 7 game-design stages remain skeleton; `GD-P09` (save migration) and `GD-P10` (netcode/determinism) are operational |
| Blockchain / smart contracts | **Adequate** | `CHAIN-P01..P04` (new) — threat model with exploit-path ranking, key custody tiers and drilled rotation, upgrade with storage-layout diff and fork rehearsal, exploit response with containment-first ordering |
| Performance | Partial | audit and incident touch it; `performance` skeleton; `PERF-BUDGET-01` covers budgets and `BUILD-01` build/CI time |
| Supply chain integrity | **Adequate** | `SUPPLY-01`: delivery chain with evidence per link, lockfile enforcement, install-script execution, dependency confusion, CI trust boundaries, digest pinning, provenance verified once, SBOM queried before it is needed |
| Licence obligations | **Adequate** | `LIC-01`: distribution perimeter first, obligation families rather than labels, outbound/inbound compatibility, generated notices with versions, disposition with owner and expiry, CI gate |
| Standards conformance | **Adequate** | `STD-01`: verbatim requirement set, applicability with justification, claimed/practised/evidenced/enforced separation, periodic controls dated, honest position; `WF-COMPLY` sequences the response |

## 7. Execution mode

| Mode | Status | Evidence / gap |
|------|--------|----------------|
| Read-only investigation | Adequate | `diagnostic` prompts declare it; risk class A enforced by validator |
| Planning | Adequate | planning-mode systems with gates |
| Implementation | Adequate | `REC-P06`, `SEC-P06`, `QA-P05` |
| Remediation | Adequate | `SEC-P06`, `AUDIT-P07/P08` → workflow |
| Autonomous completion | Partial | adequate for recovery and contribution; `feature-completion` covers one feature, not multi-feature delivery |
| Orchestration | **Adequate** | `AUDIT-P09`, `SEC-P07` single-run orchestration; `WF-MULTIAGENT` (new) covers decomposition, interface freezing, ownership, integration and independent verification |
| Independent verification | Adequate | `WF-VERIFY` (new) |

## 8. Quality assurance

| Element | Status | Evidence / gap |
|----------|--------|----------------|
| Acceptance criteria | Adequate | every operational prompt has completion criteria; `FC-P04` adds role/state matrices |
| Reproducibility | **Adequate** | `ENVPARITY-01`: behaviour-relevant divergence ranked by consequence (config/flags, data shape and volume, dependency versions, service inventory, network, limits, identity, time/locale, build mode), cause proven by single-variable experiment, config contract with a CI parity check. `DEVENV-01` covers reproducible setup; this covers behaviour that survives a correct setup |
| Regression prevention | Adequate | `QA-P06`, `DEP-P04` and `WF-VERIFY` all require mutation probing |
| Integration testing | Partial | `QA-P04` names contract tests; no dedicated contract-testing prompt |
| Security validation | Adequate | `SEC-P06` route × role matrix; `ABUSE-01` adds the abuse axis — limiting dimension per abuse type, staged enforcement with a measured false-positive budget, exemption and appeal paths |
| Release readiness | Adequate | `REL-P01` |
| Post-change monitoring | Adequate | `REL-P04`, `OBS-P03` |

## 9. Human collaboration

| Element | Status | Evidence / gap |
|--------|--------|----------------|
| Clarification / intake | Partial | `06-interactive` skeleton |
| Approvals / gates | Adequate | workflows define `[GATE]`s; `SEC-P01` authorisation |
| Handoffs | Adequate | `00-core/agent-orchestration`, `WF-HANDOFF` |
| Escalation | Adequate | `FIXFAIL-01`, `RECOVERY-AND-FAILURE`, incident lead model |
| Review / decision-making | Adequate | `WF-VERIFY`, audit P07/P08 |
| Continuation across sessions | Adequate | `PROJECT-STATUS.md`, ledgers, handoff contract |

## 10. Operational safety

| Element | Status | Evidence / gap |
|--------|--------|----------------|
| Backup | Partial | required by `DB-P03`; no general backup-strategy prompt |
| Restore / restore drills | Adequate for DB changes | `DB-P03` requires an executed drill; no system-wide DR exercise |
| Rollback | Adequate | `REL-P03` three layers, `DB-P05` reverse-path status |
| Access control | **Adequate** | `ACCESS-01`: entitlement inventory from providers rather than the roster, per-entitlement decisions, removals verified in the system, break-glass verified unused, standing-access and exception registers |
| Secret protection | Adequate | `00-core/safety-and-security`, `SEC-P03/P06` |
| Deployment target provisioning (managed PaaS/serverless/VPS) | **Adequate** | `DEPLOY-01` + `PLATFORM-PROFILES.md`: app-shape classification, build/runtime/preview variable scopes, ephemeral disk, timeouts, cold starts, region/residency, cost metering, tested rollback, exit route. Provider is an input, not an assumption |
| Host migration (changing platform without an outage) | **Adequate** | `HOSTMIG-01`: peripheral inventory (DNS, MX/TXT, cookies, callbacks, egress IPs, cron), TTL lowered ahead, dual running, pre-declared abort, data checksums, old host retained past TTL, decommission checklist |
| Reproducible dev environment and editor parity | **Adequate** | `DEVENV-01`: pinned runtimes, no global installs, one entry point, container + script, `.gitattributes` and case-sensitivity checks, CI parity, time-to-green measured |
| AI-assistant context and IDE adaptability | **Adequate** | `CTX-P01..P04`: surface inventory by tool, one canonical `AGENTS.md` with thin adapters, adherence probes (command/convention/boundary/ambiguity), machine checks and drift triggers |
| Tenant isolation (cross-customer leakage) | **Adequate** | `TENANCY-01`: store inventory, enforcement classification, seven leak patterns, two-tenant regression suite, existence-disclosure checks |
| Background job correctness | **Adequate** | `JOBS-01`: idempotency by constraint, overlap locks, visibility-timeout alignment, cursor resume, UTC scheduling |
| Email deliverability | **Adequate** | `EMAIL-01`: DNS-verified SPF/DKIM/DMARC with alignment, stream separation, bounce/suppression handling, warm-up |
| Accessibility conformance | **Adequate** | `A11Y-01`: WCAG 2.2 AA by testing, including the four 2.2 additions and a "not tested" statement |
| Secret rotation capability | **Adequate** | `SEC-ROT-01`: inventory by consumer, per-class runbook, drilled rotation with proof the old credential is rejected |
| Time and date correctness | **Adequate** | `TIME-01`: instants vs wall-clock vs dates, eight anti-patterns, DST/month-end/leap tests, frozen clocks |
| Third-party integration resilience | **Adequate** | `INTEG-01`: eight failure modes, body validation over status codes, outbound idempotency, webhook signatures, degradation |
| File upload safety | **Adequate** | `UPLOAD-01`: magic-byte validation, private bucket, signed URLs, scanning, lifecycle, deletion tied to objects |
| Localisation correctness | **Adequate** | `I18N-01`: no concatenation, locale plural rules, pseudo-localisation, RTL layout, locale-aware sorting |
| Infrastructure as code | **Adequate** | `IAC-01`: provider-API truth, provenance, per-resource drift decisions, state posture, policy checks |
| Performance budgets | **Adequate** | `PERF-BUDGET-01`: p75 baselines, deterministic CI gate, bundle attribution, third-party budget |
| Monorepo health | **Adequate** | `MONO-01`: import-level graph, boundary violations, affected-only evidence, CI time breakdown |
| API versioning | **Adequate** | `API-VER-01`: change classification, schema artifact, contract tests, deprecation with traffic thresholds |
| Disaster recovery and restore drills | **Adequate** | `DR-01`: six disaster classes, backup-chain silent failures, isolated restore drill, measured RTO/RPO, application-level verification including sequences, account-loss path |
| Operational readiness (launch gate) | **Adequate** | `OPS-01`: silence/saturation/dependency/partial failure signals, alert triage page/ticket/remove, runbook outsider test, dated proof of rollback/restore/failover, on-call access checked today, timed dry exercise |
| Incident communications | **Adequate** | `INC-COMMS-01`: facts sheet citing incident-channel messages, announced cadence, four-state vocabulary, audience separation, no unverified data-safety assurance, append-only log |
| Client-side secret exposure | **Adequate** | `SECRET-CLIENT-01`: built artifact scanned, framework inlining mechanisms, capability-based severity, extraction evidence, replacement architecture per capability, revocation before removal |
| Data residency | **Adequate** | `RESIDENCY-01`: six location kinds, configuration as evidence, client-side SDK flows, transfer register with named mechanism, enforcement control demonstrated, resilience trade-off escalated |
| Feature-level retirement | **Adequate** | `SUNSET-01`: usage by account/workflow/concentration, telemetry blind spots, dependency map, three notices, reversible sequence with the last reversible point, data decision owned and dated |
| Capacity and quota exhaustion | **Adequate** | `CAPACITY-01`: every finite resource including pools, sequences, quotas with reset windows, and certificate/key expiries; peak rather than average; date-to-ceiling and date-to-headroom per resource; autoscaler maximum and cooldown interrogated; plan per resource (scale / shed / eliminate / accept) |
| Vendor selection and concentration risk | **Adequate** | `VENDOR-01`: dependency class by blast radius, data map including what the vendor could infer, security facts with document scope and date, reliability from incident history, SLA compared to your own promise, lock-in quantified in switching days, exit plan with triggers |
| Build and CI performance | **Adequate** | `BUILD-01`: phase timings before any fix, three loops separated, work reduced before cached, hit rates measured, before/after on the same method |
| On-call shift handover | **Adequate** | `ONCALL-01`: state from systems (alerts, silences, deploys), about-to-break dates, known-noise, "if this pages you tonight", read-back, authority transfer |
| Prompt generation from a description | **Adequate** | `GEN-P01`: five modes (compose / interview / improve / decompose / port), routing against existing coverage, risk-class derivation, runnable verification table, self-score, provenance marked `draft`. Companion `GEN-P02` supplies the evaluation protocol |
| Timeboxed delivery with a demo deadline | **Adequate** | `HACK-01`: rubric mapped to demo moments, demo script as the build order, pre-declared cut lines, reserved freeze/rehearsal/submission time, stage-failure fallbacks, disclosed mocks. Scope coverage only — not team coordination under a 24-hour clock |
| Ownership handover (person, team, or agent) | **Adequate** | `HAND-P01..P05`: capability-based acceptance criteria, dual-control for lockout-risk accounts, revocation with proof, receiver-performed exercises, conditions with owners, review point. Excluded by design: recovery with no counterpart (`project-recovery`) |
| External surface audit (live URL, host, API) | **Adequate** | `SURFACE-01`: rules of engagement, baseline, redirect/header/cookie/CORS checks on the final response, sampled error behaviour, evidence per finding, coverage statement, no enumeration or exploitation |
| Feature flags and progressive delivery | **Adequate** | `FF-P01..P05` (new): inventory reconciled across code/provider/config, purpose-based typing, safe defaults, pre-declared rollout thresholds with sample-size reasoning, kill-switch use with a recorded prediction, retirement that deletes the branch |
| Destructive actions | Adequate | risk classes A–D; validator flags inconsistencies |
| Production changes | Adequate | Category C/D gates in workflows |

## 11. Maintainability

| Element | Status | Evidence / gap |
|--------|--------|----------------|
| Documentation | **Adequate** | `DOC-P01..P08`: product contract (SRS/design/ADR/handbook/runbook/API), truth audit with executed checks, task-first structure, consequence-ranked gaps, maintenance mechanism, PDF/DOCX export verified page by page |
| Technical debt | **Adequate** | `REF-P01..P07` (new) turns debt into a measured refactoring with a proven net; audit P04/P08 still quantify it |
| Dependency management | **Adequate** | `DEP-P01..P05` (new) — inventory, breaking-change assessment, execution, verification, policy |
| Architecture evolution | Partial | architecture-review skeleton; no ADR prompt |
| Knowledge preservation | **Adequate** | `WF-HANDOFF` (promoted: four failure modes, receiver-verifies-dependencies, machine-readable form) + `HAND-P02` state capture (proven vs believed, 3 a.m. brief) + `PROJECT-STATUS.md` checkpoint. Still partial on the on-call shift loop (backlog 12) |

## 12. Prompt ecosystem quality

| Element | Status | Evidence / gap |
|--------|--------|----------------|
| Discoverability | Adequate | root README routing table, catalog, system READMEs, workflows, and `GEN-P01` which routes a new request to existing coverage before writing anything |
| Consistency | Adequate | one authoring standard, validator-enforced metadata |
| Uniqueness | **Adequate** | identifiers unique (validator); `find_overlaps.py` reports four signals — shingle containment, vocabulary containment, structure similarity, and their product — because shingles miss reordered and reworded clones. CI gates shingle at 0.55 and combined at 0.75; `scripts/test_overlaps.py` pins 13 cases including a reworded clone that defeats the shingle metric. Highest current shingle pair is 0.18 and highest combined is 0.68 (the `01-contribution` parallel variants, backlog #100) |
| Metadata | Adequate | required keys, validator-enforced |
| Validation | Partial | `scripts/validate_library.py` (structural) with `scripts/test_validator.py` (6 fixtures), `scripts/test_overlaps.py` (13 fixtures), and `_meta/evidence-levels.md` generated from `_meta/evidence.json` so the executed-prompt count cannot be hand-written. Still one recorded empirical run (`DBG-01`), which that report states as 0.5% of the operational library. `GEN-P02` now defines the missing empirical protocol (frozen fixtures, two runs, trace grading, defect classification), but only `DBG-01` has been executed; every other operational prompt remains structurally reviewed only |
| Versioning | Adequate | per-prompt semver tied to maturity |
| Maintenance | Adequate | roadmap, review log, continuation checkpoint, CI |
| Prompt input configuration | **Adequate** | `_meta/prompt-inputs.md` (convention, canonical names, fallbacks), `**Inputs:**`/`{{NAME}}` validator gate, `00-core/inputs/RUN-SHEET.md`. 109/118 prompts at the time of the audit (the library has since grown to 123 operational) declare inputs; the 9 that do not are artifact-only stages where a declaration would be unused |

---

## Critical workflow end-to-end assessment

| Workflow | Entry condition | Stage order | Artifacts compatible | Acceptance | Failure handling | Safety | Verification | Status |
|----------|----------------|-------------|---------------------|------------|------------------|--------|--------------|--------|
| Idea → release (`greenfield-delivery`) | Partial — scope prompt is a skeleton | Yes | Yes | Yes | Yes | Yes | Yes | **Partial** |
| Interrupted-agent recovery (`recover-abandoned-project`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Production defect without losing changes (`INC-01` + `DBG-01` + `FIXFAIL-01`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Safe DB migration (`DB-P01..P05`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Security discovery → remediation → independent verification (`SEC-P01..P07` + `WF-VERIFY`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Legacy modernisation | **Partial** — design/strategy stages are skeletons; no cutover verification | Partial | Unknown | Partial | Partial | Partial | Partial | **Partial** |
| Frontend/backend/infra integration (`WF-INTEGRATE`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Dependency/framework upgrades (`DEP-P01..P05`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Failed deployment / corrupted config / failed migration recovery | Partial — `REL-P03` rollback + `DB-P05` reverse path; still no single combined runbook for a failed deploy with a half-applied migration | Partial | Partial | Partial | Partial | Yes | Partial | **Partial** |
| Feature completed across all layers (`FC-P01..P04`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Enterprise readiness (`GOV-P01..P03`) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Introducing AI agents with oversight and rollback | Partial — `ai-agentic` covers the product; not the engineering-workflow adoption | Partial | Partial | Partial | Partial | Yes | Partial | **Partial** |
| Handoff between engineers/agents | Adequate — `WF-HANDOFF`, `project-recovery`, status checkpoint | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Long-term maintenance loop (`continuous-improvement`) | Partial — draft, no empirical run | Yes | Yes | Yes | Partial | Yes | Partial | **Partial** |
| Compliance response end to end (`WF-COMPLY` → `STD-01` → `GOV-*` → `LIC-01`/`SUPPLY-01`/`RESIDENCY-01` → readiness) | Yes — standard, scope, owner, deadline are entry conditions | Yes | Yes — each stage produces a named artifact | Yes — gates at scope, remediation, readiness, and send | Yes — failure routing table | Yes | Yes — dated evidence per requirement | **Adequate** |

---

## Summary

Counts are computed from the tables above; they are not estimates.

| Status | Dimension rows | Workflow rows |
|--------|---------------:|--------------:|
| Adequate | 114 | 10 |
| Partial | 27 | 5 |
| Missing | 0 | 0 |
| Defective | 0 | 0 |
| Indirect | 0 | 0 |
| **Total assessed** | **141** | **15** |

**Reading this honestly:** roughly 81% of assessed dimension rows are adequate. The remainder are mostly *partial* — a prompt exists but a stage, verification, or failure path is missing — and those are named in the evidence column rather than hidden in a percentage.

**Closed in 2.19.0:** environment parity (`ENVPARITY-01`, closes the last quality-assurance gap in §8), capacity and quota exhaustion (`CAPACITY-01`), vendor selection (`VENDOR-01`); the duplicate detector gained vocabulary and structure signals with fixtures (#98); the executed-prompt count became a generated artifact (`_meta/evidence-levels.md`, #91) instead of a sentence; and a worked run sheet (#99) shows two systems composing rather than asserting that they do.

**Closed in 2.18.0:** record migration between systems (`DATA-MIG-01`), access review as a procedure (`ACCESS-01`), deletion verification (`PRIV-P04`); licence obligations (`LIC-01`), standards conformance against a named standard (`STD-01`), the compliance response workflow (`WF-COMPLY`), automation of described tasks (`AUTO-01`), client-side secret exposure (`SECRET-CLIENT-01`), supply-chain integrity (`SUPPLY-01`), data residency (`RESIDENCY-01`), feature-level sunset (`SUNSET-01`), incident communications (`INC-COMMS-01`), operational readiness (`OPS-01`), build/CI performance (`BUILD-01`), and verification of AI output (`AIVERIFY-01`).

**Closed in 2.17.0:** disaster recovery and restore drills (`DR-01`); desktop/CLI — the last missing domain (`DESK-P01..P02`); time correctness (`TIME-01`); third-party integration (`INTEG-01`); file uploads (`UPLOAD-01`); localisation (`I18N-01`); infrastructure as code (`IAC-01`); performance budgets (`PERF-BUDGET-01`); monorepo (`MONO-01`); API versioning and contract testing (`API-VER-01`); validator regression tests (`scripts/test_validator.py`).

**Closed in 2.16.0:** tenant isolation (`TENANCY-01`), secret rotation drills (`SEC-ROT-01`, closes backlog #51), background jobs (`JOBS-01`), email deliverability (`EMAIL-01`), accessibility conformance (`A11Y-01`, closes #32), data engineering as a discipline (`DE-P01..P02`, closes #71 in part).

**Corrected in 2.16.0:** SLO definition (backlog #55) was already covered by `OBS-P03` (SLIs, error budgets, burn-rate alerting); a duplicate draft was written and deleted rather than shipped.

**Closed in 2.15.0:** prompt generation and prompt evaluation (`GEN-P01`, `GEN-P02`); blockchain (`CHAIN-P01..P04`); mobile (`MOB-P01..P03`); embedded/IoT (`IOT-P01..P02`); games save data and netcode (`GD-P09`, `GD-P10`); agent tool permissions and RAG groundedness (`AI-P06`, `AI-P07`).

**Closed in 2.14.0:** deployment targets (`DEPLOY-01`), host migration (`HOSTMIG-01`), dev environment (`DEVENV-01`), agent context/IDE (`CTX-P01..P04`), on-call handover (`ONCALL-01`).

**Closed in 2.13.0:** hackathon and demo-deadline delivery (`HACK-01`); licensing.

**Closed in 2.12.0:** project handover (`HAND-P01..P05`), stage handoff contract promoted (`WF-HANDOFF`).

**Closed in 2.11.0:** documentation products and export (`DOC-P01..P08`), live surface audit (`SURFACE-01`).

**Closed in 2.10.0:** feature flags (`FF-P01..P05`).

**Closed in 2.9.0:** input retrofit across the operational library.

**Closed in 2.8.0:** code review (`CR-P01..P06`).

**Closed in 2.7.0:** git operations (`GIT-P01..P05`), prompt inputs and variables (`_meta/prompt-inputs.md`).

**Closed in 2.6.0:** money correctness (`PAY-P01..P03`).

**Closed in 2.4.0:** cost engineering (`COST-P01..P04`), privacy requests (`PRIV-P01..P03`).

**Closed in 2.3.0:** refactoring (`REF-P01..P07`).

**Closed in 2.1.x:** enterprise readiness (`GOV-P01..P03`), multi-agent orchestration (`WF-MULTIAGENT`), cross-layer integration (`WF-INTEGRATE`), decommissioning (`DEC-P01..P04`), and database engineering (`DB-P01..P05`), dependency/framework upgrades (`DEP-P01..P05`), vertical feature completion (`FC-P01..P04`), independent verification (`WF-VERIFY`), failed-fix escalation (`FIXFAIL-01`), data-loss recovery (`DATALOSS-01`), security incident response (`SECINC-01`).

**No dimension or workflow row is currently marked Missing.** The last four (data engineering, mobile, embedded/firmware, desktop CLI) were closed between 2.15.0 and 2.17.0.

The honest remainder is not "missing", it is **partial and unproven**:

- 27 dimension rows are partial — a prompt exists, but a stage, a verification, or a failure path is thin. The largest clusters are frontend, backend (P01–P08 still skeletons), infrastructure, distributed-systems design, architecture evolution, and prototype/spike discipline.
- 5 workflow rows are partial: greenfield delivery, legacy modernisation, failed-deployment-plus-half-applied-migration recovery, AI-agent adoption (`WF-AGENTADOPT` is operational, the underlying `from-scratch` stages are not), and the continuous-improvement loop.
- **Only one prompt has ever been executed against a fixture** (`DBG-01`). Every "Adequate" in this table means *structurally adequate*, evidenced by content review — not demonstrated on a real repository. Backlog #83 and #91 hold that distinction open.

*Assessed and deliberately not implemented:* prototype/spike discipline as a separate prompt (the discipline is short enough to live in `from-scratch` guidance and does not justify a file), and new domain systems for hardware/EDA and scientific computing (no evidence of demand in this library's usage).

## Maintenance of this matrix

- Re-assess whenever a system's maturity changes or a new system is added.
- A row moves to **Adequate** only when a prompt addresses the scenario's distinctive verification and failure handling — not when a related prompt exists.
- Add new rows when a workflow assessment or an incident reveals an unrepresented scenario.
- Record the reassessment date at the top; a matrix older than the latest system addition is stale.
