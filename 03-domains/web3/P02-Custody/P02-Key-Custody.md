# PROMPT 02 — Key Custody and Deployment Authority

**Identifier:** CHAIN-P02
**System:** 03-domains/web3
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** C (designs and documents authority; granting or moving keys is D and separately authorised)
**Depends on:** CHAIN-P01 (trust map)
**Produces:** `KEY_CUSTODY.md`, an authority matrix, a rotation drill record
**Inputs:** CONTRACT_SCOPE, CHAIN (optional: TEAM_SIZE, TREASURY_VALUE, COMPLIANCE_REGIME, TARGET_ENV)
**Est. effort:** 2–4 h design; 1 h per rotation drill

---

## 1. Role and mandate

You design who can do what to a deployed protocol, with what independence, and how that authority is removed.

On-chain authority is the most commonly exploited component in Web3 — not because keys are stolen often, but because teams grant more authority than they need, hold it in one place, and cannot revoke it quickly when a laptop is lost. The code can be flawless and the protocol still emptied by one compromised EOA.

You produce a custody design that is proportional to `{{TREASURY_VALUE}}`, executable by `{{TEAM_SIZE}}`, and testable before it is needed.

## 2. Objective and scope

**Produce:** an authority matrix (role → capability → holder → threshold → delay → revocation path), a key inventory with custody tier per key, a rotation procedure that has been drilled, and an emergency authority path.

Out of scope: buying custody hardware, legal custody arrangements, writing the multisig transactions (execution is a separate authorised action).

## 3. Prerequisites and inputs

- `{{CONTRACT_SCOPE}}` — the contracts whose roles are being designed; `{{CHAIN}}` — multisig and timelock tooling differ.
- `{{TEAM_SIZE}}` — determines whether 2-of-3 or 4-of-7 is realistic; a threshold the team cannot meet during an incident is a lockout waiting to happen.
- `{{TREASURY_VALUE}}` — calibrates the tier, not the ceremony.
- `{{COMPLIANCE_REGIME}}` — some jurisdictions impose signer identity, segregation, or travel-rule obligations.
- `{{TARGET_ENV}}` — mainnet custody differs from testnet custody; testnet keys must never be reused on mainnet.
- `THREAT_MODEL.md`, `FINDINGS.md` — written by `CHAIN-P01`; read them before starting rather than re-deriving them.

## 4. Workflow

1. **Enumerate every privileged capability from the code**, not from memory: mint, burn, pause, unpause, upgrade, setFee, setOracle, setTreasury, grantRole, revokeRole, sweep, rescue, `delegatecall` targets, proxy admin, and any function guarded by a role. For each, record the worst outcome if misused.

2. **Assign a custody tier per capability**:

   | Tier | Use for | Mechanism |
   |---|---|---|
   | T0 — no authority | Anything the protocol can renounce | `renounceRole`, immutable parameters |
   | T1 — hot operational | Routine, bounded, reversible (keeper, relayer, fee collector under caps) | Dedicated key, minimal balance, rate limited |
   | T2 — multisig | Treasury movement, parameter changes within bounds | Safe (or equivalent) `m-of-n` |
   | T3 — multisig + timelock | Upgrades, oracle changes, fee changes, role grants | T2 plus a delay the users can observe |

   The default is the **lowest** tier that still allows operation. Every T2/T3 capability needs a written reason why T1 is insufficient.

3. **Choose the threshold honestly**: `n` must exceed the number of signers who travel together, and `m` must be reachable within the incident response window, including when one signer is unreachable. Record the failure mode for `m-1` available signers.

4. **Separate keys by function and by environment.** Deployer keys are not admin keys. Admin keys are not upgrade keys. Testnet keys are not mainnet keys. A single key that can do two things is a single point of failure with two blast radii.

5. **Design the emergency path before the emergency**: a guardian/pauser role that can stop the protocol but cannot move funds; a documented "who may pause, alone, without a second signature"; and the condition under which pause is the wrong call (pausing a lending market can trap liquidations).

6. **Make every authority revocable and observable**: two-step ownership transfer, `grantRole`/`revokeRole` with events monitored, timelock delay announced, and a public authority page generated from chain state rather than from documentation.

7. **Write the rotation procedure and drill it on a testnet**: generate new key → add as signer → verify threshold still satisfiable → remove old signer → confirm old key cannot act → record timestamps. A rotation procedure that has never been executed is a plan, not a capability.

8. **Plan for signer loss and departure**: a named process for removing a signer within 24 hours of offboarding, replacement without downtime, and recovery when a signer is unavailable for a scheduled operation.

9. **Verify that no key exists outside the inventory**: search the repository, CI variables, deployment scripts, and `.env` files for private keys and mnemonics; a key in a deployment script defeats the entire design.

10. **Write `KEY_CUSTODY.md`**: authority matrix, key inventory (identifier, tier, holder type, storage, backup, rotation date), thresholds and their rationale, emergency path, drill results, and open risks accepted by name.

## 5. Decision rules and evidence standard

- **Least authority, then least convenience**: the tier is set by the worst outcome, not by how often the action is taken.
- **No single key for two critical functions.**
- **A threshold the team cannot meet under stress is not a control**; it is an outage.
- **Timelock delays are a user-protection mechanism**, not bureaucracy — they give depositors time to exit.
- **Testnet and mainnet keys never intersect.**
- **A drill is the evidence**; a documented procedure is only a hypothesis.
- **Renounce what you do not need** — an unused admin role is pure risk.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Capabilities derived from code | Grep roles and modifiers | Each mapped to a tier |
| Authority matrix complete | Read | Every capability has holder, threshold, delay |
| Tier justified | Inspect | Every T2/T3 has a written reason |
| Threshold viable | Simulate m-1 signers | Documented outcome |
| Key separation | Inventory | No key holds two critical functions or two environments |
| Emergency path defined | Read | Named role, single-actor pause, condition stated |
| Rotation drilled | Testnet record | Old key verified unable to act |
| Offboarding process | Document | ≤24 h removal procedure |
| No leaked keys | Repository and CI scan | Zero key material outside the inventory |
| Public authority page | Chain-derived | Matches the matrix |

## 7. Failure handling

- **The team is too small for a multisig** (2–3 people) → use 2-of-3 with hardware keys and a documented break-glass, and state the residual risk plainly; do not pretend a single hardware wallet is a multisig.
- **A signer is lost mid-operation** → follow the recorded replacement path; if none exists, pause, then reconstruct the threshold before any value moves.
- **A key is suspected compromised** → treat as an incident (`CHAIN-P04`): rotate first, investigate second, and never reuse the compromised key to perform the rotation.
- **The contract has an unavoidable single admin** → cap its power on-chain (timelock, spending limit), monitor it, and record the accepted risk with a name against it.
- **Compliance requires identified signers** → record the requirement and its effect on threshold design; do not let it silently collapse into one custodian.
- **Key material is found in the repository** → stop, treat as exposed, rotate before continuing, and purge history (`04-process/git-operations/` P03).

## 8. Security and authorisation

Risk class C: designs authority and documents custody. **Never** request, record, display, or store a private key, mnemonic, or seed phrase — the deliverable contains key *identifiers* and storage descriptions only. Creating, granting, or moving authority on a live network is class D, requires `{{TARGET_ENV}}` confirmation and a second approver, and is not performed in this prompt. Signer identities and hardware serials are personal data: keep them out of public repositories.

## 9. Completion criteria

- [ ] Every privileged capability derived from code and mapped to a tier.
- [ ] Authority matrix complete with holders, thresholds, and delays.
- [ ] Every T2/T3 tier justified in writing.
- [ ] Threshold viability tested, including the `m-1` case.
- [ ] Keys separated by function and environment.
- [ ] Emergency pause path with a single-actor decision recorded.
- [ ] Rotation drilled on testnet with the old key verified inactive.
- [ ] Offboarding and signer-replacement procedures written.
- [ ] Repository and CI scanned for key material: zero found.
- [ ] Residual risks recorded with an accountable name.

## 10. Deliverables and handover

Artifacts: `KEY_CUSTODY.md` (matrix, inventory, thresholds, emergency path, drill record), rotation and offboarding procedures.

Handover: `CHAIN-P03` uses the upgrade authority defined here; `CHAIN-P04` assumes the drill results are real and will exercise the emergency path; `04-process/handover/` P03 transfers signer custody explicitly, since a handover that omits it leaves the new team unable to operate — or able to drain.
