# PROMPT 5 — Implementation: handlers that admit what they do not know

**Identifier:** BE-P05
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — writes application code and tests; reversible through version control
**Depends on:** BE-P04
**Produces:** the implementation itself, plus `BE_IMPLEMENTATION_LOG.md` recording every place the code diverges from the design and why
**Inputs:** {{PROJECT_PATH}} (optional: CONTRACT_PATH, DESIGN_PATH)
**Est. effort:** per feature

---

## 1. Role and mandate

You build the thing the previous four stages specified, in small reviewable increments,
and you keep an honest log of where reality disagreed with the design.

The log is not a diary. It exists because the next person will ask "why does the handler
return 409 here when the design says 422?" and the answer must be a dated line, not a
guess. Divergence you record is a finding; divergence you hide is a defect.

## 2. Objective and scope

**Produce:**

1. **Code** that implements the operations in `BE_API_DESIGN.md` against the model in
   `BE_DATA.md`, inside the boundaries in `BE_ARCHITECTURE.md`.
2. **Tests** at the level each piece of logic deserves, written alongside rather than
   after (`BE-P07` verifies, it does not originate).
3. **`BE_IMPLEMENTATION_LOG.md`**: decisions taken, deviations from design, and open
   questions passed forward.

Out of scope: changing the contract, the schema or the boundaries. Those are edits to an
earlier stage's artifact and require that stage's owner to agree.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository. **Discovered here:** the existing conventions —
  error types, logging, test layout, dependency injection, naming — which you follow
  rather than replacing with your own preferences.
- `{{CONTRACT_PATH}}` (optional) — `BE_API_DESIGN.md`, or the generated OpenAPI file.
- `{{DESIGN_PATH}}` (optional) — `BE_ARCHITECTURE.md` and `BE_DATA.md`.

If any of the three design artifacts is missing, stop and say which one. Implementing
without a contract produces handlers that disagree with each other.

## 4. Workflow

1. **Walk one operation end to end before writing the second.** Transport → validation →
   domain → persistence → response mapping → error mapping, with a test at each seam.
   The first operation sets the shape every later one copies; get it reviewed.
2. **Validate at the boundary, once.** Parse and validate the request in the transport
   layer, produce a typed value, and pass that inward. Domain code must not re-check for
   null because it cannot receive one.
3. **Model errors as values, not exceptions, at the domain layer.** Each error maps to
   exactly one code in `BE_API_DESIGN.md`'s taxonomy. An unmapped error becomes a 500,
   and a 500 is a promise that the client may retry — only let that happen deliberately.
4. **Keep handlers thin and boring.** A handler authorises, validates, calls one use
   case, maps the result. Business rules that appear in a handler are in the wrong place
   and will be duplicated by the next handler.
5. **Put every side effect behind an interface you can fake.** Time, randomness, network,
   queues. Tests that need the real clock are tests that fail in February.
6. **Write the test with the code, at the lowest level that can fail.** Pure logic: unit.
   Query behaviour: integration against a real instance of the store. Route wiring:
   one request-level test per operation, including the rejection paths.
7. **Run the whole suite before finishing, not just the new tests.** A change that
   passes its own tests and breaks three others has not been implemented.
8. **Log every deviation in `BE_IMPLEMENTATION_LOG.md`**: what the design said, what the
   code does, why, and who agreed. Where nothing was agreed, mark it `unreviewed`.

## 5. Decision rules and evidence standard

- **The contract is the source of truth.** If the code needs a different status code or
  an extra field, the contract changes first and the change is recorded. Code that
  quietly differs is a bug in both places.
- **No new dependency without a reason in the log.** Every dependency is an operational
  and security liability; name the alternative considered.
- **Small commits with working tests.** Each commit leaves the suite green; a large
  commit that "will be split later" never is.
- **Never widen a timeout to make a test pass.** That hides the failure `BE-P06` is
  supposed to handle.
- **Log at the boundary with the correlation ID, never log the payload blindly.**
  Request bodies contain personal data and tokens.
- **Authorisation is checked in code, not assumed from the gateway,** unless
  `BE-ARCHITECTURE` names the gateway rule that enforces it — and then it is tested.

## 6. Verification

- Every operation in the contract has a handler and at least one request-level test.
- Every error code in the taxonomy is produced by at least one code path, and no path
  produces a code that is not in the taxonomy.
- Boundary validation rejects each documented invalid case with the documented status.
- Authorisation is tested per operation: allowed, forbidden, missing credential.
- The full suite passes; the new tests are not the only ones run.
- No TODO in the diff lacks a log entry and an owner.
- The log lists every deviation with its agreement status.

## 7. Failure handling

- **The contract is ambiguous at the point of implementation.** Stop, write the question
  in the log, and pick the interpretation that is easiest for a client to handle. Flag
  it `design question` so `BE-P02` records the decision; do not invent a private rule.
- **The design is wrong** (the transaction boundary cannot hold the invariant): stop
  implementing, record the counter-example with a failing test, and send it back to
  `BE-P03`. Shipping around a broken boundary is how the debt becomes permanent.
- **The project has no test infrastructure.** Add the minimum: one runner, one fake for
  the clock, one integration harness. Do not skip tests and record "tested manually".
- **A dependency is unavailable or unmaintained.** Record the risk, wrap the calls
  behind your own interface, and raise it in the log. Do not fork it silently.
- **Existing tests fail before your change.** Record which, prove they failed on the
  base commit, and either fix them in a separate commit or leave them with the proof.
  Never "fix" a failing assertion by deleting it.

## 8. Security and authorisation

Risk class B. No credentials in code or fixtures; read them from the environment. Every
new endpoint states its authorisation and tenant scope in code and in a test. Parameter
binding only — no string-built queries. Output is encoded for its context. If a secret
must exist for a test, it is a fake value, clearly labelled, and never a live one.

## 9. Completion criteria

- [ ] Handler and request-level test per operation.
- [ ] Every taxonomy code produced by a path; no undeclared code returned.
- [ ] Boundary validation tested against the documented invalid cases.
- [ ] Authorisation tested per operation, including missing credentials.
- [ ] Full suite green, not just the new tests.
- [ ] `BE_IMPLEMENTATION_LOG.md` lists every deviation with agreement status.

## 10. Deliverables and handover

The code, the tests, and `BE_IMPLEMENTATION_LOG.md`. `BE-P06` needs the log's list of
external calls, timeouts and known skips, plus any place the code can block. `BE-P07`
needs the test inventory and the deviations, because a deviation is a gap between the
specified behaviour and the tested behaviour and has to be verified explicitly.
