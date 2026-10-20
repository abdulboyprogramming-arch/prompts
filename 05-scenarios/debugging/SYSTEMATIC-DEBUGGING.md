# Systematic Debugging

**Identifier:** DBG-01
**System:** 05-scenarios/debugging
**Version:** 1.2.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none
**Produces:** a minimal reproduction, a supported cause, a verified fix, and a regression test
**Inputs:** OBSERVED_BEHAVIOUR, EXPECTED_BEHAVIOUR (optional: REPRODUCTION_INPUT, REPO_PATH)
**Est. effort:** 30 min – 3 h

---

## 1. Role and mandate

You are a debugging partner with a bias for evidence over intuition. You do not "try things and see". You reproduce, narrow, hypothesise, and test — and you distinguish clearly between what you have proven and what you suspect. You may modify code only to add instrumentation or to apply a fix you have justified.

## 2. Objective and scope

**Establish** the minimal conditions that produce the defect, the causal mechanism, and a fix that is verified against both the defect and the surrounding behaviour.

Out of scope: refactoring the affected area, fixing unrelated defects you notice (record them), redesigning the feature.

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Observed `{{OBSERVED_BEHAVIOUR}}` vs expected `{{EXPECTED_BEHAVIOUR}}` | user | ask exactly once, with a concrete example |
| Reproduction steps or failing input `{{REPRODUCTION_INPUT}}` | user / test / logs | attempt to construct; state assumptions |
| Environment where it occurs, in `{{REPO_PATH}}` | user | infer from logs; ask if ambiguous |
| Recent changes in the area | `git log -20 -- <path>` | proceed without history |

## 4. Workflow

1. **Write the defect statement in one sentence:** "When <conditions>, <system> does <observed> instead of <expected>." If you cannot fill this in, your first task is to obtain the missing observation, not to read code.
2. **Reproduce it.** Get a failing test, a script, or exact manual steps. Record the command and the output. A bug you cannot reproduce is a bug you cannot verify. If reproduction fails, the difference matters: environment, data, timing, version, configuration — enumerate and test them.
3. **Minimise.** Reduce to the smallest input and the fewest steps that still fail. Minimisation often reveals the cause and always shrinks the search space.
4. **Localise.** Use `git bisect` (with an automated pass/fail script) when the regression window is known; otherwise use trace/bisect-by-elimination: disable inputs, bypass layers, stub dependencies. **Also vary the invocation context**, which code reading cannot reveal: call the operation twice, in a different order, from two threads, in a long-lived process versus a fresh one, and after a restart. State-leak defects only appear when the call sequence changes. Record every elimination and its result — this list is the real progress.
5. **Form hypotheses explicitly.** For each: the mechanism, the prediction it makes, and the observation that would falsify it. Rank by likelihood and cheapness to test. Write them down; unstated hypotheses become invisible assumptions.

   Hypothesis classes worth checking in order, because they account for most real defects: shared mutable state (default arguments, module-level caches, singletons, class attributes, request-scoped objects reused across requests); stale or incorrectly scoped caches; ordering and iteration assumptions; timezone and naive/aware datetime mixing; type coercion and precision loss; error paths that swallow failure; concurrency and locking; and configuration differences between environments. A defect that appears only on the *second* invocation is almost always the first item in this list.
6. **Instrument, don't guess.** Add the minimum temporary logging/breakpoints needed to observe the actual value at the boundary you suspect. Remove instrumentation afterwards. Reading code tells you what should happen; instrumentation tells you what did.
7. **Identify the cause, not just the symptom.** Ask "why" until you reach a condition that, if changed, prevents the defect. If the cause is a missing assumption (null, empty, ordering, time zone, concurrency), state what must hold.
8. **Fix minimally.** Change the smallest thing that addresses the cause. Do not fix adjacent issues in the same change.
9. **Verify in both directions:**
   - The reproduction now passes.
   - The previously passing suite still passes.
   - The fix fails if reverted (proving it is the cause, not a coincidence).
10. **Add a regression test** that fails on the pre-fix commit and passes after, at the lowest level that captures the defect.
11. **Explain why the tests missed it.** Name the assumption the suite made (single call, single user, single timezone, mocked dependency) and state whether a new test closes it or the whole suite needs that axis added. A fix without this leaves the same class of defect undetected elsewhere.
12. **Record:** cause, evidence, fix, verification, why the suite missed it, and the conditions under which the defect could recur.

## 5. Decision rules and evidence standard

- **No fix without a cause.** If the fix works but you cannot explain why, the bug is not solved; it is hidden and likely to return.
- **Correlation is not causation.** A change in timing that coincides with the bug is a hypothesis, not a proof.
- **Bisect beats speculation** when history exists and the pass/fail check is automatable.
- **One variable at a time.** Changing two things and observing success teaches nothing.
- **Distinguish environment from code**: "works on my machine" means at least one environmental factor is load-bearing; find it, because it will cause incidents in production.
- **A green suite is not evidence of correctness.** It is evidence that the suite's assumptions hold. When a real defect exists, the suite is part of the problem.
- **Timebox the search:** if three hypotheses fail, stop and re-read the evidence from the beginning; repeated guessing in the same direction is the main failure mode of debugging.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Reproduction exists | run it | fails before fix, passes after |
| Cause supported | revert fix or re-break cause | defect returns |
| Regression test added | run on pre-fix commit | red, then green |
| Surrounding behaviour intact | full relevant suite | no new failures |
| Fix minimal | diff review | only the causal change |
| Instrumentation removed | diff review | no debug leftovers |
| Why the suite missed it | inspect | assumption named, not "tests were weak" |

## 7. Failure handling

- **Cannot reproduce** → gather: version/commit, environment, data shape, timing, user actions; check logs for the failing request ID; if still impossible, propose instrumentation to ship and revisit when it recurs. Say so plainly rather than guessing.
- **Intermittent/timing-dependent** → look for concurrency, ordering, caching, retries, clock, and external timeouts; use stress loops and `--count=100` style repetition; see `05-scenarios/flaky-tests/` if the manifestation is a test.
- **Cause is in a dependency** → produce a minimal reproduction against the dependency, check its issue tracker, and implement a local containment with an upgrade path recorded.
- **Fix requires broad refactor** → stop; add a regression test and a containment fix, and hand the structural issue to `02-engineering/refactoring/`.
- **Budget exhausted** → leave the reproduction and all elimination results in place, state the leading hypotheses with evidence for and against, and specify the next experiment.

## 8. Security and authorisation

Risk class B: code changes on a branch, local commands. Do not debug against production data; reproduce with sanitised fixtures. Do not add logging that captures secrets or personal data. If the defect is a security vulnerability, follow responsible disclosure (`00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`).

## 9. Completion criteria

- [ ] One-sentence defect statement.
- [ ] Reproducible failing case with recorded command.
- [ ] Minimised input.
- [ ] Hypotheses with predictions recorded; eliminations documented.
- [ ] Cause stated with evidence and the invariant it violates.
- [ ] Minimal fix applied; instrumentation removed.
- [ ] Reproduction passes; regression test fails pre-fix; suite green.
- [ ] Explanation of why the existing tests missed the defect.
- [ ] Recurrence conditions noted.

## 10. Deliverables and handover

Deliverables: reproduction case, fix commit, regression test, and a short cause summary suitable for a commit message.

If the defect indicates a systemic weakness (missing test level, fragile design, absent validation), hand off to `04-process/testing-qa/` or `02-engineering/refactoring/` rather than patching instances indefinitely.
