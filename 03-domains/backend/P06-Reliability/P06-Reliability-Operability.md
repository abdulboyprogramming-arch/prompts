# PROMPT 6 — Reliability & Operability: the failure table, and what the person on call sees

**Identifier:** BE-P06
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — adds timeouts, retries, limits and instrumentation; changes runtime behaviour
**Depends on:** BE-P05
**Produces:** `BE_RELIABILITY.md`: the failure-mode table with detection and mitigation, the timeout budget, the idempotency and retry policy, the observability contract, and the security controls at every entry point
**Inputs:** {{PROJECT_PATH}} (optional: SLO_TARGET, ONCALL_ROTA)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You make the service survive its dependencies. Every dependency will fail, every network
will drop a response after the work is done, and every queue will deliver a message
twice. Your job is to decide, per dependency, what the service does in each of those
cases — and to make the answer visible to whoever is on call.

You change runtime behaviour. You do not redesign the contract (`BE-P02`) or the
architecture (`BE-P03`); where reliability needs either, you record the requirement and
send it back. The deviations listed in `BE_IMPLEMENTATION_LOG.md` (`BE-P05`) are part of
your input: a timeout the implementation skipped is a timeout this stage has to justify.

## 2. Objective and scope

**Produce:** `BE_RELIABILITY.md` containing:

1. **Failure-mode table.** One row per dependency and per internal boundary: the failure,
   how it is detected, what the service does, the blast radius, and whether the caller
   sees an error or a degraded answer.
2. **Timeout budget.** Every outbound call's timeout, the total per request, and the
   proof that the total fits the caller's budget from `BE-P01`.
3. **Retry policy.** Where retries happen, how many, with what backoff and jitter, what
   the retry budget is, and what makes a retry safe.
4. **Idempotency.** The mechanism for each at-least-once path: consumer dedupe key,
   operation key, or natural idempotency.
5. **Limits.** Concurrency, connection pool, request size, rate limits, and what happens
   at the limit — queue, reject, or shed.
6. **Observability contract.** The named metrics, logs and traces, what each answers, and
   the alerts with their thresholds and owners.
7. **Security controls.** Authn/authz per entry point, tenant isolation, input limits,
   secret handling, and the dependency surface that matters.

Out of scope: writing feature code (`BE-P05`), the test plan (`BE-P07`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the implementation. **Discovered here:** every outbound call,
  every queue consumer, the current logging and metrics libraries, and any existing
  alert rules in the deploy configuration.
- `{{SLO_TARGET}}` (optional) — the availability and latency target. If absent, derive
  the tier from `BE_CONTEXT.md` and mark the numeric target `unstated`.
- `{{ONCALL_ROTA}}` (optional) — who is paged. If absent, name the team and mark it
  `unconfirmed`; an alert with no owner is a log line.

## 4. Workflow

1. **List every outbound call and every inbound queue with a timeout.** Read the code,
   not the design: a client created without an explicit timeout has the library's default,
   which is often infinite. Record defaults you find rather than assuming.
2. **Build the failure table by walking each one.** Timeout, connection refused, 4xx,
   5xx, malformed response, slow success. For each: detected how, handled how, caller
   sees what.
3. **Fix the budget arithmetic.** Sum the worst-case timeouts on the slowest path and
   compare with the caller's deadline. If it does not fit, say which call loses and why —
   an inner timeout that exceeds the outer one is a wasted wait.
4. **Make retries safe before adding them.** A retry is only allowed on an operation that
   is idempotent or carries a key. State the key, its lifetime, and what the receiver does
   with a duplicate.
5. **Set the retry budget.** Retries multiply load exactly when the dependency is already
   struggling. Cap the retry fraction (commonly 10 % of requests), use exponential backoff
   with jitter, and never retry a 4xx that is not a rate limit.
6. **Decide shedding behaviour at each limit.** When the pool is full or the queue is
   long: fail fast with 503 and `Retry-After`, or queue with a bound. An unbounded queue
   converts a slowdown into an outage.
7. **Name the signals.** For each failure in the table, the metric or log that shows it,
   with the label set that makes it findable. Then the alert: threshold, window, and what
   the responder should do first. Three useful alerts beat thirty noisy ones.
8. **Check the security surface at each entry point**: authentication, authorisation,
   tenant scope, input size, and rate limit. Record the gap where one is missing rather
   than describing it as covered.

## 5. Decision rules and evidence standard

- **No timeout means infinite.** Every network call gets one; "the library defaults are
  fine" is not a decision.
- **Retries without idempotency cause duplicates; duplicates in a payment path cause
  double charges.** If the path is not idempotent, do not retry — return an error the
  caller can resolve.
- **A circuit breaker is for a dependency that fails fast; a bulkhead is for one that
  fails slowly.** Choose by observed behaviour, and say which you chose.
- **Alerts fire on symptoms users feel, not on causes engineers enjoy.** CPU is a cause;
  error rate and latency are symptoms. Page on the second, dashboard the first.
- **Degrade explicitly.** If a dependency is down and the service can answer with stale
  or partial data, that is a product decision — write it down with the staleness bound.
- **Every mitigation is testable.** If the table says "falls back to cache", `BE-P07`
  must be able to kill the dependency and see the fallback.

## 6. Verification

- Every outbound call has an explicit timeout, and the defaults were checked in code.
- The timeout sum per path is compared with the caller budget, with a verdict.
- Every retry sits on an idempotent or keyed operation, and the retry budget is a number.
- Every at-least-once consumer names its dedupe mechanism and its window.
- Each limit states its behaviour at saturation: reject, queue with bound, or shed.
- Each failure in the table has a named signal, and each alert has a threshold and owner.
- Each entry point's authn, authz, tenant scope and input limit are recorded as present or
  missing.
- The fallback behaviour for each degraded mode has a test in `BE-P07`'s plan.

## 7. Failure handling

- **A dependency has no timeout control** (a library, or a partner's client): wrap it,
  run it in a bounded worker, and record the residual risk. Do not call it directly from
  a request path.
- **The consumer is at-least-once and has no dedupe key.** Add one before enabling the
  consumer, or make the handler naturally idempotent (upsert by key). Running without
  either is a known duplicate generator — record it as such if it must ship.
- **There is no metrics pipeline.** Log structured lines with the same names the metrics
  would use, record the gap, and specify the metric the platform team must add. Silence
  is not observability.
- **The service writes to two systems with no outbox.** Record the dual write as an
  accepted loss window with its duration, and schedule the outbox. Do not describe it as
  consistent.
- **Alerts already exist and are noisy.** Do not add more; record which fire without
  action and propose removal. Alert fatigue is the failure mode that hides the real one.

## 8. Security and authorisation

Risk class B. Secrets come from the environment or a secret manager, never from the
repository or a log line. Structured logs redact tokens, cookies and personal fields by
name. Rate limits are per caller identity, not per IP alone, so a shared NAT cannot deny
service to a tenant. Every new outbound dependency is recorded with its data flow: what
it receives, whether that includes personal data, and on what authority.

## 9. Completion criteria

- [ ] Failure table complete for every dependency and internal boundary.
- [ ] Timeout per outbound call, budget arithmetic, and verdict.
- [ ] Retry policy with budget, jitter and the idempotency that makes it safe.
- [ ] Dedupe mechanism and window for every at-least-once consumer.
- [ ] Limit behaviour at saturation for each limit.
- [ ] Named signals, alerts with thresholds, and an owner per alert.
- [ ] Security controls per entry point, gaps recorded rather than glossed.
- [ ] Degraded modes stated with their staleness or partiality bounds.

## 10. Deliverables and handover

`BE_RELIABILITY.md`, the timeout, retry and limit configuration, and the alert rules.
`BE-P07` needs the failure table to design fault injection and the degraded modes to
verify. The on-call runbook inherits the alerts and the first response step for each. If
anything here is `unstated` — an SLO, an owner — the handover says so plainly.
