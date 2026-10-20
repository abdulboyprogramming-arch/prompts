# PROMPT 06 — Cleanup & Documentation

**Identifier:** REF-P06
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** REF-P05 (behaviour preserved)
**Produces:** `REFACTOR_SUMMARY.md`, removal commits
**Inputs:** TARGET_ENV (optional: RETIREMENT_DATE)
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You are the engineer removing what the refactoring left behind. Refactorings that stop at "the new code works" leave the old path, the flag, the compatibility shim, and the stale documentation in place — and the codebase ends up with both structures, which is worse than before.

## 2. Objective and scope

**Complete the change:** remove the old path once telemetry proves it is unused, delete dead code with evidence, update documentation and diagrams, and write the summary that lets a future engineer understand what moved and why.

Out of scope: further structural work, new features, fixing the bugs recorded during the refactoring (they get their own changes).

## 3. Prerequisites and inputs

- `VALIDATION.md` with behaviour preserved.
- The coexistence design from P02: what was dual-run, what flag guarded it, and the planned retirement date `{{RETIREMENT_DATE}}`; traffic evidence from `{{TARGET_ENV}}`.
- Telemetry showing the old path's usage (zero, or the remaining consumers).

## 4. Workflow

1. **Do not remove the old path on the day the new one works.** Wait for the observation window defined in P02; record the window and the date. Immediate removal removes the rollback option while risk is highest.
2. **Prove the old path is unused** with three signals where available: telemetry (no calls), code search across all repositories (no references), and the owners of any consumer confirming migration. Absence of telemetry is not absence of use — if the path is unobservable, instrument it first.
3. **Remove in dependency order**: callers switched → compatibility shim deleted → old implementation deleted → tests of the old path removed (their behaviour is covered by the net) → configuration keys removed → flags removed → feature-flag definitions deleted in the flag system.
4. **Delete dead code with evidence**: unreferenced exports, unused dependencies, orphaned fixtures, commented-out blocks, and duplicated helpers. Record the search that proved each is dead; "it looks unused" is how production incidents start.
5. **Update the documentation that now lies**: architecture diagrams, module READMEs, ADRs, onboarding docs, runbooks with file paths, and any code examples. Grep the repository for the old names — documentation referencing a moved module is a trap for the next engineer.
6. **Record the decision** if the project keeps ADRs: what was refactored, why, what alternatives were rejected, and what the new structure intends. This is the difference between a refactoring that teaches and one that merely happens.
7. **Update the goal artifact**: mark the target achieved with the measurement from P05, or record why it was not.
8. **Write `REFACTOR_SUMMARY.md`:** what moved (before → after map), why, the target and its measurement, what was deleted and the evidence, the net that now protects the area, risks that remain, and follow-ups (bugs found, slices deferred, performance items).
9. **Hand off the follow-ups** to their owning systems rather than leaving them in a document nobody reads.

## 5. Decision rules and evidence standard

- **No removal without two independent signals of non-use**, or an unobservable path that has been instrumented for a full cycle.
- **The flag goes last**, after the code path it guards is gone; deleting the flag first leaves dead code that will be "temporarily" re-enabled.
- **Documentation is part of the refactoring**, not a follow-up task. A stale diagram is a defect in the shared model of the system.
- **Do not delete tests that still describe current behaviour.** Delete only tests of removed implementations.
- **Record what remains.** An honest "these three modules still duplicate the rule; deferred because X" is more valuable than a claim of completeness.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Observation window elapsed | dates | matches P02 plan |
| Non-use proven | telemetry + search + owner confirmation | all available signals |
| Removal in dependency order | commit review | shims before implementations |
| Dead code deletions evidenced | search results recorded | no references |
| Docs and diagrams updated | grep old names | none remain |
| ADR/summary written | inspect | decision rationale present |
| Follow-ups routed | inspect | owning system named |
| Suite still green after removals | run | green |

## 7. Failure handling

- **Telemetry shows the old path still in use** → do not remove; identify the consumer, notify, and extend the window. Record the identity of the consumer in the summary.
- **A flag cannot be removed** because another system still reads it → treat it as a contract; deprecate via `04-process/decommissioning/` with a timeline, and record the residual.
- **Documentation is generated elsewhere** (docs site, wiki) → record the location and mark it as an outstanding item with an owner; do not claim it is updated.
- **Removal breaks the build** (an unexpected reference appears) → revert the removal commit, find the reference, and add it to the dependency order.
- **Follow-ups accumulate** → triage into the ledger with severity; do not leave them unnamed in prose.

## 8. Security and authorisation

Risk class B. Removing authentication shims or compatibility layers that still serve traffic is a security-relevant change: verify consumers migrated before deletion, and never remove a check because the new path "also has one" without confirming it is equivalent.

## 9. Completion criteria

- [ ] Observation window elapsed and recorded.
- [ ] Non-use proven with available signals.
- [ ] Old path, shim, flags, and configuration removed in order.
- [ ] Dead code and dependencies deleted with evidence.
- [ ] Documentation, diagrams, and examples updated.
- [ ] Decision record written where the project uses them.
- [ ] Goal marked achieved or explicitly unmet.
- [ ] Summary written; follow-ups routed; suite green.

## 10. Deliverables and handover

Artifacts: `REFACTOR_SUMMARY.md`, removal commits, updated docs.

Handover: follow-ups to their systems (bugs → debugging; deferred structure → P01 of a later cycle; performance → `02-engineering/performance/`); the summary to the team's architecture record; the net stays as permanent protection for the area.
