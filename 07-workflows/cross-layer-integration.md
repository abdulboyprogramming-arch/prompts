# Workflow — Cross-Layer Integration

**Identifier:** WF-INTEGRATE
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** B (may reach C when wiring shared environments)
**Depends on:** each layer's own completion state
**Produces:** `INTEGRATION_PLAN.md`, `INTEGRATION_REPORT.md`
**Inputs:** INTEGRATION_ENV, LAYER_BRANCHES
**Est. effort:** 1–4 hours per integration

---

## 1. Role and mandate

You are the integrator. Independently developed frontend, backend, infrastructure, and data work each pass their own tests and still fail when joined. Your job is to make the seams explicit and prove they hold — not to rewrite any layer.

**The characteristic failure:** every component is "done" and the product does not work. The frontend calls a field name the API does not return; the API expects a header the proxy strips; the queue topic is subscribed by nothing; the migration ran in staging and not in the integration environment.

## 2. Objective and scope

**Prove** that the layers interoperate: contracts match, configuration is coherent, identity propagates, failures degrade as designed, and deployment order does not break the system.

Out of scope: implementing missing features in a layer (return that layer to its own system), performance tuning, release approval.

## 3. Prerequisites and inputs

| Input | If missing |
|-------|------------|
| The branches/artefacts `{{LAYER_BRANCHES}}` from each layer, with their own completion claims | ask what is actually done vs planned; integrate the done parts only |
| An integration environment `{{INTEGRATION_ENV}}` (or a documented local composition) | build a local composition and record what it cannot prove |
| The agreed contract: API schema, event schema, config keys | derive from the code and **state that it is derived**, then reconcile explicitly |
| Each layer's own test suite, runnable | integration cannot substitute for unit verification |

## 4. Workflow

### Phase 1 — Reconcile the contract before touching infrastructure

1. **Establish the contract's source of truth.** If there is a spec/OpenAPI/schema, use it. If not, derive it from the *serving* side (backend route handler) and compare with the *consuming* side (frontend client) field by field.
2. **Build the seam table** — one row per interaction:

   | Interaction | Producer | Consumer | Shape agreed | Auth mechanism | Failure contract |
   |-------------|----------|----------|--------------|----------------|------------------|

3. **Diff the two sides mechanically**:  generate the client types from the server schema (or vice versa) instead of comparing by eye. Record the differences: missing fields, wrong optionality, different date formats, enums that do not match, pagination shape, error envelope, nullability.
4. **Check the error contract explicitly.** What does the producer return on validation failure, unauthorised, not found, conflict, and internal error? What does the consumer do with each? A UI that renders "Something went wrong" for a 422 is an integration defect, not a polish item.
5. **Check identity propagation.** How does the caller's identity reach the data layer? Tokens in headers, cookies with CORS implications, service-to-service credentials, tenant identifiers derived from the token rather than the request body. Every hop is a place where authorisation silently disappears.

### Phase 2 — Wire the environment

6. **Enumerate every configuration key** each layer needs, where it comes from, and its default. Diff the sets: a key the backend requires and the environment does not define is a guaranteed runtime failure; a default that differs between environments is a latent one.
7. **Verify the transport realities**: base URLs, ports, path prefixes, CORS origins and preflight, proxy and header forwarding, timeouts, body size limits, TLS trust. These account for most "works locally, fails in the browser" reports.
8. **Verify infrastructure dependencies exist and are reachable from where the code runs** (inside a container, not from the host): database, cache, queue topics and subscriptions, object storage buckets, secrets. A topic with no subscriber is an integration gap even though nothing errors.
9. **Check deployment order constraints.** Can the backend deploy before the frontend? Does the migration run before the new code starts? Does the worker need the new queue before the producer publishes? Record the required order and what breaks if it is reversed.

### Phase 3 — Prove the seams

10. **Run one end-to-end journey** through every layer, from the user action to the persisted record and back, recording requests and responses at each hop. Not a smoke test of each service in isolation.
11. **Exercise the failure paths at the seams:** stop the backend and confirm the frontend shows a recoverable error rather than hanging; return a 500 and confirm it is not rendered as success; kill the worker and confirm the job is retried rather than lost. Then make the third-party dependency time out and confirm the timeout is shorter than the user's patience.
12. **Test authorisation across the boundary**, with real credentials for at least two roles, through the actual transport — not by calling the service function directly.
13. **Measure one realistic volume path**: the list endpoint with production-shaped data, the payload size the UI actually receives, and the p95 latency across the boundary. Integration is where N+1 queries and unbounded payloads become visible.

### Phase 4 — Record and hand over

14. **Write `INTEGRATION_REPORT.md`:** the seam table with status, contract diffs and how each was resolved, configuration diffs, transport findings, order constraints, journey evidence, failure-path results, authorisation results, volume findings, and **the list of what this integration did not prove**.
15. **Assign defects to their layer.** Each finding goes back to the owning system (`feature-completion`, `backend`, `devops-infra`, `documentation`), not fixed here.
16. **State the integration verdict:** `integrated` (all seams proven), `integrated with gaps` (named seams unproven and why), or `not integrated`.

## 5. Decision rules and evidence standard

- **The contract is agreed before the environment is debugged.** Wiring a mismatched contract produces hours of misleading errors.
- **Derived contracts must be labelled.** If no spec exists, say so — and recommend generating one rather than re-deriving it next time.
- **Never "fix" a contract mismatch by making the consumer tolerant** of a broken producer (silently defaulting missing fields). That converts a visible defect into silent data loss.
- **Test through the transport.** Function-level tests do not exercise CORS, serialisation, or header propagation.
- **A layer that is not deployed is not integrated**, however complete its branch.
- **Integration does not grant release approval**; it feeds `04-process/release-engineering/` P01.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Seam table complete | inspect | every interaction has a row |
| Contract diffed mechanically | generated types or schema diff | differences resolved or recorded |
| Config keys reconciled | diff of required vs defined | none missing |
| Transport verified in the real browser/runtime | request log | no CORS/proxy/timeout surprises |
| Dependencies reachable from the runtime | connection check | all reachable, topics subscribed |
| Deployment order stated | inspect | order + failure if reversed |
| End-to-end journey recorded | request/response per hop | observed |
| Failure paths exercised | induced failures | degrade as designed |
| Authorisation through transport | two roles | denials observed |
| Not-proven list written | inspect | explicit |

## 7. Failure handling

- **No integration environment** → compose locally with containers; state that TLS, DNS, and managed-service behaviour are unproven.
- **A layer is missing entirely** → integrate against a contract stub, mark every seam touching the stub as `unproven`, and do not call the result integrated.
- **Contract disagreement is a design dispute** (not a bug) → stop; the two owners agree the shape, or the integration is premature.
- **Seams pass but the journey fails** → the defect is in the composition (routing, ordering, state), not in a layer; bisect by replacing one layer with a stub at a time.
- **Environment differs from production materially** → list the differences; they are risks for release, not integration failures.
- **Integration reveals a missing feature** (not a mismatch) → route to `02-engineering/feature-completion/`; do not build it here.

## 8. Security and authorisation

Risk class B, C if wiring a shared environment. Use test credentials, never production secrets. Do not weaken CORS, TLS verification, or auth checks to make integration pass — record the constraint instead. Do not copy production data into an integration environment; generate representative data.

## 9. Completion criteria

- [ ] Contract source of truth identified (or derivation labelled).
- [ ] Seam table complete with auth and failure columns.
- [ ] Contract diffs resolved or recorded.
- [ ] Error and identity propagation verified across every hop.
- [ ] Config keys reconciled; transport verified in the real runtime.
- [ ] Dependencies reachable; topics subscribed.
- [ ] Deployment order recorded with its failure mode.
- [ ] One end-to-end journey proven with per-hop evidence.
- [ ] Failure paths and two-role authorisation exercised.
- [ ] Volume path measured.
- [ ] Defects assigned to owning layers; not-proven list written; verdict stated.

## 10. Deliverables and handover

Artifacts: `INTEGRATION_PLAN.md` (seams and order), `INTEGRATION_REPORT.md` (evidence and verdict).

Handover: `integrated` → `04-process/release-engineering/` P01. `Integrated with gaps` → gaps become the next task with an owner. `Not integrated` → the blocking seam goes back to its layer. Systemic findings (contract drift, missing schema, no composed test) → `02-engineering/codebase-audit/` or `04-process/testing-qa/`.
