# Coverage Matrix

**Version:** 1.1.0 · **Last assessed:** 2026-10-20 (post-2.1.0 reassessment) · **Method:** evidence review of every prompt file; a scenario counts as covered only when an existing prompt addresses its distinctive requirements, constraints, and verification — not because a related prompt exists.

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
| Requirements | Partial | `REC-P02` recovers them; `from-scratch` P01 is a skeleton; no requirements-change prompt |
| Design / architecture | Partial | `AUDIT-P03` recovers; `AI-P02` designs. `architecture-review`, `feature-design-suggestion` are skeletons |
| Planning | Adequate | `REC-P05`, `QA-P04`, `SEC-P05`, `AI-P03`, workflow gates |
| Implementation | Adequate | `REC-P06`, `SEC-P06`, `QA-P05`, `AI-P04/P05`, contribution agent `P11` |
| Verification | Adequate | `QA-P06`, `SEC-P06`, `REL-P04`, `WF-VERIFY` |
| Release | Adequate | `REL-P01..P04` |
| Operation | Adequate | `OBS-P01..P05`, `INC-01` |
| Maintenance / improvement | Partial | `WF-IMPROVE` (draft), `systems-building-improvement` skeleton |
| Modernisation | Partial | `rewriting-migration` skeleton; DB change covered by `DB-P01..P05`, but no language/platform modernisation procedure |
| Retirement / decommissioning | **Adequate** | `DEC-P01..P04` (new) — consumer discovery by class with positive evidence, derived notice period, staged reversible shutdown with a quiescence window, asset-by-asset retirement decisions |

## 2. Task coverage

| Task | Status | Evidence / gap |
|------|--------|----------------|
| Creation | Partial | `from-scratch` skeleton; `WF-GREENFIELD` (draft) |
| Completion of incomplete work | Adequate | `project-recovery` whole system |
| Review | Partial | `WF-VERIFY` (adequate for claims); `code-review` skeleton |
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
| Enterprise system | **Missing** | No governance, compliance-evidence, or enterprise-readiness system (see backlog) |
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
| Orchestration | Partial | `AUDIT-P09`, `SEC-P07` adequate; multi-agent coordination missing |
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
| Destructive actions | Adequate | risk classes A–D; validator flags inconsistencies |
| Production changes | Adequate | Category C/D gates in workflows |

## 11. Maintainability

| Element | Status | Evidence / gap |
|--------|--------|----------------|
| Documentation | Partial | `documentation` skeleton; `REC-P02` reconstructs |
| Technical debt | Partial | audit P04/P08 quantify; no debt-repayment workflow |
| Dependency management | **Adequate** | `DEP-P01..P05` (new) — inventory, breaking-change assessment, execution, verification, policy |
| Architecture evolution | Partial | architecture-review skeleton; no ADR prompt |
| Knowledge preservation | Partial | handoff contract + status checkpoint; no onboarding-maintenance loop |

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
| Enterprise readiness | **Missing** — no governance/compliance system | — | — | — | — | — | — | **Missing** |
| Introducing AI agents with oversight and rollback | Partial — `ai-agentic` covers the product; not the engineering-workflow adoption | Partial | Partial | Partial | Partial | Yes | Partial | **Partial** |
| Handoff between engineers/agents | Adequate — `WF-HANDOFF`, `project-recovery`, status checkpoint | Yes | Yes | Yes | Yes | Yes | Yes | **Adequate** |
| Long-term maintenance loop (`continuous-improvement`) | Partial — draft, no empirical run | Yes | Yes | Yes | Partial | Yes | Partial | **Partial** |

---

## Summary

Counts are computed from the tables above; they are not estimates.

| Status | Dimension rows | Workflow rows |
|--------|---------------:|--------------:|
| Adequate | 57 | 8 |
| Partial | 36 | 5 |
| Missing | 5 | 1 |
| Defective | 0 | 0 |
| Indirect | 0 | 0 |
| **Total assessed** | **98** | **14** |

**Reading this honestly:** roughly 58% of assessed dimension rows are adequate. The remainder are mostly *partial* — a prompt exists but a stage, verification, or failure path is missing — and those are named in the evidence column rather than hidden in a percentage.

**Closed in 2.1.x:** cross-layer integration (`WF-INTEGRATE`), decommissioning (`DEC-P01..P04`), and database engineering (`DB-P01..P05`), dependency/framework upgrades (`DEP-P01..P05`), vertical feature completion (`FC-P01..P04`), independent verification (`WF-VERIFY`), failed-fix escalation (`FIXFAIL-01`), data-loss recovery (`DATALOSS-01`), security incident response (`SECINC-01`).

**Missing scenarios still open**, in priority order:

*Dimension rows marked Missing (5):*

1. **Enterprise system readiness / governance** — control evidence, change management, auditability.
2. **Data engineering** (ingest, quality, lineage, backfills at scale).
3. **Mobile** domain system.
4. **Embedded / firmware** domain system.
5. **Desktop / CLI** domain system.

*Workflow rows marked Missing (1):*

6. **Enterprise readiness** end-to-end (depends on item 1).

*Also missing but not a row above:* prototype/spike discipline and near-duplicate detection tooling for the library itself.

## Maintenance of this matrix

- Re-assess whenever a system's maturity changes or a new system is added.
- A row moves to **Adequate** only when a prompt addresses the scenario's distinctive verification and failure handling — not when a related prompt exists.
- Add new rows when a workflow assessment or an incident reveals an unrepresented scenario.
- Record the reassessment date at the top; a matrix older than the latest system addition is stale.
