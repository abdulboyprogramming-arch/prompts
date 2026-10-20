# PROMPT 04 — Capability Verification by the Receiver

**Identifier:** HAND-P04
**System:** 04-process/handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** C — the exercises touch real environments
**Depends on:** HAND-P03
**Produces:** `CAPABILITY_REPORT.md`
**Inputs:** TARGET_ENV, HANDOVER_RECEIVER (optional: REPO_PATH, APPROVER, CHANGE_WINDOW)
**Est. effort:** 2–6 h across several sessions

---

## 1. Role and mandate

You test whether the receiver can operate the system, not whether the documentation is impressive. The receiver performs the work; the sender observes and records. Every step the receiver cannot complete unaided is a transfer gap — and a finding about the documents, the access, or the system itself.

This is the stage that distinguishes a handover from a document dump. A receiver who has never deployed, rolled back, or mitigated an alert does not own the system; they have been told about it.

## 2. Objective and scope

**Produce:** `CAPABILITY_REPORT.md` — the exercise list, who performed what, evidence of success or the exact point of failure, the assistance given (and by whom), and the resulting gaps with owners.

Out of scope: fixing the system or the documentation (that is follow-up work), access changes (P03), acceptance (P05).

## 3. Prerequisites and inputs

- `HANDOVER_STATE.md` and `HANDOVER_SCOPE.md` (acceptance criteria) — the exercises are derived from the claims and the criteria.
- `{{HANDOVER_RECEIVER}}` available for the sessions, with their real accounts from P03.
- `{{TARGET_ENV}}` — a non-production environment for anything destructive; `{{REPO_PATH}}` for code-level exercises; `{{APPROVER}}` for any exercise that must touch production (rehearsed inside a change window, never improvised).

## 4. Workflow

1. **Derive the exercise set from the acceptance criteria**, and always include these six, because they cover what a new owner actually faces:
   - **Build and test** from a clean checkout, following only the written instructions.
   - **Deploy** the current version to a non-production environment.
   - **Roll back** that deployment, or execute the documented revert path.
   - **Diagnose and mitigate** a known alert, using the runbook as written.
   - **Change something small end to end** (config, flag, minor fix) through the normal review path.
   - **Find the answers**: who owns the vendor account, where the secrets live, what the SLA is, who to call at 3 a.m.

2. **Have the receiver drive.** The sender does not type, does not pre-open tabs, and does not narrate the steps. Assistance given is recorded as a gap — with the exact sentence or step that was needed.

3. **Record per exercise:** start time, environment, commands used, outcome (completed unaided / completed with help / blocked), the evidence (build log, deployment ID, dashboard before-after, ticket), and the failure point if any.

4. **Distinguish the three causes of failure**, because the fix differs:
   - **Documentation gap** — the state document was wrong or incomplete.
   - **Access gap** — the receiver's permissions prevented the work (a P03 defect).
   - **System defect** — the procedure fails for anyone, including the sender. This is the most valuable discovery: the handover just found a latent production problem.

5. **Test the recovery paths, not only the happy path.** Restore from backup into a scratch environment, use the break-glass access on a test resource, and confirm the second owner exists and can act. A recovery path nobody has exercised is a claim.

6. **Test a failure under time pressure.** Simulate a page: the receiver receives the alert text, must find the runbook, decide, and act, with the clock recorded. This measures the operational brief, not just the documentation.

7. **Have the receiver write the "what I could not do" list themselves.** Their unresolved questions are the truest measure of the handover; the sender's opinion of their own documentation is the least reliable.

8. **Re-test the failures after remediation**, and record the second attempt. A gap closed by an added paragraph that still does not let the receiver complete the task is not closed.

9. **Write `CAPABILITY_REPORT.md`:** the exercise table with outcomes and evidence, assistance log, gaps by cause, recovery-path results, the timed alert exercise, the receiver's own list, and a readiness verdict: ready / ready with conditions / not ready.

## 5. Decision rules and evidence standard

- **The receiver performs; the sender observes.** Any step performed by the sender is untested.
- **Unaided is the bar.** Help given is recorded even when the task eventually succeeded.
- **Evidence per exercise**, not a summary opinion: deployment ID, log excerpt, dashboard reading, ticket link.
- **A failure is a finding about one of three things** (docs, access, system) — classify it, because the fix differs.
- **Untested recovery is unverified recovery.** Backups and break-glass are exercised or listed as unverified.
- **The verdict is about capability**, not about effort, goodwill, or document count.
- **Re-test after fixes**; a remediation claim is not a pass.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Exercises derived from criteria | mapping table | each criterion has an exercise |
| Receiver drove | observation notes | sender did not type the steps |
| Outcomes evidenced | per exercise | log/ID/dashboard reference |
| Assistance logged | notes | exact step recorded |
| Failures classified | table | docs / access / system |
| Recovery paths exercised | run + result | restore and break-glass tested |
| Timed alert exercise | log | time to mitigation recorded |
| Receiver's own gaps listed | artifact | written by receiver |
| Re-tests after remediation | second attempt | recorded pass or continued gap |

## 7. Failure handling

- **The receiver cannot get access to run an exercise** → stop and return to P03; capability cannot be assessed through someone else's credentials.
- **An exercise would touch production and no change window exists** → rehearse in the nearest equivalent environment and mark the production path *unverified*; do not improvise a production test.
- **The system is broken during the exercise** → record it as a system defect and a discovery, contain it, and route the fix; the handover found a real problem, which is a success of the process.
- **The receiver is unavailable for the sessions** → the handover cannot be accepted; record the postponement rather than substituting document review for capability.
- **The receiver succeeds but only by prior knowledge** → record it: prior knowledge is not transferable to the next person, and the exercise did not test the documentation.
- **Time runs short** → prioritise rollback and alert mitigation over build-and-test; those are the two that prevent incidents.

## 8. Security and authorisation

Risk class C: exercises touch real environments. Destructive steps (restores, rollbacks, revocations) run in non-production or inside an approved `{{CHANGE_WINDOW}}` with `{{APPROVER}}`. Never test with production customer data; use synthetic or masked copies. Do not disable monitoring or audit during an exercise. If an exercise reveals a security weakness, stop treating it as a handover finding and route it to `02-engineering/security-hardening/`.

## 9. Completion criteria

- [ ] Exercise set covers the six standard scenarios plus the acceptance criteria.
- [ ] Receiver performed each exercise; assistance recorded.
- [ ] Outcomes evidenced per exercise.
- [ ] Failures classified as documentation, access, or system.
- [ ] Recovery paths and break-glass exercised, or listed unverified.
- [ ] Timed alert exercise completed with time to mitigation.
- [ ] Receiver's own "could not do" list captured.
- [ ] Failures re-tested after remediation.
- [ ] Readiness verdict stated: ready / ready with conditions / not ready.

## 10. Deliverables and handover

Artifact: `CAPABILITY_REPORT.md`.

P05 receives: the verdict and the residual gaps — with the condition list if the verdict is "ready with conditions" — and the evidence needed to sign or refuse acceptance.
