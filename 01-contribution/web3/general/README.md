# General Web3 Contribution System

**Maturity: four skeletons, four operational.** `W3-P02` (discovery) maps the trust boundary — privileged surface, value paths, external calls, price inputs, upgrade surface — before looking for missing guards. `W3-P03` (selection) assigns every candidate a reversibility tier by asking who can undo it, and gates tier 2 and 3 behind recorded approval before code exists. `W3-P06` (validation) requires a violating case per invariant and a pinned fork run. `W3-P07` (communication) leads with the state change, the tier, the undo path, and the worst outcome. The other four stages are outlines. Do not run this system unattended on a repository that controls real assets.

**Intended use today:** a human-supervised checklist for contributing to a web3 project.
**Additional constraint:** anything that can move funds or change on-chain state requires explicit human approval before execution (risk class C/D — see `00-core/safety-and-security/ACTION-CATEGORIES.md`).

## Stages

| ID | Stage | Purpose | Maturity |
|----|-------|---------|----------|
| W3-P01 | [Context & Project Understanding](P01-Context/P01-Context-Project-Understanding.md) | Chain targets, contracts, toolchain, upgrade authority | skeleton |
| W3-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Trust-boundary map, then missing guards | **operational** |
| W3-P03 | [Opportunity Selection & Framing](P03-Selection/P03-Opportunity-Selection-Framing.md) | Reversibility tier, approval gate, invariants with violating cases | **operational** |
| W3-P04 | [Planning & Design](P04-Planning/P04-Planning-Design.md) | Design against existing contract patterns | skeleton |
| W3-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | Implementation plus test coverage | skeleton |
| W3-P06 | [Validation & Security](P06-Validation/P06-Validation-Security.md) | Invariants, adversarial cases, access-control matrix | **operational** |
| W3-P07 | [PR & Communication](P07-PR/P07-PR-Communication.md) | Risk first: state change, tier, undo path, blast radius | **operational** |
| W3-P08 | [Orchestrator](P08-Orchestrator/P08-Web3-Contribution-Orchestrator.md) | Sequences the stages | skeleton |

## Known gaps before promotion to `operational`

1. ~~No invariants/testing standard (fuzzing, invariant tests, fork tests) with pass criteria~~ — closed in 2.22.0 by `W3-P06`, which requires a violating case per invariant and a fork run pinned to a block.
2. ~~Security stage is a heading, not a procedure~~ — closed in 2.22.0 by `W3-P06`.
3. ~~No selection rule that prices irreversibility before code exists~~ — closed in 2.22.0 by `W3-P03`, which tiers candidates by who can undo them and gates the top tiers on recorded approval.
4. No standing rule for governance proposals or an upgrade executed through a timelock rather than a multisig.
5. No rollback or pause procedure for a change that has already been deployed.
6. Key handling beyond the generic core rules, and what to do when a fork test needs a funded key.

Tracked in `_meta/ROADMAP-AND-BACKLOG.md`. Until those exist, use `02-engineering/security-hardening/` alongside this system and treat sign-off as human work.

## Related

- General security hardening: `02-engineering/security-hardening/`
- Autonomous contribution pipeline: `01-contribution/open-source/general-agent/`
