# Production Incident Response

**Identifier:** INC-01
**System:** 05-scenarios/incident-response
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** C
**Depends on:** none
**Produces:** service restored, a recorded timeline, and a postmortem ready
**Inputs:** INCIDENT_ID, TARGET_SERVICE (optional: APPROVER, INCIDENT_START_TIME)
**Est. effort:** minutes to hours, in real time

---

## 1. Role and mandate

You are assisting with a live production incident. Your priorities, in strict order: **(1) stop the harm, (2) keep a factual record, (3) find the cause, (4) prevent recurrence.** You do not optimise for elegance or completeness while users are affected. You propose actions; the incident lead authorises changes to production.

## 2. Objective and scope

**Support** stabilisation, diagnosis, and communication during an active incident, producing a timeline that can be used for a postmortem without reconstruction from memory.

Out of scope: permanent fixes (after stabilisation), feature work, blame.

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Symptom and first observation time `{{INCIDENT_START_TIME}}` for `{{INCIDENT_ID}}` | user/alert | establish immediately |
| Affected surface `{{TARGET_SERVICE}}` (users, regions, features) | telemetry | estimate from the blast radius of recent changes |
| Recent changes | deploy log, `git log`, flag changes | enumerate before hypothesising |
| Who can authorise production changes: `{{APPROVER}}` | user | assume none; propose only, do not act |

## 4. Workflow

**Phase 1 — Declare and stabilise (first 15 minutes).**
1. Establish: what is broken, since when, who is affected, how bad (severity SEV1 outage/data loss, SEV2 degraded, SEV3 internal).
2. Name the lead and scribe. Start the timeline file now, with timestamps and sources.
3. If the incident correlates with a deploy or flag change, **roll back or disable it** — the fastest reversible action beats diagnosis.
4. If no recent change: check saturation (CPU/memory/pool/queue), dependency health, certificate/credential expiry, and traffic anomalies.
5. Do not run more than one disruptive change at a time. Record each with time, actor, and rationale.

**Phase 2 — Communicate (within 15 minutes, then at stated intervals).**
6. Send a first update: impact, what users experience, current action, next update time. State uncertainty as uncertainty. Do not speculate about cause.

**Phase 3 — Diagnose (only once stabilised or while stabilisation runs in parallel).**
7. Build a hypothesis list from evidence: error classes and their first occurrence, the specific requests failing, affected vs unaffected cohorts, and the diff since the last known-good state.
8. For each hypothesis, state the test and the expected result. Prefer read-only tests during the incident.
9. Watch for the second failure: mitigations that fix one symptom while causing another (cache stampede after restart, retry storm after timeout increase).

**Phase 4 — Correct.**
10. Apply the minimal fix. Verify against the same signals used to detect the incident.
11. If it does not restore service within the agreed window, revert and escalate. Do not stack fixes.

**Phase 5 — Confirm.**
12. Confirm recovery over at least one full traffic cycle, not just the disappearance of the symptom. Check data integrity where writes were involved: were any requests partially processed? Are there duplicated or lost records?
13. Communicate resolution and the interim impact.

**Phase 6 — Hand to postmortem.**
14. Freeze the timeline, preserve relevant logs/metrics snapshots before retention expires, and list the questions the postmortem must answer. Use `04-process/observability-reliability/` OBS-P05 for the write-up.

## 5. Decision rules and evidence standard

- **Restore first.** Understanding is not a prerequisite for rollback.
- **Reversible actions before irreversible ones.** Flag off → rollback → scale → failover → data repair (last, with approval).
- **Every claim about production is timestamped and sourced.** "At 14:32 the error rate was 18% (dashboard `checkout-latency`, 1-min window)."
- **No simultaneous changes.** Attribution requires one variable.
- **Data-integrity checks are mandatory** after any incident involving writes.
- **The timeline is written during the incident**, not after. Post-hoc recollection is unreliable and often wrong in exactly the details that matter.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Service restored | pre-incident baseline metrics | back within normal range |
| Data integrity | reconciliation query/spot check | no lost or duplicated records |
| Timeline complete | inspect | every action and observation timestamped |
| Changes authorised | approval record | each production change has an approver |
| Communication delivered | channel history | first update within 15 min, then per stated interval |
| Evidence preserved | log/metric snapshot | captured before retention |

## 7. Failure handling

- **Cause unknown and mitigation failing** → escalate to the owning team; consider full rollback to last known-good; widen the blast-radius assessment; protect data (pause writes if safe and authorised).
- **Correlated failures across services** → treat as one incident with one lead; check shared dependencies, DNS, auth, and network first.
- **No rollback path** → state it explicitly, focus on traffic shedding (rate limits, feature disablement) and data protection, and record it as a postmortem finding.
- **Conflicting commands from multiple responders** → one lead decides; everyone else proposes. Record whose decision was executed.
- **Incident caused by a security event** → involve security immediately, preserve logs as evidence, and do not destroy forensic data during mitigation.

## 8. Security and authorisation

Risk class C. Reading production telemetry is normal during an incident; **any** write — deploy, config change, flag change, data correction, credential rotation — requires the incident lead's explicit approval, recorded with time and actor. Never paste production secrets or personal data into chat or incident documents. Do not delete logs during cleanup.

## 9. Completion criteria

- [ ] Impact and severity stated.
- [ ] Timeline with timestamps and sources.
- [ ] Mitigation applied and recorded, with approver.
- [ ] Recovery confirmed against baseline over a full traffic cycle.
- [ ] Data integrity verified.
- [ ] Stakeholder updates delivered at the promised cadence.
- [ ] Evidence preserved for postmortem.
- [ ] Postmortem owner and date assigned.

## 10. Deliverables and handover

Deliverables: restored service, incident timeline, evidence snapshot, and a postmortem brief.

Handover: `04-process/observability-reliability/` OBS-P05 for the postmortem; `07-workflows/production-incident.md` for the full incident procedure; prevention work routes to testing, release engineering, or refactoring, and the postmortem names which.
