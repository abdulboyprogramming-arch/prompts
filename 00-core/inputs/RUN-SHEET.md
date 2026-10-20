# Run Sheet — fill this in once per engagement

Copy this block, replace every value, and paste it at the top of the conversation when running any prompt that declares `**Inputs:**`. One sheet per engagement: every stage receives the same values, so scope cannot drift between stages, agents, or sessions.

**Why a sheet and not prose:** the same facts restated from memory change subtly each time ("the api folder", "the API module", "backend/api"). A filled sheet is a single source of truth that the prompt can echo into its output, so a later reader knows exactly which configuration produced which artifact.

---

## Sheet

```text
ENGAGEMENT:      <short name, e.g. "checkout hardening Q4">
DATE:            <YYYY-MM-DD>

REPO_PATH:       <absolute or repo-relative path>
BASE_REF:        <branch, tag, or commit the work starts from>
BRANCH:          <branch name this work will use, or "none">
TARGET_AREA:     <path(s) or module(s) in scope>
OUT_OF_SCOPE:    <explicit exclusions — the most useful line on this sheet>

TARGET_ENV:      <local | staging | production>
RISK_TOLERANCE:  <conservative | standard | aggressive>
DEADLINE:        <date or "none">
APPROVER:        <who authorises Category C/D actions>

SENSITIVE:       <names of secret inputs, never values; e.g. SECRET_DEPLOY_TOKEN>
NOTES:           <anything a new engineer must know before reading the output>
```

---

## Rules for filling it

1. **`OUT_OF_SCOPE` is mandatory.** Every prompt in this library expands scope by default if it is not bounded; an empty line means "everything is in scope", which is never true.
2. **Never put a secret value on the sheet.** Put the *name* and let the prompt read it from the environment or credential store.
3. **Use the same identifiers the prompt declares** (`REPO_PATH`, not "the repo").
4. **Update the sheet, do not fork it.** If scope changes mid-engagement, amend the sheet and note the change; a second sheet is how two agents end up with two truths.
5. **Ask the prompt to echo the sheet** into its output artifact, so the record is self-describing.

## Minimal sheets for common situations

| Situation | Minimum inputs |
|-----------|----------------|
| Debugging a defect | `REPO_PATH`, `TARGET_AREA`, observed vs expected behaviour, `TARGET_ENV` |
| Refactoring | `REPO_PATH`, `TARGET_AREA`, `OUT_OF_SCOPE`, measurable target, `RISK_TOLERANCE` |
| Database change | `REPO_PATH`, database identifier, `TARGET_ENV`, maintenance window, `APPROVER` |
| Git recovery | `REPO_PATH`, the ref or SHA involved, whether the history is shared, `APPROVER` |
| Security review | `REPO_PATH`, `TARGET_AREA`, authorisation to assess, `SECRET_` input names |
| Incident | `TARGET_ENV`, service name, incident start time, `APPROVER`, communication owner |

## When the prompt asks for a name that is not on this sheet

The core sheet covers 13 names. The library declares 97 in total; the rest are **system-scoped** values such as `MIGRATIONS_DIR`, `PREFLIGHT_ENV`, `BILLING_EXPORT_PATH`, or `EVAL_DATASET_PATH`. When a prompt's `**Inputs:**` line names one:

1. Read that prompt's §3 table — every system-scoped input has a "if missing" fallback documented there.
2. Fill it in the *system's* section of the sheet (append a short block titled with the system path), not in the core block.
3. If two systems name the same thing differently, use the core name where the meaning matches and note the alias. Aliases are a defect to report, not a preference to keep.
