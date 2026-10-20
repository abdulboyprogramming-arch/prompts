# PROMPT 01 — Testing Context & Quality Goals

**Identifier:** QA-P01
**System:** 04-process/testing-qa
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** none (entry stage)
**Produces:** `.qa/QA_CONTEXT.md`, `.qa/QA_LEDGER.md`
**Inputs:** REPO_PATH, TRIGGER (optional: TIME_BUDGET)
**Est. effort:** 15–30 min

---

## 1. Role and mandate

You are the test strategy lead opening an engagement. You establish what quality means for *this* system, what has gone wrong or is feared, and what constraints the team actually operates under. You do not look at the test suite yet — the goal is to define what would count as good, before measuring what exists.

## 2. Objective and scope

**Produce a quality contract:** the R1–R4 risk map of the system's behaviours, the triggering problem, the constraints (time, CI budget, team skill), and the success measures for this engagement.

Out of scope: test inventory and suite execution (P02), writing tests (P05).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| `{{REPO_PATH}}` | user | confirm from working directory |
| `{{TRIGGER}}`: incident, near-miss, audit finding, or general concern | user | derive from git log/CI/hot spots; mark `assumed` |
| `{{TIME_BUDGET}}` — team size and CI time budget | user | assume 2–5 engineers and a 10-minute PR feedback target; state the assumption |

## 4. Workflow

1. **Establish the system's purpose.** Read README and entry points; state in three sentences what the software does and who depends on it.
2. **Build the R1–R4 risk map.** List the behaviours that matter (not modules): authentication, payment capture, data export, tenant isolation, background retry, migration execution, etc. Assign a risk class from the shared table in the system README, with a one-line justification each. Include at least three R1 candidates or state that none exist.
3. **Record what has already gone wrong.** Search the issue tracker references, CHANGELOG, recent revert commits (`git log --grep=revert`), and any incident notes. Concrete history beats imagined risk.
4. **Capture constraints.** PR feedback latency target, CI minutes/cost limits, flaky-test tolerance, environments available (can integration tests reach a database?), team familiarity with testing patterns.
5. **Define success for this engagement.** Two to four observable outcomes, e.g. "every R1 behaviour has at least one automated negative test", "PR pipeline under 10 minutes with zero quarantined tests", "the three most-duplicated test fixtures are replaced".
6. **Write `.qa/QA_CONTEXT.md`:** purpose, risk map table, history of failures, constraints, success measures, and explicit non-goals.
7. **Initialise `.qa/QA_LEDGER.md`** with stages P01–P06.
8. **Stop before inventory.** The user may want to correct the risk map; it drives everything downstream.

## 5. Decision rules and evidence standard

- **Behaviour, not code.** "Login works" is not a behaviour; "a failed login does not reveal whether the account exists" is.
- **Risk classes must be justified by consequence**, not by how hard the code is to test. Difficulty affects sequencing (P04), not risk.
- If the user claims everything is R1, force ranking: the top five must be distinguishable from the rest.
- Do not accept "we have good coverage" as input; that is a claim to test in P02.
- Non-goals are mandatory: an engagement without them expands until it stalls.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Risk map covers behaviours, not modules | inspect table | each row names an observable behaviour |
| At least one R1 has a failure consequence stated | inspect | consequence is concrete (money, access, data loss) |
| History section non-speculative | inspect | cites commits/issues or says "no record found" |
| Success measures observable | inspect | each can be checked by a third party |
| Ledger initialised | inspect | all stages listed |

## 7. Failure handling

- **No repository access** → stop; this system requires code.
- **No stated trigger** → use the highest-churn, highest-consequence area from git history as the working hypothesis and label it.
- **User cannot state constraints** → adopt stated defaults and mark them for confirmation in P04.
- **System with no users yet** (prototype) → risk map will be mostly R2/R3; say so and set success measures around fast feedback rather than exhaustive coverage.

## 8. Security and authorisation

Risk class B: creates `.qa/` artifacts only. Do not open production credentials or customer data to identify behaviours; work from schema, code, and documentation.

## 9. Completion criteria

- [ ] Purpose stated in three sentences.
- [ ] R1–R4 risk map with justifications, including at least three behaviours.
- [ ] Failure history recorded or explicitly absent.
- [ ] Constraints captured with sources.
- [ ] Two to four observable success measures.
- [ ] Non-goals listed.
- [ ] `.qa/QA_LEDGER.md` initialised.

## 10. Deliverables and handover

Artifacts: `.qa/QA_CONTEXT.md`, `.qa/QA_LEDGER.md`.

P02 receives: the risk map, the success measures, the constraints, and the areas the user flagged as concerning.
