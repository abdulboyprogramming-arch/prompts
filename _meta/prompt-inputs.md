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

## Migration status (honest)

The convention is normative for **new and touched prompts**. Prompts written before this convention use prose ("the user", "the target area") and are being retrofitted as they are edited; the validator enforces consistency only for prompts that declare `Inputs:`. A full retrofit of the existing library has not been performed, and this document does not claim it has.
