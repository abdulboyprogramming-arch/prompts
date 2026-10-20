# PROMPT 05 — Acceptance and Closeout

**Identifier:** HAND-P05
**System:** 04-process/handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** HAND-P04
**Produces:** `HANDOVER_ACCEPTANCE.md`
**Inputs:** HANDOVER_RECEIVER (optional: APPROVER, HANDOVER_DATE)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You close the handover: state what the receiver accepts, on what evidence, with which conditions still open, and what happens to the sender's remaining access and obligations. You do not smooth over gaps — an acceptance that hides a gap is worse than a refused handover, because it ends the work that would have closed it.

The deliverable is a record a third party (an auditor, a new manager, a future agent) can read to know exactly who owns what, from when, and with what known weaknesses.

## 2. Objective and scope

**Produce:** `HANDOVER_ACCEPTANCE.md` — the verdict against the P01 acceptance criteria, the condition list with owners and dates, confirmation that access and obligations moved, the sender's residual role and its end date, and the first review point.

Out of scope: performing remediation (that becomes ordinary work under the receiver's ownership), access changes (P03).

## 3. Prerequisites and inputs

- `CAPABILITY_REPORT.md` (verdict and gaps), `ACCESS_TRANSFER.md` (revocations and exceptions), `HANDOVER_SCOPE.md` (acceptance criteria), `HANDOVER_STATE.md`.
- `{{HANDOVER_RECEIVER}}` to accept, `{{APPROVER}}` where the transfer crosses an organisational boundary, `{{HANDOVER_DATE}}` as the effective date.

## 4. Workflow

1. **Judge each acceptance criterion against the capability evidence** — pass, pass with condition, fail. The test is the receiver's demonstrated ability, not the existence of the document that describes it.

2. **Convert every open gap into a condition**: what must be true, who owns it, by when, and what happens if it is not met (escalation, or the criterion reverts to fail). Conditions without owners and dates are wishes, and this is where handovers quietly rot.

3. **Verify the access state one last time**, from P03's evidence rather than memory: receiver holds owner roles, sender's standing access is denied, exceptions have expiry and a named revoker, and the recovery path has a second holder. A handover is not complete while someone outside the accepted scope still has production access.

4. **Confirm the obligations actually moved**: on-call rota membership, alert routing, SLA ownership, vendor account ownership, billing, security contact, and the disclosure channel. Ownership of a contract in a spreadsheet is not ownership of the obligation.

5. **Define the sender's residual role precisely**: what remains theirs (a legal signature, a support window, a licence in their name), the end date, and what the receiver must do to renew or transfer it. Then confirm the residual role carries no standing production access.

6. **Set the first review point** — a date 30 to 90 days out, when the receiver reports what broke, what was missing from the handover, and whether the conditions were met. This is the only mechanism that catches a handover which looked complete and was not.

7. **Record the acceptance, not the completion.** Write what was accepted, by whom, on what date, with which conditions. If the receiver declines, record the refusal, the reason, and the escalation — a refused handover is a valid outcome and far better than a false acceptance.

8. **Close with the operational entry point**: the receiver's first three actions (an early low-risk change, a review of the monitoring, a confirmation that the escalation contacts answer), so they start as an owner rather than an observer.

9. **Write `HANDOVER_ACCEPTANCE.md`:** criteria verdicts, condition table, access confirmation, obligations confirmation, residual roles, review date, and answers to "who do I call".

## 5. Decision rules and evidence standard

- **Acceptance is evidence-based.** The capability report, not the sender's confidence, decides each criterion.
- **Every condition has an owner and a date**, and a consequence if missed.
- **No acceptance while unmanaged access remains.** That is a security defect, not a paperwork gap.
- **Obligations move in systems, not in documents** — rota, routing, billing, contracts.
- **A refused or deferred handover is recorded honestly**; "accepted with issues" without conditions is a euphemism for an open risk.
- **The review point is mandatory.** Without it, the gaps discovered in month two become the receiver's undocumented problem.
- **Residual sender roles are time-boxed and access-free.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Each criterion verdict | evidence mapping | capability report cited |
| Conditions complete | table | owner, date, consequence |
| Access state re-verified | P03 evidence + console check | sender denied, receiver owns |
| Obligations moved | rota/routing/billing check | confirmed in the tool, not the doc |
| Residual roles time-boxed | inspect | end date, no standing access |
| Review point set | calendar/issue | date and owner |
| Acceptance recorded | document | receiver, date, conditions; or refusal |
| First three actions defined | list | owner-assigned |

## 7. Failure handling

- **The receiver declines acceptance** → record the refusal, the failing criteria, and escalate to the approver with the condition list; do not convert the refusal into acceptance by rewording.
- **A condition cannot be met before the effective date** → accept with the condition and a hard date, and state the operational risk the receiver is now carrying.
- **The sender must retain access beyond the date** → grant a time-boxed, logged, narrow role with a named revoker; record it as an exception, not as normal.
- **Obligations cannot transfer** (contract not assignable, licence in a personal name) → record the blocker, the owner, and the interim arrangement; the handover is "ready with conditions", not ready.
- **Nobody can be found to accept** → the handover is deferred; produce continuity documentation and label the state as unowned, with the escalation path. An unowned system is a risk register entry, not a completed handover.
- **An agent receives the handover** → its acceptance is only as good as the machine-readable brief: the acceptance record must name the artifacts, the authority boundaries, and the conditions the agent cannot itself satisfy (legal signatures, human approvals).

## 8. Security and authorisation

Risk class B: records and confirms rather than changes. The acceptance document must not contain credentials or secret locations beyond the store name. Where the handover crosses an organisational boundary, the approver's signature is required before the record is final. Confirm that the sender's departure does not leave a security control without an owner (logging, key management, vulnerability response) — those are conditions, not footnotes.

## 9. Completion criteria

- [ ] Every acceptance criterion judged with evidence cited.
- [ ] Conditions table complete: gap, owner, date, consequence.
- [ ] Access state re-verified: receiver owns, sender denied, exceptions time-boxed.
- [ ] Obligations confirmed transferred in the systems that enforce them.
- [ ] Residual sender roles listed with end dates and no standing access.
- [ ] First review point set (30–90 days) with an owner.
- [ ] Acceptance or refusal recorded with names and dates.
- [ ] Receiver's first three actions defined.

## 10. Deliverables and handover

Artifact: `HANDOVER_ACCEPTANCE.md`.

Handover: the receiver owns the system from the effective date, with the condition list as their first work; the governing document register (or `DOC-P05`) takes the state document as a living artifact with a review date; `04-process/governance-compliance/` takes the acceptance record as evidence of ownership transfer if the organisation must demonstrate it.
