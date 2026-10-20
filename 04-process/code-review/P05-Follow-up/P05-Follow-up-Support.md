# PROMPT 05 — Follow-up Support

**Identifier:** CR-P05
**System:** 04-process/code-review
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** A
**Depends on:** CR-P04
**Produces:** `FOLLOW_UP.md`
**Inputs:** PR_REF (optional: AUTHOR_RESPONSES)
**Est. effort:** 10–30 min

---

## 1. Role and mandate

You close the review loop. Most review value leaks here: findings are discussed, some are fixed, one is "noted for later" and never seen again, and the reviewer never checks whether the fix is correct or whether the fix broke something else.

## 2. Objective and scope

**Produce:** a resolution for every finding, a re-verification of the fixes, and a tracked disposition for anything deferred.

Out of scope: reopening the whole review (return to P03), being the author's project manager.

## 3. Prerequisites and inputs

- `REVIEW_FINDINGS.md`, `REVIEW_FEEDBACK.md`, and the author's responses in `{{AUTHOR_RESPONSES}}`.
- The updated PR `{{PR_REF}}` at its new head.
- The ability to run the tests (re-verification).

## 4. Workflow

1. **Track findings by state**, one row each: open, fixed, disputed, deferred, withdrawn. Every finding ends in exactly one state — "unaddressed" is not a state, it is an omission.
2. **Re-verify each fix rather than accepting the claim.** Read the new diff for that area, run the reproduction, confirm the test fails without the fix where practical. "Fixed" in a comment is a claim.
3. **Check for fix-induced regressions** — the most common follow-up failure: a fix that adds a guard breaks a legitimate path, or a test added to satisfy a review asserts the wrong thing.
4. **Resolve disputes with evidence, not seniority**: restate the consequence, ask for the counter-example, and if the author is right, say so plainly and withdraw the finding.
5. **Convert deferrals into tracked items**: each deferred finding gets an owner, a ticket reference, and a reason it is safe to defer. A deferred blocker blocks; a deferred nit does not.
6. **Update the review summary** with the final state and the merge decision, and note the review's own outcome: was the change materially improved by the review? A review that changed nothing may indicate the change was fine — or that the review was shallow.
7. **Write `FOLLOW_UP.md`:** findings table with final state and evidence, re-verification results, regressions found, deferred items with owners, disputes and resolutions, and the final decision.

## 5. Decision rules and evidence standard

- **A fix is verified, not accepted.** Re-run the reproduction.
- **Every finding has a final state.** Silence is how findings disappear.
- **Deferred ≠ dismissed**: it requires an owner, a ticket, and a reason.
- **A fix that causes a regression reopens the finding** and is treated as a new finding with its own severity.
- **Withdraw your finding when the author is right**, explicitly. Reviewers who never concede lose the ability to be believed.
- **Do not re-review the whole PR** at this stage; scope to the delta and the affected areas.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every finding has a state | table | no blanks |
| Fixes re-verified | reproduction re-run | evidence per fix |
| Regression check | tests + affected paths | no new failures |
| Deferrals have owner and ticket | inspect | all present |
| Disputes resolved with evidence | inspect | reasoning recorded |
| Final decision stated | summary | explicit |

## 7. Failure handling

- **Author marked "fixed" but the code is unchanged** → point at the diff and reopen; this is a process finding worth recording.
- **Re-verification is impossible** (environment) → say so; the finding stays `fixed-unverified` rather than `fixed`.
- **A deferral is really a refusal** → record it as disputed, name the accepting owner, and note the risk; do not let it vanish.
- **The PR has changed substantially** (new commits beyond the findings) → the delta needs a fresh P01/P03 pass on the new scope; say so instead of approving blind.
- **The review revealed a systemic problem** (the same class of bug appears in five PRs) → route to P06 for a convention or a lint rule rather than fixing them one at a time.

## 8. Security and authorisation

Risk class A: verification and comments. Do not merge on the author's behalf unless explicitly authorised, and never approve a security finding on the basis of "will fix in a follow-up" without the accepting owner recorded.

## 9. Completion criteria

- [ ] All findings in a final state with evidence.
- [ ] Fixes re-verified by reproduction or diff review.
- [ ] Regression check performed.
- [ ] Deferrals tracked with owner and ticket.
- [ ] Disputes resolved and recorded.
- [ ] Final merge decision stated.

## 10. Deliverables and handover

Artifact: `FOLLOW_UP.md`.

P06 receives: the residue — findings deferred, conventions missing, and patterns that recur — so the next review is shorter.
