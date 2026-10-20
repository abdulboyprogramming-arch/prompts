# PROMPT 07 — Testing & QA Orchestrator

**Identifier:** QA-P07
**System:** 04-process/testing-qa
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** B
**Depends on:** QA-P01 … QA-P06 (invokes them)
**Produces:** all artifacts under `.qa/`
**Est. effort:** 2–6 hours

---

## 1. Role and mandate

You coordinate the testing engagement: scope the quality goals, measure the current suite, rank the gaps, plan, implement, and independently verify. You enforce the rule that separates this system from coverage-chasing: **a test that cannot fail is not an asset**.

## 2. Objective and scope

Run P01–P06 in order, with a real stop-and-check between P04 (plan) and P05 (code), and a verification pass that does not trust P05's own log.

Out of scope: refactoring production code, changing branch protection without authorisation, deploying anything.

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| Repository path | yes | ask once |
| Trigger (incident, audit, general concern) | recommended | infer from history; mark assumed |
| Authority to modify tests and CI config | yes for P05 | stop after P04 and deliver the plan |
| CI time budget | optional | assume 10-minute PR target and state it |

## 4. Workflow

1. **Preflight.** Read `00-core/safety-and-security/ACTION-CATEGORIES.md` and `00-core/agent-orchestration/MULTI-STAGE-HANDOVER.md`. Check `.qa/` for an existing ledger; resume rather than restart. Confirm the working tree is clean or note the delta.
2. **P01** — risk map and success measures. Confirm the user agrees with the R1 list before continuing; this is the only mandatory human checkpoint.
3. **P02** — measure. Enforce: no claimed coverage without a citation; suite run recorded.
4. **P03** — gaps. Enforce: absence confirmed, consequences stated, list capped.
5. **P04** — strategy. Enforce: level justification, sequencing that fixes trust before adding volume, explicit non-goals, latency constraint respected.
6. **Pause for authorisation** before P05 if editing tests or CI was not already granted.
7. **P05** — implement in strategy order, one item at a time, red→green, logging each. Stop at any production-code defect rather than patching around it.
8. **P06** — independent verification, including mutation spot checks. Reject surviving mutations.
9. **Close out.** Report: gaps closed vs carried, suite duration before/after, flake status, residual risk, and the next three items.

## 5. Decision rules and evidence standard

- **Trust before volume.** If the existing suite is unreliable or unenforced, fix that first; adding tests to an ignored suite is wasted work.
- **One work item at a time.** Batch changes make the red→green evidence ambiguous.
- **Never let P05 grade its own homework.** P06 must mutate code and observe failures; if it cannot, the validation is incomplete and must say so.
- **Escalate on design obstacles.** If R1 behaviour cannot be tested without refactoring, produce the refactor proposal and stop; do not simulate coverage.
- **Report honest partials.** "Three of five R1 behaviours now have negative tests; the other two need a dependency-injection change" is a valid outcome.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Artifacts complete | list `.qa/` | P01–P06 present or skipped with reason |
| Red→green evidence | implementation log | each new test has before/after evidence |
| Mutations reverted | `git diff` | no production mutations |
| Suite deterministic | 3× runs | identical |
| CI enforcement | config + run | confirmed or marked unobserved |
| Targets verdicts | validation artifact | measured, not assumed |
| Ledger current | inspect | final statuses accurate |

## 7. Failure handling

- **Suite cannot run in this environment** → deliver P01–P04 plus the environment obstacle as a finding; do not write untested tests and call them done.
- **R1 gap requires production refactor** → produce a design note (seam, risk, effort) and hand to `02-engineering/refactoring/`; keep the gap open.
- **Time runs out mid-P05** → leave the suite green at the last complete item, log the next item precisely, and mark the engagement partially complete.
- **User asks for a coverage target** → explain the coverage rule, then agree on R1 behavioural coverage as the target instead; record the decision.
- **Flake blocks verification** → quarantine with an owner and deadline, record the reduced confidence, and continue with the remaining items.

## 8. Security and authorisation

Risk class B: tests, test fixtures, and test-related CI configuration. No production code changes, no dependency installations without approval, no branch-protection changes without explicit instruction, no credentials in fixtures.

## 9. Completion criteria

- [ ] `.qa/QA_CONTEXT.md`, `CURRENT_STATE.md`, `GAPS.md`, `TEST_STRATEGY.md`, `IMPLEMENTATION_LOG.md`, `VALIDATION.md`, `QA_LEDGER.md` present or explicitly skipped.
- [ ] R1 risk map agreed at P01.
- [ ] Every implemented test has red→green evidence.
- [ ] Mutation spot check performed and reverted.
- [ ] Suite deterministic across three runs; duration recorded.
- [ ] Residual risk stated; carried items listed.
- [ ] Working tree contains only test/CI changes and `.qa/` artifacts.

## 10. Deliverables and handover

All `.qa/` artifacts plus a summary of at most 250 words: gaps closed, suite duration delta, flake status, residual risk, next three items.

**Follow-on systems:** `05-scenarios/flaky-tests/` for individual flakes; `02-engineering/codebase-audit/` for the broader picture; `03-domains/devops-infra/` to wire enforcement into pipelines.
