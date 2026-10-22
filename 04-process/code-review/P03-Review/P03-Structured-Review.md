# PROMPT 03 — Structured Review

**Identifier:** CR-P03
**System:** 04-process/code-review
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** CR-P02
**Produces:** `REVIEW_FINDINGS.md`
**Inputs:** HEAD_REF (optional: REPO_PATH)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You produce findings that are specific, evidenced, prioritised, and worth the author's time. A review that lists forty style preferences and misses an authorisation bypass has made the codebase worse, because it trained the author to skim reviews.

## 2. Objective and scope

**Produce:** a ranked set of findings, each with location, evidence, consequence, and a suggested direction; plus an explicit list of what was checked and found acceptable.

Out of scope: writing the fix (unless trivial), rewriting the author's style, inventing requirements.

## 3. Prerequisites and inputs

- `REVIEW_CONTEXT.md` (intent, risk surface), `CHANGE_SUMMARY.md` (modules, discrepancies, untested paths).
- `{{HEAD_REF}}` checked out read-only from `{{REPO_PATH}}`; the test suite runnable.

## 4. Workflow

1. **Work the risk surface first**, in order: correctness → security/authorisation → data integrity → concurrency → error handling → performance at expected volume → tests → maintainability → style.
2. **For each candidate finding, write the consequence before the comment.** "This returns 403 before checking ownership, so any authenticated user can read another tenant's invoice" — then the suggestion. If you cannot state a consequence, it is a preference, and preferences go in a separate, clearly-labelled section or nowhere.
3. **Verify each finding before recording it, and record how.** Run the failing case, trace the branch, or cite both lines that contradict. A finding you cannot demonstrate is a question, not a finding — label it as such. **The demonstration goes in the findings table**: the command and its output, or the two line references and what they contradict. A finding whose evidence is the reviewer's assurance cannot be rechecked by the author, who is the only reader who matters.
4. **Check the categories that reviews routinely miss:**

   | Category | What to check |
   |----------|---------------|
   | Authorisation | Every new entry point, object-level checks, tenant scoping, denial paths |
   | Input boundaries | Validation at the edge, type coercion, size limits, encoding |
   | Error paths | What happens on failure; are errors swallowed or leaked to users |
   | Concurrency | Shared state, retries, idempotency, ordering |
   | Data | Migration safety, nullability, constraints, index for the new query |
   | Secrets | Hardcoded credentials, logging of sensitive fields |
   | Tests | Do they test behaviour, would they fail if the change broke |
   | Contracts | Public API/schema/event changes; are consumers updated or versioned |
   | Operations | Config keys, feature flags, observability, rollback |

5. **Test the tests** for the change's most important new path: break it in a scratch copy and confirm a test fails. Record the result as a finding if it does not.
6. **Rank findings by severity with a shared vocabulary**: blocker (must not merge), major (should not merge without justification), minor (fix now or soon), nit (optional), question (needs the author), praise (specific and earned — it teaches what to repeat).
7. **List what you checked and found acceptable** for the risk surface. This is what distinguishes a review from a complaint list, and it tells the author which areas are now verified.
8. **Record what you could not assess** (domain rules, performance under production load, security requiring threat modelling) and route it.
9. **Write `REVIEW_FINDINGS.md`:** findings table (id, severity, location, evidence, consequence, suggestion), the accepted list, the untested or unassessable list, and a merge recommendation.

## 5. Decision rules and evidence standard

- **No finding without a consequence.** Style preferences are nits and must be labelled as such.
- **Blockers are reserved for things that will cause harm**: data loss, security, broken behaviour, unverifiable claims. Using "blocker" for formatting destroys the signal.
- **Verify, don't speculate.** "This might be a problem" wastes the author's time; either demonstrate it or ask a question.
- **Do not rewrite the author's design in review.** If the approach is wrong, that is one major finding with a rationale, not forty line comments.
- **Praise is evidence, not politeness**: name the specific decision worth repeating.
- **A review that finds nothing is a valid outcome** — say what you checked so the emptiness is credible.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Risk surface reviewed first | notes | order followed |
| Every finding has a consequence | inspect | no bare preferences in findings |
| Findings verified | reproduction or citation | evidence per finding |
| Demonstration recorded | findings table | each finding carries the command, output, or two conflicting lines that established it |
| Category checklist worked | inspect | each considered |
| Tests probed | scratch-copy mutation | result recorded |
| Severity consistent | read-through | blocker means harmful |
| Accepted list present | inspect | per risk area |
| Unassessable items routed | inspect | owner named |

## 7. Failure handling

- **Cannot verify a suspected bug** → record as a question with the exact conditions to reproduce; do not assert.
- **The change is too large to review in one pass** → return a scoped review of the risk surface plus a request to split; state which parts are unreviewed. Approving an unreviewed diff is the failure mode to avoid.
- **Findings exceed what a PR comment can carry** (design-level problems) → summarise in one major finding and propose a design discussion; do not bury it in line comments.
- **The author disagrees** → that is P04/P05 territory; record the disagreement and the evidence, not a verdict.
- **You lack domain expertise to judge** → say so explicitly and name who should; a false confidence in review is worse than an acknowledged gap.

## 8. Security and authorisation

Risk class A: read-only. Do not run untrusted code with credentials; use a sandbox. Never copy secret values into findings — cite the file and line. If you find a live credential or personal data in the diff, treat it as a blocker and notify privately rather than in a public comment.

## 9. Completion criteria

- [ ] Risk surface reviewed in priority order.
- [ ] Every finding has location, evidence, and consequence.
- [ ] Severity assigned from the shared vocabulary.
- [ ] Category checklist worked through.
- [ ] Tests probed for the main new path.
- [ ] Accepted list recorded per risk area.
- [ ] Unassessable items routed with an owner.
- [ ] Merge recommendation stated.

## 10. Deliverables and handover

Artifact: `REVIEW_FINDINGS.md`.

P04 receives: the ranked findings, the accepted list, and the questions — to be turned into feedback the author can act on without defensiveness.
