# Prompt Inputs and Variables

**Status:** normative convention · **Applies to:** every prompt that needs configuration before it can run
**Related:** `_meta/prompt-authoring-standard.md` §2 (metadata), `00-core/inputs/RUN-SHEET.md` (fill-in template)

---

## The problem this solves

A prompt says "analyse the target area" and "the repository". Which repository? Which area? Whose definition of done? When the answer lives only in prose, three things go wrong:

1. **The agent guesses.** It picks the current directory, the largest module, or the first plausible interpretation — and the output is confident and wrong.
2. **The user re-types context every stage.** In a six-stage system the same five facts (repo path, branch, environment, scope, risk tolerance) are restated by hand, drifting between stages.
3. **Multi-agent runs diverge.** Two agents given "the same" task from prose produce different scopes, and their work cannot be merged.

Declaring inputs fixes all three: the prompt states what it needs, the user supplies it once, and every stage receives the same values.

## The convention

### 1. Declare inputs in metadata

```
**Inputs:** REPO_PATH, TARGET_AREA, BRANCH (optional: BASE_REF), RISK_TOLERANCE
```

- Comma-separated names, `UPPER_SNAKE_CASE`.
- Optional inputs marked `(optional: NAME, NAME)` or given a default in the prompt body.
- Only declare what the prompt genuinely cannot proceed without or would otherwise guess.

### 2. Use the same names as placeholders in the body

```
Analyse {{TARGET_AREA}} in the repository at {{REPO_PATH}}.
```

Rules:

- `{{NAME}}` must match a declared input exactly. The validator rejects an undeclared placeholder and warns about a declared-but-unused one.
- Placeholders appear **inside instructions**, not inside code samples meant to be run literally. If you need a literal `{{`, write it inside a fenced block and mark the block `text` — the validator ignores fenced content.
- Do not invent a second syntax (`<NAME>`, `$NAME`, `[NAME]`). One convention, checkable.

### 3. Provide defaults and fallbacks in §3 of the prompt

| Input | Source | If missing |
|-------|--------|------------|
| `REPO_PATH` | user | use the current working directory and state it in the output |
| `TARGET_AREA` | user | stop; scope cannot be guessed |

A default is a decision the prompt makes on the user's behalf, so it must be visible and recorded in the output — never silent.

### 4. Mark sensitive inputs

Prefix with `SECRET_` or note it in §8: `SECRET_DEPLOY_TOKEN`. Sensitive inputs are never echoed into artifacts, never committed, and never requested in chat if a credential store is available. The prompt must say how the value is supplied (environment variable, credential helper, existing session) rather than asking the user to paste it.

### 5. Fill a run sheet once per engagement

For any multi-stage system, copy `00-core/inputs/RUN-SHEET.md`, fill the values once, and paste the same sheet into each stage. This is the practical equivalent of passing a configuration object between functions.

Every stage's output should echo the run sheet (or a hash of it) so a later reader can tell which configuration produced which artifact.

## What counts as an input

| Kind | Example | Declare? |
|------|---------|----------|
| Path or location | `REPO_PATH`, `TARGET_AREA`, `MIGRATIONS_DIR` | Yes — the agent cannot infer it reliably |
| Identity or credential | `SECRET_API_TOKEN`, `CI_RUNNER_ID` | Yes, marked sensitive |
| Environment | `TARGET_ENV` (`staging`/`production`), `BASE_REF` | Yes |
| Policy or tolerance | `RISK_TOLERANCE`, `SLA_TARGET`, `RETENTION_DAYS` | Yes — these change the answer |
| Scope boundary | `IN_SCOPE`, `OUT_OF_SCOPE` | Yes |
| A file the prompt must read | `SPEC_FILE`, `INCIDENT_TICKET` | Yes |
| General domain knowledge | "how to review code" | No — that is the prompt's content |
| Anything the prompt could safely discover itself | the current branch name | No — discover and record it |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "Ask the user for anything you need" | Transfers the work back to the user at the worst moment, mid-run |
| Twenty inputs for a 40-line prompt | The prompt is really a system; split it |
| Inputs that duplicate what the repository states | Drift: the input says `main`, the repo is on `release/2.1` |
| A required input with no fallback and no stop rule | The agent improvises |
| Naming a variable in prose but not in metadata | Unvalidatable; the next editor breaks it silently |

## Canonical names

Use these names rather than inventing a synonym per prompt. A synonym is a defect: the same value then has two names, and the run sheet stops being pasteable.

| Name | Meaning | Typical form |
|------|---------|--------------|
| `REPO_PATH` | Root of the repository under work | absolute path, `.` for the current directory |
| `BASE_REF` | Ref the work starts from | branch, tag, or SHA |
| `HEAD_REF` | Ref produced or under review | branch or SHA |
| `BRANCH` | Working branch the agent may commit to | `feat/…`, `fix/…` |
| `TARGET_COMMIT` | Commit being released, audited, or reviewed | SHA or tag |
| `LAST_TAG` | Previous release tag, for changelogs and ranges | `v2.7.0` |
| `TARGET_AREA` | Subtree, module, or component in scope | path or component name |
| `TARGET_ENV` | Environment the change lands in | `staging`, `production` |
| `TARGET_SERVICE` | Named deployable, queue, or job | service identifier |
| `RELEASE_VERSION` | Version being produced | `2.8.0` |
| `TRIGGER` | What prompted the engagement | incident ID, audit finding, concern |
| `TIME_BUDGET` | Effort or CI-time ceiling that changes the plan | `2h`, `10-minute PR target` |
| `CHANGE_WINDOW` | When production-affecting work is permitted | `Sun 02:00–04:00 UTC` |
| `APPROVER` | Named human who authorises irreversible steps | name or role |
| `RISK_TOLERANCE` | How much uncertainty is acceptable | `conservative`, `move fast` |
| `IN_SCOPE` / `OUT_OF_SCOPE` | Explicit boundary expressed by the user | comma-separated list |
| `SECRET_*` | Anything credential-like | supplied from a store, never pasted |

Rules that keep the set small:

- Declare only what the prompt cannot safely discover or assume.
- Prefer one input over two: `TARGET_COMMIT` covers "target commit/tag and intended version" poorly — use `TARGET_COMMIT` plus `RELEASE_VERSION`, not `RELEASE_POINT`.
- An upstream artifact is **not** an input. `.qa/QA_CONTEXT.md` belongs in `Depends on`, even if §3 lists it as a prerequisite.
- `(optional: NAME)` is the only way to mark an optional input; a bare `(optional)` is rejected because it names nothing.

## Names in use (audited 2026-10-20)

97 distinct names are declared across the library. That is more than a run sheet can hold at once, which is why they are tiered:

| Tier | Names | Where they come from |
|------|-------|----------------------|
| **Core engagement** (13) | `REPO_PATH`, `BASE_REF`, `HEAD_REF`, `BRANCH`, `TARGET_COMMIT`, `TARGET_AREA`, `TARGET_ENV`, `TARGET_SERVICE`, `RELEASE_VERSION`, `APPROVER`, `RISK_TOLERANCE`, `TIME_BUDGET`, `TRIGGER` | The run sheet in `00-core/inputs/RUN-SHEET.md`; reused by every system |
| **Cross-system operational** (25) | `LAST_TAG`, `CHANGE_WINDOW`, `DEADLINE`, `IN_SCOPE`, `OUT_OF_SCOPE`, `TEAM_SIZE`, `SLA_TARGET`, `BUILD_COMMAND`, `TEST_COMMAND`, `PR_REF`, `PR_DESCRIPTION`, `AUTHOR_INTENT`, `AUTHOR_CONTEXT`, `AUTHOR_RESPONSES`, `REVIEW_FINDINGS_FILE`, `SECURITY_AUTHORISATION`, `SECURITY_REVIEW_AUTHORISATION`, `WRITE_AUTHORITY`, `DISCLOSURE_CONTACT`, `DISCLOSURE_OWNER`, `SUBJECT_IDENTIFIERS`, `VERIFICATION_METHOD`, `REQUEST_ID`, `INCIDENT_ID`, `SHARED_STATE_REF` | Values a second system plausibly needs; fill them when the engagement crosses systems |
| **System-scoped** (59) | e.g. `MIGRATIONS_DIR`, `PREFLIGHT_ENV`, `PROVIDER_NAME`, `API_VERSION`, `SUPPORTED_CURRENCIES`, `CLOUD_ACCOUNT`, `BILLING_EXPORT_PATH`, `EVAL_DATASET_PATH`, `MY_DETAILS_FILE`, `LOST_REF`, `DATA_LOSS_WINDOW` | One system only; declared in that system's prompts and documented in its README |

The audit is reproducible: `python3 -c` against `load()` in `scripts/validate_library.py`, or read the `**Inputs:**` lines directly. The full list is in the catalog.

Two rules keep this from growing without limit:

- If an existing core name means the same thing, reuse it. `TARGET_COMMIT` covers a release, an audit, and a review; do not add `REVIEW_COMMIT`.
- A name that exists in exactly one prompt and is never referenced by a sibling stage is probably not an input at all — it is a paragraph of the prompt's content.

## Migration status (honest)

**109 of the 118 operational prompts assessed declare `Inputs:`.** The retrofit was done system by system in 2.9.0, using each prompt's own §3 as the source of truth: where §3 already named a value ("Repository path", "Named approver for Category C actions"), that value became a canonical name and a placeholder; where §3 named an upstream artifact (`.qa/QA_CONTEXT.md`), it stayed in `Depends on`.

Nine operational prompts deliberately declare **no** inputs, because they consume only artifacts from the previous stage and would otherwise carry an unused declaration:

`AUDIT-P02`, `AUDIT-P03`, `AUDIT-P04`, `AUDIT-P05`, `AUDIT-P07`, `FC-P02`, `REC-P03`, `SEC-P03`, `QA-P03`.

What the retrofit does **not** claim:

- It does not claim the names are all optimal. 97 names for 118 prompts is a wide vocabulary; consolidation is backlog item 26.
- It does not claim the prompts have been executed with filled run sheets. The validator proves declared/used consistency, not that the value is available at runtime.
- Draft and skeleton prompts (163) were not retrofitted. They declare inputs when they are promoted.
