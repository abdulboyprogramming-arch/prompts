# Coverage Matrix

**Version:** 1.1.0 · **Last assessed:** 2026-10-20 (post-2.14.0 reassessment) · **Method:** evidence review of every prompt file; a scenario counts as covered only when an existing prompt addresses its distinctive requirements, constraints, and verification — not because a related prompt exists.

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
| Migration (data/schema) | Adequate | `DB-P01..P05` (new) |
| Recovery | Adequate | `project-recovery`, `INC-01`, `DB-P05` |
| Integration | **Adequate** | `WF-INTEGRATE` (new) — contract reconciliation before wiring, seam table, transport and config diffs, end-to-end journey, failure paths per seam |
| Feature completion across layers | **Adequate** | `FC-P01..P04` (new) — contract, layer map, implementation, acceptance |
| Independent verification of others' work | **Adequate** | `WF-VERIFY` (new) — claims audit, clean-state reproduction, mutation probing, undeclared-change audit |
| Failed-fix escalation | **Adequate** | `FIXFAIL-01` (new) — attempt ledger, failure classification, decision to revert/re-scope/escalate |
| Continuous improvement | Partial | `WF-IMPROVE` draft; no measurement harness |

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
| Frontend | Partial | `03-domains/frontend` skeleton (a11y/state lack criteria) |
| Backend / APIs | Partial | `backend` skeleton |
| Databases | Adequate | `DB-P01..P05` (schema truth, migration design, pre-flight drills, execution/reconciliation, rollback and verification) |
| Infrastructure | Partial | `devops-infra` skeleton |
| Security | Adequate | `security-hardening` (assessment/remediation) |
| Testing | Adequate | `testing-qa` |
| AI / LLM | Adequate | `ai-agentic` |
| Data engineering | **Missing** | `data-ml-ai` conflates pipelines with modelling; no ingest/quality/lineage |
| Cost / FinOps | **Adequate** | `COST-P01..P04` (new) — attribution, waste diagnosis sized in money, safe optimisation, guardrails and unit economics |
| Privacy / subject rights | **Adequate** | `PRIV-P01..P03` (new) — cross-system subject data inventory, verified export/deletion, enforced retention |
| Money correctness | **Adequate** | `PAY-P01..P03` (new) — representation and invariants, idempotency and unknown outcomes, provider reconciliation and change-safety checklist |
| Version control operations | **Adequate** | `GIT-P01..P05` (new) — state check before destructive commands, conflict resolution by intent, history repair with a shared-history gate, reflog-based recovery, written conventions. Previously only prohibitions existed |
| Distributed systems | Partial | architecture/audit cover analysis; no design or failure-mode prompt |
| Mobile | **Missing** | No system; `03-domains/README` states the gap |
| Embedded / firmware | **Missing** | No system |
| Desktop / CLI | **Missing** | No system |
| Games | Partial | `games` skeleton (vertical-slice stage is sound) |
| Performance | Partial | audit and incident touch it; `performance` skeleton |

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
| Reproducibility | Partial | `REC-P04`, `DB-P03`; no environment-parity prompt |
| Regression prevention | Adequate | `QA-P06`, `DEP-P04` and `WF-VERIFY` all require mutation probing |
| Integration testing | Partial | `QA-P04` names contract tests; no dedicated contract-testing prompt |
| Security validation | Adequate | `SEC-P06` route × role matrix |
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
| Access control | Partial | covered in security review, not as a change procedure |
| Secret protection | Adequate | `00-core/safety-and-security`, `SEC-P03/P06` |
| Deployment target provisioning (managed PaaS/serverless/VPS) | **Adequate** | `DEPLOY-01` + `PLATFORM-PROFILES.md`: app-shape classification, build/runtime/preview variable scopes, ephemeral disk, timeouts, cold starts, region/residency, cost metering, tested rollback, exit route. Provider is an input, not an assumption |
| Host migration (changing platform without an outage) | **Adequate** | `HOSTMIG-01`: peripheral inventory (DNS, MX/TXT, cookies, callbacks, egress IPs, cron), TTL lowered ahead, dual running, pre-declared abort, data checksums, old host retained past TTL, decommission checklist |
| Reproducible dev environment and editor parity | **Adequate** | `DEVENV-01`: pinned runtimes, no global installs, one entry point, container + script, `.gitattributes` and case-sensitivity checks, CI parity, time-to-green measured |
| AI-assistant context and IDE adaptability | **Adequate** | `CTX-P01..P04`: surface inventory by tool, one canonical `AGENTS.md` with thin adapters, adherence probes (command/convention/boundary/ambiguity), machine checks and drift triggers |
| On-call shift handover | **Adequate** | `ONCALL-01`: state from systems (alerts, silences, deploys), about-to-break dates, known-noise, "if this pages you tonight", read-back, authority transfer |
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
| Discoverability | Adequate | root README routing table, catalog, system READMEs, workflows |
| Consistency | Adequate | one authoring standard, validator-enforced metadata |
| Uniqueness | Partial | identifiers unique; no near-duplicate detection |
| Metadata | Adequate | required keys, validator-enforced |
| Validation | Partial | `scripts/validate_library.py` (structural) + one recorded empirical run of `DBG-01` in `_meta/empirical-evaluation-01.md`, which produced three prompt fixes; 80 operational prompts remain structurally reviewed only |
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

---

## Summary

Counts are computed from the tables above; they are not estimates.

| Status | Dimension rows | Workflow rows |
|--------|---------------:|--------------:|
| Adequate | 78 | 9 |
| Partial | 30 | 5 |
| Missing | 4 | 0 |
| Defective | 0 | 0 |
| Indirect | 0 | 0 |
| **Total assessed** | **112** | **14** |

**Reading this honestly:** roughly 70% of assessed dimension rows are adequate. The remainder are mostly *partial* — a prompt exists but a stage, verification, or failure path is missing — and those are named in the evidence column rather than hidden in a percentage.

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

**Missing scenarios still open**, in priority order:

*Dimension rows marked Missing (4):*

1. **Data engineering** — ingest, quality, lineage, backfills at scale.
2. **Mobile** domain system.
3. **Embedded / firmware** domain system.
4. **Desktop / CLI** domain system.

*Workflow rows marked Missing:* none. Every critical workflow in the table now has a procedure, at least at `Partial`.

*Also missing but not a row above:* prototype/spike discipline, near-duplicate detection tooling for the library itself, and empirical validation of all but one prompt.

## Maintenance of this matrix

- Re-assess whenever a system's maturity changes or a new system is added.
- A row moves to **Adequate** only when a prompt addresses the scenario's distinctive verification and failure handling — not when a related prompt exists.
- Add new rows when a workflow assessment or an incident reveals an unrepresented scenario.
- Record the reassessment date at the top; a matrix older than the latest system addition is stale.
