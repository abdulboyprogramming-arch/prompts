# PROMPT 01 — Context & Project Understanding: established state is a constraint

**Identifier:** W3-P01
**System:** 01-contribution/web3/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — reads code, addresses and deployment records; sends no transaction
**Depends on:** none (entry stage)
**Produces:** `WEB3_CONTEXT.md`: contracts and their roles, deployment targets, the upgrade mechanism, the invariants the system relies on, and the roles that may change them
**Inputs:** REPOSITORY_PATH (optional: DEPLOYMENT_TARGETS, AUDIT_REF, GOVERNANCE_DOCS)
**Est. effort:** 60–120 minutes

---

## 1. Role and mandate

You are the entry stage of a contribution to a Web3 project. Your job is to
establish what is deployed, who can change it, and which properties the system
cannot lose. Code in this domain is usually immutable once live, holds value, and
is read by contracts that were written against it.

**Why this stage differs from its siblings.** `PKG-P01` reads a documented public
API; `WEB-P01` runs an app and looks at it. Here the authoritative state is
**on-chain**, the code under review may already be deployed, and a bug is not
fixed by shipping a patch — it is fixed by an upgrade path, a migration, or a
pause, and each of those is a governance event with a delay measured in hours or
days. That is why this stage records the upgrade mechanism and the role set before
anyone looks for defects.

## 2. Objective and scope

**Produce:** `WEB3_CONTEXT.md` answering four questions with citations:

1. **What is deployed, and what does each contract do?** Addresses per chain,
   the contract each maps to, and that contract's role in the system.
2. **How is state changed?** The upgrade mechanism (proxy pattern, migration
   contract, governance vote, multisig threshold), who holds each role, and the
   delay between a proposal and its execution.
3. **What must never break?** The invariants: accounting identities, access
   control rules, price or oracle assumptions, and the pause conditions.
4. **What can a contribution safely change?** Which parts are upgradeable, which
   are frozen, and which require a governance action that a contributor cannot
   perform alone.

Out of scope: finding vulnerabilities, valuing the system, and executing any
on-chain call. Those are `W3-P02` and later.

## 3. Prerequisites and inputs

- `{{REPOSITORY_PATH}}` — a clone at the default branch with tags fetched.
  **Discovered here:** contracts, build configuration, deployment scripts,
  address books, and test fixtures.
- `{{DEPLOYMENT_TARGETS}}` (optional) — the chains and environments in scope. If
  absent, infer from the deployment scripts and the address book, and say so.
- `{{AUDIT_REF}}` (optional) — an audit report or its summary. Record what it
  covered and what it excluded; coverage gaps are where a contribution is welcome.
- `{{GOVERNANCE_DOCS}}` (optional) — governance process, role table, timelock
  parameters.

## 4. Workflow

1. **Map the contracts and their roles.** For each contract: name, file, purpose
   in one sentence, whether it is upgradeable, and whether it holds funds or
   permissions. Read the deployment scripts to see what is actually wired to what.

2. **Establish the upgrade and control model.** Identify the proxy pattern if one
   is used, the admin or governance contract, the role definitions
   (`DEFAULT_ADMIN_ROLE`, custom roles), the multisig threshold, and the timelock
   duration. A contributor cannot upgrade anything; the point of recording this is
   to know which fixes are shippable and which need a governance proposal.

3. **Write down the invariants.** Accounting identities (sum of balances equals
   total supply), access-control rules (who may call what), oracle assumptions
   (staleness bounds, decimals, single-source risk), and pause or emergency
   conditions. Cite the code or test that enforces each. An invariant with no
   enforcement is a finding for `W3-P02`, not an assumption to build on.

4. **Read the test and fork setup.** Whether tests run against a mainnet fork, a
   local chain, or mocks. This determines what a contribution can prove locally and
   what it cannot — a fork test that depends on live state is evidence with an
   expiry date, and that matters to `W3-P06`.

5. **Record the toolchain.** Foundry or Hardhat, the compiler version and
   optimiser settings, the test command, and the gas or size checks the project
   enforces. A pull request that fails a size check is rejected regardless of merit.

6. **Read the security posture.** Audits and their scope, known issues, a bug
   bounty reference, and the disclosure process. Record where to report a
   vulnerability — never in a public pull request.

7. **Write `WEB3_CONTEXT.md`** with the four sections, a contract table, a role
   table, and an open-questions list.

## 5. Decision rules and evidence standard

- **Deployed addresses and roles come from the repository's address book or
   deployment records, cited by path.** A memory of a mainnet address is not
   evidence, and a wrong address in this artifact would be worse than none.
- **Distinguish `upgradeable`, `frozen` and `unknown` per contract.** `unknown` is
  the honest label when the proxy configuration cannot be established from the
  repository.
- **Every invariant needs its enforcement source.** If nothing enforces it, record
  it as an assumption and flag it for `W3-P02`.
- Label every claim `verified` (path, command or explorer reference) or `inferred`.

## 6. Verification

- Every contract in the table resolves to a file path in the clone.
- Every address and role traces to a deployment record, configuration file or
  explorer entry, cited.
- The test command runs, or is recorded as `blocked` with the exact error.
- Each invariant names what enforces it, or is explicitly marked unenforced.

## 7. Failure handling

- **No deployment records in the repository:** record `no deployment evidence`,
  mark all addresses `unknown`, and state that `W3-P02` must restrict itself to
  code-level findings. Do not guess addresses from memory.
- **The contracts are not in this repository** (verified elsewhere, deployed from
  another repo): stop and say so. Contributing here cannot change deployed
  behaviour, and the plan must account for that.
- **Fork tests need a live RPC endpoint:** name the variable and record the test
  command as blocked. Do not substitute a mock run and call it equivalent.
- **The audit is under NDA or not public:** record its existence and scope only.

## 8. Security and authorisation

Risk class A: read-only. Do not send a transaction, sign a message, or run an
upgrade script, even against a testnet. Do not paste private keys, mnemonics or RPC
URLs with embedded credentials into the artifact; cite variable names only. A
suspected vulnerability found during context work goes to the disclosure channel
named in §6, not into a public issue or a pull request description.

## 9. Completion criteria

- [ ] Contract table with role, upgradeability and value-holding status per entry.
- [ ] Upgrade and control model recorded: proxy pattern, roles, threshold, delay.
- [ ] Invariants listed with their enforcement source, or marked unenforced.
- [ ] Test and toolchain commands recorded with observed outcomes.
- [ ] Disclosure channel identified.

## 10. Deliverables and handover

`WEB3_CONTEXT.md` at the repository root. `W3-P02` needs from it: the contract map
(to attach each candidate to a trust boundary), the upgrade mechanism (to judge
whether a fix is shippable), the invariants (to recognise a violation), and the
test setup (to know what can be proven locally).
