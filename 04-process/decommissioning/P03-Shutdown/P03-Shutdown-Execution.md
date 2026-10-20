# PROMPT 03 — Shutdown Execution

**Identifier:** DEC-P03
**System:** 04-process/decommissioning
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** C
**Depends on:** DEC-P02 (timeline reached, monitoring shows migration)
**Produces:** `.decommission/SHUTDOWN_LOG.md`
**Inputs:** TARGET_SERVICE, APPROVER (optional: CHANGE_WINDOW)
**Est. effort:** 30–120 min across the stages

---

## 1. Role and mandate

You are the operator taking a deprecated artefact out of service. You do it in stages, each reversible, each verified, and you stop if the evidence contradicts the plan. You do not delete infrastructure in this stage — that is P04.

## 2. Objective and scope

**Execute** the shutdown: stop new use, drain remaining traffic, confirm quiescence, and leave the system in a restorable state for a defined window.

Out of scope: deleting data or infrastructure (P04), migrating consumers (P02).

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| Monitoring shows the consumer count has reached the planned threshold | yes | do not proceed; extend the notice period |
| Named approver for Category C actions: `{{APPROVER}}` | yes | stop |
| A restore path: the artefact can be re-enabled quickly | yes | define one before starting |
| The escalation path for the "last consumer" case of `{{TARGET_SERVICE}}`, executed no earlier than `{{CHANGE_WINDOW}}` | recommended | stop and get it |

## 4. Workflow

1. **Re-verify the consumer count immediately before acting.** The plan was written days or weeks ago; consumers appear in that window. Compare per-consumer identities against the plan.
2. **Announce the start** with the exact time and the expected user-visible effect (usually none, if the plan worked).
3. **Stage 1 — stop new adoption.** Apply the version gate or flag that rejects new consumers where that is distinguishable, or at minimum publish the hard removal notice. Verify the rejection works.
4. **Stage 2 — remove traffic gradually** (10% → 50% → 100% over a defined window) if the platform allows routing changes. At each step: check error rates, consumer complaints, and the metric for the affected path. A sudden jump in errors means an undiscovered consumer — revert the step and return to P01.
5. **Stage 3 — disable the entry point while keeping the implementation.** Return a `410 Gone` (not `404`) with a link to the replacement where applicable. Keep the code deployed but unreachable, so re-enabling is a config change, not a deploy.
6. **Stage 4 — stop the workload.** Disable the scheduler, consumer, or job. Confirm it is not running (not merely marked disabled) by checking for executed runs.
7. **Stage 5 — quiescence check.** Hold for the defined window (e.g. 7–30 days) with the entry point disabled and logs retained. Any traffic reaching the disabled path is a consumer you missed: record the identity, notify the owner, and either restore service temporarily or decide it can break.
8. **Verify the replacement is carrying the load** — if this artefact had a successor, confirm its volume increased by roughly the amount removed. A drop in total traffic suggests consumers gave up rather than migrating.
9. **Log every stage** with timestamps, approver, metrics before and after, and any reversion.
10. **Hand to P04** with: quiescence evidence, retained artefact inventory (data, storage, DNS, credentials, dashboards, alerts, pipelines), and the date after which deletion is authorised.

## 5. Decision rules and evidence standard

- **Never delete in this stage.** Deletion belongs to P04 after the quiescence window, so that a missed consumer can be served again.
- **Disable, don't remove.** The reversal path is the whole safety mechanism.
- **Traffic during quiescence is a finding, not noise.** Identify who it was.
- **Return an explicit status code** so consumers and monitoring can distinguish "retired" from "broken".
- **Check the successor's volume**; a successful migration moves traffic, it does not evaporate.
- **Stop on any unexpected consumer** rather than proceeding to the next stage.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Consumer count re-verified at start | metrics | at or below threshold |
| Each stage logged with metrics | log | before/after recorded |
| Rejection verified | attempt new use | denied appropriately |
| Reversal works | re-enable test | artefact reachable again |
| Workload actually stopped | run history | no executions |
| Quiescence window observed | log | dates recorded |
| Missed consumers identified | traffic analysis | identities recorded |
| Successor load increased | metrics | consistent with removed traffic |

## 7. Failure handling

- **Errors spike during traffic removal** → revert the step, treat as an undiscovered consumer, and return to P01/P02.
- **Traffic continues during quiescence** → identify the caller; notify the owner; restore service if the consumer is legitimate and not migratable.
- **Cannot restore the artefact** (config already changed elsewhere) → stop; deletion is now unsafe regardless of the plan.
- **The successor is not ready** → abort shutdown; a retired path with no replacement is an outage.
- **An owner asks to keep it "just in case"** → record the exception with a review date; do not leave it in a half-retired state indefinitely.

## 8. Security and authorisation

Risk class C: production configuration and routing changes require a named approver. Do not delete credentials during this stage; disable and record them for P04. Keep audit logs for the shutdown itself.

## 9. Completion criteria

- [ ] Consumers re-verified immediately before acting.
- [ ] Approver and start time recorded.
- [ ] Staged traffic removal completed with metrics per stage.
- [ ] Entry point returns an explicit retired status; reversal tested.
- [ ] Workload confirmed stopped.
- [ ] Quiescence window observed; stray traffic identified.
- [ ] Successor load verified.
- [ ] Handover inventory for P04 complete.

## 10. Deliverables and handover

Artifact: `.decommission/SHUTDOWN_LOG.md`.

P04 receives: quiescence evidence, the list of assets still existing (data, storage, DNS, credentials, dashboards, alerts, dashboards, CI pipelines), and the deletion authorisation date.
