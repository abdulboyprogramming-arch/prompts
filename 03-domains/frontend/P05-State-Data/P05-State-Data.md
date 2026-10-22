# PROMPT 5 — State & Data: stale responses, double submits, and the cache that lies

**Identifier:** FE-P05
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — changes data fetching, caching and persistence; reversible through version control
**Depends on:** FE-P04
**Produces:** `FE_STATE_DATA.md`: the enforced state map, the cache and invalidation policy per query, the race and retry behaviour, and what is persisted where
**Inputs:** {{PROJECT_PATH}} (optional: API_SCHEMA, STATE_OWNERSHIP_MAP)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You make the data layer honest: one owner per query, an invalidation rule that survives
a mutation, and defined behaviour when two requests race or the network dies mid-write.

Nearly every "random" frontend bug lives here — a list that does not refresh after an
edit, a filter that shows the previous results for a second, a form that submits twice,
a page that renders another user's cached data after a logout.

## 2. Objective and scope

**Produce:** `FE_STATE_DATA.md` and the implementation behind it:

1. **Query inventory.** Each query: key, owner, source endpoint, staleness policy, and
   what invalidates it.
2. **Mutation map.** Each mutation: what it invalidates or updates, whether it is
   optimistic, and its rollback path on failure.
3. **Race rules.** Out-of-order responses, duplicate in-flight requests, request
   cancellation on navigation, and last-write-wins where it applies.
4. **Error and retry behaviour.** Which failures retry automatically, with backoff, and
   which surface to the user immediately.
5. **Persistence.** What is stored where (URL, memory, `sessionStorage`,
   `localStorage`, IndexedDB), for how long, and why it is safe.
6. **Session boundary.** What is cleared on logout and on user switch, and how.

Out of scope: component structure (`FE-P03`), the tests themselves (`FE-P06`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the implementation and `FE_IMPLEMENTATION_LOG.md` (`FE-P04`), whose
  deviations tell you where a component already holds server data locally. **Discovered
  here:** the installed query or data library (and its version), the existing keys, and
  any current `useEffect` fetches that the map replaces.
- `{{API_SCHEMA}}` (optional) — the contract or generated types. If absent, record which
  responses are untyped; those are the ones that will break silently.
- `{{STATE_OWNERSHIP_MAP}}` (optional) — from `FE_ARCHITECTURE.md`. If absent, stop: this
  stage enforces an ownership map, and inventing one here is how two owners appear.

## 4. Workflow

1. **Enumerate every query with a key that encodes its parameters.** A key that omits a
   filter parameter serves the cached results of a different filter — the single most
   common cache defect. Check each key against the parameters the request actually uses.
2. **Set the staleness policy per query from how the data changes**, not from a global
   default: reference data can be hours stale, a user's own list cannot, a price must
   not be.
3. **Map each mutation to its invalidations.** Name the query keys it invalidates or the
   cache entries it patches; "refetch everything" is acceptable for a small app and must
   be stated as the choice it is.
4. **Decide optimism per mutation using the matrix.** Optimistic only when the write is
   reversible in the UI and the rollback is visible. A failed optimistic delete that
   silently reappears an item later is worse than a spinner.
5. **Handle the races explicitly**:
   - cancel or ignore responses for a superseded request (navigation, new filter),
   - dedupe concurrent identical requests,
   - never let a slow response overwrite a newer one — carry a request sequence or
     compare timestamps.
6. **Write the retry rule.** Retry idempotent reads with exponential backoff and jitter,
   capped; do not auto-retry a mutation unless it carries an idempotency key from
   `BE-P02` or the API documents it as idempotent.
7. **Decide persistence and justify it.** URL for shareable view state, memory for the
   rest, `sessionStorage` for draft forms the user would hate to lose. Sensitive data
   never goes to `localStorage`; tokens belong in httpOnly cookies set by the server.
8. **Define the session boundary.** On logout and on user switch: clear the query cache,
   the persisted caches, and any in-memory user data. Test it by switching users in the
   same tab and confirming no stale content renders.
9. **Verify the map against the code** before handing over: every query has a key, an
   owner, a staleness policy and an invalidation; every mutation has a failure path.

## 5. Decision rules and evidence standard

- **A query key is a promise.** If two different requests produce the same key, one of
  them is serving the other's data.
- **The cache is not the source of truth; the server is.** Never keep a second copy in
  component state and keep both in sync.
- **Stale data is a product decision with a number.** "Some seconds stale" is not a
  policy; a staleness window and the reason are.
- **Every mutation needs a failure path that a user can perceive.** Silent failure is the
  defect that reaches production because nobody saw it.
- **Persistence is a security decision.** Any storage readable by another script on the
  page is readable by any XSS; record the reasoning, not just the medium.
- **Do not retry what is not idempotent.** A retried payment is a second payment.
- **Clear on logout, always.** Cross-user leakage from a cache is the most severe defect
  this stage can ship.

## 6. Verification

- Every query has a key containing all its parameters, an owner, a staleness policy and
  an invalidation rule.
- Every mutation names its invalidations and its failure behaviour.
- Race handling is implemented and demonstrated: superseded response ignored, duplicates
  deduped, slow response cannot overwrite newer data.
- Retry applies only to idempotent operations, with backoff and a cap.
- Storage choices are listed with their justification; no sensitive value in
  `localStorage`.
- Logout and user switch clear cache and in-memory data, demonstrated in a test.
- No component holds a local copy of server data that the map assigns elsewhere.

## 7. Failure handling

- **The project has no data library** (raw `fetch` in `useEffect` everywhere): record the
  current pattern, implement the smallest correct cache for this slice behind one hook,
  and log the migration as debt. Do not hand-roll a full cache in a feature branch.
- **The API has no idempotency support and the mutation is not safe to repeat**: disable
  automatic retry, dedupe in the UI, and record the residual risk — the user who
  double-clicks and loses connection can still create two records.
- **A response shape is untyped or unstable**: write the adapter and the runtime check at
  the boundary, record the field names that have already changed, and raise the contract
  question with the API owner.
- **The app caches across users today** (a shared cache key without a user segment):
  record it as a security finding, add the user to the key, and require a test for the
  switch case before handoff.
- **Caching conflicts with correctness** (a price or a balance): do not cache it, or
  revalidate on mount and on focus, and state the number the user could see stale for.
- **Offline is claimed but not implemented**: record it as unsupported, remove the claim
  from copy, and hand it to `FE-P07` as a scope decision rather than shipping a promise
  the app does not keep.

## 8. Security and authorisation

Risk class B. Tokens go in httpOnly, `Secure`, `SameSite` cookies; never in
`localStorage`, never in a URL. Clear every cache on logout and on user switch. Do not
cache responses that contain another tenant's data under a shared key. Treat any value
from storage as untrusted input and validate it before render. Record where personal data
is persisted client-side, for how long, and how it is removed.

## 9. Completion criteria

- [ ] Query inventory with keys, owners, staleness and invalidation.
- [ ] Mutation map with invalidations, optimism and rollback.
- [ ] Race rules implemented and demonstrated.
- [ ] Retry limited to idempotent operations, with backoff and cap.
- [ ] Persistence listed with justification and security reasoning.
- [ ] Session boundary cleared on logout and user switch, with a test.
- [ ] No duplicate copy of server data outside the cache.

## 10. Deliverables and handover

`FE_STATE_DATA.md` and the data layer. `FE-P06` needs the race and retry rules to test,
the session-boundary test to keep green, and the staleness windows to check against the
matrix. `FE-P07` needs the persistence decisions and any residual risk — a double submit
that remains possible is a known limitation, not a footnote.
