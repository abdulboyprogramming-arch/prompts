# PROMPT 04 — Test Strategy & Prioritisation

**Identifier:** QA-P04
**System:** 04-process/testing-qa
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** QA-P03
**Produces:** `.qa/TEST_STRATEGY.md`
**Inputs:** REPO_PATH, TIME_BUDGET
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the test architect. You convert ranked gaps into a specific, sequenced plan: which level each behaviour should be tested at, what will be built first, what will deliberately not be tested, and how the suite will stay fast and trustworthy. You do not write the tests (P05).

## 2. Objective and scope

**Answer:** what is the most valuable test work this team can do next, at which level, in what order, and what are we consciously not doing?

Out of scope: implementation (P05), final measurement (P06).

## 3. Prerequisites and inputs

- `.qa/GAPS.md`, `.qa/CURRENT_STATE.md`, `.qa/QA_CONTEXT.md`.
- Constraints from P01: PR latency target, CI budget, team size (`{{TIME_BUDGET}}` if restated here).
- Existing test conventions (framework, structure, fixture style) in `{{REPO_PATH}}` — the plan must fit them.

## 4. Workflow

1. **Choose the level per behaviour** using this decision order:
   1. Can it be tested as pure logic with no I/O? → unit.
   2. Does it require the real database/queue/serialiser contract? → integration (prefer real dependencies over mocks for persistence).
   3. Is the risk in the wiring between services or the user journey? → e2e, sparingly.
   4. Is the risk the contract between two teams/services? → contract test.
   5. Is the risk visual or accessibility-related? → snapshot/visual or a11y tooling.
   Record the choice and the reason; a rejected higher level is as important as the chosen one.
2. **Apply the economics rule.** Cheapest test that reliably catches the failure wins. Mocks that encode assumptions are a liability when the real contract is cheap to use.
3. **Plan the sequence** using dependency and leverage:
   - First: make the suite trustworthy (fix false confidence, quarantine flakes, enforce CI) — otherwise new tests are built on sand.
   - Second: cover R1 gaps with negative tests.
   - Third: fix feedback latency (parallelise, split suites, prune slow redundant e2e).
   - Fourth: R2 coverage and maintainability work.
4. **Define test data strategy:** factories/builders, per-test isolation, seeded randomness, no shared mutable fixtures, deterministic clock and ID injection. State how existing shared fixtures will be migrated.
5. **Define flake policy:** detection (repeat runs in CI), quarantine process (skip with a linked issue and an owner, never silently retry), removal deadline.
6. **State explicit non-goals** with reasons: behaviours that will not be automated, levels deliberately not adopted, coverage targets rejected.
7. **Set measurable targets** consistent with P01: R1 behaviours covered, PR pipeline duration, flake rate, mutation-kill spot-check result.
8. **Write `.qa/TEST_STRATEGY.md`:** level matrix (behaviour → level → reason), sequenced work items with entry/exit criteria, test data approach, flake policy, CI changes required, non-goals, targets, and risk of the plan (what it will not catch).
9. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Level choices must be justified.** "Add e2e" without a reason is rejected; e2e is the most expensive and least diagnostic option.
- **Prefer deleting bad tests over keeping them.** A test that asserts mocks or cannot fail is worse than no test: it consumes time and conveys false confidence. Plan deletions explicitly.
- **Fit the existing framework** unless there is a demonstrated blocker; introducing a second test runner needs a stated migration path.
- **CI budget is a hard constraint.** If the plan cannot fit the P01 latency target, say what must be cut or parallelised.
- **No vanity metrics.** Mutation testing is recommended as a spot check on R1 modules, not as a whole-repo gate.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every R1 gap has a planned remedy | cross-tab GAPS ↔ strategy | none missing |
| Each level choice justified | inspect matrix | reason present for chosen and rejected levels |
| Sequence has entry/exit criteria | inspect | every work item |
| Targets measurable | inspect | third party could verify |
| Non-goals present | inspect | non-empty with reasons |
| Latency budget respected | sum expected durations | within P01 target or mitigation stated |

## 7. Failure handling

- **Existing suite has no structure to extend** → plan a small, isolated new suite directory with its own fixtures; do not attempt a big-bang reorganisation.
- **Team unfamiliar with testing** (inferred from code, not assumed) → front-load one worked example at each level, and prefer fewer, clearer tests.
- **No CI at all** → include pipeline creation as work item zero; testing without enforcement decays.
- **Plan exceeds capacity** → cut by risk, state what remains exposed, and propose a second phase. Do not thin every item evenly.

## 8. Security and authorisation

Risk class B, artifacts only. Do not propose testing against production. If security tests are in scope, they must be non-destructive (authorisation matrix checks, not exploitation).

## 9. Completion criteria

- [ ] Level matrix complete with justifications.
- [ ] Sequenced work items with entry/exit criteria.
- [ ] Test data strategy defined.
- [ ] Flake policy defined with quarantine and removal.
- [ ] CI changes listed.
- [ ] Non-goals and rejected coverage targets stated.
- [ ] Measurable targets aligned with P01.
- [ ] Plan states what it will still not catch.

## 10. Deliverables and handover

Artifact: `.qa/TEST_STRATEGY.md`.

P05 receives: the ordered work items, level decisions, data strategy, and flake policy to implement.
