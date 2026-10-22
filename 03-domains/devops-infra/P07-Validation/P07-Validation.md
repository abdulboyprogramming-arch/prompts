# PROMPT 7 — Validation: prove the gates fire, the restore works, and the rollback runs

**Identifier:** DI-P07
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** C — runs checks and drills; restoring into a test environment is C, anything against production is D and gated
**Depends on:** DI-P06 (`DI_OBSERVABILITY.md`)
**Produces:** `DI_VALIDATION.md`: every check with its command, its result and its artifact, the gate tests, the restore drill, the rollback drill, and the residual risks
**Inputs:** {{PROJECT_PATH}} (optional: TARGET_ENV, DRILL_ENV, DRY_RUN})
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You establish that the safety mechanisms actually work: that the plan gate fails on a
destroy, that the state backup restores, that the rollback returns the estate to the
previous state, and that the alerts fire.

A gate nobody has seen fail is a gate nobody knows works. Most of this stage is deliberately
breaking things in an environment where breaking them is allowed.

## 2. Objective and scope

**Produce:** `DI_VALIDATION.md` with:

1. **Evidence table.** Check, command, environment, result, artifact. Nothing passed without
   an artifact.
2. **Static checks.** `fmt -check`, `validate`, provider and module pin consistency, the
   secret scan, and the policy checks — each with its exit code.
3. **Gate tests.** A deliberately failing fixture for each gate: a plan containing a destroy
   of an irreversible resource, a plan over the size threshold, a drifted environment, an
   unsigned approver. Each must be rejected; a gate that passes the bad fixture is broken.
4. **Restore drill.** Restore a state version and a data backup into an isolated
   environment, then prove the restored state produces an empty plan and the restored data
   passes an integrity check.
5. **Rollback drill.** Apply a reversible change in a non-production environment and roll it
   back, timing both, and record the actual number against the rollback time claimed in
   `DI_ARCHITECTURE.md`.
6. **Alert tests.** Trigger each condition where the environment allows it (kill the
   pipeline, age a lock, use a test certificate) and confirm the alert fires and routes.
   Where a trigger is impossible, `not injectable` with the reason.
7. **Residual risks** with impact and the check that would close them.

Out of scope: fixing what failed. A failed check goes back to the stage that owns it.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the tree, the pipeline definitions and the earlier artifacts.
- `{{TARGET_ENV}}` (optional) — the environment under test. Non-production by default.
- `{{DRILL_ENV}}` (optional) — where restore and rollback drills run. If absent, record
  `no drill environment`; the drills are then blocked and that is the finding.
- `{{DRY_RUN}}` (optional) — whether applies can be simulated. If absent, assume no and
  mark the drills accordingly.

## 4. Workflow

1. **Establish the baseline.** Run the static checks on the base commit and record the
   result; then on the change. A failure that predates the change is a different finding.
2. **Test every gate with a fixture designed to fail it.** Copy the pipeline stage, point it
   at a fixture plan with a destroy of a database, and confirm the job fails and the apply
   job does not run. Repeat for the size threshold, drift, and approval. Record the exit code
   and the log line that shows the rejection.
3. **Drill the restore.** This is the highest-value check in this system and the one most
   often skipped. Restore the newest state backup into an isolated backend, point the
   provider at it, and run a plan: it must be empty, or every difference must be explainable.
   Then restore the newest data backup and run the integrity check that matters for that
   store — row counts, the application's own consistency query, or a checksum of a known
   table.
4. **Drill the rollback** with a reversible change in a drill environment. Time the forward
   apply and the rollback separately. Compare the rollback time with the number
   `DI_ARCHITECTURE.md` claimed; a claim of two minutes that measures twenty is a
   documentation defect worth fixing.
5. **Test the alerts by causing the condition.** Stop the pipeline on a schedule and confirm
   the last-success-age alert fires; hold a state lock and confirm the lock-age alert fires;
   use a short-lived test certificate and confirm the expiry alert fires at its thresholds.
6. **Check the secret path end to end**: scan the repository, the plan artifacts and the CI
   logs for credential patterns, and confirm the pipeline's scan would have caught a planted
   test value.
7. **Verify permissions in the negative direction**: confirm the pull-request job cannot
   assume the production identity, and confirm a non-production identity cannot read
   production state. Record the attempt and its denial.
8. **Write the residual risk list**, including everything `not injectable` in this
   environment, with the impact and what would close it.

## 5. Decision rules and evidence standard

- **A gate that has never rejected anything is unverified.** The failing fixture is the test.
- **A restore that has never run is not a backup strategy.** Row counts or nothing.
- **A rollback time is measured or it is a guess.** Record both the claimed and the measured
  number, and fix the document if they differ.
- **`not injectable` is a result.** It is the difference between an owned risk and an
  unknown one.
- **Never run a destructive drill against production.** Restore and rollback drills run in
  an isolated environment; if none exists, the drill is blocked and that is a finding worth
  escalating.
- **Do not weaken a check to reach a pass.** If the policy check is wrong, record the
  finding and let its owner change the policy deliberately.

## 6. Verification

- Baseline recorded for the static checks.
- Each gate tested with a failing fixture, with the rejection log line.
- Restore drill: state restored, plan empty or explained; data restored, integrity check
  recorded.
- Rollback drill: forward and back timed, compared with the claimed number.
- Each alert triggered or marked `not injectable` with the reason.
- Secret scan run across repository, plan artifacts and CI logs.
- Negative permission checks attempted, with the denial recorded.
- Residual risks listed with impact and closing check.

## 7. Failure handling

- **No environment where a drill is safe** (production is the only one): record the drills
  as `blocked`, name the exact risk that leaves — an unproven restore, an unmeasured
  rollback — and escalate to the owner as the top item. Do not simulate a drill and call it
  done.
- **The state backup has no versions to restore** (versioning never enabled): record it as a
  blocking finding and treat restore as impossible until versioning is enabled, which is a
  change to be scheduled with `DI-P04`.
- **A gate passes its failing fixture.** That is a defect in the gate, not in the fixture.
  Record it with the fixture and the log, and stop the handoff until it is fixed.
- **An alert cannot be triggered** because the condition requires a real outage: mark `not
  injectable`, say what would be needed, and leave the alert unverified rather than assumed
  working.
- **The pipeline cannot be run at all in this environment** (no runners, no credentials):
  record which checks are `blocked`, run everything that is static or local, and state
  plainly that the gates and drills are unverified. Do not infer gate behaviour from the
  pipeline YAML.

## 8. Security and authorisation

Risk class C, D for anything touching production. Drills run in isolated environments with
disposable credentials. Do not paste state file contents, secret values or account
identifiers into the report; cite the resource address and the failure, not the value. A
negative permission check is read-only — attempt the assume and record the denial, do not
attempt to obtain access.

## 9. Completion criteria

- [ ] Baseline recorded.
- [ ] Each gate rejected its designed-to-fail fixture, with evidence.
- [ ] Restore drill completed for state and data, with the integrity check.
- [ ] Rollback drill timed and compared with the claim.
- [ ] Every alert triggered or `not injectable` with a reason.
- [ ] Secret scan across repository, plans and logs.
- [ ] Negative permission checks with recorded denials.
- [ ] Residual risks with impact and closing check.

## 10. Deliverables and handover

`DI_VALIDATION.md` and its artifacts, and a deploy decision: proceed, proceed with named
risk, or do not proceed. `DI-P08` uses it to close the run. Anything `blocked` or `not
injectable` becomes a standing risk that the operator inherits and that `DI-P06` must at
least surface — an unproven restore is a fact the on-call engineer needs before the incident,
not after it.
