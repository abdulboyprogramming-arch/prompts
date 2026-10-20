# Workflow — Audit → Remediate

**Identifier:** WF-AUDIT-REMEDIATE
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** audit-remediation
**Risk class:** B
**Depends on:** AUDIT-P01…P09, QA-P01…P07, REF-P01…P07, SEC-P01…P07
**Produces:** a validated findings set, a prioritised plan, applied fixes, and independent verification

---

## When to use this

You need a defensible assessment of an existing codebase and then want the important parts fixed — without the audit becoming a permanent report nobody acts on, and without remediation turning into an unplanned rewrite.

## Sequence

| # | Stage | Prompt | Output |
|---|-------|--------|--------|
| 1 | Audit | `02-engineering/codebase-audit/` AUDIT-P01→P08 | `.audit/FINDINGS.md`, `.audit/ROADMAP.md` |
| 2 | Triage decision | this workflow | agreed workstreams and stop line |
| 3 | Safety net | `04-process/testing-qa/` QA-P04→P06 (targeted) | tests protecting the areas to change |
| 4 | Remediation | `02-engineering/security-hardening/`, `02-engineering/refactoring/`, `05-scenarios/quick-fixes/` | branch commits |
| 5 | Verification | `04-process/testing-qa/` QA-P06 + targeted re-audit | `.qa/VALIDATION.md`, delta report |
| 6 | Communication | `05-scenarios/pr-authoring/` | PR description with risk and rollback |

## Stage handoffs

1. **Audit → triage.** Handoff carries: severity counts, the five findings that matter, coverage limits, and the roadmap with effort units. The audit is *diagnostic only*; nothing has been changed.
2. **Triage — GATE.** The user selects: which workstreams to fix now, and an explicit stop line (what will not be fixed). Record the selection. Without this gate, remediation expands indefinitely and the audit's prioritisation is wasted.
3. **Safety net.** Handoff carries: which behaviours are now covered and where. Rule: **no refactor of an R1 behaviour without a passing test that demonstrates the current behaviour**, unless the behaviour is itself the defect.
4. **Remediation.** One workstream at a time, on a branch, one commit per logical change. Each fix cites the finding ID it closes. No opportunistic cleanup outside the workstream.
   - Security findings: `02-engineering/security-hardening/` (authorisation, secrets, injection).
   - Structural/coupling findings: `02-engineering/refactoring/` with its safety-net stage.
   - Small, self-contained defects: `05-scenarios/quick-fixes/`.
   - If a finding requires an architectural change, stop and route to `02-engineering/rewriting-migration/` or `architecture-review`.
5. **Verification (independent).** Handoff carries: the delta — findings closed, partially closed, unchanged, or newly introduced. Re-run the audit checks for the affected areas only; a full re-audit is expensive and rarely warranted within the same cycle.
6. **Communication.** PR body states: finding IDs, approach, alternatives rejected, verification performed, residual risk, rollback plan.

## Gates

- **GATE A — remediation scope.** After triage. Human decision required; the workflow does not authorise code changes.
- **GATE B — production-affecting change.** Any fix touching migrations, auth policy, or data deletion requires explicit approval and a rollback plan before execution.
- **GATE C — merge.** Fixes are local commits; push/PR requires authorisation (Category C).

## Completion criteria for the workflow

1. Every change traces to a finding ID or an explicitly recorded new discovery.
2. Each R1-area change has a test that would fail without it.
3. Verification was executed independently, not read from the remediation log.
4. The delta report accounts for every finding in the selected workstreams.
5. No unmatched scope: files changed outside the selected workstreams are listed and justified.
6. Residual risk and unclosed findings are written down.

## Failure routing

| Failure | Route |
|---------|-------|
| Audit findings too weak to act on | Return to AUDIT-P07 adversarial pass; delete unsupported findings |
| Fix requires breaking API change | GATE B; consider compatibility shim via `01-contribution/packages-libraries/` |
| Cannot write a test that fails without the fix | The behaviour is not understood yet — return to `05-scenarios/debugging/` |
| Test suite too slow to verify each fix | QA-P04 feedback item first; do not skip verification |
| Fix reveals systemic design problem | Stop the workstream; produce an architecture decision record and escalate |

## Anti-patterns

- Fixing everything the audit found. The roadmap exists to prevent this.
- Refactoring while remediating ("the file was open anyway") — makes the diff unreviewable.
- Verifying with the same agent that wrote the fix, without re-execution.
- Closing a finding as "fixed" because the code compiles.
