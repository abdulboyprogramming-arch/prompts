# Run Sheet — a worked example

The [run sheet](RUN-SHEET.md) defines the form. This file shows it used across **two systems and three stages**, because the claim that prompts compose is worth nothing without an example of them doing it.

The engagement below is invented but every artifact name, input name, and maturity label is real, so it can be copied and adapted rather than admired.

---

## The engagement

> A payments service inherited from a team that left. It processes refunds. Nobody knows whether the audit trail is complete, and a security questionnaire arrives in three weeks.

Two systems apply: `02-engineering/codebase-audit` to establish what exists, `02-engineering/security-hardening` to fix what the audit finds, and `07-workflows/independent-verification.md` to check the fixes rather than trust them.

## The filled sheet

```text
ENGAGEMENT:      refunds-service review (Q4)
REPO_PATH:       /srv/work/refunds-service
TARGET_AREA:     src/refunds, src/ledger, migrations/
TARGET_BRANCH:   main
TARGET_ENV:      staging
PRIMARY_OBJECTIVE: establish whether refund audit trails are complete and fix
                   the gaps before the customer security questionnaire
TICKET_OR_ISSUE: SECQ-2291
TIME_BUDGET:     2 working days for audit; 3 days for remediation
RISK_TOLERANCE:  low — money movement, no untested writes to production
CONSTRAINTS:     no schema changes without the DBA; freezes after 2026-11-14
APPROVER:        A. Bello (engineering manager)
```

## How it flows

| # | Stage | Declared inputs it reads | Artifact in | Artifact out |
|---|-------|--------------------------|-------------|--------------|
| 1 | `AUDIT-P01` scope | `REPO_PATH`, `TARGET_AREA`, `TIME_BUDGET` | — | `.audit/SCOPE.md` |
| 2 | `AUDIT-P02` inventory | `REPO_PATH` | `SCOPE.md` | `.audit/INVENTORY.md` |
| 3 | `AUDIT-P03` structure | `REPO_PATH` | `INVENTORY.md` | `.audit/ARCHITECTURE.md` |
| 4 | `SEC-P02` threat model | `TARGET_AREA`, `RISK_TOLERANCE` | `ARCHITECTURE.md` | `.security/THREAT_MODEL.md` |
| 5 | `SEC-P05` plan → `SEC-P06` implement | `RISK_TOLERANCE`, `APPROVER`, `TIME_BUDGET` | `THREAT_MODEL.md`, findings | `.security/PLAN.md`, commits |
| 6 | `WF-VERIFY` | `REPO_PATH`, `TARGET_BRANCH` | the branch diff | verification report |

Three things are worth noticing.

**1. The same sheet is pasted once.** Every stage reads the same values, so `TARGET_AREA` in stage 1 is byte-identical to `TARGET_AREA` in stage 5. When it is restated from memory instead, it drifts — "src/refunds" becomes "the refunds module", and stage 5 quietly includes `src/payouts`, which nobody scoped or approved.

**2. Artifacts carry the context forward, not the transcript.** Stage 4 does not need the conversation from stages 1–3; it needs `.audit/ARCHITECTURE.md`. That is the point of the handoff contract in [`07-workflows/HANDOFF-CONTRACT.md`](../../07-workflows/HANDOFF-CONTRACT.md), and it is what makes a stage resumable three days later by a different agent.

**3. Inputs are not the same as dependencies.** `TARGET_ENV` appears in the sheet because stage 5 verifies against staging, but it is not an input to stage 1 — `AUDIT-P01` does not declare it, and passing it anyway would be noise. A declared input that a stage does not use is a warning in the validator for exactly this reason.

## When a stage needs a system-scoped input

`SEC-P03` declares `RISK_TOLERANCE` (core) but some hardening stages declare `PROBE_ENV` or `BASELINE_REF` (system-scoped). The rule from the run sheet applies:

1. Read that prompt's §3 to find the fallback if it is missing.
2. Append a short block to the sheet for that system, rather than inventing a new core name.
3. If the same concept appears under two names across systems, use the core name and note the alias — then report the alias as a defect, because it is one.

```text
— system: 02-engineering/security-hardening —
PROBE_ENV:       staging-refunds (isolated, synthetic data)
BASELINE_REF:    audit-baseline-2026-10-21
```

## Deviations are recorded, not silently absorbed

The engagement above changed one value mid-flight: stage 5 extended `TIME_BUDGET` from 3 to 4 days after the plan found a credential-rotation dependency. That goes in the sheet as an amendment, with the stage that changed it:

```text
AMENDMENT 2 (after SEC-P05): TIME_BUDGET 3 days → 4 days.
Reason: rotation of the ledger signing key must precede the audit-log change.
Recorded by: stage SEC-P05, approved by A. Bello, 2026-10-22.
```

A sheet that is edited in place without a record makes the final artifacts unexplainable. An amended sheet makes the engagement auditable, which is the same property the prompts themselves insist on.

## What this example does not show

- **A gate being refused.** Workflows define gates where a human must decide; the interesting run is the one where the gate stops work. That lives in the workflow files, not here.
- **A failed stage.** Stage failure routing is defined per workflow; a worked failure example would be a useful addition and is not written yet.
- **A multi-agent run.** `07-workflows/multi-agent-orchestration.md` covers ownership and interface freezing; the run sheet is the same shape but one sheet per agent with the shared values copied verbatim.
