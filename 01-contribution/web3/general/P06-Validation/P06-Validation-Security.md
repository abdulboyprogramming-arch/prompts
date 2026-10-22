# PROMPT 06 — Validation & Security: prove the invariants, not the test suite

**Identifier:** W3-P06
**System:** 01-contribution/web3/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it runs checks and writes a report; it does not deploy or sign anything
**Depends on:** W3-P05
**Produces:** `VALIDATION.md` with the invariant list, the access-control matrix, the value-flow review, and an explicit confidence statement
**Inputs:** CHANGE_SCOPE, INVARIANTS (optional: CHAIN_AND_FORK_BLOCK, AUDIT_TOOLS, VALUE_AT_RISK)
**Est. effort:** 1–2 hours

---

## 1. Role and mandate

You are the validation stage for a web3 contribution. The implementation is done; your job is to decide whether it is safe, and to say so in a form a reviewer can check.

**Why this stage differs from its siblings.** `WEB-P06` proves a change works across rendering engines; `PKG-P06` proves an interface did not break. Here the failure is **irreversible and adversarial**. A passing test suite proves the cases the author thought of; the state can be changed by anyone, at any time, and cannot be rolled back. So the unit of evidence is not "tests pass" but "these invariants hold, and here is what happens when someone tries to break them".

What convinces a maintainer of a web3 change: an invariant written before the test, a failing case that shows the invariant can be violated, the access-control matrix for every external function, and a fork test at a pinned block. Static analyser output is a lead, not a verdict.

## 2. Objective and scope

**Produce:** `VALIDATION.md` containing the invariant list with the test that proves each, the access-control matrix, the value-flow review, the analyser findings triaged, and a confidence statement with its reasons.

Out of scope: writing the exploit; deploying or upgrading a live contract; replacing a professional audit for value-bearing code.

## 3. Prerequisites and inputs

- `IMPLEMENTATION.md` from `W3-P05` — the invariant each touched function must keep, and the storage-layout diff.
- `{{CHANGE_SCOPE}}` — contracts, functions, and storage touched, from `W3-P03`. Validation without it is an unaudited diff.
- `{{INVARIANTS}}` — the properties that must remain true, from `W3-P04`. If this list is empty, the change is not ready to validate: an invariant discovered after the fix is usually the fix's own assumption.
- `{{CHAIN_AND_FORK_BLOCK}}` — the network and block number for fork tests, so a re-run reproduces the same state.
- `{{AUDIT_TOOLS}}` — the analysers the project already configures (Slither, Aderyn, Semgrep, `forge test`, `hardhat test`). Run the project's configuration, not a generic one.
- `{{VALUE_AT_RISK}}` — what the changed code can move. This decides how much validation is proportional.

## 4. Workflow

1. **Restate the invariants as testable statements before running anything.** "Total supply equals the sum of balances after every external call" is testable; "the token is safe" is not. Each invariant gets an identifier (`INV-1`) used by every later section.

2. **Run the project's own suite and analysers unmodified.** Record the command and its summary line. Analyser findings are triaged into three buckets: *real and in scope*, *real and pre-existing*, *tool noise with the reason*. An untriaged report is not a validation.

3. **Write the failing case for each invariant.** A test that only proves the happy path proves nothing about safety. For `INV-1`, add the call sequence that would violate it and assert the revert or the preserved property. An invariant with no violating case has unknown strength.

4. **Build the access-control matrix for every external function in scope.** Columns: function, who can call it, what state or value it changes, and the guard that enforces the answer. A row whose guard is "the frontend does not expose it" is a finding, not a guard.

5. **Trace the value flows.** For each path that moves funds or mints supply: who pays, who receives, what can make the path revert after value has left, and whether a partial state can be left behind. Record the reentrancy surface at each external call, not as a general warning but as a specific sequence.

6. **Run the fork test at `{{CHAIN_AND_FORK_BLOCK}}`.** Fork tests catch integration assumptions that unit tests cannot: an oracle that returns a different shape, a token with a transfer fee, a pool whose liquidity moved. Pin the block so the run is reproducible, and record it.

7. **Review the upgrade and storage path** whenever the change touches a proxy, a storage layout, or an initialiser. A storage-layout collision passes every test written against fresh state and corrupts a live deployment.

8. **Report gas as a budget, not a goal.** A change that costs more gas is acceptable if it buys safety; a change that reduces gas by removing a check is a regression. State the delta and the reason.

9. **Write the confidence statement last, and make it specific.** "High confidence for the transfer path; `INV-3` unproven because the invariant needs an oracle that does not exist on the fork" is a usable statement. "Looks good" is not.

## 5. Decision rules and evidence standard

- **Tests pass ≠ invariants hold.** The distinguishing evidence is a case that violates the invariant when the guard is removed.
- **A guard not enforced on-chain is not a guard.** Ownership checks, pause switches, and allowlists are code, not documentation.
- **Static analysers generate leads.** A clean run means the tools found nothing they know how to find.
- **Fork state is part of the evidence.** An unpinned fork test is not reproducible and therefore not evidence.
- **Unknown beats optimistic.** If `{{VALUE_AT_RISK}}` is high and confidence is low, say so plainly and stop the contribution rather than ship it with a caveat buried in section 9.
- **Never validate by reading only the diff.** A new function's safety depends on the functions around it, including the ones the diff does not touch.
- **Do not write an exploit that can be run against a live deployment.** The violating case stays in the test suite, against a fork or a local chain.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Invariants testable | `VALIDATION.md` | Each has an identifier and a statement that can fail |
| Violating case per invariant | Test suite | Each invariant has a case that would break it |
| Project checks ran | Commands recorded | Suite and analysers executed with their own config |
| Analyser findings triaged | Three buckets | Every finding classified with a reason |
| Access-control matrix complete | Table | Every in-scope external function, with its on-chain guard |
| Value flows traced | Review notes | Reentrancy surface named per external call |
| Fork test pinned | Run log | Network and block recorded; result reproducible |
| Upgrade path reviewed | Storage layout diff | No collision, or the risk stated |
| Gas delta reported | Run output | Number, with the safety trade-off named |
| Confidence specific | Confidence statement | Reasons per path, not an adjective |

## 7. Failure handling

- **No fork RPC available** → mark fork-dependent claims unverified, and say which integration assumptions therefore have no evidence. Do not substitute a mock and call it a fork test.
- **An invariant cannot be written as a test** → record it as an open risk with the reason, and treat it as a finding rather than a limitation of the tooling.
- **An analyser reports a critical finding you believe is noise** → state the reasoning explicitly. A reviewer must be able to disagree with you.
- **A pre-existing vulnerability is found outside scope** → stop the contribution, report it privately to the maintainer, and do not open a public PR that describes it. Coordinated disclosure applies (`05-scenarios/security-incident/`).
- **Confidence is low on a value-bearing change** → say so before the PR, not in it. A contribution that needs an audit should wait for one.
- **The change cannot be tested at all** (missing dependencies, contract fails to compile) → that is a blocked stage: report the failure and return to `W3-P05`.

## 8. Security and authorisation

Class A: the stage runs tests and writes a report. Three limits. Never point a test at a mainnet deployment with real value; use a fork or a local chain. Never publish a working exploit before the fix ships. Never paste key material, RPC credentials, or mnemonic fragments into the report, a chat window, or a PR description.

## 9. Completion criteria

- [ ] Invariants restated as testable statements with identifiers.
- [ ] A violating case exists for each invariant.
- [ ] Project suite and analysers run with their own configuration.
- [ ] Every analyser finding triaged into real-in-scope, real-pre-existing, or noise-with-reason.
- [ ] Access-control matrix covers every in-scope external function, with the on-chain guard.
- [ ] Value flows traced, with the reentrancy surface named per external call.
- [ ] Fork test executed at a recorded network and block.
- [ ] Upgrade and storage layout reviewed where the change touches a proxy.
- [ ] Gas delta reported with the safety trade-off stated.
- [ ] Confidence statement specific per path, with its reasons.

## 10. Deliverables and handover

`VALIDATION.md` — invariants and their tests, the access-control matrix, value-flow notes, triage of analyser findings, fork evidence, gas delta, confidence statement.

Handover: defects return to `W3-P05`; unresolved risks travel into `W3-P07` as a section the maintainer must read before approving, not a footnote. Value-bearing changes also route to `03-domains/web3/P04-Exploit/` readiness work and, where the project requires it, an external audit — this stage reduces what an auditor has to find, and does not replace one.
