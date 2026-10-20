# Project Handover

**Maturity: operational (v1.0.0).** Five stages for moving ownership of a system from one person, team, or agent to another — with the access actually transferred, the sender actually revoked, and the receiver proving they can operate it.

**Entry point:** [`P01-Scope`](P01-Scope/P01-Handover-Scope.md). If the sender is already gone, start at `02-engineering/project-recovery/` instead.
**Execution mode:** planning
**Per stage:** planning (P01), diagnostic (P02, P04), implementation (P03, P05)
**Risk class:** A → B → **D → C → B** — P03 moves ownership and revokes standing access, which is the highest-consequence action in the library outside data deletion

## Why this system exists

Handovers are treated as a documentation task. They are an **ownership and access transfer**, and the failure modes are consistent:

- **Documents without capability.** A folder of architecture notes, and the new owner cannot deploy or roll back. The previous owner is still the only one who can.
- **Access without revocation.** The receiver is added; the contractor, the leaver, or the outsourced team keeps production access for another year.
- **Sole-owner lockout.** A domain, cloud root, or vendor console transfers to exactly one new holder, who then loses their laptop.
- **Obligations that never move.** On-call, SLAs, billing, vendor renewals, and security disclosure stay with someone who has left the building.
- **Agent receivers treated as readers.** An agent cannot ask a colleague what "the usual deploy" means. Anything unwritten is simply lost — and any authority not stated is either unused or overstepped.

This system makes the transfer explicit, evidenced, and testable, and it distinguishes it from the two things it is constantly confused with: the per-stage handoff block (`07-workflows/HANDOFF-CONTRACT.md`) and continuity documentation with no receiver at all.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| HAND-P01 | [Scope & receiver](P01-Scope/P01-Handover-Scope.md) | Type, parties, what transfers and what does not, acceptance criteria as capabilities, dates and support window | `HANDOVER_SCOPE.md` |
| HAND-P02 | [State & knowledge](P02-State/P02-State-and-Knowledge-Capture.md) | Proven vs believed, running reality, open work at its exact position, decisions with reasons, obligations, 3 a.m. brief | `HANDOVER_STATE.md` |
| HAND-P03 | [Access & revocation](P03-Access/P03-Access-and-Credential-Transfer.md) | Ownership transfer, secret rotation, sender revocation with proof, dual control, recovery path | `ACCESS_TRANSFER.md` |
| HAND-P04 | [Capability verification](P04-Competence/P04-Capability-Verification.md) | The receiver performs: build, deploy, roll back, mitigate an alert, change something, find people | `CAPABILITY_REPORT.md` |
| HAND-P05 | [Acceptance & closeout](P05-Acceptance/P05-Acceptance-Closeout.md) | Verdict per criterion, conditions with owners, obligation transfer, residual roles, review point | `HANDOVER_ACCEPTANCE.md` |

## The five handover types

| Type | Failures it brings | Extra requirement |
|------|--------------------|-------------------|
| Person → person | Knowledge leaves with the person | Written reasons for the odd decisions |
| Team → team | Ownership gaps at the boundary | Named owner per asset, not a team name |
| Agency → client | Accounts in the wrong legal entity | Ownership transfer in every console, not membership |
| Human → agent | Implicit knowledge and implicit authority | Everything written; permission boundaries explicit |
| Agent → human | State exists only in artifacts, some stale | Contradiction resolution and a staleness date |

## The rules

1. **Capability is the acceptance unit.** Documents are means; "the receiver can roll back unaided" is the criterion.
2. **Two halves or it did not happen.** Grant and revoke. Every time.
3. **Rotate everything the sender could read.** Access removal without rotation is a promise, not a revocation.
4. **No sole-owner end states.** Domain, cloud root, billing, and vendor consoles get dual control.
5. **Proven and believed are separate lists.** The receiver's trust depends on the distinction.
6. **Reasons, not just decisions**, or the successor will undo a deliberate choice and reintroduce the incident.
7. **Every condition has an owner and a date**, and a consequence if it slips.
8. **A handover is not complete while an outsider holds access.**

## Proportionality

| Situation | Run |
|-----------|-----|
| A colleague goes on leave for two weeks | P02 operational brief only |
| Contractor's engagement ends | P01 → P02 → P03 → P04 → P05 |
| Agency delivers a project to a client | All five; P03 and P05 carry the legal obligations |
| Long-running work resumes with a new agent | P01 (scope) → P02 (machine-readable state) → P05 with the authority boundaries named |
| The owner has already left | `02-engineering/project-recovery/` first; this system resumes once a receiver exists |
| Shift change during an incident | Not this system: `05-scenarios/incident-response/` |

## Boundaries

- State passed **between stages of one engagement**: `07-workflows/HANDOFF-CONTRACT.md` (`WF-HANDOFF`). This system consumes that block for its state document.
- Recovering a project with **no counterpart available**: `02-engineering/project-recovery/`.
- Removing a service or asset permanently: `04-process/decommissioning/`.
- Producing the handover documents themselves (handbook, runbooks, SRS): `04-process/documentation/`.
- On-call shift handover: still a backlog item (12); the operational brief in P02 is the current best answer.

## What this system will not do

- Transfer a system with no available sender and no artifacts. That is recovery, and calling it handover hides the risk.
- Make an uninterested receiver competent. The capability stage will show it, and P05 will record a refusal rather than a fiction.
- Sign for a legal transfer. It produces the approval record; a person signs.
