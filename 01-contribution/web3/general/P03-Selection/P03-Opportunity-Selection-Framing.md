# PROMPT 03 — Opportunity Selection & Framing: choose work whose failure someone else can undo

**Identifier:** W3-P03
**System:** 01-contribution/web3/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — it selects and writes a framing document; it sends no transaction
**Depends on:** W3-P02
**Produces:** `SELECTED_WORK.md` with the selected candidate, its reversibility tier, the preconditions that must hold before work starts, and the invariants the change must preserve
**Inputs:** OPPORTUNITIES, PROJECT_CONVENTIONS (optional: MAINTAINER_APPROVAL, DEPLOYMENT_TARGETS, AUDIT_REF)
**Est. effort:** 40–75 minutes

---

## 1. Role and mandate

You are the selection stage for a web3 contribution. `W3-P02` produced candidates; your job is to choose one and frame it so that the risk is decided **before** any code exists, not discovered at review.

**Why this stage differs from its siblings.** `WEB-P03` selects against what can be proven in a browser; `PKG-P03` selects against a public surface that becomes a promise. This stage selects against **irreversibility**. A deployed contract's storage layout, its access control, and its accounting are close to permanent: an upgrade may be possible, may require a timelock, may require a multisig, and may not exist at all. The characteristic failure is *submits a change to a value path, described as a small fix, that the maintainer would have declined had it been described as a change to the value path.*

The second asymmetry is time. In a web repository a wrong choice costs a day and a closed pull request; in a protocol a wrong choice at the wrong tier spends the maintainer's willingness to review contributions from strangers, and that is not recoverable by a follow-up commit.

## 2. Objective and scope

**Produce:** `SELECTED_WORK.md` naming one candidate, its **reversibility tier**, the preconditions that must hold before implementation begins, the invariants the change must preserve with the violating case that will test each, and the candidates rejected for tier or scope.

Out of scope: writing the change, deciding the upgrade mechanism, estimating the audit cost, or obtaining the maintainer's consent on the user's behalf. Selection names the tier and the approval it requires; it does not grant either.

## 3. Prerequisites and inputs

- `{{OPPORTUNITIES}}` — candidates from `W3-P02`, each with the evidence that it matters.
- `{{PROJECT_CONVENTIONS}}` — the contribution policy, the audit history, and any stated scope limits. Many protocols publish what they accept (tests, tooling, docs) and what they do not (unsolicited feature work), and that statement outranks your judgement about what is useful.
- `{{MAINTAINER_APPROVAL}}` — whether a maintainer has agreed to this class of change. For tier 2 and tier 3 candidates this input is a precondition, not a formality; absent it, the candidate is a proposal.
- `{{DEPLOYMENT_TARGETS}}` — the chains and environments the project deploys to. A change that must be deployed to a live chain has a different cost from one that cannot leave a fork.
- `{{AUDIT_REF}}` — the last audit, if one exists, so the change can be checked against what was reviewed rather than against what the code currently does.

## 4. Workflow

1. **Assign every candidate a reversibility tier before ranking anything.** The tier is a property of the code path, not of the size of the diff, and it is assigned by asking one question: *if this change is wrong and reaches a live deployment, who can undo it?*

   | Tier | What it covers | Who can undo it |
   |---|---|---|
   | **0 — Off-chain** | Tests, fuzzing harnesses, docs, scripts, indexers, front-end clients, monitoring | The author, with a revert |
   | **1 — Contract, no interface change** | Gas, comments, internal refactors, events added (never removed), test-only helpers | The maintainer, with an upgrade where one exists |
   | **2 — Interface or state** | ABI changes, storage layout, access control, oracle wiring, upgrade authority, accounting or fee logic | The timelock or multisig, at the next window, if the upgrade path is not itself broken |
   | **3 — Custody** | Anything that moves, holds, or authorises movement of user funds | Nobody, once executed against a live counterparty |

   A candidate that changes an ABI, a storage slot, a role, or a price is tier 2 even when the diff is four lines. Tier is set by the path the code executes on, not by the number of files.

2. **Apply the tier gate.** Tier 0 and tier 1 candidates may be selected on your judgement. Tier 2 and tier 3 candidates are selectable **only** when `{{MAINTAINER_APPROVAL}}` records that a maintainer asked for this change or accepted a proposal for it. Without it, write the proposal and pick a tier 0 candidate for actual work. This ordering is the whole point of the stage: the approval is cheap before code exists and expensive afterwards.

3. **Check the candidate against the project's stated scope.** If the contributing guide says the project wants tests and does not want feature work, a tier 0 test contribution is the correct selection even when the feature is more interesting. The strongest predictor of a merged contribution is that the repository asked for it.

4. **Prefer the lowest tier that answers the same problem.** For a reported bug in a payout calculation, a failing test that reproduces it is tier 0; the fix is tier 2. Selecting the test first produces a contribution the maintainer can merge immediately, and it hands them the evidence for their own decision about the fix.

5. **State the invariants the change must preserve, one sentence each, with the violating case.** An invariant is a property that must hold in every reachable state: *total shares equal the sum of balances at all times*, *only the guardian role can pause*, *a transfer never leaves a balance negative at any point in the call*. Each needs a case that would break it if the code were wrong. Invariants without violating cases are slogans.

6. **Name the preconditions that must hold before implementation starts.** For tier 2: the storage layout is read and diffed, the upgrade mechanism is identified, and the maintainer has confirmed the version. For tier 3: additionally, the accounting is documented with worked numbers and an independent reviewer is named. A precondition missing at this stage becomes an assumption discovered during validation.

7. **Establish where the change can be tested, and say what it cannot prove.** A fork pinned to a block reproduces state; it does not reproduce mempool conditions, oracle latency, or adversary behaviour. Name the gap in the document, because `W3-P06` will inherit it.

8. **Frame acceptance criteria as observable state transitions, not as features.** *Given a vault with two depositors and a share price of 1.0, a deposit of 100 tokens mints 100 shares and total assets equal 200* is checkable. *The deposit flow works* is not.

9. **Record rejected candidates with the tier or the scope rule that removed them.** A protocol maintainer reading the rejection list is checking whether you understood the risk model, and the list is where that shows.

## 5. Decision rules and evidence standard

- **Tier is decided by what can be undone, not by what the diff looks like.** A four-line change to a role check outranks a 600-line test suite in risk, and the ranking follows the undo question.
- **No approval, no tier 2 or 3 selection.** The stage does not infer consent from an old issue, a merged similar change, or a maintainer's general helpfulness.
- **The lowest tier that answers the problem wins.** Reproduce before fixing, document before changing, instrument before deploying.
- **An invariant without a violating case is unfinished.** If you cannot describe the state that breaks it, you have not identified the invariant.
- **A "small fix" that changes behaviour on a value path is a tier 2 change with a misleading name.** Rename it in the document before it reaches a reviewer who would have caught it.
- **Fork tests are evidence of code behaviour, not of protocol safety.** State the difference rather than letting a green fork run imply more than it proves.
- **A candidate whose scope cannot be stated without "and while we're in there" is two candidates.** Split it, and select the one that does not need an upgrade.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Tier assigned | Table in `SELECTED_WORK.md` | Every candidate carries tier 0–3 and the undo answer for its tier |
| Tier gate applied | Approval check | Tier 2 and 3 selections cite recorded maintainer approval; otherwise rejected |
| Scope rule checked | Contributing guide | The project's stated scope quoted, and the selection consistent with it |
| One selection | `SELECTED_WORK.md` | Exactly one primary candidate |
| Invariants stated | One sentence each | Each names a property that must hold in every reachable state |
| Violating cases | One per invariant | Each describes a state that would break it |
| Preconditions listed | Tier-dependent | Every precondition for the selected tier is present and unmet items are flagged |
| Test surface named | Fork, local chain, or unit | Where the change can run is stated, with what that environment cannot reproduce |
| Acceptance criteria | State transitions | Each names inputs, the resulting state, and the observable check |
| Rejections recorded | Framing document | Each losing candidate names the tier or scope rule that removed it |

## 7. Failure handling

- **Every candidate is tier 2 or higher and no approval exists** → the honest output is a proposal plus a tier 0 alternative. Do not select high-tier work on the theory that the maintainer will agree once they see it.
- **The maintainer approved a feature but not its implementation** → the tier is still 2. Approval of intent is not approval of a storage layout, and the layout question returns at `W3-P04`.
- **The project has no upgrade mechanism and no timelock** → every contract change is tier 3 by effect, whatever its intent. Say so; the document is more useful when it is more alarming.
- **A candidate's invariant cannot be written** → the candidate is not understood well enough to select. Return to `W3-P02` for a narrower one.
- **The reported bug is in code the project cannot change** (a dependency, a forked library, an immutable contract) → the contribution is the reproduction and the documentation of the limit, not a fix. Select that.
- **The candidate is a feature the project's own roadmap lists for a future version** → select something else. Competing with the maintainers' plan produces work that is reviewed slowly and merged never.

## 8. Security and authorisation

Class A: the stage reads code and writes one planning document. Three cautions specific to this domain. First, a fork test needs an RPC endpoint with a key; use a public or project-provided endpoint and never paste a funded key into a document or a chat window. Second, an invariant list and a tier assessment are not a security review, and the document must not read as one — an audit is a separate instrument with a separate scope. Third, selecting a tier 2 or 3 candidate without recorded approval is a social risk as much as a technical one; the gate in step 2 exists because the cost of asking is minutes and the cost of not asking is the maintainer's trust.

## 9. Completion criteria

- [ ] Reversibility tier assigned to every candidate, with the undo answer stated.
- [ ] Tier gate applied, with approval cited for tier 2 and tier 3.
- [ ] Project scope quoted and the selection checked against it.
- [ ] Exactly one candidate selected.
- [ ] Invariants written, one per line, each with a violating case.
- [ ] Preconditions for the selected tier listed, with unmet ones flagged.
- [ ] Test surface named, with what it cannot reproduce.
- [ ] Acceptance criteria written as observable state transitions.
- [ ] Rejected candidates recorded with the rule that removed them.
- [ ] The document states that it is not a security review.

## 10. Deliverables and handover

`SELECTED_WORK.md` — tier table with undo answers, approval record, scope check, the selected candidate, invariants with violating cases, preconditions, test surface and its limits, acceptance criteria, rejections.

Handover: `W3-P04` plans against the tier and the preconditions, and a plan that changes the storage layout after this document was written returns here first. `W3-P06` turns each invariant and violating case into a check, which is why they are written as properties rather than as risks. Any selection that needed approval before code needs the maintainer's name in the pull request; `W3-P07` carries it as the first paragraph so the reviewer sees the decision before the diff.
