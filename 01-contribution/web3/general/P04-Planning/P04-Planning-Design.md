# PROMPT 04 — Planning & Design: plan the deployment before you plan the diff

**Identifier:** W3-P04
**System:** 01-contribution/web3/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — it writes a plan; it changes no contract and executes nothing
**Depends on:** W3-P03
**Produces:** `PLAN.md` with the storage-layout decision, the invariant-to-test map, the deployment sequence including what happens if it stops halfway, and the approval path the tier requires
**Inputs:** SELECTED_WORK, TIER (optional: STORAGE_LAYOUT, DEPLOYMENT_TARGETS, AUDIT_REF)
**Est. effort:** 45–90 minutes

---

## 1. Role and mandate

You are the planning stage of a web3 contribution. `W3-P03` selected a candidate and assigned its tier; your job is to design the change so that its irreversible parts are decided here, in a document, rather than during implementation or — worse — during an upgrade.

**Why this stage differs from its siblings.** `WEB-P04` plans a rendered change and its centre is a state-by-breakpoint matrix. `PKG-P04` plans a surface delta and its centre is the release choreography. This stage's centre is the **deployment sequence and the storage layout**, because those are the two things that cannot be fixed afterwards. The characteristic failure is *a thorough plan for the code with one line for the upgrade.*

The asymmetry that shapes every decision: a bug in a web or library change is fixed by a follow-up release; a storage collision or a mis-ordered upgrade is fixed by a migration nobody has written, on a protocol that may be handling funds while it is fixed.

## 2. Objective and scope

**Produce:** `PLAN.md` with the changed contracts and functions, the storage decision (append-only, with the slot diff expected), the invariants mapped to the test that will prove each, the deployment sequence with checkpoints and a halt condition per step, the approval path the tier requires, and the audit consequence.

Out of scope: writing code, executing a deployment, deciding governance, or changing the tier. If the design needs more risk than the tier allows, the plan stops and says so.

## 3. Prerequisites and inputs

- `{{SELECTED_WORK}}` — from `W3-P03`: the candidate, its tier, the invariants with violating cases, and the preconditions that must hold before implementation.
- `{{TIER}}` — the reversibility tier. It bounds what the plan may propose; a plan that needs a tier 3 action for a tier 1 candidate is a selection finding.
- `{{STORAGE_LAYOUT}}` — the deployed layout from the artefact or the explorer. Planning a storage change against source alone misses what has already shipped.
- `{{DEPLOYMENT_TARGETS}}` — the chains and environments, their proxy pattern, and their upgrade delay.
- `{{AUDIT_REF}}` — the last audit and the scope it covered, so the plan can state what the change invalidates.

## 4. Workflow

1. **Start with the deployment shape, not the code.** Proxy or immutable; who holds the admin; what the timelock delay is; what an upgrade requires operationally. Write it as a short sequence before planning a single function, because the sequence constrains the code — an implementation that needs an atomic multi-contract upgrade is a different design from one that ships in a single call.

2. **Decide the storage question explicitly, and write "no change" when that is the answer.** If a variable is needed, plan it at the end of the layout, with the expected slot diff and the upgrade that carries it. If none is needed, say so in one line: the reviewer's first question is whether the layout moved, and the answer should not be inferred from silence.

3. **Map every invariant to the test that will prove it.** One row per invariant from `W3-P03`, with the violating case, the test layer (unit, fuzz, fork, integration), and what a failure looks like. This table is the plan's contract with `W3-P06`.

4. **Plan the tests by layer, and pick the cheapest layer that can fail.** Unit tests for arithmetic; fuzz properties for invariants over arbitrary sequences; fork tests for integration with deployed contracts at a pinned block; integration tests for the off-chain seam. A property the unit layer cannot express belongs in fuzz, and a fork test is for state, not for logic.

5. **Write the sequence with a checkpoint after each step and a halt condition for each checkpoint.** *Deploy implementation → verify bytecode matches the repository → upgrade proxy → verify storage reads unchanged → enable the guarded function.* Each step names what is checked and what happens if the check fails. A sequence without checkpoints is a single irreversible step with extra lines.

6. **State the halt condition at the point of irreversibility.** If the upgrade executes and the verification fails, what is the response — a second upgrade, a pause, an incident? The plan answers before it is needed, because the answer at 3 a.m. is worse.

7. **Name the approval path the tier requires, and who holds the keys.** Tier 2 needs the maintainer and the multisig threshold; tier 3 needs the governance process and its delay. The plan states it as a sequence, not as "the maintainer will handle it".

8. **State the audit consequence.** Which audited files this touches, which findings could be affected, whether a re-audit precedes the upgrade. A plan that quietly invalidates an audit is a plan that will meet an auditor's objection late.

9. **Plan for the code being reviewed but not deployed.** Contributor-submitted code often lands weeks before an upgrade. The plan should say what is true in the meantime: a guarded function disabled, a new implementation unpointed, a migration unstarted. This is the most common real state of a web3 contribution, and the plan should describe it rather than the deployment that may never happen.

10. **List what would make you abandon the plan.** A storage collision discovered during implementation, an oracle that changes its interface, a maintainer decision against the mechanism. Each with the response.

11. **Keep the plan to one contract family.** A change that spans a vault and a strategy is two plans with an interface between them, and the interface is where the risk concentrates.

## 5. Decision rules and evidence standard

- **Deployment sequence first, diff second.** The mechanism decides what the code may do; planning the reverse produces a design that cannot be shipped.
- **Storage: append or nothing.** Any plan that reorders, resizes, or repurposes a slot is not a plan, it is a migration with a missing chapter.
- **Every invariant has a test, and the test has a layer.** An invariant without a layer is a wish.
- **Every irreversible step has a checkpoint and a halt condition.** Stated in the plan, before it is needed.
- **The tier bounds the plan.** If the design needs more risk, the plan returns to selection rather than escalating quietly.
- **The audit is part of the plan.** A change inside audited code has a review cost the maintainer must price before approving.
- **Plan the review-only state.** Most contributions land without a deployment, and the plan should say what that state looks like.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Deployment shape first | First section | Proxy, admin, delay, and mechanism stated before the code plan |
| Storage decision | One paragraph | "No change" written, or the append and its slot diff planned |
| Invariant map | One row per invariant | Violating case, test layer, and failure signature each |
| Test layers chosen | Cheapest that can fail | No property asserted only at a layer that cannot detect it |
| Sequence with checkpoints | Ordered steps | Each step names its check and its halt response |
| Irreversibility halt | Written at the step | The response if verification fails after execution |
| Approval path | Tier-appropriate | Who approves, in what order, with what delay |
| Audit consequence | Files and findings | Re-audit requirement stated, not implied |
| Review-only state | One paragraph | What is true while the code is merged but not deployed |
| Abandonment triggers | Two or three | Trigger and response for each |

## 7. Failure handling

- **The design needs a storage change for a tier 1 candidate** → the tier was wrong or the design is. Return to `W3-P03` and re-tier before planning further.
- **Two contracts must upgrade atomically** → the plan says so in the deployment section and names the ordering risk; an atomic pair is a tier 3 plan whatever the individual diffs look like.
- **No timelock exists** → every change is effectively irreversible. The plan states it plainly and the approval path becomes a human decision with no undo.
- **The invariant cannot be tested at any available layer** → mark it unproven, name what would test it, and let `W3-P06` report the gap rather than asserting the property in prose.
- **A dependency's interface may change** (oracle, router, token) → plan the check that would detect it at deploy time and the fallback behaviour, because a fork test at a pinned block cannot see a future upgrade.
- **The maintainer wants a different mechanism** → the plan is rewritten, not annotated. A plan with two mechanisms is one nobody will implement.

## 8. Security and authorisation

Class A: the stage writes a plan. Three cautions. First, a deployment plan is sensitive operational detail — if the repository is public, do not include key-holder identities, internal timelock procedures, or anything that maps an upgrade to a window an attacker could time. Second, reading deployment state requires an RPC endpoint; use a public one, and never place a key in the document. Third, the plan must not read as an audit: it plans a change and states its audit consequence, and an independent review remains a separate instrument.

## 9. Completion criteria

- [ ] Deployment shape written before the code plan.
- [ ] Storage decision explicit, including "no change".
- [ ] Every invariant mapped to a test and a layer.
- [ ] Deployment sequence with checkpoints and halt conditions.
- [ ] Response written for a failed post-execution check.
- [ ] Approval path stated for the tier, with delay.
- [ ] Audit consequence stated.
- [ ] Review-only state described.
- [ ] Abandonment triggers listed with responses.
- [ ] Plan confined to one contract family, or the interface between two is planned.

## 10. Deliverables and handover

`PLAN.md` — deployment shape, storage decision, invariant map, test layers, sequenced steps with checkpoints, halt conditions, approval path, audit consequence, review-only state, abandonment triggers.

Handover: `W3-P05` implements to the invariant map and annotates each touched function; if the implementation needs a storage change the plan did not allow, it returns here. `W3-P06` executes the invariant map and the fork checks. `W3-P07` takes the tier, the undo path, and the worst outcome from this plan for its four-fact header — which is why those three must be written here, not discovered at review.
