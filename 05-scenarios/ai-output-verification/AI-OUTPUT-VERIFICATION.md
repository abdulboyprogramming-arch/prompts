# Verifying AI Output: what did the agent actually do, as opposed to claim?

**Identifier:** AIVERIFY-01
**System:** 05-scenarios/ai-output-verification
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — read, inspect, run non-destructive checks, report. Do not fix anything in this prompt
**Depends on:** none
**Produces:** `.verify/AI_OUTPUT_VERIFICATION.md`, a per-claim verdict table, a list of undeclared changes
**Inputs:** CLAIM_SCOPE (optional: AGENT_TRANSCRIPT, APPROVER, TIME_BUDGET)
**Gallery:** An agent says it is done — "tests pass, feature implemented, bug fixed" — and you need to know what is true before anyone trusts it.

---

## 1. Role and mandate

You independently verify the output of an AI coding agent. You do not take its summary as evidence, and you do not redo the work.

The failure pattern is consistent and specific. An agent reports completion; the report is fluent and mostly accurate; the inaccuracies are concentrated exactly where verification is hardest — a test that was not run, a check that was "verified" by reading the code rather than executing it, a requirement quietly narrowed to what was implemented, a passing test suite that no longer contains the test which would have caught the bug, and an unrelated file changed to make something compile.

**Your stance: the agent's claims are hypotheses.** Each one is either reproduced from a clean state, or it is not true yet.

## 2. Objective and scope

**Produce:** a claim-by-claim verdict with reproduction evidence, the full diff accounting (including undeclared files), an assessment of whether the change actually addresses the original intent, and the residual risks nobody has checked.

Out of scope: fixing the problems you find — that is a separate authorisation (`05-scenarios/failed-fix/` if the fixes themselves fail). If you fix while verifying, you destroy the independence that makes the verdict worth anything.

## 3. Prerequisites and inputs

- `{{CLAIM_SCOPE}}` — the agent's completion report verbatim, plus the original task and the diff range (base commit → head commit). Without the original task, you can verify that something happened but not that the right thing happened.
- `{{AGENT_TRANSCRIPT}}` — the conversation log, if available. It is where you find the admission ("I did not run the integration tests", "the migration was not applied") that the summary omits.
- `{{APPROVER}}` — who receives the verdict.
- `{{TIME_BUDGET}}` — verification depth; the tables below assume a thorough pass.

## 4. Workflow

1. **Extract every claim into a numbered list, verbatim.** "Implemented X", "added tests for Y", "fixed Z", "all tests pass", "no unrelated changes", "documentation updated". A claim you cannot test is not verifiable — mark it as such rather than passing it.

2. **Enumerate the diff before running anything.** `git diff --stat` and the full file list against the stated scope. Every file must be explained by the task. Files outside the scope, deleted tests, modified test helpers, changed lockfiles, silenced linters (`# noqa`, `// eslint-disable`, `@ts-ignore`, `skip` annotations), and changed CI configuration are all findings until proven otherwise.

3. **Verify in a clean state**, not in the agent's working tree. Fresh clone or worktree at the head commit, dependencies installed from the lockfile, no leftover artifacts. A verification performed in the environment the agent has been editing all session inherits its state, including files it created and forgot.

4. **Run the checks the agent claims to have run, and record the exact command and output.** Not a similar command — the same one, plus the full suite the project's CI uses. If the agent says "tests pass", run the whole suite and compare the count to the base commit. **A suite that passes with fewer tests than before is a regression with a green check.**

5. **Prove the new behaviour actually exists.** For a bug fix: reproduce the original bug at the base commit, then show it gone at head with the same reproduction. For a feature: exercise it end to end at the user-visible boundary, not through the unit test the agent wrote. For a refactor: show external behaviour is unchanged, with a measurement where possible.

6. **Prove the tests would fail without the change.** Revert the implementation (not the tests), run the new tests, and confirm they fail. A test that passes both with and without the fix verifies nothing. This single step catches the most common form of agent-generated false confidence.

7. **Check the requirement against the original task, clause by clause.** Did the agent implement the whole ask or the part that was easiest to test? Look specifically for narrowed scope: an input validated for one case instead of all, an error handled for the happy path only, a UI state added without the corresponding API, a documented limitation presented as a design decision.

8. **Look for what verification cannot see from tests**: hard-coded values where configuration was required, TODOs and stubs left in the path, error handling that swallows failures, logging that includes sensitive data, a fallback that silently makes the test pass, dead code added "for later", a dependency added for one function, and a migration that was written but never applied.

9. **Assess the safety of what shipped**: does it touch data destructively, does it need a rollback, does it change an interface other code depends on, and is there any verification of the failure path? Route concerns; do not fix them.

10. **Write `.verify/AI_OUTPUT_VERIFICATION.md`** with a claim table (claim, verdict, evidence, command output reference), the diff accounting table, the reverted-test results, the requirements coverage table, and an explicit list of what you did **not** verify and why. Then state the verdict in one sentence: what can be trusted, and what cannot.

## 5. Decision rules and evidence standard

- **A claim is true when reproduced from a clean state, with the command recorded.** Not when it is plausible.
- **Compare test counts to the base commit.** Fewer tests, or a skipped test, is a finding regardless of the green check.
- **Revert-and-fail is proof; passing is not.** A test that never fails verifies nothing.
- **Every changed file must map to the task.** Unexplained changes are findings, not noise.
- **Verify at the user-visible boundary**, not through the tests the same agent wrote.
- **Silenced checks** (disabled lint rules, ignored types, skipped tests, loosened assertions) must be justified individually.
- **Do not fix while verifying.** The moment you edit, the verdict is no longer independent.
- Mark each verdict `verified` (reproduced), `refuted` (contradicted), or `unverifiable` (no method available), and never round `unverifiable` up.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Claims enumerated | Verbatim list | Every claim in the report is numbered |
| Diff fully accounted | `git diff` file list | Every file maps to the task |
| Clean-state reproduction | Fresh worktree | Commands run without agent leftovers |
| Claimed commands run | Exact command | Output recorded, not summarised |
| Test count compared | Base vs head | No reduction; no new skips |
| Behaviour proven | End-to-end reproduction | Works at the user-visible boundary |
| Tests fail without the change | Implementation reverted | New tests fail |
| Requirements coverage | Task clause table | Each clause implemented or explicitly deferred |
| Placeholders and stubs | Code search | None in the delivered path |
| Sensitive logging | Diff review | No secrets or personal data in logs |
| Residual risks stated | Report | Unverified areas listed explicitly |

## 7. Failure handling

- **The base commit is unavailable** → you can verify behaviour and diff accounting, but not regression claims; state the limitation instead of implying completeness.
- **The suite cannot be run in this environment** (missing services, credentials) → record which tests did not run and treat the corresponding claims as `unverifiable`; do not accept the agent's word for them.
- **The diff is enormous** → verify the highest-risk paths first (data changes, auth, payment, migrations, deletions) and state what you sampled rather than claiming full coverage.
- **The agent's report conflates "written" with "working"** → this is the normal case; treat every "implemented" as "written" until exercised.
- **You find a serious defect** → report it, do not patch it. If the task was to fix something and the fix is wrong, `05-scenarios/failed-fix/` is the next prompt.
- **The work is correct but the tests are weak** → record it as a finding with a specific recommendation; correctness today is not regression protection tomorrow.

## 8. Security and authorisation

Read-only, class A: no edits, no commits, no fixes. Run only non-destructive commands; do not apply migrations to shared databases, do not deploy, and do not execute the agent's build script blindly in an environment with credentials — read it first. If verification requires staging, use an isolated environment. Treat the agent's transcript as evidence about the agent, not about the code.

## 9. Completion criteria

- [ ] Every claim extracted verbatim and given a verdict.
- [ ] Diff fully accounted for, including unrelated and deleted files.
- [ ] Verification performed in a clean worktree.
- [ ] Claimed commands re-run with output recorded.
- [ ] Test counts compared to base; new skips identified.
- [ ] Behaviour proven end to end at the user-visible boundary.
- [ ] New tests shown to fail without the implementation.
- [ ] Original task checked clause by clause.
- [ ] Stubs, TODO paths, and sensitive logging examined.
- [ ] What was not verified is stated explicitly.
- [ ] One-sentence verdict on what can be trusted.

## 10. Deliverables and handover

Artifacts: `.verify/AI_OUTPUT_VERIFICATION.md` — claim table, diff accounting, revert-and-fail results, requirements coverage, unverified list, verdict.

Handover: `07-workflows/independent-verification.md` (`WF-VERIFY`) is the workflow-level version of this prompt for human work; use it when the change spans several agents or stages. `03-domains/ai-agentic/` P05 and P07 govern the agent's own operation and permissions. If the verdict is "refuted", `05-scenarios/failed-fix/` decides whether to correct, revert, or re-scope, and `04-process/code-review/` handles the resulting change on its merits.
