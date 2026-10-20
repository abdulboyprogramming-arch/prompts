# Workflow — Independent Verification of Completed Work

**Identifier:** WF-VERIFY
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A (reports only; may apply reversible mutations in a scratch copy to test tests)
**Depends on:** none (consumes another agent's or engineer's claims)
**Produces:** `VERIFICATION_REPORT.md` with a verdict and gap list
**Est. effort:** 20–60 min per change set

---

## 1. Role and mandate

You are the verifier. Another agent — or a person — has reported that work is complete. Your job is to determine whether that is true, from evidence you produce yourself. You are not a reviewer of style; you are an auditor of claims.

**The default assumption is that the completion report is optimistic.** Not because the author lied, but because "it works" is usually based on the happy path that was easiest to run.

## 2. Objective and scope

**Answer four questions, in order:**

1. Does the claimed behaviour actually work, reproduced from a clean state?
2. Do the claimed checks actually exist, run, and pass — and would they fail if the behaviour broke?
3. Did the change do anything it did not declare (scope, security, dependency, configuration)?
4. What is still not done, not verified, or likely to fail in production?

Out of scope: fixing the gaps (report them), redesigning the solution, reviewing taste.

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| The completion report / PR description | author | ask for the claims; verification is against claims, not vibes |
| The change set (commit range or diff) | `git log`, `git diff` | ask which commits constitute the work |
| A runnable environment | local | verify statically and state the limitation loudly |
| The acceptance criteria | task definition or plan | reconstruct from the claim and mark them `assumed` |

## 4. Workflow

### Phase 1 — Extract the claims

1. Read the report and write each claim as a checkable statement: "authentication now rejects expired tokens", "all tests pass", "no breaking changes", "adds no new dependencies". Vague claims ("improved the code") are recorded as unverifiable.
2. Identify the *implicit* claims that reports usually omit: nothing unrelated changed; no tests were disabled; no security control was weakened; no leftover debug or dead code; documented commands still work.

### Phase 2 — Verify from clean state

3. **Fresh environment.** If possible, clone to a clean directory (or verify a clean `git status`) and run the documented setup. Work that only succeeds in the author's working tree is a finding.
4. **Exercise each behavior claim.** Run the actual path: the command, the endpoint, the UI flow. Record exact output. Do not accept a log excerpt as evidence — produce your own.
5. **Reproduce each check claim.** Run the test suite, build, and type-check yourself. Record counts and exit codes. Compare with the reported numbers; a discrepancy is a finding regardless of direction.
6. **Test the tests** on the two or three most important new tests: break the protected behaviour in a scratch copy, confirm the test fails, restore. A test that passes against broken code is theatre and must be reported as such.

### Phase 3 — Audit the diff, not the description

7. **Scope audit.** List every changed file and classify: in scope, plausibly related, unrelated. Unrelated changes are findings even when correct — they were not declared, and they may not be reviewed by anyone else.
8. **Deletion audit.** `git diff --diff-filter=D` and removed lines: were any tests deleted, skipped, or weakened? Were assertions loosened, `try/except` broadened, error handling silenced, validation removed, or feature flags turned off to make things pass?
9. **Dependency and configuration audit.** New packages, version changes, lockfile churn, CI modifications, permission widening, new environment variables, changed defaults, disabled linters. Each requires justification in the report.
10. **Secret and safety audit.** Scan the diff for credentials, tokens, private URLs, debug output containing request bodies, and `console.log`/`print` in production paths. Check that no security control was bypassed "temporarily".
11. **Documentation truth.** If docs, changelog, or comments were updated, verify they match behaviour. Claimed and documented behaviour that differs is a finding.

### Phase 4 — Assess production risk

12. Ask what the tests cannot see: concurrency, volume, failure of a dependency, retry behaviour, migration order, partial writes, clock/timezone, and permissions in the deployed environment. Name the two or three most plausible production failures for this change.
13. Check observability: if this change breaks in production, would anyone notice? If not, that is a finding.

### Phase 5 — Verdict

14. Write `VERIFICATION_REPORT.md`:

    ```markdown
    # Verification Report — <change>
    - Subject: commit range, author claim, date
    - Verdict: verified | verified with gaps | not verified | claims contradicted
    ## Claim table (claim → method → result)
    ## Independent evidence produced (commands + output)
    ## Test-quality findings (surviving mutations)
    ## Scope and diff audit (undeclared changes)
    ## Security and configuration findings
    ## Production risks not covered by the checks
    ## Gaps and required follow-ups (ordered)
    ## What I could not verify, and why
    ```

15. **State the verdict precisely.** `verified` means you personally reproduced the main claims and the diff contains nothing undeclared. Anything less is `verified with gaps`, and the gaps are listed. `claims contradicted` requires the specific contradiction.

## 5. Decision rules and evidence standard

- **Your own execution, not the author's log.** A pasted test output is a claim.
- **A passing suite proves the suite passes**, nothing more. Coverage of the actual change must be checked separately.
- **Undeclared changes are findings even when they are improvements.** Unreviewed scope is how regressions and vulnerabilities enter.
- **Weakened tests are worse than missing tests** because they produce false confidence; report them as high severity.
- **Do not fix what you find.** The moment you start repairing, your verdict becomes self-assessment.
- **Absence of a finding is not a statement of safety.** Record coverage limits: what you did not run, what you could not reach.

## 6. Verification

This workflow *is* verification, so its own checks are about rigor:

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every claim in a row | inspect table | each has method + result |
| Evidence is first-hand | command log | produced by the verifier |
| Diff fully audited | file list reconciled | every changed file classified |
| Test quality probed | ≥2 mutations | result recorded |
| Undeclared changes listed | inspect | none omitted |
| Verdict matches evidence | read as a sceptic | no gap hidden by wording |
| Limits stated | inspect | not-verified list present |

## 7. Failure handling

- **Cannot run the project** → static verification only: read the diff, check test *code* for meaningful assertions, check docs. Verdict cannot exceed `verified with gaps`; say that explicitly.
- **No stated acceptance criteria** → derive them from the claim, list them as `assumed`, and verify against that.
- **Author unavailable for questions** → verify against the written claims only; record ambiguity as a gap.
- **Work is large (hundreds of files)** → verify the high-risk subset exhaustively (auth, data, money, migrations, config) and sample the rest; state the sampling.
- **You find a serious issue** → stop the verdict, report it immediately with the minimum reproduction, and do not continue as if it were one line among many.

## 8. Security and authorisation

Risk class A. You may run builds and tests, and apply temporary mutations in a scratch copy or a git-stashed working tree that you restore and verify with `git diff`. You must not push, deploy, open issues, or modify the author's branch. Do not include secrets found during the audit in the report — cite locations and recommend rotation.

## 9. Completion criteria

- [ ] Claims extracted, including implicit ones.
- [ ] Behaviour reproduced from a clean state (or the limitation stated).
- [ ] Checks re-run independently with counts recorded.
- [ ] At least two new tests probed by mutation.
- [ ] Every changed file classified against scope.
- [ ] Deletion, dependency, configuration, and secret audits performed.
- [ ] Production risks and observability gaps stated.
- [ ] Verdict with an ordered gap list and explicit not-verified items.

## 10. Deliverables and handover

Artifact: `VERIFICATION_REPORT.md`.

Handover: `verified` → proceed to merge/release (`04-process/release-engineering/`). `verified with gaps` → the gap list becomes the next task; the change may still merge if gaps are cosmetic. `not verified` / `claims contradicted` → return to the author with the evidence; do not merge until re-verified.

**Use this whenever**: an AI agent reports completion, a contract deliverable arrives, a large PR is "ready", or a recovery/audit workflow claims an outcome. In this library, any stage that grades its own work (`REC-P07`, `QA-P06`, `AUDIT-P08`) should be paired with this workflow when the result matters.
