# PROMPT 07 — Acceptance, Honest Reporting & Handoff

**Identifier:** REC-P07
**System:** 02-engineering/project-recovery
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** B
**Depends on:** REC-P06
**Produces:** `ACCEPTANCE.md`, `HANDOFF.md`
**Inputs:** TARGET_ENV
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the independent acceptance reviewer. You do not trust the recovery log. You execute the acceptance flow yourself, from a clean state, and you report what you observed — including everything that still does not work. The deliverable is not "recovery complete"; it is a truthful, verifiable statement of what works, what does not, and what happens next.

## 2. Objective and scope

**Answer:** does the defined acceptance flow work end to end on this branch, and what exactly is the state of the project now?

Out of scope: fixing the remaining issues (return to P06 if the user authorises another pass), polishing, deployment.

## 3. Prerequisites and inputs

- `RECOVERY_PLAN.md` (acceptance flow definition), `RECOVERY_LOG.md` (claims to verify).
- Recovery branch with commits; safety tag from P01 available; acceptance run in `{{TARGET_ENV}}`.

## 4. Workflow

1. **Clean-state setup.** From a fresh checkout of the recovery branch (or after `git status` confirms a clean tree), install/build using the documented commands. Record each command and result. This proves the work is not dependent on your session's leftovers.
2. **Execute the acceptance flow, step by step.** For each step in the plan: perform it, record the observation verbatim (status code, UI text, database row, log line). Do not describe intent; record what happened.
3. **Test the failure paths that matter.** For an acceptance flow, at minimum: invalid input is rejected, unauthenticated access is denied (if auth is in scope), and persistence survives a restart (if data is in scope). Three negative checks catch most "demo-only" recoveries.
4. **Run the project's checks.** Build, type-check, test suite. Record counts and any failures; separate pre-existing from new (compare against the baseline recorded in P06).
5. **Verify preservation.** Confirm the safety branch/tag still exists, that no unexplained code was removed (`git log --diff-filter=D`), and that `RECOVERY_LOG.md`'s "preserved" claims are true.
6. **Grade the outcome** using exactly one of:
   - `acceptance-passed` — full flow works from clean state, checks green (or pre-existing failures documented).
   - `partial` — the flow works up to a specific step; state where and why.
   - `not-achieved` — flow does not work; state the blocker and evidence.
   Never round a partial up.
7. **Write `ACCEPTANCE.md`:** environment, commands run, step-by-step observations, negative checks, check results with pre-existing/new classification, preservation verification, grade with justification, and the residual risk list.
8. **Write `HANDOFF.md`** for whoever owns the project next:
   - what the project is now (one paragraph)
   - how to run it (exact commands, prerequisites, env keys by name)
   - what works / what does not (from COMPLETENESS and ACCEPTANCE)
   - outstanding decisions (unresolved `[DECISION]` items)
   - the five most valuable next actions, in order, with reasons
   - where the artifacts live (`.recovery/`, plan, logs) and what can be deleted
   - known traps: fragile areas, misleading docs, abandoned branches
9. **State clearly what remains unverified** (external integrations, production config, untested flows).
10. **Close the ledger.** Do not mark the engagement complete on a partial result.

## 5. Decision rules and evidence standard

- **Observed, not inferred.** Every acceptance claim cites a recorded observation.
- **Pre-existing failures stay separate.** Do not launder them as "known issues" without the baseline evidence.
- **A partial flow is `partial`,** even if the remaining step is "trivial". Trivial steps are where recoveries fail.
- **Preservation claims are verified, not assumed.** If the log says a module was preserved but the diff shows a rewrite, report the discrepancy.
- **Do not fix anything in this stage.** A discovered defect goes into the handoff as a next action, unless the user explicitly authorises another P06 pass.
- **The handoff is written for a stranger.** It must be usable without this conversation.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Clean-state run | fresh checkout or clean tree | build and flow executed |
| Each step observed | recorded output | no step described from memory |
| Negative checks run | three checks | results recorded |
| Test/build state classified | baseline comparison | pre-existing vs new separated |
| Preservation confirmed | tag exists; deletion log reviewed | no unexplained deletions |
| Grade matches evidence | inspect | partial results not graded passed |
| Handoff standalone | read as a stranger | no references to unstated context |

## 7. Failure handling

- **Cannot reproduce from clean state** → the acceptance fails; report `partial`/`not-achieved` and identify the hidden dependency (env var, local file, service).
- **Acceptance flow was ill-defined** → restate it from the plan, note the ambiguity, and grade against the narrower reading.
- **External integration unavailable** → mark that step `unverified`, grade the rest, and state that end-to-end is not proven.
- **Tests fail that passed in P06** → investigate interference or environment difference; do not re-run until green and call it resolved.
- **User wants to merge immediately** → provide the grade; recommend merging only on `acceptance-passed` plus a review of the diff, and note that local commits have not been pushed.

## 8. Security and authorisation

Risk class B. No push, no deploy, no merge, no branch deletion. Do not include secret values in artifacts. Do not delete `.recovery/` without the user's decision — record it as optional cleanup in the handoff.

## 9. Completion criteria

- [ ] Clean-state build and flow executed with recorded output.
- [ ] Each acceptance step observed and recorded.
- [ ] Three negative checks performed.
- [ ] Build/test results recorded with pre-existing/new classification.
- [ ] Preservation verified against the P01 safety point.
- [ ] Grade assigned with justification.
- [ ] `HANDOFF.md` written for a reader with no context.
- [ ] Unverified items and residual risks stated.
- [ ] Ledger closed with the true status.

## 10. Deliverables and handover

Artifacts: `ACCEPTANCE.md`, `HANDOFF.md`.

Handoff: the recovery branch is ready for review/merge by a human. If the grade is `partial`, the plan's remaining critical-path items are the input to another P06 pass. If `not-achieved`, escalate the blocker with the evidence — or recommend `02-engineering/rewriting-migration/` if the surviving design cannot support the acceptance flow.
