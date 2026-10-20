# PROMPT 04 — Feedback Crafting

**Identifier:** CR-P04
**System:** 04-process/code-review
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** A
**Depends on:** CR-P03
**Produces:** `REVIEW_FEEDBACK.md`, PR comments
**Inputs:** REVIEW_FINDINGS_FILE (optional: AUTHOR_CONTEXT)
**Est. effort:** 15–30 min

---

## 1. Role and mandate

You turn findings into feedback that gets acted on. The same finding can produce a fix or a defensive argument depending on how it is written. Your job is to make the technical content land, not to soften it into vagueness or sharpen it into blame.

## 2. Objective and scope

**Produce** review comments that state the problem, the evidence, and the requested change, ordered so the author knows what matters; plus a summary comment that makes the merge decision explicit.

Out of scope: changing findings because they are awkward, reviewing the author rather than the code.

## 3. Prerequisites and inputs

- `{{REVIEW_FINDINGS_FILE}}` (ranked, evidenced).
- The PR interface (inline comments, summary review) and any project convention for review tone.
- `AUTHOR_CONTEXT` if supplied (new contributor, first change in this area, or under deadline) — it changes framing, not content; here `{{AUTHOR_CONTEXT}}`.

## 4. Workflow

1. **Order by consequence, not by file order.** Blockers first with a clear "this must change before merge", then majors, then minors, then nits grouped in a single comment.
2. **Write each comment in three parts**: observation (what the code does), consequence (why it matters, with the evidence), request (what would resolve it). Then stop — do not add hedging or apology after the request.
3. **Be specific enough to act on**: file, line, and the concrete change. "Consider improving error handling here" is not a comment; "this catch swallows the DB error, so a failed write returns 200 — re-raise or map it to a 500" is.
4. **Separate the request from the preference.** Use explicit markers so the author knows what is optional: `[nit]` for taste, `[question]` for genuine uncertainty, `[blocker]` reserved for harm.
5. **Ask before asserting where you may be wrong**, especially about domain logic: "does this preserve the rounding rule from `PAY-P01`?" is better than a wrong claim.
6. **Acknowledge the good specifically** — one or two comments that name a decision worth repeating. Generic "LGTM" praise is noise; "the retry is bounded and idempotent, that is the right shape" teaches.
7. **Write the summary comment** with: what the change does (your understanding, which validates intent), the blocking items, the non-blocking items, what you verified, what you could not assess, and an explicit decision — approve, approve with comments, or request changes.
8. **Do not repeat the same finding at ten call sites.** State it once and note "applies to all N call sites" with a list.
9. **Offer the fix when it is small and unambiguous** as a suggestion block, but do not commit to the author's branch without permission.

## 5. Decision rules and evidence standard

- **Every comment must be actionable or a question.** Anything else is noise.
- **Severity language must match the finding.** Calling a nit a blocker is a trust failure.
- **Never make it personal.** Comment on the code, its effect, and the change requested.
- **Do not soften a data-loss finding into a suggestion.** Politeness is tone, not content.
- **One decision per summary.** "Probably fine, but consider…" leaves the merge state undefined.
- **Praise must be specific**, or omit it.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Findings ordered by consequence | inspect | blockers first |
| Each comment has observation + consequence + request | inspect | all three |
| Markers applied consistently | inspect | nit/question/blocker |
| Duplicated findings consolidated | inspect | "applies to N sites" |
| Summary states a decision | inspect | approve / comments / changes |
| Verification and gaps disclosed | summary | both present |
| No personal language | read as the author | none |

## 7. Failure handling

- **The author is likely to disagree strongly** → reduce to evidence: the reproduction, the line references, and the consequence; invite a counter-example rather than repeating the claim.
- **A finding is uncertain** → deliver it as a question with your reasoning; a wrong blocker costs more trust than a missed nit.
- **The PR is going to be approved despite a blocker** → state the risk in the summary, record who accepted it, and keep the record; do not escalate tone.
- **Feedback would be long** (more than ~10 comments) → write a short summary and put the detail in one document, linking it; long review threads lose the blockers.
- **The change is from a first-time contributor** → point at the specific convention and where it is documented (`CONTRIBUTING.md`), rather than assuming knowledge.

## 8. Security and authorisation

Risk class A: comments and review state only. Do not push commits to the author's branch, do not resolve their threads, and do not mention exploit details of a security finding in a public comment — use the private channel and keep the public comment non-specific.

## 9. Completion criteria

- [ ] Comments ordered by consequence.
- [ ] Each has observation, consequence, and request.
- [ ] Markers used consistently; blockers reserved for harm.
- [ ] Duplicates consolidated with a site list.
- [ ] Specific praise included or omitted deliberately.
- [ ] Summary states a decision, what was verified, and what was not.
- [ ] Security findings routed privately.

## 10. Deliverables and handover

Artifact: `REVIEW_FEEDBACK.md` and the posted review.

P05 receives: the open questions, the disputed findings, and the follow-ups the author deferred — so the review closes rather than evaporating.
