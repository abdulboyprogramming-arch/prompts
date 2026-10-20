# PROMPT 02 — Evidence Collection & Control Testing

**Identifier:** GOV-P02
**System:** 04-process/governance-compliance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** GOV-P01
**Produces:** `.governance/EVIDENCE.md`
**Inputs:** EVIDENCE_PERIOD, APPLICABLE_FRAMEWORKS
**Est. effort:** 45–120 min

---

## 1. Role and mandate

You are testing whether controls actually operated during a period, not whether they are documented. Auditors test a sample; you test a sample *and* look for the failures a sample can miss. Your output is evidence with dates and sources, plus an honest statement of the population you sampled and what you could not see.

## 2. Objective and scope

**Prove or disprove** that each `evidenced`/`weak` control from P01 operated over a defined period.

Out of scope: fixing failures (P03), assessing design quality beyond what testing reveals.

## 3. Prerequisites and inputs

- `.governance/CONTROL_MAP.md`.
- Access to: repository history and PR metadata, CI run history, IAM/access logs, ticket systems, incident records, backup job history.
- The **period under test** `{{EVIDENCE_PERIOD}}` (e.g. last 6 or 12 months) and the frameworks it must satisfy (`{{APPLICABLE_FRAMEWORKS}}`) — state both explicitly; evidence outside the period is not evidence for it.

## 4. Workflow

1. **Define the population per control.** For "all production changes are approved", the population is every merge to the production branch in the period — not "some PRs". Record the population size.
2. **Select a sample** — random where possible, plus **targeted selection** at the edges: the largest change, the change merged at 2 a.m., the change by the person who is also the approver, the change to CI configuration. Samples miss exactly these.
3. **Test each control with a binary criterion**, e.g. "for each sampled merge, an approval by a non-author exists with a timestamp earlier than the merge". Record pass/fail per item, not an aggregate impression.
4. **Test the mechanism itself, not only the artefacts**, for controls that can be bypassed: attempt a direct push to the protected branch (expect rejection); attempt to merge without approval (expect block); attempt to read a production secret as a non-privileged identity (expect denial). Record the result and revert nothing, because nothing should have changed.
5. **Check for the quiet failures:**
   - approvals that arrived after the merge (timestamps),
   - self-approval or approval by a bot with write access,
   - admin overrides and break-glass usage,
   - CI checks that were skipped, made non-blocking, or re-run until green,
   - alerts that exist but route nowhere, or fire into a channel nobody reads,
   - backup jobs that "succeeded" without a restore test,
   - retention jobs that never ran, or that deleted nothing.
6. **For access controls**, compare the current role assignments against the stated model: every human and service account with production access, their justification, and whether the justification is current. Count service accounts with no owner — a common and serious finding.
7. **For data controls**, trace one record end to end: where it is stored, who can read it, when it is deleted, and whether an export leaves the boundary. One traced record reveals more than a policy table.
8. **For backup/recovery**, find the last *restore test*, not the last backup. A backup job with no restore is untested.
9. **For incident management**, verify that the last N incidents have records with timelines and that actions have owners. Check whether an incident occurred that has no record — that is a control failure in itself.
10. **Record evidence with provenance**: artefact name, source system, date range, who retrieved it, and where it is stored. Evidence without provenance does not survive an audit.
11. **Write `.governance/EVIDENCE.md`:** period, population and sample sizes, per-control results with counts, mechanism test results, quiet-failure findings, access and data traces, backup restore status, the `not tested` list with reasons, and the evidence index with provenance.
12. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Sampling is stated, never implied.** "Reviewed changes" without a population and sample size is not a result.
- **Timestamps decide ordering.** An approval after the merge is not a pre-merge approval, regardless of intent.
- **Mechanism tests beat artefact review** where a bypass is plausible: the artefact shows what happened, the mechanism test shows what could have happened.
- **Never modify evidence.** No editing of tickets, no re-running a job to produce a cleaner log, no deleting a failed run.
- **A control that operated with exceptions is `operating with exceptions`**, not `passed`. Quantify the exception rate.
- **Do not fix during testing.** Record and move on; the readiness decision depends on an unaltered picture.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Period stated | inspect | explicit range |
| Population and sample stated | inspect | sizes recorded |
| Per-item results, not impressions | inspect | counts |
| Mechanism tests executed | command/settings evidence | results recorded |
| Quiet failures checked | checklist | each addressed |
| Evidence has provenance | index | source, date, retriever |
| Nothing modified | `git status`, no ticket edits | clean |

## 7. Failure handling

- **Cannot access the population** (no PR metadata, no IAM history) → record the control as `not testable` with the missing capability; this is itself a finding about observability.
- **Evidence was not retained** for older parts of the period → state the sub-period tested and treat the rest as a gap; do not extrapolate.
- **A control fails broadly** → quantify (e.g. "9 of 40 merges had no approval"), stop expanding the sample, and escalate in P03. Do not continue testing as if the finding were one item.
- **Mechanism test is disruptive** (e.g. requires modifying a production policy) → do not perform it; record it as a recommendation for a controlled test with the owner.
- **Contradiction with a previous audit or attestation** → record it explicitly; prior attestations that cannot be re-evidenced are a serious readiness issue.

## 8. Security and authorisation

Risk class A: read-only, plus non-destructive mechanism tests that should be *rejected*. Do not attempt privilege escalation, do not modify IAM, do not run destructive recovery tests on production. Handle personal data in access lists minimally — record identities as roles/IDs where possible. Store evidence in a controlled location.

## 9. Completion criteria

- [ ] Period under test stated.
- [ ] Population and sample sizes recorded per control.
- [ ] Per-item pass/fail with counts.
- [ ] Mechanism tests executed and recorded.
- [ ] Quiet-failure checklist completed.
- [ ] Access review completed with unowned service accounts counted.
- [ ] One record traced end to end for data controls.
- [ ] Last restore test identified.
- [ ] Evidence index with provenance.
- [ ] Not-tested list with reasons.

## 10. Deliverables and handover

Artifact: `.governance/EVIDENCE.md` and the evidence index.

P03 receives: pass/fail counts, exception rates, mechanism-test results, and the not-testable list — the raw material for a readiness decision that does not overstate.
