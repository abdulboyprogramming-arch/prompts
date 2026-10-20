# Testing & QA Improvement System

**Maturity: operational (v1.1.0).** All seven stages carry workflow, evidence rules, verification, failure handling, and completion criteria.

**Entry point:** [`P07-Orchestrator/P07-Testing-QA-Orchestrator.md`](P07-Orchestrator/P07-Testing-QA-Orchestrator.md)
**Execution mode:** audit-remediation
**Risk class:** B — edits tests and test configuration only; does not modify production code to make tests pass

## What this system is for

Your suite is slow, flaky, absent on the critical paths, or confidently green while production breaks. This system finds out which, then fixes the highest-value gaps in an order justified by risk rather than by coverage percentage.

## Stage sequence

| ID | Stage | Produces | Maturity |
|----|-------|----------|----------|
| QA-P01 | [Context & quality goals](P01-Context/P01-Context-Goals.md) | `.qa/QA_CONTEXT.md` | operational |
| QA-P02 | [Current state assessment](P02-Current-State/P02-Current-State-Assessment.md) | `.qa/CURRENT_STATE.md` | operational |
| QA-P03 | [Gap analysis](P03-Gap-Analysis/P03-Gap-Analysis.md) | `.qa/GAPS.md` | operational |
| QA-P04 | [Strategy & prioritisation](P04-Strategy/P04-Strategy-Prioritization.md) | `.qa/TEST_STRATEGY.md` | operational |
| QA-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | new/updated tests, `.qa/IMPLEMENTATION_LOG.md` | operational |
| QA-P06 | [Validation & measurement](P06-Validation/P06-Validation-Measurement.md) | `.qa/VALIDATION.md` | operational |
| QA-P07 | [Orchestrator](P07-Orchestrator/P07-Testing-QA-Orchestrator.md) | all of the above | operational |

## Shared contracts

### Risk classes for test prioritisation

Every gap is scored before it is scheduled:

| Risk | Meaning | Test response |
|------|---------|---------------|
| **R1** | Wrong behaviour loses money, data, or access; or is unrecoverable | Must have automated coverage at the lowest reliable level, plus an explicit negative test |
| **R2** | Wrong behaviour is user-visible and recoverable | Automated coverage expected; manual check acceptable short-term with a recorded debt item |
| **R3** | Internal inconvenience, recoverable, low blast radius | Opportunistic coverage; do not block delivery |
| **R4** | Cosmetic or fully covered by another layer | Do not add tests; record the decision |

### The coverage rule

Coverage percentage is a **diagnostic**, never a target. A suite with 85% line coverage that never exercises authorisation failure is worse than a 60% suite that does. Every coverage claim must be paired with the list of R1 paths it does *not* cover.

### Test-value rules

1. Test behaviour through public interfaces; avoid asserting private internals.
2. One logical assertion per test intent; multiple physical asserts are fine.
3. No sleeps as synchronisation; use deterministic fakes, clocks, and event waiting.
4. A test that cannot fail is not a test — verify by deliberately breaking the code once and confirming red.
5. Test data must be created by the test, not inherited from a shared mutable fixture.
6. A bug fix ships with a regression test that fails before the fix.

### Artifacts and state

`.qa/` holds all artifacts and `.qa/QA_LEDGER.md` tracks stage status. On resume, read the ledger first.

## How to run it

1. Give your agent the P07 orchestrator, the repository path, and — if you have one — the incident or near-miss that triggered the interest in testing.
2. Expect P02/P03 to produce uncomfortable but specific findings (e.g. "the payment callback path has no test and no CI job runs it").
3. P05 writes tests. Review the diff before merging; the orchestrator will not touch production code.
4. P06 measures whether the suite is actually better: it detects flakes, verifies new tests fail when the code is broken, and checks CI enforcement.

## What it will not do

- Chase a coverage number.
- Rewrite production code to make tests easy (that is `02-engineering/refactoring/`).
- Replace exploratory or manual QA. It decides where automation pays and where it does not.
- Guarantee the suite catches every regression. It measures the gap and states what remains.

## Related

- Auditing the whole codebase first: `02-engineering/codebase-audit/`
- Fixing a specific flaky test: `05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md`
- CI configuration: `04-process/observability-reliability/` and `03-domains/devops-infra/`
- Contract tests across services: `03-domains/backend/` (API design) plus QA-P04 §contract testing
