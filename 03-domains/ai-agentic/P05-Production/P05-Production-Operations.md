# PROMPT 05 — AI Production Operations

**Identifier:** AI-P05
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** AI-P04
**Produces:** `AI_OPERATIONS.md`, telemetry config
**Inputs:** TARGET_SERVICE, TARGET_ENV
**Est. effort:** 1–2 hours

---

## 1. Role and mandate

You are the AI platform operator. You make a probabilistic system operable: you can see what it did, why, at what cost, and whether it got worse. You wire human oversight where consequence demands it, and you define how a bad release is detected and reversed.

## 2. Objective and scope

**Implement** request-level telemetry, cost and latency accounting, quality monitoring, oversight checkpoints, and a safe release process for model/prompt changes.

Out of scope: infrastructure provisioning (`03-domains/devops-infra/`), initial evaluation design (P03), incident command (`05-scenarios/incident-response/`).

## 3. Prerequisites and inputs

- `AI_ARCHITECTURE.md` (contract, degradation), `EVAL_PLAN.md` (harness), `SAFETY.md` (detection signals, residual risks).
- Access to model provider metrics/billing for `{{TARGET_SERVICE}}` in `{{TARGET_ENV}}` if available.

## 4. Workflow

1. **Instrument every model call** with: timestamp, feature, model + version, prompt template version, input/output token counts, latency, cost, finish reason, retry count, validation outcome, request ID, and tenant (hashed). Do not log full prompt/response bodies by default; when debugging requires the body, use a sampled, access-controlled store with a retention measured in days.
2. **Track unit economics.** Cost per request, per feature, per tenant; token breakdown; cache hit rate; cost of retries and failed validations. Set budget alerts.
3. **Track quality in production**, not just latency: validation failure rate, refusal rate, judge score on a sampled stream, retrieval miss rate, user feedback signals, and escalation-to-human rate. Sample deliberately (e.g. 1–5%) to control cost.
4. **Wire safety detection** from P04: injection suspicion, tool-call anomalies, out-of-policy attempts, repeated refusals. Route to alerts with owners.
5. **Implement human oversight** per the P01 mapping: approval queues for destructive actions, review sampling for generated content that is published, and a visible audit trail of who approved what and when. Ensure timeouts fail closed (no action taken).
6. **Design the release process for non-code artifacts.** Prompts, model versions, retrieval config, and guardrails are releases: versioned, reviewed, evaluated against the eval set, canaried on a traffic slice, and reversible by pinning the previous version. A prompt change deployed without an eval run is an unreviewed production change.
7. **Define rollback:** previous prompt template version, previous model version, feature flag to disable the AI path, and the deterministic fallback behaviour.
8. **Define evaluation in CI and in production:** smoke eval on every change; full eval nightly; drift monitoring (input distribution, refusal rate, quality score) weekly.
9. **Write `AI_OPERATIONS.md`:** telemetry fields, dashboards to build (with the question each answers), cost model and alerts, quality monitoring, safety alerts and owners, oversight procedures, release checklist, rollback procedure, drift review cadence, and open risks.
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Non-code releases need the same rigour as code.** Version prompts like code; record who changed what and the eval delta.
- **No PII in telemetry.** Hash identifiers; redact bodies; set retention explicitly.
- **Quality monitoring requires sampling plus human calibration.** Judge-only monitoring drifts with the judge.
- **Timeouts must fail closed.** An approval that never arrives must not result in the action being taken.
- **Cost is a first-class metric.** Record the calculation method, not just a monthly total.
- **Alert thresholds must have owners and runbooks**, per OBS-P03.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Telemetry emitted for every call | test request | all required fields present |
| No PII/body leakage | inspect sampled log | redacted |
| Cost computed and attributed | reconcile sample against billing | within expected variance |
| Quality metrics populated | inspect dashboard/query | non-empty with defined window |
| Oversight timeouts fail closed | test approval expiry | no action performed |
| Release checklist executable | dry-run | prompt change goes through eval + canary |
| Rollback tested | perform in staging or dry-run | previous version restorable |

## 7. Failure handling

- **No provider metrics access** → derive cost from token counts and published prices; state the approximation.
- **No staging traffic slice** → canary on an internal user cohort or a feature flag percentage; if impossible, require manual review of the first N requests post-release.
- **Quality monitoring too expensive** → reduce sample rate, use cheaper judge, and increase human review for high-consequence features.
- **Drift detected** → do not retune silently; investigate input distribution change first, then prompt/model, then escalate.

## 8. Security and authorisation

Risk class B: telemetry configuration and application code. No production deploys without authorisation; no provider key creation; no logging of full prompt bodies containing user data; access-control any debugging store.

## 9. Completion criteria

- [ ] Per-call telemetry with the required fields.
- [ ] Cost attribution and budget alerts.
- [ ] Production quality metrics with sampling and calibration.
- [ ] Safety alerts routed with owners.
- [ ] Oversight implemented, failing closed.
- [ ] Release checklist covering prompts/models/retrieval/guardrails.
- [ ] Rollback path defined and tested.
- [ ] Drift review cadence set.

## 10. Deliverables and handover

Artifacts: `AI_OPERATIONS.md`, telemetry and alert configuration.

Handover: wire alerts into `04-process/observability-reliability/`; route recurring quality failures into P03 (evaluation gaps) rather than ad-hoc prompt patching; route systematic tool misuse into P04 (privilege reduction).
