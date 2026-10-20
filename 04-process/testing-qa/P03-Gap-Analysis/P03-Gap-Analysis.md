# PROMPT 03 — Gap Analysis

**Identifier:** QA-P03
**System:** 04-process/testing-qa
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** QA-P02
**Produces:** `.qa/GAPS.md`
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the risk analyst converting measurements into a ranked list of *specific* gaps. A gap is not "low coverage"; it is "no test fails if tenant isolation is broken in the export endpoint". You do not choose the remedy here.

## 2. Objective and scope

**Answer:** where is the difference between the risk we carry and the protection we have — ranked by consequence?

Out of scope: test design decisions, level selection, effort estimates (P04).

## 3. Prerequisites and inputs

- `.qa/CURRENT_STATE.md` (R1 coverage map, reliability signals, latency).
- `.qa/QA_CONTEXT.md` (risk map, success measures).
- Optional: audit findings from `02-engineering/codebase-audit/` if one was run.

## 4. Workflow

1. **Diff risk against protection.** For each behaviour: risk class × protection status (covered/incidental/uncovered) → gap severity. R1+uncovered is the top of the list, always.
2. **Classify gap types**, because each has a different remedy:
   - *Missing coverage* — no test for an R1/R2 behaviour.
   - *False confidence* — tests exist but cannot fail (assertion-free, over-mocked, snapshot-only).
   - *Reliability* — flaky, order-dependent, environment-coupled.
   - *Feedback* — suite too slow to run on every change.
   - *Enforcement* — tests exist but CI does not block on them.
   - *Maintainability* — duplicated fixtures, copy-pasted setup, unclear failures.
   - *Process* — tests written after release, no regression test on bug fixes, no ownership.
3. **For each gap, state the failure it would allow.** "No test for idempotent webhook retry → duplicate charges on retry after timeout."
4. **Verify each claimed gap** with a quick check: search for the test that would cover it, read the suspicious test, inspect the CI workflow. Do not list a gap you have not confirmed absent.
5. **Rank** by (risk class, exposure, likelihood of regression) — not by ease of fixing.
6. **Cap the list** at 12–15 gaps. Beyond that, group by root cause; a 60-item list will not be acted on.
7. **Note deliberate non-gaps.** Areas that look uncovered but are justified (e.g. framework-generated code, third-party UI covered by vendor tests) — this prevents P04 from re-litigating them.
8. **Write `.qa/GAPS.md`:** ranked table (ID, behaviour, risk, gap type, protection status, failure allowed, evidence), narrative for the top five, non-gaps, and the coverage limits of this analysis.
9. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Confirm absence before claiming a gap.** The search you performed must be described (paths, patterns, commands).
- **One gap per behaviour failure mode.** Do not merge unrelated behaviours into a single "coverage" gap.
- **Reliability gaps need observed evidence** — a re-run that differed, a sleep in the code, a shared fixture. "Might be flaky" is not a gap.
- **Do not treat 100% coverage as a goal.** A gap is defined by risk exposure, not by coverage delta.
- **Process gaps are legitimate findings** but must be evidenced (e.g. three bug-fix commits in the last 90 days with no accompanying test change — cite the commits).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every R1 behaviour appears | compare with P01/P02 maps | none missing |
| Each gap's absence confirmed | re-run the search described | still absent |
| Failure consequence stated | inspect | concrete, not generic |
| Ranking justified | inspect | ordered by risk, not effort |
| Non-gaps recorded | inspect | present where applicable |
| Gap count within cap | inspect | ≤15 entries or grouped |

## 7. Failure handling

- **P02 was partial** → mark gaps in unexamined areas as `unverified`, not as gaps. State which areas remain unknown.
- **No risk map** (P01 skipped) → reconstruct a minimal risk map from entry points and consequences before ranking; flag the shortcut.
- **Too many R1 gaps** → retain all R1 gaps and group R2–R4 into themes; recommend a stabilisation phase rather than a full list.
- **Conflicting evidence** (a test exists but is disabled) → record as `false confidence` with the disabled marker cited.

## 8. Security and authorisation

Risk class B, artifacts only. Descriptions of security-relevant gaps should state the missing control, not a working exploit (see `00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`).

## 9. Completion criteria

- [ ] Risk × protection diff complete for all behaviours in the risk map.
- [ ] Gaps classified by type with evidence.
- [ ] Failure consequences stated.
- [ ] Ranked by risk; capped or grouped.
- [ ] Verification method for each absence recorded.
- [ ] Non-gaps noted; ledger updated.

## 10. Deliverables and handover

Artifact: `.qa/GAPS.md`.

P04 receives: the ranked gaps, their types, and the non-gaps so strategy can allocate effort by remedy type rather than uniformly.
