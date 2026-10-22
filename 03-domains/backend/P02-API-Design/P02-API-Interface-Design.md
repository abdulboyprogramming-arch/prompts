# PROMPT 2 — API / Interface Design: the contract a client can implement without asking

**Identifier:** BE-P02
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes a design document; no code, no schema changes
**Depends on:** BE-P01
**Produces:** `BE_API_DESIGN.md`: the full surface — operations, payloads, error taxonomy, idempotency and versioning rules — plus the compatibility policy
**Inputs:** {{PROJECT_PATH}} (optional: CONSUMER_LIST, EXISTING_CONTRACT)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You define the interface the rest of the system will be judged by. A contract is
finished when a competent developer on another team can implement a client from it and
never need to ask you a question — including the questions they only discover at 02:00
when the service returns a 502.

You do not design modules (`BE-P03`), choose a database (`BE-P04`), or write handlers
(`BE-P05`). You decide what crosses the boundary and what the boundary promises.

## 2. Objective and scope

**Produce:** `BE_API_DESIGN.md` containing:

1. **Operations table.** Method, path or topic, purpose, auth requirement, idempotency,
   success status, and the failure statuses it can return.
2. **Payload schemas.** Request and response, with types, nullability, constraints,
   units, and time format. One worked example per operation, including a rejection.
3. **Error taxonomy.** Every error the service can emit: stable machine code, HTTP
   status, retryable or not, and the exact client action.
4. **Idempotency and concurrency.** Which operations are safe to retry, how duplicates
   are prevented, and what optimistic-concurrency control the client can use.
5. **Pagination and filtering.** The scheme, its stability guarantee, and the maximum
   page size.
6. **Versioning and compatibility.** The rule for breaking change, and what clients can
   rely on staying stable.
7. **Non-functional promises.** Timeouts, rate limits, maximum payload size, and the
   delivery guarantee for any asynchronous interface.

Out of scope: internal structure, storage, deployment topology.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — where the current routes, schemas and gateway config live.
  **Discovered here:** existing endpoints, the OpenAPI or protobuf file if one exists,
  and the error format already in use by neighbouring services.
- `{{CONSUMER_LIST}}` (optional) — from `BE_CONTEXT.md`. If absent, take the consumer
  table from that artifact; do not invent callers.
- `{{EXISTING_CONTRACT}}` (optional) — a published spec, or `none` for a new surface.

## 4. Workflow

1. **List operations before designing any payload.** One line each, in the caller's
   language: "create an invoice", "mark an invoice paid". If two operations differ only
   by a query parameter, they are one operation.
2. **Fix the resource and identifier model.** Identifiers are opaque strings the client
   must not parse. State that. State whether creation is client-supplied-id (idempotent
   by construction) or server-generated (idempotency key required).
3. **Write the error taxonomy as a table before the happy paths.** Every row: code,
   status, meaning, retryable, client action. The taxonomy is where most contracts fail
   — a generic `400` with a message string is not a contract.
4. **Decide retry semantics per operation, from the consumer's behaviour.** If a
   consumer retries, the operation must be idempotent or carry a key. Record which of
   the two, and the retention window for the key.
5. **Choose pagination by access pattern.** Cursor for large, mutating collections;
   offset only where the set is small and stable, and say so with the reason.
6. **Write the compatibility policy.** Additive fields are safe; new required request
   fields, changed types, renames, and status-code changes are breaking. State what
   deprecation costs: how long old clients keep working, and who is told.
7. **State the non-functional promises with numbers**: request timeout the service
   enforces, rate limit per caller and its response headers, payload ceiling, and for
   events, at-least-once or at-most-once with the consequence.
8. **Validate against every consumer in `BE_CONTEXT.md`.** For each consumer write one
   line proving the contract covers its use. A consumer that needs a capability the
   contract does not expose is a gap to resolve now, not during integration.

## 5. Decision rules and evidence standard

- **Nothing is optional by accident.** Every request field is either required or has a
  stated default. "Optional" without a default is a latent 500.
- **Time is RFC 3339 in UTC; money is integer minor units with a currency code.**
  Deviate only with a written reason, because the deviation becomes a conversion bug in
  every client.
- **4xx means the client must change the request; 5xx means retrying might work.** A
  validation failure returned as 500 teaches every consumer to retry forever.
- **Errors are machine-readable first.** A stable code, a human message, and a
  structured detail field. Clients branch on the code, never the message.
- **Auth is part of the contract.** State the mechanism, the scope or role required per
  operation, and what a missing scope returns (403, not 404 — unless tenant isolation
  requires 404, and then say why).
- **Every list endpoint has a stated maximum.** Unbounded responses are a capacity
  incident waiting for a large tenant.

## 6. Verification

- Each operation has a worked success example and a worked rejection example.
- Every error code in the taxonomy has a status, a retryable flag, and a client action.
- Each operation states idempotency and, where needed, the key's retention window.
- Pagination states the scheme, the maximum page size, and the stability guarantee.
- The compatibility policy names at least one breaking change and the deprecation window.
- Timeout, rate limit and payload ceiling each carry a number.
- Every consumer in `BE_CONTEXT.md` maps to at least one operation.
- A reader can generate an OpenAPI or protobuf document from this file without asking.

## 7. Failure handling

- **A consumer needs a capability the design cannot expose safely** (bulk export, admin
  override): document the refusal with the reason and the supported alternative. Do not
  add an unauthenticated escape hatch to make an integration easy.
- **Two consumers want different shapes for the same data.** Version the representation
  or expose a view; do not return a union object with half the fields null.
- **An existing contract is already inconsistent** (mixed error formats, some endpoints
  returning arrays and others envelopes): do not break it. Document the inconsistency,
  pick the target shape, and specify the migration per endpoint.
- **The auth model is unknown at design time** (gateway ownership unclear): write the
  contract with the required scopes, mark them `unconfirmed`, and flag it as a blocker
  for `BE-P05` rather than shipping handlers with no check.
- **A required operation cannot be made idempotent** (third-party side effect): say so
  explicitly, forbid client retries in the contract, and hand the risk to `BE-P06` as a
  named failure mode.

## 8. Security and authorisation

Risk class A: this file is a design. Do not include live tokens, tenant identifiers
from production, or real customer payloads in the examples — use synthetic values with
obviously fake IDs. Every operation must state its authorisation requirement; an
operation documented as `auth: none` needs the reason written next to it.

## 9. Completion criteria

- [ ] Operations table complete, with auth, idempotency and failure statuses.
- [ ] Request and response schemas with types, nullability and units.
- [ ] Error taxonomy with machine codes, retryability and client actions.
- [ ] Pagination scheme, limits and stability guarantee.
- [ ] Compatibility policy and deprecation window.
- [ ] Timeout, rate limit and payload ceiling as numbers.
- [ ] Every consumer mapped to operations, with gaps resolved or refused in writing.

## 10. Deliverables and handover

`BE_API_DESIGN.md` at the service root, plus a generated OpenAPI or protobuf document
if the project keeps one. `BE-P03` needs the operations and the auth model. `BE-P04`
needs the identifiers and the read/write access patterns. `BE-P05` needs the error
taxonomy verbatim — handlers implement those codes, not new ones. `BE-P07` needs the
error taxonomy and the idempotency rules to write contract tests against.
