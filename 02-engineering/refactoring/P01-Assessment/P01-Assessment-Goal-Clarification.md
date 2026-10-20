# PROMPT 01 — Assessment & Goal Clarification

**Identifier:** REF-P01
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `REFACTOR_GOAL.md`, `REFACTOR_LEDGER.md`
**Inputs:** PERCEIVED_PROBLEM, TARGET_AREA (optional: DEADLINE)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer deciding whether a refactoring should happen at all. Most refactoring work is started because code "feels bad", proceeds without a measurable goal, and ends with no way to say whether it helped. Your job is to replace that with a testable objective, or with a decision not to proceed.

You do not design the change (P02) and you do not modify code.

## 2. Objective and scope

**Answer:** what pain does this area cause today, what measurable outcome would justify the work, which parts must change, and what would make us stop?

Out of scope: the refactoring plan, the tests, the code.

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| The perceived problem `{{PERCEIVED_PROBLEM}}` ("this module is a mess") | user | ask what it blocks: a feature, a bug rate, an onboarding time |
| The area's location and rough size: `{{TARGET_AREA}}` | repository | locate by the symptom (files changed together, the code behind the slow endpoint) |
| History: churn, defects, incidents in the area | git log, issue tracker | state that history is unavailable; the goal becomes weaker and must say so |
| Any deadline or forcing event `{{DEADLINE}}` (feature, migration, audit) | user | ask; it determines whether a big refactor is even available |

## 4. Workflow

1. **Restate the complaint as an observation.** "The billing module is a mess" becomes "every change to invoice rounding touches six files and has caused three production defects in two quarters". If no observation exists, the refactoring has no evidence base — say so.
2. **Measure the pain with what is available.** Commit churn in the area (`git log --since=... --name-only`), defect and incident counts attributable to it, time-to-change for recent features, test coverage of the area (not the repo), and the number of callers/dependents. Record the commands used.
3. **Name the outcome as a measurable target**, for example: "adding a payment provider no longer edits the core module", "the area's test coverage rises from 22% to 70% so changes are safe", "duplicate implementations of the tax rule drop from 4 to 1", "p95 latency of the endpoint falls below 300 ms". A target that cannot be evaluated afterwards is not a target.
4. **Classify the work honestly:**
   - **Refactoring** — behaviour-preserving restructure; the goal is a structural property.
   - **Rewrite / migration** — replace the implementation; behaviour may change; route to `02-engineering/rewriting-migration/`.
   - **Repair** — the area is broken, not ugly; route to `05-scenarios/debugging/`.
   - **Optimisation** — the goal is a performance number; that is `02-engineering/performance/` (refactoring may be the method, but the goal and verification differ).
   - **Feature disguised as refactoring** — new behaviour is wanted. Separate the two: behaviour changes have their own review and verification.
5. **Delineate the boundary.** List the files/modules in scope and — explicitly — the ones adjacent that are out of scope. Scope creep into adjacent modules is how refactorings double in size and never land.
6. **Check the forcing function.** Is there a deadline that makes a long-lived branch impossible? Does the next feature require this area to be extensible? Timing determines strategy in P02.
7. **State the stop conditions before starting:** the maximum acceptable diff size, the maximum elapsed time, the regression tolerance, and what evidence would show the approach is wrong. Precommitting to these is what prevents a refactoring from becoming an open-ended project.
8. **Write `REFACTOR_GOAL.md`:** observation, measurements with commands, target outcome and how it will be measured, classification, in-scope and out-of-scope lists, forcing function, stop conditions, and risks.
9. **Initialise `REFACTOR_LEDGER.md`** (decisions, increments, verification results).

## 5. Decision rules and evidence standard

- **No measurable target, no refactoring.** "Cleaner" is not a target; "one place to change a tax rate instead of four" is.
- **Behaviour change is not refactoring.** If the change alters what the system does, it is a feature or fix and must be verified as one.
- **Prefer the smallest area that delivers the target.** Whole-repo reformatting is usually a way to avoid deciding what matters.
- **Do not accept "we'll add tests later"** as an input; the absence of a safety net is a finding that shapes P03, not a footnote.
- **A refactoring with no forcing function and no owner will stall**; record the owner and the deadline, or recommend deferring.
- **Do not estimate effort here.** Effort estimates belong to P02, where the slices are known.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Complaint restated as an observation | inspect | concrete, attributable |
| Measurements recorded with commands | inspect | at least two independent signals |
| Target is evaluable | read as a sceptic | has a before/after measure |
| Classification justified | inspect | refactor vs rewrite vs repair vs feature |
| Scope boundary explicit | inspect | in and out lists |
| Stop conditions recorded | inspect | diff size, time, regression tolerance |
| Owner and forcing function identified | inspect | named, or deferral recommended |
| No code changed | `git status` | clean |

## 7. Failure handling

- **The complaint cannot be substantiated** → recommend not proceeding; record what evidence would justify revisiting (e.g. defect count rising, feature blocked).
- **The area is untested and unbounded** (no clear seams, no tests) → this is a high-risk refactoring; say so, and make P03's safety net the dominant cost in P02's strategy.
- **The real problem is a design flaw** (the module is messy because the boundaries are wrong) → route to `02-engineering/architecture-review/`; a mechanical refactor will reorganise the mess without fixing it.
- **Deadline makes incremental work impossible** → the honest options are a scoped rewrite with a cutover plan or deferral; both belong in P02, and the risk must be recorded now.
- **Multiple goals compete** (speed and testability, say) → pick one primary target and record the secondary as a constraint, because two optimisation targets usually conflict.

## 8. Security and authorisation

Risk class A: read-only. Do not modify code, tests, or configuration. Do not read production data to characterise behaviour. If the area handles secrets or personal data, record its sensitivity now — it constrains how the refactoring can be tested in P03 (fixtures, redaction).

## 9. Completion criteria

- [ ] Complaint expressed as an observation with evidence.
- [ ] At least two measurements recorded with the commands used.
- [ ] Measurable target with a stated evaluation method.
- [ ] Work classified (refactor / rewrite / repair / optimisation / feature).
- [ ] In-scope and out-of-scope lists.
- [ ] Forcing function, deadline, and owner identified.
- [ ] Stop conditions recorded.
- [ ] Risks and sensitivity noted.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `REFACTOR_GOAL.md`.

P02 receives: the target, the boundary, the evidence base, the stop conditions, and whether a safety net exists — the last of which dominates strategy selection.
