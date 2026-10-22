# PROMPT 8 — DevOps & Infrastructure Master Orchestrator: the gates between seven stages

**Identifier:** DI-P08
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** A — coordinates stages and checks artifacts; changes nothing itself
**Depends on:** DI-P01 … DI-P07
**Produces:** `DI_RUN.md`: the stage ledger, each gate's verdict with its evidence, the open questions carried forward, and the deploy decision
**Inputs:** {{PROJECT_PATH}} (optional: SCOPE, START_STAGE)
**Est. effort:** minutes per gate

---

## 1. Role and mandate

You run the infrastructure system and you stop it when a gate fails. The value is the
refusal: an estate with no locked state, a plan gate nobody has seen reject anything, or a
restore that has never run does not reach production because the sequence says it is time.

You do not write the artifacts. You read them, check them against their own completion
criteria, and record the verdict.

## 2. Objective and scope

**Produce:** `DI_RUN.md` containing the stage ledger (ran, skipped, blocked), each gate's
verdict and evidence, every open question with its owner, and the final decision: proceed,
proceed with named risk, or stop.

Out of scope: doing the stages' work. A failed gate sends you back to the owning stage.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the infrastructure tree. **Discovered here:** which artifacts exist,
  their versions, and whether they predate the code and the estate they describe.
- `{{SCOPE}}` (optional) — the change under review: a new environment, a pipeline change, a
  migration. If absent, infer from the diff and state the inference.
- `{{START_STAGE}}` (optional) — resume point, valid only if earlier artifacts exist and
  are current.

## 4. Workflow

1. **Take the inventory.** Seven artifacts, their version and modification date against the
   code's. An artifact older than the change that invalidates it is stale, and a stale
   `DI_ARCHITECTURE.md` is worse than none because the blast-radius assumptions are believed.
2. **Run the gates in order**, each against the evidence below.
3. **Record each verdict** as `pass`, `pass with note`, `fail` or `blocked`, with the line of
   evidence that decided it.
4. **Carry open questions forward** with owners — a question that disappears between stages
   was dropped, not answered.
5. **Re-check the cheap invariants after any change**: every environment in `DI_CONTEXT.md`
   appears in the pipeline; every gate in `DI_IAC_PIPELINES.md` has a test in
   `DI_VALIDATION.md`; every irreversible resource in `DI_ARCHITECTURE.md` has a backup
   referenced in `DI_IMPLEMENTATION_LOG.md`.
6. **Make the deploy decision** from the evidence: `proceed`, `proceed with risk` (naming the
   risk and the accepting owner), or `stop`. Never `proceed` past a failed gate.
7. **Hand the run to the owner** with the ledger, the open questions and the decision.

## 5. The gates

| Gate | Passes only when | Evidence |
| --- | --- | --- |
| G1 after `DI-P01` | `DI_CONTEXT.md`: environments with their deltas, shared resources, blast radius per workspace, access model, state location | Artifact, with every `unknown` named |
| G2 after `DI-P02` | `DI_REQUIREMENTS.md`: four delivery metrics with formulas, SLIs with exclusions, error-budget policy with a trigger, security requirements as testable properties | Artifact |
| G3 after `DI-P03` | `DI_ARCHITECTURE.md`: isolation boundaries, promotion path by artifact digest, blast-radius table, irreversible resources named | Artifact |
| G4 after `DI-P04` | `DI_IAC_PIPELINES.md`: locked remote state with versioning, plan gate with four failure conditions, separate gated apply, rollback per change type | Artifact plus the pipeline definitions |
| G5 after `DI-P05` | `DI_IMPLEMENTATION_LOG.md`: plan summary and approver per apply, verification assertion with output, post-apply drift check, rollback recorded | Artifact plus the verification artifacts |
| G6 after `DI-P06` | `DI_OBSERVABILITY.md`: pipeline, drift, lock-age, expiry, quota and backup-age signals; every alert with an action and an owner | Artifact |
| G7 after `DI-P07` | `DI_VALIDATION.md`: every gate rejected its failing fixture, restore drill completed, rollback timed, residual risks listed | Artifact plus its artifacts |

Two rules apply at every gate:

- **No silent scope growth.** An environment, resource class or pipeline stage that appeared
  after `DI-P03` is either in the architecture or out of scope in writing.
- **No gate passes on prose.** "State is safe" is not evidence; a backend block, a lock
  mechanism and a restore result are.

## 6. Decision rules and evidence standard

- **A failed gate stops the run.** The fix belongs to that stage's owner; re-run the gate and
  keep both verdicts.
- **Unlocked or local state fails G4 outright,** whatever else is green. Two concurrent
  applies corrupt the state, and the corruption is silent until the next plan.
- **An unproven restore fails G7.** It is the single most common gap and the one with the
  worst consequences.
- **Six green gates and one blocked is not six-sevenths safe.** The blocked one decides.
- **The ledger is append-only.** A report showing only the final pass has destroyed the
  record of what was fixed.

## 7. Verification

- All seven artifacts present, with versions and staleness verdicts.
- Each gate has a verdict and the evidence line behind it.
- Invariants re-checked: environments ↔ pipeline, gates ↔ tests, irreversible ↔ backups.
- Open questions carried forward with owners.
- The decision is one of the three permitted values and matches the gates.
- Every earlier verdict retained.

## 8. Failure handling

- **A stage was skipped** (the estate "already has a design"): mark it `not run`, record the
  risk it leaves — an unknown blast radius, an unowned target — and let the owner accept it
  in writing.
- **Two artifacts contradict each other** (`DI-P05` applied something `DI-P03` never
  designed): the later stage does not win. Record the contradiction, hold at that gate, and
  send it to the design owner.
- **Scope changed mid-run**: re-enter at the earliest stage the change touches. A new
  environment returns to G1; a new pipeline stage to G4.
- **The environment cannot run the drills** (no non-production environment): record `blocked`
  at G7 with the exact missing capability and the risk carried into the deploy decision.
- **An owner is unavailable**: record the question, its deadline, and proceed only on gates
  that do not depend on it. Do not answer on their behalf.

## 9. Security and authorisation

Risk class A. Record the trust boundaries found at G1 and G3, and refuse a gate where the
pipeline identity can reach every environment, where a secret exists in the repository or a
plan artifact, or where a production credential is available to a pull-request job. Never
paste credentials, state contents or customer data into the ledger; cite the location and
the key name.

## 10. Completion criteria

- [ ] Inventory with versions and staleness verdicts.
- [ ] Verdict per gate with its evidence, earlier runs retained.
- [ ] Invariants reconciled across the artifacts.
- [ ] Open questions carried forward with owners.
- [ ] Decision consistent with the gates, or a named risk with an accepting owner.

## 11. Deliverables and handover

`DI_RUN.md` at the infrastructure root, handed to the estate owner and to the release
record. The decision, the accepted risks and the open questions travel with the change; the
ledger stays in the repository as the record of what was checked and what was not.
