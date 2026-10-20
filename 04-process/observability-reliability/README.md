# Observability & Reliability

**Maturity: operational (v1.0.0).** Five stages covering instrumentation, SLOs, alerting, on-call readiness, and postmortems.

**Entry point:** [`P01-Instrumentation/P01-Observability-Assessment.md`](P01-Instrumentation/P01-Observability-Assessment.md)
**Execution mode:** audit-remediation
**Risk class:** B — configuration, dashboards, alert rules, and documentation; no production deploys without explicit authorisation

## Why this system exists

Most teams do not lack monitoring; they lack *answers*. They have dashboards nobody reads, alerts that fire on causes instead of symptoms, and incidents that are rediscovered from scratch every time. This system builds the chain that actually shortens recovery: **signals → objectives → alerts that matter → a runbook that works → a postmortem that changes something.**

## Stages

| ID | Stage | Produces |
|----|-------|----------|
| OBS-P01 | [Observability assessment](P01-Instrumentation/P01-Observability-Assessment.md) | `OBS_CURRENT.md` |
| OBS-P02 | [Instrumentation: logs, metrics, traces](P02-Signals/P02-Instrumentation-Signals.md) | `SIGNALS.md`, config/dashboard changes |
| OBS-P03 | [SLOs and alerting](P03-SLO-Alerting/P03-SLOs-Alerting.md) | `SLOS.md`, alert rules |
| OBS-P04 | [On-call readiness and runbooks](P04-Oncall-Runbooks/P04-Oncall-Runbooks.md) | runbooks, `ONCALL.md` |
| OBS-P05 | [Postmortem and reliability review](P05-Postmortem/P05-Postmortem-Reliability-Review.md) | `POSTMORTEM.md`, action register |

## Shared principles

1. **Symptoms alert; causes inform.** Alert on what users experience (error rate, latency, saturation, correctness), not on CPU unless CPU is the user-visible failure.
2. **Every alert has an owner, a runbook, and an action.** An alert without a runbook is a page to nowhere; an alert without an action should be a dashboard panel.
3. **Three pillars must be correlated.** A log line, a metric spike, and a trace should be joinable via the same identifiers (trace ID, request ID, tenant ID).
4. **Cardinality is a budget.** Do not put unbounded values (user IDs, raw URLs) in metric labels; use logs or traces for those.
5. **Dashboards serve questions, not vanity.** Each panel answers a specific operational question; delete panels nobody uses.
6. **Reliability work is measured in recovery time, not in tool count.**

## Boundary with other systems

- This system does not deploy or reconfigure production infrastructure. Use `03-domains/devops-infra/` for pipeline and platform changes with the appropriate authorisation.
- Postmortems here are engineering documents. Incident *response* is `05-scenarios/incident-response/` and `07-workflows/production-incident.md`.
- Capacity planning is covered in `02-engineering/performance/`; this system consumes its output for saturation signals.

## Anti-patterns this system rejects

- "Add more logging" as a reliability strategy.
- SLOs written to match current performance rather than user expectations.
- Alert thresholds copied from defaults without a burn-rate or error-budget rationale.
- Postmortems whose actions are all "be more careful".
