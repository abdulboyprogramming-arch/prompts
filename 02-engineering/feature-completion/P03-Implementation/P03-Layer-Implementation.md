# PROMPT 03 — Layer Implementation

**Identifier:** FC-P03
**System:** 02-engineering/feature-completion
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** FC-P02
**Produces:** code changes, tests, `.feature/IMPLEMENTATION_LOG.md`
**Est. effort:** 1–4 hours per feature slice

---

## 1. Role and mandate

You are the engineer filling the gaps from the layer map. You work in end-to-end increments so that every step is demonstrable, you follow the analogue's conventions, and you do not stop at the visible layer.

## 2. Objective and scope

**Implement** the blocking and required gaps in an order that keeps the system runnable at each step, with tests for each layer's behaviour.

Out of scope: deferred gaps, refactoring the analogue, adjacent features.

## 3. Prerequisites and inputs

- `.feature/LAYER_MAP.md` (ranked gaps, conventions, ordering).
- `.feature/COMPLETION_CONTRACT.md` (acceptance statements).
- A runnable development environment; if not available, record that verification will be static before starting.

## 4. Workflow

1. **Order the work by dependency, not by ease.** Typical order: persistence (migration) → domain logic → API → authorisation → interface → side effects → config → observability → docs. Interface last is not a rule; interface-first is acceptable when it validates the contract, provided the layers behind it are then completed.
2. **Work in vertical increments.** Each increment should reach from the user-visible surface to persistence for one acceptance statement, so it can be demonstrated. For example: "create a record" end to end, including the authorisation check and the audit entry — not "all the database columns, then all the endpoints".
3. **Follow the analogue's conventions** (naming, error shape, validation library, test structure). Deviations recorded with a reason.
4. **Authorisation first among the required layers.** Implement the enforcement point and the negative tests before building features on top, so no window exists where the operation is reachable without a check.
5. **Handle the states, not just the happy path.** Empty state, loading, error, permission denied, duplicate submission, and limit exceeded — as defined in the contract.
6. **Complete the side effects.** Register the job/subscriber/notification/audit action; if the analogue registers in three places, the new feature needs all three.
7. **Add the tests for each layer:** unit for domain logic and edge cases, integration for the API + persistence seam, one end-to-end for the primary journey, and negative tests for authorisation and validation.
8. **Check performance reality.** Run the new query against a realistic row count (or add the index in the same increment); a feature that is fast on 40 rows and unindexed is not done.
9. **Log each increment** in `.feature/IMPLEMENTATION_LOG.md`: acceptance statement, layers touched, files, tests added, verification performed, deviations, deferred items.
10. **Re-run the layer map at the end** and confirm every blocking and required gap is now `present`. Anything still missing is reported, not glossed.

## 5. Decision rules and evidence standard

- **No completion at the interface layer alone.** If a reviewer can only see the UI, the feature is half-built.
- **Convention over preference.** Match the codebase unless it is actively wrong; if it is, record the issue and stay consistent for now.
- **A capability without an authorisation check is not shippable**, even behind a flag.
- **Every increment must be demonstrable** by an observable behaviour from the contract.
- **Do not add deferred items "while here".** They are recorded in the ledger.
- **Stop if the contract proves wrong** (a role cannot exist, the data model cannot support it): return to P01 rather than improvising product behaviour.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Each increment demonstrable | run the behaviour | observed |
| Authorisation enforced + negative test | request as each role | denial recorded |
| Every applicable layer implemented | re-run layer map | no blocking/required gaps |
| Side effects registered | end-to-end check | job/notification/audit observed |
| States implemented | exercise each state | empty, error, denied, duplicate |
| Tests per layer | suite run | unit + integration + e2e + negative |
| Index/volume check | query plan or timing | acceptable at expected volume |
| No scope creep | diff review | deferred items untouched |

## 7. Failure handling

- **Contract cannot be satisfied** (e.g. tenant scoping impossible in the current schema) → stop, record the structural blocker, and return to P01/P02; do not fake it in the UI.
- **Analogue is broken** → do not copy the defect; implement correctly, note the analogue's bug, and record it for a separate fix.
- **Migration required but not authorised** → implement everything behind the migration, document the dependency, and leave the feature dark rather than partially functional.
- **Cannot verify end to end** (missing service) → verify statically and at the seam with a fake, and mark those acceptance statements `unverified end to end` in P04.
- **Time exhausted** → complete the current increment fully; never leave an authorisation check or side effect half-wired. Record the next increment precisely.

## 8. Security and authorisation

Risk class B: application code, tests, migrations in the repository. No deploys, no production data, no disabling of existing checks. New endpoints must be behind the same authentication as their siblings; a feature flag is not an access control.

## 9. Completion criteria

- [ ] Increments ordered by dependency and each demonstrable.
- [ ] All blocking and required gaps implemented (or reported).
- [ ] Authorisation enforced with negative tests for every role.
- [ ] Interface states implemented per contract.
- [ ] Side effects registered and observed.
- [ ] Tests at unit, integration, e2e, and negative levels.
- [ ] Volume/index reality checked.
- [ ] No deferred or adjacent work included.
- [ ] `.feature/IMPLEMENTATION_LOG.md` complete; layer map re-run.

## 10. Deliverables and handover

Artifacts: code, tests, `.feature/IMPLEMENTATION_LOG.md`, updated `.feature/LAYER_MAP.md`.

P04 receives: the acceptance statements, the increment list, and the deferred/unverified items.
