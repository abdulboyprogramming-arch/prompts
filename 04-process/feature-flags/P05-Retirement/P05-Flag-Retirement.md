# PROMPT 05 — Flag Retirement

**Identifier:** FF-P05
**System:** 04-process/feature-flags
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** FF-P03 (rollout evidence) or FF-P04 (a permanent off state)
**Produces:** `.flags/RETIREMENT.md`, a removal commit
**Inputs:** REPO_PATH, BRANCH, FLAG_ID (optional: BASE_REF, APPROVER)
**Est. effort:** 20–60 min per flag

---

## 1. Role and mandate

You remove a flag and the path it no longer needs. Removal is the only part of a flag's life that reduces complexity, and it is the part everyone defers — which is why codebases end up with three coexisting implementations of one feature.

The discipline: **prove the winning state is permanent, then delete the other one completely** — branch, config, tests, docs, and the assumption that it could come back.

## 2. Objective and scope

**Produce:** a removal commit that leaves one code path, no flag evaluation, no dead tests, and a record of the evidence and the residual risk.

Out of scope: deleting an operational kill-switch that is still needed (retire only if the operator agrees the control is obsolete); removing a permission gate (move it to the authorisation system, do not delete it); database migrations for data written by the removed path.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` at `{{BASE_REF}}`, worked on `{{BRANCH}}`; `{{FLAG_ID}}` to retire.
- Evidence the winning state is permanent: exposure at the winning value for the declared period, no targeting exemptions in use, and no open experiment depending on the losing state. For a kill-switch being retired, the operator's agreement that the control is obsolete (`{{APPROVER}}` if the control was approved by someone).

## 4. Workflow

1. **Confirm the evidence, do not accept the intention.** "We've been on the new path for months" is a claim. Check: provider shows the flag at the winning value with timestamps; no overrides; no code evaluates a third state; no experiment or A/B analysis still needs the losing branch. If any of these is unverifiable, say so and either wait or remove with the gap recorded.

2. **Decide which state becomes the code.** Usually the current winning state. Occasionally the losing state is the better implementation and the retirement should restore it — that is a different, riskier change; name it and treat it as such rather than smuggling it into a cleanup commit.

3. **Find every read site, including the ones grep misses.** SDK wrappers, config keys, environment variables, feature-flag templates in infrastructure-as-code, mobile client defaults, documentation, runbooks, and test utilities. Removal with one read site left behind produces a runtime default — usually "off" — and a silent behaviour change.

4. **Delete the losing branch completely.** Remove the conditional, not just its configuration: the old function, its tests, its fixtures, its analytics events, its error strings, and the docs describing a choice that no longer exists. A flag removed from config but still read in code is the worst outcome — the code now runs on the default, unversioned and untested.

5. **Check the data and contract surface before deleting.** If the removed branch wrote a different schema, event format, or message shape, other systems may still consume it. Confirm with a repository search, and with instrumentation showing no reads of the old shape where the shape emits a measurable event. Deleting a writer is safe only if nothing still reads what it wrote.

6. **Keep the safety property.** If the flag was also the kill-switch for that behaviour, removal deletes the control. Decide explicitly: is the behaviour now safe to run with no switch (it is the only path, monitored, with a rollback mechanism), or does an operational switch remain (with an owner and an exercise date)? Never leave the implicit answer.

7. **Update the tests to the surviving reality.** Both-states tests collapse to one path; keep a regression test for the behaviour the flag used to guard, and delete the harness. If a test only existed to exercise the losing branch, it goes with it.

8. **Verify by running, not by reading the diff.** Build, run the suite, and (where available) exercise the affected flow in a non-production environment. Confirm the flag no longer appears anywhere: code, config, IaC, provider, docs.

9. **Close the loop on prevention.** Record what would have caught this flag earlier: an expiry check in CI, a lint rule against flags older than N days, a provider-side auto-archive, a review checklist item. Where a mechanism is cheap, add it in the same change or open the ticket.

10. **Write `.flags/RETIREMENT.md`:** evidence and its source, read sites found and their disposition, what was deleted, what was kept and why, data/contract checks, verification performed, residual risk, and the prevention item.

## 5. Decision rules and evidence standard

- **Evidence of permanence, not intent.** Timestamps and overrides, not memory.
- **Delete the branch, not just the switch.** A leftover conditional on a removed flag silently changes behaviour.
- **One flag per commit**, with the removal of its tests and docs in the same commit. Batching makes a regression unattributable.
- **Deleting a writer is not deleting its data.** Check readers before removing a format, and route the data question to the owning domain system.
- **A retired kill-switch must be replaced by something**: monitoring, an alert, a rollback procedure, or a documented acceptance. "No switch" is a decision that needs a reason.
- **Never retire a permission gate as if it were a flag.** Move it to the policy layer, with review and audit, before removal.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Permanence evidenced | provider/console + timestamps | winning value held for the declared period |
| No hidden read sites | grep across code, IaC, config, docs | zero references to `FLAG_ID` |
| Losing branch fully deleted | diff review | no conditionals, functions, fixtures left |
| Data/contract surface checked | reader search | no consumer of the removed shape |
| Safety property decided | review | switch retained with owner, or risk accepted |
| Tests updated | suite run | passes; regression test present |
| Verification run | build + tests + flow exercise | recorded result |
| Prevention item recorded | artifact | mechanism or ticket |

## 7. Failure handling

- **A read site cannot be removed** (mobile clients in the field on old versions, a partner integration) → do not delete the flag; convert it to an explicitly-owned compatibility switch with a dated plan, and record the blocker. This is the most common honest reason a flag survives.
- **Evidence of permanence is unavailable** → either extend the observation period or remove with the gap stated and a rollback plan for the removal itself (the removal is a normal change and can be reverted).
- **Removal reveals the losing branch was still doing work** → stop, restore the flag, and treat it as a defect discovery: record what depended on the old path and fix that dependency before retrying.
- **The flag guards money or personal data** → route to the domain system before removal; the losing branch may be a compensating control.
- **The provider retains the flag but the code no longer reads it** → archive it in the provider too, with a date; stale definitions become the next engineer's false lead.

## 8. Security and authorisation

Risk class B: this changes code and configuration but is reversible by normal review. Do not remove a flag that gates security behaviour without the security owner's agreement. Do not paste provider tokens or customer targeting lists into the artifact. If the retirement deletes an audit or logging path, stop and escalate — a silent loss of auditability is a class D consequence dressed as cleanup.

## 9. Completion criteria

- [ ] Permanence evidenced with source and timestamps.
- [ ] Winning state chosen; any reversal treated as a separate change.
- [ ] All read sites found: code, config, IaC, mobile, docs, runbooks.
- [ ] Losing branch, tests, fixtures, docs deleted.
- [ ] Data and contract readers checked.
- [ ] Safety property decided (switch retained with owner, or risk accepted).
- [ ] Build, suite, and flow verified.
- [ ] Provider definition archived.
- [ ] Prevention mechanism added or ticketed.

## 10. Deliverables and handover

Artifact: `.flags/RETIREMENT.md` plus the removal commit on `{{BRANCH}}`.

Handover: the inventory (`FF-P01`) is updated to remove the flag; the owner of any retained operational switch receives its exercise date; `04-process/release-engineering/` receives the change in the changelog if the removal is user-visible.
