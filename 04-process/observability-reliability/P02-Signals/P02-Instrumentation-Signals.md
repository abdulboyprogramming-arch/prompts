# PROMPT 02 — Instrumentation: Logs, Metrics, Traces

**Identifier:** OBS-P02
**System:** 04-process/observability-reliability
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** OBS-P01
**Produces:** instrumentation code/config, `SIGNALS.md`
**Inputs:** IN_SCOPE
**Est. effort:** 1–3 hours

---

## 1. Role and mandate

You are the instrumentation engineer adding the minimum signals that remove the biggest blind spots found in OBS-P01. You instrument for questions, not for completeness: every signal added must answer a question an on-call engineer will actually ask.

## 2. Objective and scope

**Implement** correlation IDs, structured logging, golden-signal metrics, and trace propagation on the critical paths identified in P01.

Out of scope: dashboards and alerts (P03), runbooks (P04), performance optimisation, log platform procurement.

## 3. Prerequisites and inputs

- `OBS_CURRENT.md` (blind spots, existing conventions).
- Approved scope for what may change: `{{IN_SCOPE}}` (instrumentation is usually low-risk, but it touches production code paths).

## 4. Workflow

1. **Rank targets.** Take the top three blind spots and the two most critical request paths. State what question each new signal answers.
2. **Correlation first.** Ensure a request ID is generated at ingress (or taken from an upstream header), propagated through outbound calls and async boundaries, included in every log line and error response payload (as a safe reference, not internal detail). This single change usually yields the largest diagnostic gain.
3. **Structured logs.** Convert key production paths to structured (JSON or key-value) logs with consistent field names: `timestamp, level, service, request_id, route, status, duration_ms, error_class`. Remove or downgrade debug prints. Redact secrets/PII at the logger boundary.
4. **Metrics.** Add the missing golden signals for the critical paths: request count, error count by class, latency histogram (percentiles, not averages), saturation (pool usage, queue depth, worker utilisation). Keep label sets bounded; no user IDs or raw paths.
5. **Tracing.** Initialise the tracer and exporter, instrument inbound/outbound HTTP and database calls, and propagate context through queues/jobs. Sample deliberately (head or tail) and record the sampling policy.
6. **Business events.** For critical flows, emit a small number of domain events with stable names (e.g. `payment.capture.succeeded`) usable for alerting on *correctness*, not just uptime.
7. **Verify locally.** Run the service (if possible), trigger a request, and show the log line, metric series, and trace span in the local collector or output. If no collector is available, unit-test the instrumentation and show the emitted payload.
8. **Measure overhead.** Compare a representative operation's latency and CPU before and after instrumentation, and record the impact. Instrumentation that costs 20% throughput needs justification.
9. **Write `SIGNALS.md`:** question → signal mapping, field/metric/span naming conventions, sampling and retention assumptions, redaction rules, overhead measurement, rollout notes, and what remains uninstrumented.
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **No signal without a question.** Delete any addition that cannot name the question it answers.
- **Follow existing conventions** for logger/metric libraries unless they cannot express the need; introducing a second observability library requires justification and a migration note.
- **Redaction is not optional.** Never log tokens, passwords, full card numbers, or raw PII. Validate with a test.
- **Overhead must be measured, not assumed**; if measurement is impossible, say so and state the expected cost.
- **Do not touch alerting or dashboards** in this stage, even if obviously wrong; note them for P03.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Correlation works end to end | run a request through the path | same ID in log, trace, downstream log |
| Logs structured and complete | inspect sample output | required fields present |
| Metrics emit | query local collector or test | series with expected labels |
| Cardinality bounded | review label sources | no unbounded labels |
| Redaction effective | test with a synthetic secret | not present in output |
| Overhead measured | before/after numbers | recorded, or limitation stated |
| Tests pass | project test command | no regressions |

## 7. Failure handling

- **No local collector** → emit to stdout in the expected format and unit-test the payload; mark end-to-end verification `unverified locally`.
- **Framework lacks hooks** → add a minimal middleware/wrapper and document the seam; do not fork the framework.
- **Overhead unacceptable** → reduce sampling or field count, and record the trade-off.
- **Cannot run the service** (missing deps/services) → instrument and test at unit level; leave integration verification to a runnable environment and say so.

## 8. Security and authorisation

Risk class B: code and configuration in the repository. No production configuration changes, no deploys. Do not add a logging field that captures request bodies wholesale.

## 9. Completion criteria

- [ ] Correlation IDs propagated and verified.
- [ ] Structured logs on critical paths with consistent fields.
- [ ] Golden-signal metrics including percentiles.
- [ ] Trace propagation across sync and async boundaries.
- [ ] Redaction verified by test.
- [ ] Overhead measured or limitation stated.
- [ ] `SIGNALS.md` complete; ledger updated.

## 10. Deliverables and handover

Artifacts: instrumentation changes, `SIGNALS.md`.

P03 receives: the available metrics and business events, plus the naming conventions, so alerts are written against real series.
