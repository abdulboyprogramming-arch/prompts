# Blockchain & Smart Contract Systems

**Maturity: operational (v1.0.0).** Four stages for code that moves value irreversibly on a public, adversarial, readable network.

**Entry point:** [`P01-Review/P01-Contract-Threat-Model.md`](P01-Review/P01-Contract-Threat-Model.md)
**Execution mode:** diagnostic
**Per stage:** diagnostic (P01), planning (P02), implementation (P03), specialised (P04)
**Risk class:** A (review) → D (upgrade, exploit response)
**Identifiers:** `CHAIN-P01..P04` (the `W3-*` identifiers belong to `01-contribution/web3/`, which covers contributing to someone else's project)

## Why this system exists

Web3 inherits every failure mode of ordinary software and adds four that general engineering intuition does not cover:

1. **Irreversibility.** A wrong write is not reverted by a deploy; it is the new on-chain truth.
2. **Adversarial transparency.** Your code and your transactions are public, so exploits are a race, not a discovery.
3. **Authority is the attack surface.** Most losses come from a privileged key or an over-broad role, not from a subtle bug in arithmetic.
4. **Upgrades reinterpret existing state.** A storage layout change does not throw; it silently reinterprets every user's balance.

The library previously covered Web3 only as an *opportunity-contribution* skeleton (`01-contribution/web3/`), which answers "how do I get involved in someone's protocol", not "is this protocol safe to change". This domain answers the second question.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| CHAIN-P01 | [Threat model & review](P01-Review/P01-Contract-Threat-Model.md) | Assets, trust map, eight attack surfaces, exploited-path findings ranked by profit | `THREAT_MODEL.md`, `FINDINGS.md` |
| CHAIN-P02 | [Key custody & authority](P02-Custody/P02-Key-Custody.md) | Roles → tiers → thresholds → delays; rotation drilled on testnet | `KEY_CUSTODY.md` |
| CHAIN-P03 | [Upgrade & storage migration](P03-Upgrade/P03-Upgrade-Migration.md) | Layout diff, append-only rule, fork rehearsal, rollback position | `.upgrade/UPGRADE_PLAN.md` |
| CHAIN-P04 | [Exploit response](P04-Exploit/P04-Exploit-Response.md) | Contain, preserve evidence, quantify, patch, re-review, disclose | `INCIDENT_LOG.md` |

## The rules

1. **Append-only storage, or it is a migration.**
2. **Every privileged capability has a tier and a threshold**; an EOA admin is a finding.
3. **The fork rehearsal is the evidence**; unit tests against a fresh deployment prove nothing about live state.
4. **A pause path that cannot be exercised in one block is not a pause path.**
5. **Deployed bytecode must match the repository**, or you are reviewing a different program.
6. **Never demonstrate a live exploit on mainnet.** Suspected vulnerabilities are handled privately.
7. **Loss numbers carry a block and a timestamp.**
8. **Authority is a security control, not an operational convenience.**

## Proportionality

| Situation | Run |
|-----------|-----|
| Inherited a protocol / pre-launch review | P01 |
| "Who can actually pause this?" | P01 trust map → P02 |
| Upgrading a live proxy | P03 (P01 on the new implementation) |
| Funds leaving right now | P04 immediately |
| Post-incident | P04 log → P01 review → P02 gap closure |

## Boundaries

- Contributing to someone else's Web3 project: `01-contribution/web3/`.
- Payments and fiat settlement: `03-domains/payments/`.
- Secrets and repository hygiene: `02-engineering/security-hardening/`, `04-process/git-operations/` P03.
- General incident command and postmortem discipline: `05-scenarios/incident-response/`, `04-process/observability-reliability/` P05.

## What this system will not do

- Certify a contract as safe. It ranks exploitable paths and states what it did not review.
- Replace an independent audit for high-value deployments — it makes you ready for one and able to read it.
- Advise on token economics, securities classification, or legal disclosure obligations.
