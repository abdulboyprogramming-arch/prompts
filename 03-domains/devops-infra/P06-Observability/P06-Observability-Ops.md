# PROMPT 6 — Observability & Ops: the signal that fires before the customer calls

**Identifier:** DI-P06
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — adds instrumentation, alerts and runbook notes; no estate mutation
**Depends on:** DI-P05 (`DI_IMPLEMENTATION_LOG.md`)
**Produces:** `DI_OBSERVABILITY.md`: the signals per changed component, the alerts with thresholds and owners, the runbook entries for the failure modes the design created, and the gaps that were accepted
**Inputs:** {{PROJECT_PATH}} (optional: ALERT_ROUTING, SLO_TARGETS, ONCALL_ROTA)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You make the estate observable where this change made it newly fragile, and you write the
runbook entries for the failures the design introduced.

Infrastructure observability has a specific trap: the platform team's own changes are the
ones with the least monitoring, because the metrics that would catch them are the ones
nobody instruments. A pipeline that silently stops applying, a certificate that expires,
a state lock nobody releases — all invisible until an outage.

You implement signals and alerts. You do not replace the service-level instrumentation and
alerting programme: that is `OBS-P01` … `OBS-P05` and `OPS-01`. Where their scope covers
the question, this stage cites them instead of writing a second, competing alert set.

## 2. Objective and scope

**Produce:** `DI_OBSERVABILITY.md` with:

1. **Signal inventory** per changed component: the metric, log or check, what question it
   answers, and its label set.
2. **Platform-specific checks** that services do not provide: pipeline success and duration,
   drift detection results, state lock age, certificate and credential expiry, quota usage,
   backup age, and apply failures.
3. **Alerts** with threshold, window, severity, routing and a first action. Each mapped to a
   symptom an operator or user feels.
4. **Runbook entries** for the failure modes `DI_ARCHITECTURE.md` and `DI_PIPELINES`
   introduced, each with the diagnostic step and the safe action.
5. **The deletion list**: existing alerts that fire without action, named for removal.
6. **Accepted gaps** with impact and owner.

Out of scope: service SLI/alert design (`OBS-P03`), the readiness review (`OPS-01`), and
any production change beyond adding monitoring.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the tree and `DI_IMPLEMENTATION_LOG.md`, which lists what changed and
  what was left unverified.
- `{{ALERT_ROUTING}}` (optional) — where alerts go. If absent, name the channel and mark
  the routing `unconfirmed`; an alert with no destination is a dashboard.
- `{{SLO_TARGETS}}` (optional) — from `DI_REQUIREMENTS.md`, which defines what "unhealthy"
  means for the user-facing capabilities.
- `{{ONCALL_ROTA}}` (optional) — who is paged. If absent, name the team and mark it
  `unconfirmed`.

## 4. Workflow

1. **Start from the change, not the estate.** For each resource the implementation touched,
   ask: what failure mode does this create, and what would show it before a user notices?
2. **Instrument the platform path itself.** Pipeline failure rate and duration, queue time,
   and time since last successful apply per environment. A pipeline that has not deployed in
   three days is usually a broken pipeline, and it is the failure nobody notices because
   nothing is customer-facing.
3. **Instrument drift and lock age.** Drift count per environment, with the age of the oldest
   unexamined drift, and state lock age with an alert on a lock older than the longest
   legitimate apply.
4. **Instrument expiry.** Certificates, credentials, tokens, and signing keys, with alerts at
   a multiple of the renewal window — 30 and 7 days for a 90-day certificate, not "when it
   expires".
5. **Instrument capacity against quota.** Cloud quotas and limits are the outage that looks
   like an application bug; alert at a stated percentage and name the request process.
6. **Write each alert as an action.** Threshold, window, what the responder should do first,
   and the runbook link. Remove any alert whose first action is "investigate".
7. **Instrument backups by their age, not their job status.** A backup job that succeeds
   while writing nothing is the classic failure; the check is the age of the newest
   restorable artifact, plus the date of the last restore test.
8. **List the alerts that already exist and fire without action**, and propose their removal
   in the same document. Adding signals to a noisy system makes it worse.

## 5. Decision rules and evidence standard

- **Every alert has an action and an owner.** An alert that says "investigate" is a
  notification, not an alert.
- **Page on symptoms, ticket on causes.** Certificate expiry is a cause with a known date —
  a ticket, escalated to a page inside the final window.
- **A metric with no threshold is a dashboard.** State the number that makes it actionable.
- **Backup success is not backup health.** Age of the newest artifact and the last restore
  test are the only two signals that mean anything.
- **Cite the existing programme where it exists.** Service SLIs belong to `OBS-P03`, the
  on-call review to `OPS-01`, readiness to `OPS-01`. A second set of competing alerts is a
  defect, not thoroughness.
- **Silence is a signal too.** If the pipeline stops and nothing alerts, the estate is
  unmonitored in the direction that matters most.

## 6. Verification

- Every changed component appears in the signal inventory or is explicitly excluded with a
  reason.
- Pipeline success, duration and last-success age are instrumented per environment.
- Drift, lock age, expiry, quota and backup-age checks each exist with a threshold.
- Every alert has severity, routing, first action and a runbook entry.
- Runbook entries exist for each new failure mode, with the safe action.
- The noisy-alert removal list is written, with owners.
- Accepted gaps are listed with impact and owner.

## 7. Failure handling

- **No metrics platform exists.** Use structured logs with the same field names the metrics
  would carry, record the gap, and specify the exact metric the platform team must add. Do
  not describe log lines as alerts.
- **Alerts cannot be routed** (no paging integration): record `no paging destination`, and
  route to the channel the team actually reads while the integration is fixed. An alert to
  a channel nobody watches is worse than a dashboard, because it looks handled.
- **The responsible team is unknown.** Record the owner as `unconfirmed` and escalate to
  the platform owner; do not assign alerts to whoever is convenient.
- **Existing alerts are already overwhelming.** Do not add the new ones silently; record the
  total, propose the removals, and add the new alerts only for failure modes with no
  coverage. Say in the document which new alerts are deferred for that reason.
- **A backup cannot be verified** (no restore test possible in this environment): record
  `backup unverified`, treat the restore path as an accepted risk with an owner, and make
  `DI-P07` carry it as a residual risk rather than a solved problem.

## 8. Security and authorisation

Risk class B. Monitoring data often contains personal information: record what the new
signals collect, and keep request bodies, tokens and personal fields out of them. Alert
messages must not include secrets or full resource identifiers that leak account structure
to a broad channel. Do not add a monitoring agent or a third-party exporter without
recording the data flow and who approved it.

## 9. Completion criteria

- [ ] Signal inventory per changed component, with exclusions reasoned.
- [ ] Platform checks: pipeline, drift, lock age, expiry, quota, backup age.
- [ ] Every alert with severity, routing, first action and runbook entry.
- [ ] Runbook entries for each new failure mode.
- [ ] Noisy-alert removal list with owners.
- [ ] Accepted gaps with impact and owner.

## 10. Deliverables and handover

`DI_OBSERVABILITY.md`, the alert definitions and the runbook entries. `DI-P07` uses the
alert set to test that each one fires on an injected condition where the environment allows
it, and inherits the accepted gaps. `OPS-01` uses this document as an input when it reviews
whether the service can be operated at 03:00 by someone who did not build it.
