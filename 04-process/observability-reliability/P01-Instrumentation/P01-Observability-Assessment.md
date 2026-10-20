# PROMPT 01 — Observability Assessment

**Identifier:** OBS-P01
**System:** 04-process/observability-reliability
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none (entry stage)
**Produces:** `OBS_CURRENT.md`
**Inputs:** REPO_PATH, TARGET_SERVICE (optional: OBS_DATA_SOURCE)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the reliability engineer auditing the ability of this system to explain its own failures. You assess what signals exist, what questions they can answer, and where an on-call engineer would be blind. You change nothing in this stage.

## 2. Objective and scope

**Answer:** when this system breaks at 03:00, what will the responder know, how fast, and what will they still have to guess?

Out of scope: designing new instrumentation (P02), alert rules (P03), runbooks (P04).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` for `{{TARGET_SERVICE}}`; read-only access to observability configuration in the repo.
- Optional: sample dashboards, alert definitions, or incident records behind `{{OBS_DATA_SOURCE}}` that the user can share.
- If production telemetry is accessible read-only, use it; otherwise assess configuration and code.

## 4. Workflow

1. **Inventory the signals found in the repository.** Logging framework and levels, metric library and metric names, tracing instrumentation and propagation, health/readiness endpoints, audit logs, and business-event events.
2. **Check correlation capability.** Is there a request/trace ID generated at ingress and propagated to logs, downstream calls, and responses? Can you join a user complaint to a log line? Cite the code.
3. **Assess log quality.** Structured vs free text; presence of timestamps, level, service, request ID, tenant/user (hashed), error context; redaction of secrets and PII; log volume controls; presence of `print`/`console.log` debugging in production paths.
4. **Assess metric coverage** against the four golden signals per critical path: latency (with percentiles), traffic, errors (by class), saturation. Note missing percentiles (averages hide tail latency).
5. **Assess trace coverage.** Are inbound requests traced? Are outbound calls instrumented? Are async/queue boundaries propagated? If tracing is absent, say so and note the cost.
6. **Review alerting configuration.** What alerts exist, on what signals, with what thresholds, to whom, and does each have a runbook link? Count alerts; identify duplicate/overlapping alerts and purely causal alerts (CPU, memory) with no symptom linkage.
7. **Review the health surface.** Do health checks test dependencies (and risk cascading failure) or only liveness? Is there a readiness distinction? Would a load balancer remove a broken instance?
8. **Check deployment and change visibility.** Are deploys logged, annotated on dashboards, and correlated with error spikes? Can you tell which version is serving traffic?
9. **Check the data-retention and cost posture.** Retention periods, sampling, cardinality risks, and cost hotspots visible from configuration.
10. **Write `OBS_CURRENT.md`:** signal inventory table, correlation verdict, log/metric/trace assessment with gaps, alert inventory with problems, health-check assessment, change visibility, cost/cardinality notes, and the top five blind spots ranked by recovery impact.
11. **Update `.obs/OBS_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Configuration is not behaviour.** A tracing library in the manifest does not mean traces are emitted; look for initialisation and export configuration.
- **Alert quality is judged by actionability**, not by count.
- **Blind spots need a failure scenario:** "no database latency metric → a slow query appears as generic 500s with no separating signal".
- Do not propose the full observability stack; P02 decides scope.
- If production telemetry is inaccessible, mark all runtime-quality conclusions `unverified` and assess configuration only.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Signal inventory cites code/config | inspect | each signal has a path |
| Correlation claim verified | inspect ID generation/propagation code | cited |
| Alert inventory complete | reconcile with config files | all rules listed |
| Blind spots have scenarios | inspect | consequence stated |
| No changes made | `git status --porcelain` | clean apart from `.obs/` |

## 7. Failure handling

- **No observability configuration in the repo** (managed externally) → record `externally managed`, list the questions to ask the platform owner, and assess what the code emits.
- **No access to telemetry** → static assessment only; state that blind-spot ranking is based on code coverage of signals, not observed behaviour.
- **No incidents on record** → rank by critical-path exposure instead of historical pain, and say so.
- **Very large system** → assess the top three critical paths exhaustively and summarize the rest.

## 8. Security and authorisation

Risk class B, artifacts only. Do not query production logs for personal data; if you must sample, use aggregated queries and redact identifiers. Do not modify alert rules or dashboards in this stage.

## 9. Completion criteria

- [ ] Signal inventory with code/config evidence.
- [ ] Correlation capability verdict.
- [ ] Log, metric, trace assessments with gaps.
- [ ] Alert inventory with actionability assessment.
- [ ] Health-check and change-visibility assessment.
- [ ] Five blind spots with failure scenarios.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `OBS_CURRENT.md`.

P02 receives: the blind spots, the signal gaps, and the correlation verdict, which determine instrumentation priorities.
