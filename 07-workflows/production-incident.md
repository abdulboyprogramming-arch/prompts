# Workflow — Production Incident

**Identifier:** WF-INCIDENT
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** specialised
**Risk class:** C (read access to production signals; changes gated)
**Depends on:** `05-scenarios/incident-response/`, `05-scenarios/debugging/`, `04-process/observability-reliability/`
**Produces:** service restored, a causal explanation, and prevention work
**Gallery:** Production is broken now: restore service, keep evidence, communicate, then run the postmortem — in that order.

---

## When to use this

Something is broken in production now. Users or systems are affected. The priority is restoring service, not understanding perfectly — but the two must not be conflated.

## Sequence

| # | Phase | Prompt | Output |
|---|-------|--------|--------|
| 0 | Declare and assign | this workflow | incident channel, severity, incident lead, scribe |
| 1 | Stabilise | `05-scenarios/incident-response/` §Contain | mitigation applied or decision to wait |
| 2 | Communicate | incident response §Communicate | status update to stakeholders |
| 3 | Diagnose | `05-scenarios/debugging/` adapted to live evidence | ranked hypotheses with evidence |
| 4 | Correct | targeted fix or rollback | verified restoration |
| 5 | Confirm | monitoring + user-visible check | service-level confirmation |
| 6 | Postmortem | `04-process/observability-reliability/` postmortem stage | RCA, timeline, actions |

## Non-negotiables

1. **Mitigate before you diagnose.** Rollback, feature-flag off, failover, or rate-limit — whichever is fastest and reversible. Understanding can wait; data loss cannot.
2. **One change at a time.** Two simultaneous mitigations make attribution impossible. Record what was changed and when, to the minute.
3. **Write the timeline as you go.** Memory reconstructs fiction after 40 minutes of pressure.
4. **Production access is Category C/D.** Read-only access to logs/metrics is normal during an incident; any write (config change, data correction, deploy) needs the incident lead's explicit approval recorded in the channel.
5. **Do not "fix forward" without a rollback plan.** If the fix fails, you must be able to return to the last known state.

## Phase detail

**0 — Declare.** State severity (SEV1 user-facing outage or data loss; SEV2 degraded; SEV3 internal), affected surface, start time, lead, scribe. Confirm who can authorise production changes.

**1 — Stabilise.** Gather only the evidence needed to choose a mitigation: error rate, last deploy time, dependency status, saturation signals. Prefer the most reversible action. If the cause is a recent deploy → roll back first, diagnose second.

**2 — Communicate.** First update within 15 minutes: what is affected, what users experience, current action, next update time. No speculation about cause.

**3 — Diagnose.** Use the debugging prompt, but: evidence comes from production telemetry (logs, traces, metrics, deploy diff), hypotheses must be falsifiable with available data, and every experiment is read-only until the lead approves a change. Track a hypothesis list with evidence for and against.

**4 — Correct.** Minimal change. Record the exact command/diff. Verify against the same signals used to detect the incident. If the fix does not restore service within the agreed window, revert it and escalate.

**5 — Confirm.** Observe for a defined period (at least one traffic cycle) that error rate and latency are back to baseline, not merely that the symptom disappeared. Confirm with a user-visible check.

**6 — Postmortem.** Within 48 hours: timeline, contributing factors (plural — incidents rarely have one cause), what went well, what was luck, detection gaps, and 3–5 actions with owners and dates. Blameless: name systems and decisions, not people.

## Gates

- **GATE 1 — mitigation choice** if the action is not obviously reversible (e.g. data correction, schema change).
- **GATE 2 — production write** for any change beyond rollback to a known-good artifact.
- **GATE 3 — incident closure** requires both service confirmation and the timeline artifact.

## Failure routing

| Failure | Route |
|---------|-------|
| Cause unknown, mitigation fails | Escalate to domain owner; widen blast-radius assessment; consider full rollback to last known-good |
| Data corruption suspected | Stop writes if safe; involve data owner before any correction; preserve evidence |
| Monitoring cannot confirm recovery | Treat as unresolved; do not close on anecdote |
| Incident caused by an unauthorised change | Follow the change-management and security escalation path; preserve audit trail |
| Recurring incident | Promote to continuous improvement: the previous postmortem actions were insufficient |

## Verification

Recovery is verified, not assumed:

| Check | Method | Pass condition |
|-------|--------|----------------|
| Service restored | pre-incident baseline metrics over a full traffic cycle | within normal range |
| Data integrity | reconciliation or spot check of writes made during the incident | no lost or duplicated records |
| User-visible confirmation | the failing user path executed successfully | observed |
| Mitigation recorded | timeline entry with actor and approver | present |

## Completion criteria for the workflow

1. Service confirmed restored against pre-incident baseline signals.
2. A timestamped timeline exists, produced during the incident.
3. Every production change is recorded with who approved it.
4. Causal explanation distinguishes trigger, contributing factors, and detection gap.
5. Prevention actions have owners and dates, and at least one is scheduled.
6. User-facing impact and duration are stated accurately for any external communication.

## Anti-patterns

- Diagnosing for an hour while the service is down and a rollback is available.
- Multiple concurrent changes.
- Closing the incident when the symptom stops rather than when the metric returns to baseline.
- Postmortem that concludes "human error" and produces no systemic action.
