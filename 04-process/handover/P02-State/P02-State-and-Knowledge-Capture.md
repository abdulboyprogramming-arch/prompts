# PROMPT 02 — State and Knowledge Capture

**Identifier:** HAND-P02
**System:** 04-process/handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** HAND-P01
**Produces:** `HANDOVER_STATE.md`
**Inputs:** REPO_PATH, TARGET_SERVICE (optional: TARGET_ENV, HANDOVER_RECEIVER)
**Est. effort:** 1–4 h

---

## 1. Role and mandate

You write down what is true about the system at the moment of transfer, in a form the receiver can act on without asking the sender. Everything that exists only in the sender's head or in a chat thread disappears at cutover.

The standard is unfashionable and effective: **a claim the receiver cannot verify is not captured state, it is folklore.** Each fact you record gets a pointer — a file, a command, a dashboard, a commit, a ticket.

## 2. Objective and scope

**Produce:** `HANDOVER_STATE.md` — what works and how that was proven, what is broken and what is at risk, open work with its exact position, decisions with their reasons, obligations, and the operational facts a responder needs at 3 a.m.

Out of scope: transferring access (P03), proving the receiver can operate it (P04).

## 3. Prerequisites and inputs

- `HANDOVER_SCOPE.md` (inventory, acceptance criteria) and the `{{TARGET_SERVICE}}` inventory it names.
- `{{REPO_PATH}}` read-only; `{{TARGET_ENV}}` for checking what is actually deployed.
- `{{HANDOVER_RECEIVER}}` — so the level of explanation matches their starting knowledge, and so you can test what they can follow.

## 4. Workflow

1. **Establish the system's shape in five sentences**: what it does, who depends on it, where it runs, how a change reaches production, and what breaks first when it fails. If any of the five cannot be answered, that is a finding, not a paragraph to skip.

2. **Separate proven from believed.** For each claimed capability (builds, tests, deploys, backs up, restores, alerts), record the evidence: the command and its output, the pipeline run, the dashboard. Anything unverified goes into a *believed, unverified* list — which is one of the most valuable sections in the document.

3. **Capture the running reality, not the intended one**: deployed version and commit per environment, configuration drift between them, scheduled jobs, queues, external integrations, certificates and their expiry, DNS, feature flags left in non-default states, and manual steps that only one person performs.

4. **Record open work at its exact position.** For each item: what it is, where it stopped (branch, PR, ticket, failing test), what the next action is, and how risky it is to leave. "In progress" with no pointer is a trap for the receiver.

5. **Record decisions with their reasons** — especially the ones that look wrong: why the retry is hand-rolled, why the schema has two sources of truth, why the deploy skips staging for hotfixes. A receiver who does not know the reason will "clean it up" and reintroduce the incident that produced it.

6. **Capture the obligations** from P01's inventory: on-call expectations, SLAs and their measurement, contracts and renewal dates, vendor accounts and their owners, compliance commitments, security contacts and disclosure terms.

7. **Write the operational brief** the receiver needs before their first incident: where the alerts go, what the top five alerts mean, who to escalate to, what the rollback procedure is, where the credentials live (never the values), and which actions are irreversible.

8. **Capture the risks and the debt honestly**, ranked: known defects, fragile areas, single points of failure, manual processes, security exceptions, and the things everyone knows but nobody fixed. Include the "if this breaks, we are in trouble because…" list.

9. **Structure it for the receiver's query, not the sender's chronology.** Sections by question: *What is this? What runs where? How do I change it? How do I know it is healthy? What do I do when it fails? What is unfinished? What is fragile? Who do I talk to?*

10. **Write `HANDOVER_STATE.md`** with pointers throughout, and a header stating the commit and date the state was captured — after which it is expected to drift.

## 5. Decision rules and evidence standard

- **Every fact gets a pointer.** File path, command, dashboard, ticket, commit. Without one, it is unverifiable.
- **Proven and believed are different lists.** Never merge them; the receiver's trust depends on the distinction.
- **Write the reason, not just the decision.** Undocumented rationale is what makes a successor undo a deliberate choice.
- **Deployed reality beats repository intention.** Capture what is running in each environment, including drift.
- **Never write a secret value.** Name the store, the account, and the owner.
- **State the staleness date.** A handover document is a snapshot; the receiver must know when it stops being authoritative.
- **If the receiver could not act on it alone, it is not captured** — test by asking them to follow a section.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Five-sentence shape present | inspect | all five answerable |
| Proven list evidenced | spot-check 3 claims | command or run shown |
| Unverified list present | inspect | honestly populated |
| Running reality captured | environment check | version per environment recorded |
| Open work has pointers | table | branch/PR/ticket per item |
| Decisions carry reasons | sample | non-obvious choices explained |
| Obligations captured | compare to P01 inventory | no gap |
| Operational brief usable | receiver dry-read | escalation and rollback clear |
| Staleness header | inspect | commit and date present |

## 7. Failure handling

- **The build or deploy cannot be run here** → record the exact command, where it is expected to run, and mark it *unverified*; state what evidence would settle it.
- **The sender is unavailable for questions** → reconstruct from `02-engineering/project-recovery/` and label every inference as such; do not present reconstruction as first-hand knowledge.
- **The system is too large for the time available** → capture the operational brief and the fragile list first (they prevent incidents), then the architecture, then the rest; state what was not captured.
- **Two sources of truth disagree** (docs vs deployed, two schemas) → record both and name the one that behaviour follows, confirmed by running both sides; the disagreement itself is a risk item.
- **A secret appears in a document or config** → do not copy it; record the location, notify the owner, and treat rotation as a P03 action.

## 8. Security and authorisation

Risk class B: reads systems and produces a document that concentrates knowledge. Treat the artifact as sensitive by default — it describes topology, accounts, and weaknesses. Do not include credentials, customer data, or exploit-relevant detail; where a risk is security-relevant, describe its class and route it to `02-engineering/security-hardening/` rather than publishing specifics. Do not change anything in the running system while capturing it.

## 9. Completion criteria

- [ ] Five-sentence system shape complete.
- [ ] Proven capabilities with evidence; believed-unverified list separate.
- [ ] Running reality per environment, including drift and flags.
- [ ] Open work at exact position with next action and risk of leaving it.
- [ ] Non-obvious decisions with reasons.
- [ ] Obligations compared against the P01 inventory with no gaps.
- [ ] Operational brief: alerts, escalation, rollback, irreversible actions.
- [ ] Risks and fragile areas ranked.
- [ ] Staleness header (commit, date) present.

## 10. Deliverables and handover

Artifact: `HANDOVER_STATE.md`.

P03 receives: the access references and secret locations, to transfer ownership and revoke the sender. P04 receives: the claims list — because the receiver's capability test is a test of this document as much as of the system.
