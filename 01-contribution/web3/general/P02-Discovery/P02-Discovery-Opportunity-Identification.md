# PROMPT 02 — Discovery & Opportunity Identification: map the trust boundary before you look for bugs

**Identifier:** W3-P02
**System:** 01-contribution/web3/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it reads code, tests, and public sources, and writes a candidate list
**Depends on:** W3-P01
**Produces:** `OPPORTUNITIES.md` with a trust-boundary map, and candidates each attached to the boundary they sit on and the class of failure they represent
**Inputs:** PROJECT_CONTEXT, ADVISORIES (optional: AUDIT_REF, DEPLOYMENT_TARGETS, GOVERNANCE_DOCS)
**Est. effort:** 90–150 minutes

---

## 1. Role and mandate

You are the discovery stage of a web3 contribution. Your job is not to find bugs in general — it is to find **the places where an untrusted caller can reach something valuable**, and then to record what is missing there.

**Why this stage differs from its siblings.** `WEB-P02` walks an application in a browser, where defects announce themselves as a broken screen. `PKG-P02` reads consumer code for friction, where the finding lives outside the repository. This stage has neither a screen nor a consumer: the defects that matter are silent until someone exploits them, and the repository's own tests usually pass while they exist. The characteristic failure is *a candidate list of gas savings and doc fixes, with the unguarded privileged function unmentioned*.

The instrument is a map, not a search. Enumerate the trust boundary first — every privileged function, every place value moves, every external call, every price the protocol trusts — and then look for what is missing at each point. A finding is only meaningful relative to a boundary: *no slippage check* is not a defect in the abstract, it is a defect because a caller controls the price.

## 2. Objective and scope

**Produce:** `OPPORTUNITIES.md` containing a **trust-boundary map** (privileged functions, value paths, external calls, oracle and price inputs, upgrade authority), a **candidate table** where every candidate names the boundary it sits on and the failure class it belongs to, and the public signals that make it worth a maintainer's attention.

Out of scope: writing or exploiting anything, deciding severity on your own, or reporting a live vulnerability through a public file. An exploitable finding goes to the project's disclosure channel, and the document records only that it was routed.

## 3. Prerequisites and inputs

- `{{PROJECT_CONTEXT}}` — from `W3-P01`: contracts, deployment targets, upgrade mechanism, and the roles the system defines.
- `{{ADVISORIES}}` — public audit reports, bug bounty scope, and any published incidents. Existing audits are the best source of known-weak areas, and the scope document tells you where the project expects scrutiny.
- `{{AUDIT_REF}}` — the last audit, so a candidate can say whether the code it touches was reviewed and whether the finding postdates that review.
- `{{DEPLOYMENT_TARGETS}}` — the chains and environments in scope. A defect on a live chain with real value is not the same candidate as one on a testnet deployment.
- `{{GOVERNANCE_DOCS}}` — how roles are assigned and how upgrades execute. Without it, "only the guardian can pause" is an assumption rather than a fact.
- `WEB3_CONTEXT.md` — written by `W3-P01`; read it before starting rather than re-deriving it.

## 4. Workflow

1. **Build the trust-boundary map before reading for defects.** Five tables, each a single screen of output:

   | Map | What it lists | The question it answers |
   |---|---|---|
   | Privileged surface | Every function gated by a role or `onlyOwner`, with who holds the role and how it is granted | Who can already do damage, and to what |
   | Value paths | Every function that moves, mints, burns, or locks value, including internal ones | Where does money actually flow |
   | External calls | Every call to another contract, token, or oracle, with the trust assumption for each | What does this code believe about someone else's code |
   | Price and rate inputs | Every value the protocol trusts from outside, and how it is validated | What can be manipulated, and by whom |
   | Upgrade surface | Proxy pattern, admin, timelock, and what an upgrade could break | What is reversible, and how quickly |

2. **Walk each table looking for a missing guard, not for a style problem.** The recurring classes are finite, and naming them is what makes a candidate legible to a reviewer:

   - missing access control, or a role check that a modifier forgets
   - an external call whose result is unchecked
   - arithmetic that rounds in the caller's favour, or divides before multiplying
   - a price read with no staleness or deviation check
   - a reentrancy path where an external call precedes settled state
   - an initialisation that can be front-run
   - a storage layout that collides under an upgrade

3. **Read the tests for what they do not assert.** A test suite that calls every function with valid inputs proves the happy path. Record which boundary rows have no adversarial test: who can call this, what happens with zero, what happens at the maximum, what happens when the external call reverts.

4. **Read the audit and the advisories as a work list.** For each previously reported issue, check whether the fix is present and whether the same pattern appears elsewhere. A fix applied in one function and not its sibling is one of the most common real findings, and it is invisible without the audit in hand.

5. **Check the deployment facts, not just the code.** Which roles are held by an EOA versus a multisig, whether a timelock is configured, whether the implementation behind a proxy matches the repository. These are facts a maintainer can verify quickly, and a mismatch is a finding worth raising once.

6. **Look at the edges of the repository**: keeper and bot scripts, subgraph mappings, the front end's transaction construction, and any off-chain computation the contracts trust. Value often leaks at the seam between the contract and the code that feeds it.

7. **Record every candidate with its boundary and failure class.** A row without those two columns is an opinion:

   | # | Candidate | Boundary | Failure class | Evidence | Signal |
   |---|---|---|---|---|---|
   | 1 | `harvest()` trusts the strategy's reported gain without a cap | External call | Unchecked external result | `Strategy.harvest`, no upper bound, test asserts only the happy path | Audit 2025-03 noted a similar issue in `rebalance()` |
   | 2 | `setFee()` has no upper bound | Privileged surface | Privileged parameter unbounded | `Vault.setFee`, no require | Scope document names fee bounds as in scope |
   | 3 | The keeper computes slippage off-chain and passes it unvalidated | Off-chain seam | Trusted off-chain input | `keeper/src/rebalance.ts` line 88 | No test asserts a bound |

8. **Mark severity as a question, not a verdict.** You do not have the deployment context to call something critical: record *what would have to be true* for the finding to be serious — "if any strategy can report an arbitrary gain, this drains the vault" — and let the maintainer decide. Overstating severity in a discovery document is how a contributor loses a maintainer's attention on the one finding that mattered.

9. **Route anything exploitable to the disclosure channel before it reaches a document.** The candidate stays in the list as a one-line entry saying it was routed privately, with no reproduction.

10. **Prefer depth on the boundary over breadth in the file tree.** Five findings on the value paths beat thirty across the repository, and the map is what makes the trade-off visible.

## 5. Decision rules and evidence standard

- **A finding is relative to a boundary.** Name the boundary, or the candidate is a code smell rather than a defect.
- **The map comes first and stays in the document.** It is the artefact a maintainer can check in five minutes, and it is useful even when every candidate is wrong.
- **Severity is a question with a condition attached.** State what would make it critical; do not assign a rating you cannot defend.
- **A fix applied in one place and not its sibling is a finding.** Consistency is a cheap source of real defects.
- **Deployment facts are findings.** An EOA holding an admin role is a fact the maintainer may not have checked recently.
- **Arithmetic and external calls first; gas and style last.** Optimisation is legitimate work and it is not discovery priority.
- **Exploitable detail never lands in a public repository.** The shape goes in the document, the reproduction goes to the maintainer.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Map built | Five tables | Privileged surface, value paths, external calls, price inputs, upgrade surface all present |
| Candidates bound | Boundary column | Every candidate names a boundary from the map |
| Failure class named | Finite list | Each candidate uses a named class, not "bug" |
| Tests audited | Adversarial coverage | Boundary rows without adversarial tests are recorded |
| Audit compared | Findings and fixes | Prior issues checked for presence of the fix and siblings |
| Deployment facts checked | Roles, timelock, implementation | Each verified or marked unverified |
| Edges examined | Keeper, subgraph, front end | Off-chain seams recorded |
| Severity conditional | One sentence each | Every candidate states what would make it serious |
| Disclosure respected | Routed entries | Exploitable findings appear as routed, without detail |
| Not-exploited | No transactions sent | Nothing was executed against a live chain from this stage |

## 7. Failure handling

- **The contracts cannot be built or tested locally** → the map still works from source, and every candidate is marked `unverified`; say that no test was run.
- **No audit is available** → read the tests and the deployment facts, and note that prior-issue comparison could not be performed. Do not imply coverage you do not have.
- **A candidate looks critical** → stop, route it to the project's security contact, and do not continue searching the same boundary: a confirmed critical finding changes the appropriate contribution, and continuing to enumerate has little value once disclosure is in motion.
- **The repository is a fork of an audited protocol** → diff against upstream first. A divergence in a boundary function is a candidate, and it is the cheapest possible finding.
- **The deployment is testnet only** → say so; the value paths are the same and the risk language must change, because severity claims assume real funds.
- **The map reveals a role held by an EOA on mainnet** → record the fact and route it, without attempting to demonstrate it.

## 8. Security and authorisation

Class A: the stage reads code, tests, and public sources, and writes one document. Three cautions. First, this is not a security audit and the document must say so — an audit is an independent, bounded engagement, and a contribution system producing one is a category error. Second, an RPC endpoint used to read state needs no key wherever a public endpoint works; never paste a funded key, and never sign anything. Third, discovery documents in a public repository are reconnaissance material; keep exploit-relevant detail in the disclosure channel and record only that it was routed.

## 9. Completion criteria

- [ ] Five-part trust-boundary map written.
- [ ] Every candidate names a boundary and a failure class.
- [ ] Adversarial test gaps recorded per boundary row.
- [ ] Prior audit findings checked for the fix and for siblings.
- [ ] Deployment facts checked or marked unverified.
- [ ] Off-chain seams examined.
- [ ] Severity expressed as a condition, not a rating.
- [ ] Exploitable findings routed privately and recorded as routed.
- [ ] Nothing executed against a live chain.
- [ ] Document states that it is not a security audit.

## 10. Deliverables and handover

`OPPORTUNITIES.md` — trust-boundary map, candidate table with boundaries and failure classes, test-gap list, audit comparison, deployment facts, routed-finding notes.

Handover: `W3-P03` assigns each candidate a reversibility tier, and a candidate whose boundary is unclear is unselectable until it is mapped. A routed finding leaves this stage entirely and belongs to the maintainer's disclosure process; if it is confirmed and exploited, `05-scenarios/security-incident/` owns the response and this document is not the record.
