# PROMPT 03 — Contract Upgrade and Storage Migration

**Identifier:** CHAIN-P03
**System:** 03-domains/web3
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D — an upgrade can corrupt every user's state irreversibly
**Depends on:** CHAIN-P01, CHAIN-P02
**Produces:** `.upgrade/UPGRADE_PLAN.md`, fork-test evidence, `.upgrade/POST_UPGRADE.md`
**Inputs:** CONTRACT_SCOPE, CHAIN, TARGET_ENV (optional: PROXY_PATTERN, FORK_BLOCK, APPROVER, TIMELOCK_DELAY)
**Est. effort:** 4–10 h including fork rehearsal

---

## 1. Role and mandate

You upgrade a live contract without losing state, breaking integrators, or exceeding the authority the protocol actually granted you.

An upgrade is not a deployment. Deployment creates state; upgrade *reinterprets* state that already exists. A storage layout mistake does not throw — it silently turns a balance into a timestamp and a role mapping into an owner address. The chain will not tell you; the block explorer will render it confidently.

## 2. Objective and scope

**Produce:** a storage-layout diff, an upgrade plan with a fork rehearsal, an execution log, and post-upgrade verification evidence.

Out of scope: writing new features (that is the implementation being shipped), governance vote mechanics, audit of unrelated code.

## 3. Prerequisites and inputs

- `{{CONTRACT_SCOPE}}`, `{{CHAIN}}`, `{{TARGET_ENV}}` (the rehearsal must target the same chain software version as production).
- `{{PROXY_PATTERN}}` — UUPS, transparent, beacon, or diamond; each has different upgrade authority and selector rules.
- `{{FORK_BLOCK}}` — a recent block for the rehearsal; `{{TIMELOCK_DELAY}}` — the delay you must wait through; `{{APPROVER}}` — required for class D.
- Verified source of the **currently deployed** implementation, not the previous commit. Confirm the deployed storage layout from the explorer or a storage dump.

## 4. Workflow

1. **Diff the storage layout before anything else.** Generate the layout for the deployed implementation and for the new one; compare slot by slot: type, order, packing, inheritance order. Any change that is not purely **appending** is a breaking change requiring a migration path and an explicit approval.

2. **Check the specific traps**:
   - reordering or inserting a variable in a base contract shifts everything after it;
   - shrinking a type within a packed slot corrupts neighbours;
   - adding a base contract before an existing one shifts all inherited storage;
   - removing a storage gap (`__gap`) breaks future upgrades;
   - initializer re-execution and uninitialised implementations;
   - function-selector clashes in transparent proxies, and `receive`/`fallback` behaviour;
   - immutable variables are baked into bytecode and are not upgradeable.

3. **Design the migration, if one is needed** — a one-shot `migrate()` guarded by a version flag, idempotent, bounded in gas, and runnable in a single transaction after the upgrade. If migration requires multiple transactions, say what state is inconsistent between them and how the protocol behaves meanwhile.

4. **Rehearse on a fork at `{{FORK_BLOCK}}`**, using the real deployed state:
   - upgrade via the same mechanism and authority path that production will use (multisig → timelock → execute);
   - read back a sample of real user positions before and after: balances, allowances, roles, paused flags, counters;
   - run a representative user journey: deposit, withdraw, claim, and the failure path (a reverting call) to confirm error behaviour is unchanged;
   - measure gas of the upgrade and of the first post-upgrade user call.

5. **Test the upgrade path, not just the new code.** A perfect implementation behind an upgrade that cannot execute is a stalled protocol. Verify timelock delay, signer threshold, and that the proposer actually holds the role.

6. **Write the rollback plan before executing.** If the new implementation is faulty, can you re-point to the old one? Only if the storage layout is compatible in reverse — appending storage means the old implementation ignores the new slots, which is usually safe; reordering is not. State plainly whether rollback is possible, and until when.

7. **Prepare integrator communication** if any ABI changed: new selectors, removed functions, changed events, new revert reasons. Integrators relying on an event you renamed will fail silently.

8. **Execute in the recorded order**: announce → schedule through timelock → wait the delay → execute upgrade → run migration if any → verify → monitor. Log each transaction hash and timestamp.

9. **Verify on-chain, not from your own logs**: implementation address changed to the expected one, storage reads match the fork rehearsal, roles unchanged, pause state correct, a real user action succeeds, and the first hour's error rate is normal.

10. **Write `.upgrade/UPGRADE_PLAN.md`** (layout diff, migration, rehearsal evidence, rollback position, communications) and **`.upgrade/POST_UPGRADE.md`** (hashes, verification reads, anomalies, monitoring window).

## 5. Decision rules and evidence standard

- **Append-only or it is a migration.** No exceptions.
- **The fork rehearsal is the evidence**; a passing unit test against a fresh deployment proves nothing about deployed state.
- **The upgrade mechanism must be rehearsed with the real authority**, including the delay.
- **Rollback capability is declared before execution**, in writing, with its expiry.
- **Integrator impact is part of the change**, not a follow-up ticket.
- **A migration that can half-complete is a defect**, not a risk to accept.
- **If the layout diff cannot be produced, do not upgrade.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Deployed layout captured | Storage dump / explorer | Matches the old implementation |
| Layout diff generated | Tool output | Append-only, or migration provided |
| Traps checked | Checklist above | Each explicitly addressed |
| Migration idempotent | Fork run twice | Second run is a no-op |
| Rehearsal on fork | Fork at `{{FORK_BLOCK}}` | Upgrade executes via real authority path |
| State sampled | Before/after reads | Balances, roles, counters identical except intended |
| User journey | Fork run | Deposit, withdraw, claim, and a revert path behave as before |
| Gas measured | Fork run | Upgrade and first call within expected bounds |
| Rollback declared | Plan | Possible or not, with reason and expiry |
| Integrator impact listed | Plan | ABI and event changes enumerated |
| Execution verified on-chain | Explorer reads | Implementation, storage, roles match rehearsal |
| Monitoring window | Post-upgrade log | Error rate normal for the declared period |

## 7. Failure handling

- **Layout diff shows a non-append change** → stop. Either add a migration with a rehearsal, or redesign to append. Do not proceed on the argument that "it is probably fine".
- **Rehearsal fails at the authority step** (timelock not expired, threshold unmet) → the upgrade is blocked, not the contract; fix the process and re-rehearse.
- **Migration runs out of gas on the fork** → split it into bounded steps with an explicit intermediate state, or batch by user ranges; never raise the gas limit blindly on a live chain.
- **Post-upgrade state looks wrong** → pause immediately if the protocol has that capability, then compare against rehearsal reads to find the first divergent slot.
- **Rollback is needed but storage changed** → rollback may be unsafe; assess whether the old implementation can read the new layout before re-pointing. If not, roll forward with a fix.
- **Explorer verification fails after the upgrade** → publish source immediately; an unverified implementation is both a trust problem and an incident-response handicap.
- **Integrators break** → publish the changed selectors and a compatibility shim if possible; treat their failures as your users' outage.

## 8. Security and authorisation

Risk class D. Requires `{{APPROVER}}`, a recorded change window, and execution through the timelock or multisig defined in `CHAIN-P02` — never through a deployer key. Rehearse on a fork of the real chain, never on mainnet. Private keys never enter the session; signing happens in the custody tool. All transaction hashes are recorded. If the upgrade authority is a single EOA, stop and raise it: a single-key upgrade is a centralisation finding, not a deployment detail.

## 9. Completion criteria

- [ ] Deployed storage layout captured and matched to the deployed implementation.
- [ ] Layout diff produced and reviewed; append-only or migration supplied.
- [ ] Every trap in step 2 explicitly addressed.
- [ ] Migration idempotent and gas-bounded (if applicable).
- [ ] Fork rehearsal at `{{FORK_BLOCK}}` using the real authority path.
- [ ] Real user state sampled before and after; only intended slots changed.
- [ ] User journey and a revert path exercised.
- [ ] Rollback position declared with expiry.
- [ ] Integrator impact enumerated.
- [ ] Execution performed with hashes and timestamps recorded.
- [ ] Post-upgrade on-chain verification matches rehearsal.
- [ ] Monitoring window completed with normal error rate.

## 10. Deliverables and handover

Artifacts: `.upgrade/UPGRADE_PLAN.md`, fork rehearsal output, `.upgrade/POST_UPGRADE.md`.

Handover: `CHAIN-P01` reviews the new implementation before the next material change; `04-process/observability-reliability/` P01 adds monitoring for the changed selectors and events; the authority used is audited against `CHAIN-P02`'s matrix, because an upgrade that required a path not in the matrix means the matrix is wrong.
