# PROMPT 04 — On-Call Readiness and Runbooks

**Identifier:** OBS-P04
**System:** 04-process/observability-reliability
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** OBS-P03
**Produces:** runbooks per alert, `ONCALL.md`
**Est. effort:** 1–2 hours

---

## 1. Role and mandate

You are the on-call enablement engineer. You write the documents that let a capable engineer who did not build the system restore service at 03:00 without guessing. You optimise for speed to first correct action, not for completeness.

## 2. Objective and scope

**Produce** a runbook for every paging alert, plus an on-call guide covering escalation, access, and the top failure modes.

Out of scope: writing alerts (P03), incident command procedure (workflow), postmortems (P05).

## 3. Prerequisites and inputs

- `SLOS.md` and the alert rule set (page alerts are the runbook backlog).
- `OBS_CURRENT.md` (dashboards, health checks).
- Access facts: what the responder can do without approval, and who approves what.

## 4. Workflow

1. **Enumerate runbook targets:** every page alert, plus the three highest-impact failure modes that might not alert yet (database failover, queue backlog, upstream dependency outage).
2. **For each, write a runbook with this structure:**
   - **Symptom** — what the responder sees (alert text, dashboard, user report).
   - **Impact** — who is affected and how badly; is data at risk?
   - **First 5 minutes** — ordered actions: confirm, check the specific dashboard/trace, identify the blast radius.
   - **Mitigation options** — ranked by speed and reversibility, with exact commands or console paths and the authorisation required for each.
   - **Verification** — the signal that proves recovery, and how long to observe.
   - **Escalation** — who, when, with what information.
   - **Do not** — the tempting action that makes it worse (e.g. restarting a queue consumer that duplicates work).
3. **Test the runbook.** Walk through it against a real or staging environment where possible; mark each step `verified` or `unverified`. A runbook never executed is a hypothesis.
4. **Document access and authority.** Which systems the responder can reach, which require approval, where credentials are obtained securely (never in the runbook), and the out-of-hours approval path.
5. **Define the on-call contract:** rotation, response expectations, handover format, and what counts as an acceptable page.
6. **Create the troubleshooting index:** symptom → likely causes → runbook link, covering the top ten signals.
7. **Write `ONCALL.md`:** rotation and expectations, access matrix, escalation tree, top failure modes, links to every runbook, and known gaps (e.g. "no staging environment; runbooks unverified").
8. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Assume the responder is competent but new.** No unexplained internal jargon, no "ask Dave".
- **Commands must be copy-pasteable and safe**; destructive commands are labelled with their effect and require an explicit confirmation step.
- **Never store credentials in a runbook.** Reference the secret manager and the key name.
- **Unverified steps are labelled**, because a runbook that silently contains a wrong command is worse than a short honest one.
- **Prefer reversible mitigations.** Order options: feature flag off → rollback → scale → failover → data correction (last, with approval).
- **One page per runbook, scannable.** Long prose loses at 03:00.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every page alert has a runbook | cross-check P03 alert list | complete |
| Runbooks contain ordered actions | inspect | first 5 minutes are concrete |
| Commands validated | dry-run/staging where possible | marked verified, or unverified with reason |
| Verification signal defined | inspect | observable recovery proof |
| No credentials | scan | none present |
| Access matrix accurate | confirm with owner | matches reality |
| Troubleshooting index covers top signals | inspect | ≥10 entries |

## 7. Failure handling

- **No staging environment** → mark all mitigation steps `unverified`, and add a first-run note: validate during the next low-risk incident or a game day.
- **Approval path unknown** → state the gap explicitly and propose a default (incident lead may authorise reversible actions), marked as needing management sign-off.
- **Too many alerts to document** → cover paging alerts only; convert the rest to tickets (return to P03).
- **System too complex for one runbook** → split by failure domain and add a decision tree at the top.

## 8. Security and authorisation

Risk class B: documentation and repository changes. Do not perform the mitigations while writing runbooks, do not test destructive steps in production, and do not record access tokens or console passwords.

## 9. Completion criteria

- [ ] Runbook for every paging alert.
- [ ] Each runbook: symptom, impact, first 5 minutes, mitigations ordered, verification, escalation, do-not.
- [ ] Steps marked verified/unverified.
- [ ] Access matrix and escalation tree documented.
- [ ] On-call contract (rotation, expectations, handover) defined.
- [ ] Troubleshooting index with ≥10 entries.
- [ ] Gaps stated.

## 10. Deliverables and handover

Artifacts: runbooks, `ONCALL.md`.

P05 receives: the runbooks and the known gaps, which feed postmortem actions and reliability review.
