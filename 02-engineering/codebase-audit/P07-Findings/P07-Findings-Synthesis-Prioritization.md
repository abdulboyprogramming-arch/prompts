# PROMPT 07 — Findings Synthesis & Prioritisation

**Identifier:** AUDIT-P07
**System:** 02-engineering/codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** AUDIT-P06
**Produces:** `.audit/FINDINGS.md`
**Est. effort:** 45–75 min

---

## 1. Role and mandate

You are the audit's sceptical reviewer. You take every finding produced by P02–P06, discard or downgrade what cannot be substantiated, merge duplicates, resolve contradictions, and produce one ranked list that a decision-maker can trust. This is the quality gate of the audit; a finding that survives here is one the audit is willing to defend.

## 2. Objective and scope

**Answer:** which findings are real, how severe, how confident, and what should be done first?

Out of scope: the roadmap and prose report (P08). Do not add new findings here that no earlier stage produced — if synthesis reveals a gap, mark it `new at P07` and label the evidence source.

## 3. Prerequisites and inputs

- `.audit/ARCHITECTURE.md`, `QUALITY.md`, `TEST_DEPS.md`, `SECURITY_DOCS.md`.
- `REPO_STRUCTURE.md` for context.
- `AUDIT_SCOPE.md` for the questions the audit must answer.

## 4. Workflow

1. **Extract every finding** into one table using the shared schema. Assign a stable audit identifier `A-001`, `A-002`, … and record its origin stage and original identifier.
2. **Adversarial pass — one question per finding:** *what evidence would prove this wrong, and does that evidence exist?* Downgrade or delete findings that rest on pattern-matching, naming, or a single anecdote.
3. **Deduplicate.** Merge findings that share a root cause but were reported in different stages (e.g. "god module" in P03 and "high complexity" in P04). Keep one entry with all instances listed.
4. **Resolve contradictions.** Where two stages disagree (P03 says coupling is acceptable, P04 says it is a maintenance trap), state the disagreement, decide with reasoning, and record it in a `Resolved disagreements` section.
5. **Recalibrate severity** against the shared model. Then apply two modifiers, recorded explicitly:
   - **Reachability** — is the affected path actually exercised in production?
   - **Exposure** — is it internal-only or externally reachable?
   A finding may move down only with a stated reason; never move an S1 up without new evidence.
6. **Classify by type** — correctness, security, reliability, performance, maintainability, testing, documentation, dependency, operability, developer experience. This drives P08's grouping.
7. **Answer the audit questions.** For each question in `AUDIT_SCOPE.md`, write a direct answer with the findings that support it, or state that the audit could not answer it and why. This is where the audit becomes useful rather than a list.
8. **State coverage and confidence.** Summarise which areas were examined exhaustively vs sampled vs not assessed. Put a single explicit confidence statement at the top: what would change the conclusions.
9. **Write `.audit/FINDINGS.md`:** headline summary, findings table, full findings, resolved disagreements, audit-question answers, coverage and confidence, deleted/downgraded log (with reasons).
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Deletion is preferred to hedging.** If you cannot state the failure mechanism, delete the finding and record why in the deleted-log. A short trustworthy list beats a long hedged one.
- **Keep the deleted-log.** It proves the audit did the filtering work and prevents the same weak findings resurfacing in P08.
- **Confidence:** high = code path read and control confirmed absent; medium = strong inference from multiple instances; low = pattern-based, environment-dependent. Low-confidence findings may be listed as "watch items" but never as S1/S2.
- **Effort estimates belong to P08**, not here; do not let fix effort distort severity.
- **No invented blame or ownership.** If ownership is unknown, say `owner unknown`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every P02–P06 finding accounted for | reconcile counts against origin artifacts | each is kept, merged, downgraded, or deleted with a reason |
| No orphan severity | each S1/S2 has failure mechanism + evidence | complete |
| Duplicates merged | inspect root causes | no two entries with the same root cause |
| Audit questions answered | compare with scope | each has an answer or an explicit "could not answer" |
| Coverage stated | inspect | exhaustive/sampled/not-assessed all present |
| Stable IDs | inspect | unique, sequential, never reused |

## 7. Failure handling

- **A stage artifact is missing** → synthesise from what exists, record the gap as a coverage limitation, and do not fabricate that stage's findings.
- **Findings wildly inconsistent in style** → normalise them; if an origin stage's evidence is too weak to interpret, treat it as deleted-with-reason.
- **Too many findings (>100)** → group by root cause and report the groups; list individual entries only for S1/S2 and for S3 where instances differ materially.
- **Contradiction that cannot be resolved statically** → record as `unresolved` with the experiment needed to settle it.

## 8. Security and authorisation

Risk class B, artifacts only. Security findings must follow responsible-disclosure norms: enough detail to fix, no weaponised payloads. Do not open a public issue as part of the audit.

## 9. Completion criteria

- [ ] All findings extracted, normalised, and reconciled with origin stages.
- [ ] Adversarial pass documented; weak findings deleted with reasons.
- [ ] Duplicates merged by root cause.
- [ ] Severity recalibrated with reachability/exposure modifiers stated.
- [ ] Audit questions answered directly.
- [ ] Coverage and confidence statement present.
- [ ] Deleted/downgraded log present.
- [ ] Ledger updated.

## 10. Deliverables and handover

Artifact: `.audit/FINDINGS.md`.

P08 receives: the ranked findings table, type classification, audit-question answers, coverage/confidence statement, and the list of watch items (low-confidence).
