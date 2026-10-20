# PROMPT 01 — Third-Party Integration That Survives the Vendor

**Identifier:** INTEG-01
**System:** 05-scenarios/third-party-integration
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B (writes integration code and configuration; changing production credentials or webhook URLs is C)
**Depends on:** none
**Produces:** `.integrations/INTEGRATION.md`, a failure-mode matrix, contract tests
**Inputs:** VENDOR, INTEGRATION_TYPE (optional: CRITICALITY, SANDBOX, WEBHOOK_URL, TARGET_ENV)
**Est. effort:** 2–5 h

---

## 1. Role and mandate

You make an integration with someone else's service behave predictably when that service is slow, wrong, down, or changed without telling you.

The defining property: **you do not control the other side, and they will change.** Their API will add a required field, deprecate an endpoint, return a 200 with an error body, time out after 30 seconds while the operation succeeded, and send the same webhook three times. An integration that works in the sandbox on a good day is a demo, not a system.

## 2. Objective and scope

**Produce:** an integration contract (what you depend on, what you assume), a failure-mode matrix with handling per mode, idempotency and retry design, contract tests, and a degradation plan.

Out of scope: vendor selection, contract negotiation, and cost modelling (`03-domains/cost-engineering/`).

## 3. Prerequisites and inputs

- `{{VENDOR}}` and `{{INTEGRATION_TYPE}}` — outbound API calls, inbound webhooks, embedded widget, batch file exchange, or OAuth connection.
- `{{CRITICALITY}}` — does the product work when this vendor is down (degradable), or is the integration the product (blocking)?
- `{{SANDBOX}}` — whether a sandbox exists and how it differs from production (it always differs).
- `{{WEBHOOK_URL}}` and `{{TARGET_ENV}}`.

## 4. Workflow

1. **Write the dependency contract first**: which endpoints, which fields, which response codes, which limits (rate, payload size, timeout), which events. Then state what you assume and did not verify — an assumption you can name is a risk you can monitor.

2. **Map the failure modes**, each with a defined behaviour:

   | Mode | What it looks like | Required handling |
   |---|---|---|
   | Slow | p99 above your timeout | Timeout, then retry with backoff; never hold a request open |
   | Down | connection refused / 5xx | Circuit breaker, queued retry, degraded UI |
   | Wrong | 200 with an error payload, or stale data | Validate the body against a schema, not the status code |
   | Duplicate | webhook delivered twice | Idempotency key on every state change |
   | Out of order | events arrive reversed | Sequence or timestamp check, not arrival order |
   | Changed | new required field, renamed key | Contract test that fails before production does |
   | Rate limited | 429 with headers | Respect `Retry-After`, queue rather than hammer |
   | Partial success | some items processed | Per-item results, not one status for a batch |

3. **Design idempotency explicitly**, in both directions: your outbound calls carry a stable idempotency key derived from the business operation (not a random UUID generated per attempt), and your inbound webhook handler deduplicates on the provider's event ID, stored before processing.

4. **Never trust the status code alone.** A 200 can carry `{"error": ...}`. Parse and validate the body against a schema; treat schema violations as failures and alert, because they are the earliest signal of a breaking change.

5. **Handle the timeout ambiguity**: a timeout does not mean the operation did not happen. For anything that moves money or creates resources, design a reconciliation path — query the provider for the state of the operation by your idempotency key before retrying blindly.

6. **Verify webhooks properly**: signature verification with the raw body (not the parsed JSON), timestamp tolerance to bound replay, and a response fast enough to avoid provider retries — do the work asynchronously and acknowledge immediately.

7. **Test the sandbox's differences**, then stop trusting it: sandbox APIs often skip rate limits, always succeed, and lag behind production schema. Record every known difference.

8. **Build contract tests** that run on a schedule against a recorded fixture or the sandbox: assert the response shape, the required fields, the error format, and the auth flow. A vendor change should fail your build before it reaches a customer.

9. **Define degradation**: what the user sees when the vendor is unavailable. "Error 500" is not a degradation plan. For `{{CRITICALITY}}` blocking integrations, state the business consequence in one line.

10. **Write `.integrations/INTEGRATION.md`**: contract, failure matrix, idempotency strategy, webhook handling, sandbox differences, contract tests, degradation behaviour, and the vendor-change watch (changelog subscription, deprecation contacts).

## 5. Decision rules and evidence standard

- **The vendor will be slow, wrong, and changed.** Design for all three.
- **Validate the body, not the status code.**
- **Every retry needs an idempotency key that is stable across attempts.**
- **A timeout is an unknown outcome**, not a failure — reconcile before retrying.
- **Webhooks are at-least-once**; deduplicate on their event ID.
- **The sandbox is not production**; record the differences you know and monitor for the ones you do not.
- **Degradation is a product decision**, written down, not an error page.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Contract written | Document | Endpoints, fields, limits, assumptions listed |
| Failure matrix | Document | Eight modes with defined handling |
| Timeout handling | Code + test | Timeout returns without hanging the request |
| Circuit breaker | Test with a failing endpoint | Opens and recovers |
| Body validation | Test with error-in-200 | Treated as failure, alerted |
| Outbound idempotency | Replay a request | No duplicate effect at the vendor |
| Inbound deduplication | Replay a webhook | Processed once, event ID stored first |
| Signature verification | Tampered payload | Rejected; raw body used |
| Out-of-order events | Reversed delivery | State remains correct |
| Rate limiting | 429 simulation | Retry-After respected, queue drains |
| Contract test | Scheduled run | Fails on a schema change |
| Degradation | Vendor disabled in staging | Defined user-visible behaviour |
| Vendor watch | Process | Changelog/deprecation notifications owned |

## 7. Failure handling

- **The vendor has no idempotency support** → keep your own request log keyed by operation, and reconcile by querying state before retrying; document the residual duplicate risk.
- **Webhooks cannot be verified** (no signature) → treat the endpoint as public: verify a shared secret, restrict by IP where possible, and never trust the payload for authorisation decisions.
- **The sandbox differs materially** → build contract tests against recorded production responses (sanitised) and test in production-equivalent conditions at low volume.
- **The vendor deprecates an endpoint with a short window** → treat as a migration (`05-scenarios/platform-migration/`), not a refactor; feature-flag both paths and cut over with evidence.
- **The integration is blocking and the vendor is down** → the business accepts an outage; state that explicitly and make the status page honest rather than inventing a fallback at 2am.
- **Duplicate charges appear** → `03-domains/payments/` reconciliation first; then fix idempotency, not the symptom.
- **The vendor changes a field type silently** → the contract test should have caught it; if it did not, add the assertion that would have.

## 8. Security and authorisation

Risk class B. Vendor credentials are secrets (`02-engineering/secrets-rotation/`) and should be scoped to the minimum and rotated. Verify webhook signatures with constant-time comparison. Never log full request or response bodies by default — they routinely contain tokens and personal data. OAuth scopes are a permission grant: request the narrowest that works, and re-review when the vendor adds scopes.

## 9. Completion criteria

- [ ] Dependency contract written, including unverified assumptions.
- [ ] Eight failure modes mapped with defined handling.
- [ ] Body validated against a schema; error-in-200 tested.
- [ ] Outbound idempotency key stable across retries.
- [ ] Inbound deduplication on provider event ID, stored before processing.
- [ ] Signature verification using the raw body and a replay window.
- [ ] Timeout-outcome reconciliation designed for state-changing calls.
- [ ] Sandbox differences documented.
- [ ] Contract tests running on a schedule.
- [ ] Degradation behaviour defined and tested with the vendor disabled.
- [ ] Vendor change watch assigned to a person.

## 10. Deliverables and handover

Artifacts: `.integrations/INTEGRATION.md`, contract tests, failure-mode matrix.

Handover: `04-process/observability-reliability/` P03 adds per-vendor error-rate, latency, and schema-violation alerts; `05-scenarios/incident-response/` treats a vendor outage as an incident with a known degradation; `02-engineering/secrets-rotation/` registers the vendor credential with its consumers; `03-domains/payments/` owns reconciliation for any money-moving integration.
