# PROMPT 01 — Scope, Receiver, and Terms

**Identifier:** HAND-P01
**System:** 04-process/handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `HANDOVER_SCOPE.md`
**Inputs:** TARGET_SERVICE, HANDOVER_RECEIVER (optional: HANDOVER_DATE, APPROVER)
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You define what is actually being transferred, to whom, by when, and what "accepted" means. Handovers fail before any document is written, in the definition: the sender assumes "the code" and the receiver inherits production access, a vendor contract, an on-call rotation, and three deadlines nobody mentioned.

Your output is a contract between two parties — even when both are the same organisation, and even when the receiver is an agent.

## 2. Objective and scope

**Produce:** `HANDOVER_SCOPE.md` — the handover type, the receiver and their starting competence, the transfer inventory (assets, obligations, accesses, knowledge), what is explicitly **not** transferring, the acceptance criteria, the date, and the sender's availability after the handover.

Out of scope: capturing state (P02), moving access (P03), proving the receiver can operate it (P04), sign-off (P05).

## 3. Prerequisites and inputs

- `{{TARGET_SERVICE}}` — the system, product, repository, or portfolio being handed over.
- `{{HANDOVER_RECEIVER}}` — a person, a team, or an agent, with their current knowledge of the system (none, partial, deep) and their authority to accept.
- `{{HANDOVER_DATE}}` and `{{APPROVER}}` — when it takes effect, and who signs for each side.

## 4. Workflow

1. **Classify the handover**, because each type fails differently:

   | Type | Typical trigger | Characteristic failure |
   |------|-----------------|------------------------|
   | Person → person | Someone leaves, changes team, or goes on long leave | Undocumented knowledge leaves with them |
   | Team → team | Reorg, outsourcing, insourcing | Ownership gaps at the boundary; nobody feels responsible |
   | Agency / contractor → client | Contract end | Access and vendor accounts stay in the wrong legal entity |
   | Human → agent | Long-running work resumed by an AI agent, or automation taking over operations | Everything unwritten is lost; implicit authority becomes forbidden action |
   | Agent → human | An agent's run ends mid-project | State exists only in artifacts, some stale or contradictory |

2. **Name the receiver precisely**, with their starting knowledge and their accept authority. "The team" cannot accept; a named person can. An agent receiver has no ability to ask a colleague — that constraint changes every artifact requirement.

3. **Build the transfer inventory** across five kinds of asset. Handovers that cover only the first one leave the rest to be discovered during an incident:

   | Kind | Examples |
   |------|----------|
   | **Code and repository** | source, branches, tags, build and release pipelines, package registries |
   | **Running system** | environments, infrastructure, databases, queues, DNS, certificates, domains |
   | **Access and identity** | cloud accounts, owner/admin roles, service accounts, CI secrets, third-party consoles, billing |
   | **Obligations** | on-call, SLAs, contracts, vendor agreements, licences, compliance commitments, security disclosures |
   | **Knowledge and state** | architecture, decisions and their reasons, known defects, open work, risk register, roadmaps, relationships |

4. **State what is not transferring**, explicitly. Repository forks that stay behind, environments being decommissioned, personal accounts, historical incidents outside retention, contracts that end. Ambiguity here becomes the receiver's problem in month two.

5. **Convert the inventory into acceptance criteria** — observable statements the receiver can check, phrased as capability rather than document existence: "the receiver can restore the staging database from backup without assistance", "the receiver holds owner on the cloud account", "an alert fired at 02:00 reaches a named responder". Documents are means; capability is the criterion.

6. **Set the date structure**: the effective date, the freeze window (no changes except by agreement), the cutover moment for authority, and the sender's availability window afterwards (a named end date, not an open-ended "reachable whenever").

7. **Fix the dispute and rollback path.** If the receiver cannot accept by the date, who decides — delay, partial handover, or escalate? A handover with no failure path becomes a handover that "happened" while nothing transferred.

8. **Write `HANDOVER_SCOPE.md`:** type, parties, inventory table with owners, non-transferring list, acceptance criteria, dates, authority cutover, post-handover support terms, and the failure path.

## 5. Decision rules and evidence standard

- **Capability is the acceptance unit**, not document delivery. A folder of documents proves nothing.
- **Name a person who can accept**, and a person who can refuse. "The team" is not a receiver.
- **An agent receiver requires everything written down**, including permission boundaries; if that is not available, the handover is not ready and P02 will show why.
- **Obligations transfer even when nobody remembers them.** Check contracts, SLAs, and on-call before declaring the inventory complete.
- **The sender's support window has an end date.** Open-ended availability means the handover never completed.
- **Scope creep is death**: transferring "everything the leaver did" produces an unfinishable list; transfer the named system and state the rest as out of scope with an owner.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Handover type classified | document | one of the five, with the trigger |
| Receiver named with authority | inspect | person/role and accept authority |
| Inventory covers all five kinds | table | no kind omitted without reason |
| Non-transferring list explicit | inspect | each exclusion has an owner |
| Acceptance criteria observable | read-through | capability, not document presence |
| Dates and cutover set | inspect | effective date, authority moment |
| Support window bounded | inspect | end date |
| Failure path stated | inspect | escalate/defer decision recorded |

## 7. Failure handling

- **No receiver identified** → stop at scope and record the gap; the work becomes continuity documentation, which is a different deliverable and should be labelled as such.
- **The receiver lacks the authority to accept** (no budget, no mandate) → escalate to the approver; a handover to someone who cannot decide is a delay with extra steps.
- **The scope is a whole job, not a system** → force a boundary: list the systems and pick what can actually transfer by the date; delegate the rest explicitly.
- **The sender is already unavailable** (left, contract ended) → switch to `02-engineering/project-recovery/`; recovery reconstructs state without a counterpart.
- **Legal or regulatory constraint blocks a transfer** (data residency, contract assignment) → record it as a blocking dependency with the owner and date; do not proceed to P03.

## 8. Security and authorisation

Risk class A: scoping only. Record that access exists and who owns it — never a credential value. Where the handover crosses an organisational or legal boundary, data transfer and account ownership must be confirmed by the approver before P03, not during it. A handover is also an authorisation event: the receiver's access should be least-privilege for their role, not a copy of the sender's accumulated permissions.

## 9. Completion criteria

- [ ] Handover type and trigger recorded.
- [ ] Receiver named, with starting knowledge and accept authority.
- [ ] Inventory covers code, running system, access, obligations, knowledge.
- [ ] Non-transferring items listed with owners.
- [ ] Acceptance criteria written as observable capabilities.
- [ ] Dates, authority cutover, and bounded support window set.
- [ ] Failure path and escalation recorded.

## 10. Deliverables and handover

Artifact: `HANDOVER_SCOPE.md`.

P02 receives: the inventory, to capture the truth of each asset. P03 receives: the access list, to plan the transfer and the revocation of the sender's standing access.
