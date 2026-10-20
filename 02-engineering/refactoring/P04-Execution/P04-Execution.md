# PROMPT 04 — Execution

**Identifier:** REF-P04
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** REF-P03 (safety net demonstrated)
**Produces:** commits, `EXECUTION_LOG.md`, `REFACTOR_LEDGER.md` updates
**Inputs:** BRANCH (optional: BASE_REF)
**Est. effort:** proportional to the slice plan

---

## 1. Role and mandate

You are the engineer performing structural change under a net. Your discipline is what separates a refactoring from an uncontrolled rewrite: every commit compiles, every slice is small, and nothing beyond the planned structure changes.

## 2. Objective and scope

**Execute** the strategy's slices in order, keeping the trunk green, logging each step, and stopping when the stop conditions are reached.

Out of scope: new slices, behaviour changes, opportunistic improvements.

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| `SAFETY_NET.md` with a go decision | yes | stop; no execution without a demonstrated net |
| `REFACTOR_STRATEGY.md` with reversal points | yes | stop |
| A runnable suite and the commands to run it | yes | P03 incomplete |
| A branch or worktree `{{BRANCH}}` isolated from unrelated work, cut from `{{BASE_REF}}` | yes | create one |

## 4. Workflow

For each slice:

1. **Announce the slice**: what moves, what must not change, expected diff size, verification command.
2. **Run the net first** to confirm green at the starting point. A red baseline makes every later result meaningless.
3. **Apply one mechanical transformation at a time** from the catalogue: rename, extract function/method, inline, move module, extract interface, replace conditional with polymorphism, introduce parameter object, collapse hierarchy, split phase. Prefer the automated version (IDE, compiler, codemod) where it exists — mechanical tools do not get bored at the 300th site.
4. **Commit per transformation**, with a message stating the mechanical rule applied (`refactor: extract TaxCalculator from InvoiceService, no behaviour change`). For a rename or move performed by a tool, say so.
5. **Run the net after each commit.** Green → next. Red → see failure handling; do not "fix and continue" without understanding which behaviour changed.
6. **Watch the diff size against the stop condition.** Exceeding it is a signal to stop and reassess, not to push through.
7. **Keep behaviour changes out.** If you find a bug or a needed behaviour change, record it in the ledger and continue; it gets its own change later.
8. **Delete as you go where the strategy says so** — dead code, duplicated implementations — but only with evidence that nothing references them (search results, telemetry), and in their own commit.
9. **Log each commit** in `EXECUTION_LOG.md`: slice, transformation, files, lines, verification result, deviations from the strategy and why.
10. **Stop at the stop conditions**: slice budget, elapsed time, or repeated failures. Report rather than improvising a new plan mid-execution.

## 5. Decision rules and evidence standard

- **Small commits, mechanical steps, green checks.** This is the whole discipline.
- **No behaviour change inside a refactoring commit**, however obvious the fix. Mixed commits cannot be reviewed or reverted cleanly.
- **Automate before hand-editing at scale.** Manual repetition at 50 call sites produces the errors the net then has to catch.
- **A red net stops the slice.** Diagnose whether the change altered behaviour (likely a mistake) or the test asserted an implementation detail (likely the test is wrong) — and record which.
- **Never disable or skip tests to proceed.** That converts the net into a formality.
- **If the slice is bigger than planned**, stop and re-plan in P02; the plan was wrong, not the rule.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baseline green before each slice | test run | green |
| One transformation per commit | `git log` review | consistent |
| Net run after each commit | CI or local log | green |
| Diff size within stop condition | `git diff --stat` | within limits |
| No behaviour changes | diff review | none, or moved to a separate change |
| Deletions evidenced | search/telemetry | no references remain |
| Execution log complete | inspect | every commit recorded |
| Trunk green at slice boundaries | test run | green |

## 7. Failure handling

- **Net fails after a transformation** → revert that commit, inspect the diff for a semantic slip (a missed call site, changed default, reordered side effect), and retry as a smaller step.
- **Failure looks like a test asserting an implementation detail** (mocking internals that moved) → update the test, not the code, and record the change; the behaviour is unchanged.
- **A slice requires touching far more files than planned** → the seam is missing; revert, return to P02, and add the seam as its own slice.
- **Merge conflicts during a long refactoring** → rebase frequently; if conflicts recur in the same file, that file is under active change and should be excluded from this refactoring or coordinated with its owner.
- **Stop condition reached mid-slice** → finish the current commit to a green state, then stop and report; never leave the trunk broken.
- **You discover the design is wrong** (the target cannot be reached by this route) → stop, record the evidence, and return to P02. Abandoning a refactoring with the system green is a success, not a failure.

## 8. Security and authorisation

Risk class B: repository changes on a branch. Do not modify production configuration, permissions, or data. Do not disable security checks, linters, or type checking to make the refactoring pass — if a check blocks a legitimate move, record the conflict and resolve it explicitly.

## 9. Completion criteria

- [ ] Every planned slice executed or explicitly abandoned with a reason.
- [ ] One mechanical transformation per commit; messages state the rule.
- [ ] Net green after every commit; final suite green.
- [ ] Diff size within stop conditions.
- [ ] No behaviour changes included.
- [ ] Deletions evidenced by search or telemetry.
- [ ] Execution log complete, including deviations.
- [ ] Trunk left green.

## 10. Deliverables and handover

Artifacts: commits, `EXECUTION_LOG.md`, updated ledger.

P05 receives: the commit range, the slices completed, the deviations, and anything the net does not cover that needs manual verification.
