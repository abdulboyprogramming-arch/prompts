# Operational Readiness: would the on-call engineer survive this system?

**Identifier:** OPS-01
**System:** 05-scenarios/operational-readiness
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for assessment; B for adding dashboards, alerts, and runbooks; **C** for production configuration changes
**Depends on:** none
**Produces:** `.ops/READINESS_REVIEW.md`, `.ops/RUNBOOK_GAPS.md`, alert and runbook changes
**Inputs:** SERVICE_SCOPE (optional: SLO_TARGETS, APPROVER, TIME_BUDGET)
**Est. effort:** 3–5 h for a service review; follow-up work dominates
**Gallery:** Before a launch, or after a painful incident — test whether this service can be operated at 03:00 by someone who did not build it.

---

## 1. Role and mandate

You review a running service as an operator, not as its author.

The question is not "does it work" but **"when it fails, will someone know, will they know what to do, and can they do it at 03:00 without the person who built it?"** Teams build systems they can operate in daylight with their author present. Production does not offer those conditions.

You are looking for the specific class of gap that only becomes visible when a service is on fire: an alert that pages on a symptom nobody can act on, a runbook that says "restart the service", a dashboard whose absence of data is indistinguishable from health, a queue with no age metric, a dependency with no timeout, and a deployment with no rollback because it was never tried.

## 2. Objective and scope

**Produce:** a readiness verdict per area with evidence, the concrete gaps, and changes to alerts, dashboards, runbooks, and configuration. The verdict must be usable by a decision-maker: "ready", "ready with conditions", or "not ready", with the conditions named.

Out of scope: architecture redesign, performance optimisation, and the incident response itself. Out of scope: reviewing services that do not exist yet — that is `02-engineering/from-scratch/` and `07-workflows/greenfield-delivery.md`.

## 3. Prerequisites and inputs

- `{{SERVICE_SCOPE}}` — the service, its dependencies, its users, and whether it is customer-facing, internal, or batch.
- `{{SLO_TARGETS}}` — availability and latency targets if they exist; if not, deriving them is part of the review (`04-process/observability-reliability/` P02).
- `{{APPROVER}}` — for changes to alerting and production configuration.
- `{{TIME_BUDGET}}` — depth of the review.

## 4. Workflow

1. **Establish what "working" means in observable terms.** A user-visible signal (a successful login, an order placed, a job completed), the rate expected, and the latency expected. If the only signal is "the container is running", the service is unobservable and that is the first finding.

2. **Test the signals against four failures**, using real data rather than the dashboard's presence:
   - **Silence** — the service is down and no data arrives. Does an alert fire on *absence* of data, or does the graph quietly go blank?
   - **Saturation** — CPU, memory, disk, connection pool, queue depth, and file descriptors. Which one hits the ceiling first, and is it alerted before it does?
   - **Dependency failure** — the database, cache, or vendor is slow or down. Is there a per-dependency signal, and does failure degrade or cascade?
   - **Partial failure** — one instance bad, or one tenant/route failing. Is the signal aggregated in a way that hides it?

3. **Audit every alert against three questions**: does it page a human, is there an action, and does the action help? Classify each alert as **page** (someone must act now), **ticket** (act in business hours), or **remove** (nobody would ever act). Most estates have a long tail of the third kind, and they are why real pages get ignored.

4. **Read the runbooks as an outsider would, under pressure.** For each alert, find its runbook entry and check it contains: the symptom, the likely causes ranked, the commands to diagnose, the safe first action, the escalation route, and how to confirm recovery. "Restart the pod" is not a runbook; it is a coincidence that sometimes works.

5. **Verify the recovery mechanisms by inspecting them, not by trusting them**:
   - Rollback: does the deployment have a previous known-good artifact, and has a rollback been performed in the last 90 days? If not, assume it does not work.
   - Backups: does a restore exist, and when was it last proven (`05-scenarios/disaster-recovery/`)?
   - Failover: is it automatic, tested, and does it split-brain?
   - Kill switches: is there a way to disable the risky path without a deploy?

6. **Check the operational facts that are always forgotten**: timeouts and retries on every outbound call (including the retry-storm risk), connection pool sizing versus instance count, idempotency of the operations the runbook tells people to repeat, log retention and whether logs contain personal data, cron/scheduled jobs and who notices when they do not run, and the certificate/credential expiry calendar.

7. **Walk the on-call path end to end.** Who is on call, how are they paged, do they have production access today (not "after approval"), can they reach the systems from outside the office network, and do they have the authority to make the call to roll back? A runbook that requires a permission the on-call engineer does not hold is a fiction.

8. **Run one dry exercise with no advance notice**: inject a realistic failure in a safe environment or read through the response together — page received → runbook found → diagnosis command run → action taken → recovery confirmed. Time it. Whatever breaks in this exercise breaks at 03:00.

9. **Write `.ops/READINESS_REVIEW.md`** with a per-area verdict and evidence, and **`.ops/RUNBOOK_GAPS.md`** listing each alert that lacks an actionable runbook, its owner, and the fix. Then make the changes that are cheap and safe immediately (missing absence alerts, runbook sections, timeout configuration) and schedule the rest.

10. **State the conditions of "ready with conditions" precisely**, with owners and dates. A conditional approval without conditions is an approval.

## 5. Decision rules and evidence standard

- **If nobody would act on it, it must not page.**
- **Absence of data is a failure**, and it must alert like one.
- **Rollback, restore, and failover are unproven until performed.** Recency matters; the answer is a date, not a design.
- **Every alert needs an owner and an action.** An alert without a runbook is a notification that a human is about to improvise.
- **A runbook that requires access the on-call lacks is broken**, regardless of its content.
- **Degradation is designed, not discovered**: the service must have a defined behaviour when a dependency is unavailable.
- **Timeouts and retries are reliability controls.** Missing timeouts cause cascading failure; unbounded retries amplify outages.
- Mark each area `verified` (evidence inspected) or `inferred` (documented only).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| User-visible signal | Dashboard or query | Exists, with expected rate and latency |
| Absence alerting | Alert config | Fires when telemetry stops |
| Saturation coverage | Metrics | CPU/memory/disk/pool/queue each alerted before limit |
| Dependency signals | Dashboard | Per-dependency health and latency visible |
| Alert triage | Alert inventory | Every alert classified page/ticket/remove |
| Runbook completeness | Read against alerts | Symptom, causes, commands, first action, escalation, recovery check |
| Rollback proven | Date of last rollback | Performed within 90 days, or stated as unproven |
| Restore proven | Drill record | Dated; see `DR-01` |
| Timeouts and retries | Code/config | Every outbound call has both, bounded |
| On-call access | Confirmed with the rota | Access and authority available today |
| Dry exercise | Timed walkthrough | Completed; findings recorded |
| Conditional approval | Review document | Each condition has an owner and a date |

## 7. Failure handling

- **No SLOs exist** → establish a minimal version from user expectations and current performance; do not block the review on perfect targets.
- **Nobody can perform a rollback** → treat as a blocker: rehearse it in a staging environment before calling the service ready.
- **Alerts are managed elsewhere** (a central platform team) → audit what exists, and record requests with an owner rather than assuming control.
- **The service has no staging equivalent** → review the production configuration directly and prefer changes that are reversible without a deploy.
- **The team disputes a finding** → ask for the evidence (the last time it worked); record the disagreement rather than deleting the finding.
- **The review identifies a redesign-level gap** → do not attempt it here; scope the minimal mitigation and route the redesign to `02-engineering/architecture-review/`.

## 8. Security and authorisation

Analysis is class A. Adding dashboards, alerts, and documentation is B. Changing production configuration, access, or failover behaviour is C and requires `{{APPROVER}}` plus a rollback path. Do not induce failures in production to test readiness; use a staging environment or a tabletop exercise. Dashboards and runbooks frequently contain hostnames and internal detail: keep them in the internal knowledge base, not in public repositories.

## 9. Completion criteria

- [ ] User-visible success signal defined with rate and latency.
- [ ] Silence, saturation, dependency, and partial failures each examined.
- [ ] Every alert classified as page/ticket/remove, with the removes actually removed or owned.
- [ ] Every paging alert has a runbook that passes the outsider test.
- [ ] Rollback, restore, and failover each carry a date of last proof.
- [ ] Timeouts, retries, pools, and scheduled jobs reviewed.
- [ ] On-call access and authority confirmed today.
- [ ] One timed dry exercise completed with findings.
- [ ] Verdict stated, with conditions owned and dated.
- [ ] Cheap fixes applied immediately; the rest scheduled.

## 10. Deliverables and handover

Artifacts: `.ops/READINESS_REVIEW.md`, `.ops/RUNBOOK_GAPS.md`, alert and dashboard changes, runbook updates.

Handover: `04-process/observability-reliability/` owns the SLO and alerting model this review tests; `05-scenarios/incident-response/` depends on the runbooks it validates; `05-scenarios/on-call-handover/` transfers the operational state it documents; `05-scenarios/disaster-recovery/` provides the restore evidence it requires. `04-process/release-engineering/` P01 is the pre-launch gate — this prompt is the service-level test that gate should include.
