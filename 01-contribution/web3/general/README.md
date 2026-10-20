# General Web3 Contribution System

**Maturity: skeleton (v0.1.0).** These eight stage files are structural outlines: a reasonable sequence with named artifacts, but without the evidence rules, verification steps, and failure handling the library standard requires. Do not present this system as operational, and do not run it unattended on a repository that controls real assets.

**Intended use today:** a human-supervised checklist for contributing to a web3 project.
**Additional constraint:** anything that can move funds or change on-chain state requires explicit human approval before execution (risk class C/D — see `00-core/safety-and-security/ACTION-CATEGORIES.md`).

## Stages

| ID | Stage | Purpose | Maturity |
|----|-------|---------|----------|
| W3-P01 | [Context & Project Understanding](P01-Context/P01-Context-Project-Understanding.md) | Chain targets, contracts, toolchain, upgrade authority | skeleton |
| W3-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Defects, gas, safety gaps worth fixing | skeleton |
| W3-P03 | [Opportunity Selection & Framing](P03-Selection/P03-Opportunity-Selection-Framing.md) | Choose one, define acceptance and blast radius | skeleton |
| W3-P04 | [Planning & Design](P04-Planning/P04-Planning-Design.md) | Design against existing contract patterns | skeleton |
| W3-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | Implementation plus test coverage | skeleton |
| W3-P06 | [Validation & Security](P06-Validation/P06-Validation-Security.md) | Tests, invariants, adversarial review | skeleton |
| W3-P07 | [PR & Communication](P07-PR/P07-PR-Communication.md) | Change description maintainers will trust | skeleton |
| W3-P08 | [Orchestrator](P08-Orchestrator/P08-Web3-Contribution-Orchestrator.md) | Sequences the stages | skeleton |

## Known gaps before promotion to `operational`

1. No invariants/testing standard (fuzzing, invariant tests, fork tests) with pass criteria.
2. No standing rule on upgradeable contracts, admin keys, or governance proposals.
3. No guidance on secrets/key handling beyond the generic core rules.
4. No rollback/pause procedure for a deployed change.
5. Security stage is a heading, not a procedure.

Tracked in `_meta/ROADMAP-AND-BACKLOG.md`. Until those exist, use `02-engineering/security-hardening/` alongside this system and treat sign-off as human work.

## Related

- General security hardening: `02-engineering/security-hardening/`
- Autonomous contribution pipeline: `01-contribution/open-source/general-agent/`
