# PROMPT 04 — Maintenance and Drift Control

**Identifier:** CTX-P04
**System:** 04-process/agent-context
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** continuous-improvement
**Risk class:** B
**Depends on:** CTX-P03
**Produces:** `.agent-context/MAINTENANCE.md`, CI checks, review schedule
**Inputs:** REPO_PATH (optional: BRANCH, APPROVER, REVIEW_CADENCE)
**Est. effort:** 30–60 min to set up; minutes per review

---

## 1. Role and mandate

Agent context rots faster than documentation, because it describes *how to operate* a repository that changes weekly. The failure is silent: the file stays plausible, the commands stop working, and every agent that reads it is now confidently wrong.

Your job is to make drift **detectable by a machine** where possible and **cheap to fix** everywhere else.

## 2. Objective and scope

**Produce:** automated checks that fail when the context is stale, an updating convention tied to real triggers, an ownership record, and a review cadence with a defined scope.

Out of scope: the initial authoring (P02) and the adherence experiment (P03).

## 3. Prerequisites and inputs

- `AGENTS.md`, the adapters, `.agent-context/ADHERENCE.md` (accepted gaps and mechanical checks to build), and the build files in `{{REPO_PATH}}`.
- `{{BRANCH}}` to make changes; `{{APPROVER}}` if the repository protects its default branch; `{{REVIEW_CADENCE}}` — the interval the team will actually honour (quarterly is honest; weekly is aspirational).

## 4. Workflow

1. **Turn every verifiable claim into a check.** The context file asserts facts; most are mechanically testable:
   - Commands referenced exist in `package.json`/`Makefile`/`Taskfile` — check the script names.
   - Paths referenced exist — check they resolve.
   - The canonical file and its adapters agree on the source — check for duplicated blocks.
   - No secret-shaped strings — scan for token patterns.
   - Version pins match CI — compare against the workflow files.
   - Adapter formats still parse (frontmatter, globs).

   Add these as a job that runs on pull requests touching the context files, the build files, or the directory structure.

2. **Bind updates to triggers, not to memory.** Name the events after which the context must be revisited:
   - a new or renamed script, package, or service;
   - a directory move or a new top-level module;
   - a change of build tool, package manager, or runtime version;
   - a new tool adopted by the team (or one dropped);
   - a policy change (branch protection, review rules, secret handling);
   - an adherence failure (P03) — the strongest trigger.

3. **Name one owner per file**, in the file itself. A context file with no owner is maintained by whoever happens to notice, which is nobody.

4. **Set the review loop with a bounded scope**, so it actually happens: re-run three probes from P03 (one command, one boundary, one convention), re-run the checks, and read the diff since the last review. Fifteen minutes, not a project.

5. **Measure decay instead of guessing.** Track two numbers over time: the proportion of context claims that still verify, and the number of adapter files that are out of sync with the canonical source. Both should be trend-visible in the check output.

6. **Handle tool churn.** Agent tools change how they read context (file names, frontmatter, precedence). On any adapter change: verify against the tool's current documentation, keep the adapter minimal so breakage is cheap, and never move guidance *into* an adapter to work around a format change.

7. **Remove, do not accumulate.** Each review deletes sections that no longer change behaviour (P03's removal test), files for tools nobody uses, and prohibitions that no longer apply. Context growth is the default failure mode.

8. **Keep the human documents authoritative.** If the context file and `CONTRIBUTING.md` disagree, the human document wins and the context file is edited; the reverse would let agent instructions silently redefine process.

9. **Write `.agent-context/MAINTENANCE.md`:** the checks and where they run, the trigger list with owners, the review cadence and scope, the decay metrics and their current values, and the removal log.

## 5. Decision rules and evidence standard

- **If it can be checked, check it.** A convention that depends on someone remembering is already broken.
- **Triggers beat schedules.** Review when something changed, plus a cadence as a backstop.
- **One owner per file, named in the file.**
- **Deletion is maintenance.** Growth without removal is how context becomes unread.
- **Human documents win conflicts.** Agent instructions describe the process; they do not define it.
- **Adapters stay minimal** so a tool's format change costs ten lines, not a rewrite.
- **Checks must be cheap** — a slow check gets disabled.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Claims mechanised | CI run | failing case proves the check fires |
| Commands and paths verified | script output | zero missing references |
| Duplication detected | diff check | adapters contain no canonical guidance |
| Secrets scanned | pattern check | none found |
| Triggers documented | list | each with an owner |
| Owner named in each file | inspect | present |
| Review cadence + scope | document | interval and 3-probe scope stated |
| Decay metrics reported | script or doc | current values shown |
| Removal log maintained | artifact | deletions recorded with reasons |

## 7. Failure handling

- **The repository cannot run CI** → provide a script (`scripts/check-agent-context.py` or equivalent) and document running it before a release; a manual check is weaker, not worthless.
- **Checks are too strict and block unrelated work** → scope them to changes touching the context, build files, or structure, and keep the failure message actionable.
- **A tool changes its file format** → fix the adapter, re-run one probe, and record the change date; if the format is undocumented, prefer the plainest Markdown that works.
- **Nobody honours the cadence** → drop to the minimum that has actually happened (a release-time check) and say so, rather than keeping a quarterly ritual nobody performs.
- **The context is correct but agents still fail** → that is an adherence problem, not maintenance; reopen P03 with the failing probe and consider a mechanical gate.

## 8. Security and authorisation

Risk class B: writes repository files and CI configuration. Checks must not print secret values — detect and report the location only. Adapter changes must not widen tool permissions; a rule change that grants shell, network, or write access to new paths requires review by the code owner, and any credential found in a context file is treated as exposed and rotated.

## 9. Completion criteria

- [ ] Mechanical checks exist for commands, paths, duplication, secrets, pins, adapter format.
- [ ] Checks run on relevant pull requests and fail with an actionable message.
- [ ] Trigger list documented with an owner per trigger.
- [ ] Owner named in each context file.
- [ ] Review cadence and bounded scope recorded.
- [ ] Decay metrics defined with current values.
- [ ] Removal log started.
- [ ] `.agent-context/MAINTENANCE.md` written.

## 10. Deliverables and handover

Artifacts: `.agent-context/MAINTENANCE.md`, the checks, the review schedule.

Handover: the checks become part of the repository's CI alongside `04-process/documentation/` P05's maintenance mechanisms; `04-process/handover/` P02 receives the context file as a knowledge asset whose owner and review date must transfer with the project.
