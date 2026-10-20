# PROMPT 02 — Change Understanding

**Identifier:** CR-P02
**System:** 04-process/code-review
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** CR-P01
**Produces:** `CHANGE_SUMMARY.md`
**Inputs:** BASE_REF, HEAD_REF
**Est. effort:** 20–45 min

---

## 1. Role and mandate

You are the reviewer building an accurate mental model of the change before judging it. Reviewers who start at the first hunk and move downward miss the things that matter: a removed authorisation check thirty files in, a behaviour change hidden inside a rename, a test that was weakened to pass.

## 2. Objective and scope

**Answer:** what does this diff actually do — mechanically, semantically, and behaviourally — including the parts the description does not mention?

Out of scope: issuing findings (P03), writing feedback (P04).

## 3. Prerequisites and inputs

- `REVIEW_CONTEXT.md` (ref range, intent, risk surface, hypotheses).
- The repository at `{{HEAD_REF}}`, and `{{BASE_REF}}` for comparison.
- Test suite and build commands for the touched area.

## 4. Workflow

1. **Read the diff in three passes, deliberately:**
   - **Structure pass** — `git diff --stat` and `--name-status`: what was added, modified, deleted, renamed. Deletions and renames first: they carry the most risk and get the least attention.
   - **Semantic pass** — read the diff grouped by concern (by module, not by file order): what behaviour changes in each.
   - **Detail pass** — line-level reading only of the areas the risk surface named.
2. **Reconcile the diff against the stated intent.** List anything in the diff not explained by the intent (scope creep, drive-by fixes, unrelated formatting) and anything the intent requires that is absent.
3. **Audit deletions and weakening specifically** — the highest-yield review activity:
   - tests deleted, skipped, or with assertions loosened;
   - caught exceptions broadened, error handling silenced, validation removed;
   - feature flags turned off, retries added to mask flakiness;
   - permission checks moved, duplicated inconsistently, or dropped on one path;
   - dependencies removed (does anything still import them?).
4. **Check the seams, not only the lines**: does the changed function still satisfy its callers? Were all call sites updated (search for the old symbol)? Do the types, schemas, migrations, and config keys match across the change?
5. **Trace one real path end to end** through the change — the primary journey for a feature, the failing input for a bug fix. Reading code in isolation misses wiring errors that a single traced path exposes.
6. **Identify what is untested**: which new branches, error paths, or edge cases have no test. Record as hypotheses, not findings.
7. **Note the parts you cannot evaluate** — domain logic you do not know, performance implications, security properties requiring threat modelling. State them; a reviewer who claims universal competence is not credible.
8. **Write `CHANGE_SUMMARY.md`:** structural summary, semantic summary per module, intent reconciliation (extra and missing), deletion audit, seam checks, traced path result, untested areas, and expert questions.

## 5. Decision rules and evidence standard

- **Deletions before additions.** Removed code is where regressions hide.
- **Never review only the added lines.** A diff is a change to a system, and context lines are where the contradiction usually is.
- **Every claim about behaviour must be traceable to a line**, or marked as an inference.
- **A traced path beats reading every file.** Choose the most representative path from the risk surface.
- **Do not raise findings yet.** This stage separates understanding from judgement so the findings that follow are grounded.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| All three passes performed | notes | structure, semantic, detail |
| Deletions/renames reviewed first | inspect | listed and explained |
| Intent reconciliation | diff vs description | extra and missing both listed |
| Deletion/weakening audit | `git diff --diff-filter=D`, grep | results recorded |
| Call sites checked | symbol search | all updated or listed |
| One path traced | execution or reading | result recorded |
| Untested areas listed | inspect | specific |
| Unknowns declared | inspect | expert questions listed |

## 7. Failure handling

- **Diff too large to read** → group by module, read the risk surface fully, sample the rest, and record the sampling; recommend splitting on the PR.
- **Code cannot be understood without running it** → run it in a scratch environment; if not possible, record the limitation and review structurally.
- **Renames dominate the diff** → use `git diff -M --stat` to detect renames and review the *content* change separately from the move.
- **The change depends on another unmerged branch** → record the dependency; reviewing a diff whose dependency is invisible produces false findings.
- **Behaviour differs from what the tests assert** → that is a finding for P03, not something to resolve here; note the discrepancy precisely.

## 8. Security and authorisation

Risk class A: read-only. Do not check out and run untrusted PR code on a machine with credentials; use a container or a clean environment. Do not paste secret values from the diff into the summary.

## 9. Completion criteria

- [ ] Structural summary with deletions and renames first.
- [ ] Semantic summary grouped by module.
- [ ] Intent reconciliation complete (extra and missing).
- [ ] Deletion and weakening audit performed.
- [ ] Seams and call sites checked.
- [ ] One path traced with result recorded.
- [ ] Untested areas and unknowns listed.

## 10. Deliverables and handover

Artifact: `CHANGE_SUMMARY.md`.

P03 receives: the modules, the risk areas, the discrepancies, and the untested paths — the raw material for findings that are specific and evidenced.
