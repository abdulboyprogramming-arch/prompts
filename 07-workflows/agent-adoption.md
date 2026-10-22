# Workflow — Adopting Coding Agents Without Losing Control

**Identifier:** WF-AGENTADOPT
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** B (writes configuration and policy; enabling broad permissions is C/D and separately approved)
**Depends on:** `CTX-P01..P04`, `AI-P07`, `WF-VERIFY`, `GEN-P02`
**Produces:** `AGENT_ADOPTION.md`, an approved permission profile, a pilot report, a rollback plan
**Inputs:** REPO_PATH, TEAM_SCOPE (optional: AGENT_TOOLS, RISK_APPETITE, APPROVER)
**Est. effort:** 1–2 weeks elapsed for a pilot; 4–6 h of actual work

---

## 1. Role and mandate

You introduce AI coding agents into a team's workflow as an engineering change with evaluation, permissions, oversight, and a rollback — not as a tool someone installed on a Tuesday.

The failure pattern is consistent across organisations: one enthusiastic engineer enables an agent with shell access and a broad token, it produces impressive results for two weeks, a subtle incident occurs (a force-push, a leaked credential, a "fixed" test that was deleted), and the response is either a blanket ban or nothing at all. Both outcomes lose the value and keep the risk.

## 2. Objective and scope

**Produce:** a written adoption plan with a bounded pilot, an evidence standard for "good enough", a permission profile reviewed as a security decision, an oversight model, and a rollback that does not depend on goodwill.

Out of scope: vendor selection, procurement, and any claim about model capability that is not measured in your repository.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the codebase the agent will work in.
- `{{TEAM_SCOPE}}` — who gets access, in which repositories, with what review obligations.
- `{{AGENT_TOOLS}}` — the tools and IDEs in scope; `{{RISK_APPETITE}}` — prototype speed versus production caution; `{{APPROVER}}` — who accepts the residual risk.
- `VERIFICATION_REPORT.md` — written by `WF-VERIFY`; read it before starting rather than re-deriving it.

## 4. Workflow

1. **Write down what you are trying to improve**, in a measurable term: cycle time on small changes, time-to-first-PR for new joiners, review backlog, test coverage of new code. "Productivity" is not measurable and will be the subject of an argument in six weeks.

2. **Inventory the agent surface before granting anything** (`CTX-P01`): which tools read which files, what each can execute, what credentials are in the environment. Then reduce it (`AI-P07`): explicit allowlists, scoped paths, per-command secret injection, approval gates on irreversible actions, and no unpinned remote execution.

3. **Define the machine-readable rules of the road** (`CTX-P02`): one canonical `AGENTS.md` with build/test/lint commands that were actually executed, concrete prohibitions with alternatives (never force-push; never edit generated files), and the definition of done. Every other tool file is a thin adapter.

4. **Choose the oversight model deliberately**, per risk class:
   - **autonomous with review** — the agent may open PRs; a human reviews every diff;
   - **supervised** — a human approves each command that writes;
   - **advisory** — the agent proposes, the human applies.

   Set the model by blast radius, not by enthusiasm. Production code and infrastructure get the stricter model.

5. **Run a bounded pilot** on a real, low-risk slice: one repository, one team, two to four weeks, a fixed set of tasks. Pre-register what success looks like (`GEN-P02` discipline applied to the team rather than a prompt): defect rate on agent-authored changes, review rework rate, time to merge, and **incidents attributable to agent actions**.

6. **Verify independently, not from the agent's summary** (`WF-VERIFY`). Agents report success confidently and wrongly; the review must re-run the tests, check the diff for undeclared scope, and confirm that no test was weakened to pass.

7. **Watch for the four failure signatures** and treat each as a stop signal for that task type: weakened tests, undeclared refactors, "fixed" by deleting the assertion, and confident claims with no command executed. Each maps to a missing instruction, an ambiguous one, or a missing mechanical gate — fix the cause, not the prompt wording.

8. **Make the audit trail real**: who ran what, on which repository, with which permissions. Without it, an incident becomes an investigation into people's memories, and you cannot answer the first question a security team will ask.

9. **Write the rollback before you need it**: how to disable the agent (token revocation, config revert), how to identify and revert agent-authored commits (they should be labelled by author or trailer), and who decides. A rollback that requires the enthusiast to cooperate is not a control.

10. **Decide from evidence, then write the policy**: what is allowed, what requires approval, what is prohibited; how new tools are approved (`AI-P07` step 10); and when the decision is reviewed. Record dissent and residual risk with a name against it.

## 5. Decision rules and evidence standard

- **Adopt on evidence, not enthusiasm.** Pre-registered metrics, measured over a pilot, compared to baseline.
- **Permissions are a security decision**, reviewed like one.
- **Every irreversible action has a human gate** until the evidence justifies otherwise — and "the evidence" means a measured period, not a feeling.
- **Independent verification is non-negotiable** for agent-authored changes.
- **A rollback that depends on the tool's own cooperation does not exist.**
- **Rules that cannot be checked will be ignored**; convert them to CI checks (`CTX-P04`).
- **Residual risk has a name and a review date.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Objective measurable | Plan | Baseline and target metrics named |
| Surface inventoried | `CTX-P01` output | Tools, capabilities, credentials listed |
| Permissions reduced | Config diff | Allowlists, scoped paths, no unpinned remote execution |
| Rules executable | Canonical `AGENTS.md` | Commands run successfully by a fresh agent |
| Oversight model set | Policy | Per-risk-class model defined |
| Pilot bounded | Plan | Scope, duration, task types fixed |
| Metrics measured | Pilot report | Baseline versus pilot, with counts |
| Independent verification | Sample of PRs | Re-run tests, diff audited, no weakened tests |
| Failure signatures monitored | Review log | Each tracked, with causes fixed |
| Audit trail exists | Logs | Actor, repository, action, permission |
| Rollback tested | Drill | Agent disabled and a commit reverted in a drill |
| Policy written | Document | Allowed / approval / prohibited; review date; named risk owner |

## 7. Failure handling

- **The pilot produces no measurable improvement** → say so; the tool may still be worth keeping for specific task types, but that is a narrower decision and should be stated as one.
- **An incident is attributable to agent actions** → contain first (`05-scenarios/security-incident/` or `05-scenarios/incident-response/`), then re-audit permissions and rules before resuming; do not resume on reassurance.
- **Engineers bypass the review obligation** ("it was faster") → the oversight model is wrong for that risk class, or the incentive is; fix the model rather than issuing a memo.
- **The agent cannot work within the reduced permissions** → the permission set is an engineering constraint to solve (scoped credentials, sandbox, fixtures), not a reason to grant the home directory.
- **Rules multiply without effect** → apply the removal test: delete every rule that changed no behaviour in the last month.
- **A vendor changes the tool's behaviour or defaults** → treat as a new permission review, and re-run the pilot metrics on the change.
- **Leadership wants a blanket ban after one incident** → present the incident's actual cause and the control added; a ban and a shrug both leave the underlying gap.

## 8. Security and authorisation

Risk class B; granting shell, network, or credential access is class C/D and requires `{{APPROVER}}`. Never place production credentials in an agent's environment; inject short-lived credentials per command (`02-engineering/secrets-rotation/`). Agent-authored commits must be attributable — use a distinct author or commit trailer so an incident can be scoped by query rather than by memory. Treat anything the agent reads from a repository or the web as untrusted input: a malicious `AGENTS.md` or tool description is an attack path (`AI-P07`).

## 9. Completion criteria

- [ ] Objective and baseline metrics written.
- [ ] Agent surface inventoried; permissions reduced and recorded as a diff.
- [ ] Canonical rules file with executed commands and concrete prohibitions.
- [ ] Oversight model defined per risk class.
- [ ] Pilot scoped, time-boxed, and pre-registered.
- [ ] Pilot metrics compared to baseline, including incidents.
- [ ] Independent verification performed on a sample of agent-authored changes.
- [ ] Four failure signatures monitored with causes fixed.
- [ ] Audit trail available (actor, repository, action).
- [ ] Rollback drilled and attributable commits in place.
- [ ] Policy written with allowed / approval / prohibited, review date, and named risk owner.

## 10. Deliverables and handover

Artifacts: `AGENT_ADOPTION.md`, permission profile, pilot report, policy, rollback drill record.

Handover: `CTX-P04` maintains the rules and their checks; `AI-P07` is re-run whenever a new tool is added; `04-process/code-review/` absorbs the independent-verification obligation into normal review for agent-authored changes; `04-process/governance-compliance/` uses the audit trail as evidence when a customer or auditor asks how AI-generated code is controlled.
