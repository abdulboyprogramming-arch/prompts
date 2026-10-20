# Instructions for AI Agents Working in This Repository

This repository is a library of engineering prompts. Changes are content changes, not code changes, except for `scripts/`.

## Before you write anything

1. Read `PROJECT-STATUS.md` — current state, decisions, known weaknesses, next actions.
2. Read `_meta/prompt-authoring-standard.md` — the metadata block and required sections are enforced.
3. Run `python3 scripts/validate_library.py` — establish whether the baseline is clean before you add to it.
4. Read `_meta/taxonomy.md` before creating a folder or system.

## Rules

- **Never claim more maturity than the artifact has.** `skeleton` prompts are outlines; their versions are `0.x`. Promoting to `draft`/`operational` requires the required sections and a review record.
- **Do not add a system README status that the validator would reject.** It checks for overclaims.
- **One canonical template.** Do not create a second authoring template.
- **Do not delete unexplained material.** Deprecate into `archive/` with a note; retire identifiers rather than reusing them.
- **Preserve existing work.** If the working tree has changes you did not make, inspect them before editing; never revert them.
- **No empty folders, no placeholder-only files.** A folder earns its place with content at `draft` or above.
- **Keep identifiers unique and system-prefixed** (`AUDIT-P03`, `REC-P01`), matching `^[A-Z][A-Z0-9]*(-[A-Z0-9]+)*$`.
- **Risk class must be honest.** Read-only work is `A`, even when the surrounding system is `B`. Do not describe destructive actions in an `A` prompt unless they are explicitly gated.
- **Do not restate core safety rules.** Reference `00-core/safety-and-security/`.

## After you change something

1. `python3 scripts/validate_library.py` — zero errors.
2. `python3 scripts/validate_library.py --catalog` — regenerate `_meta/CATALOG.md`.
3. `python3 scripts/generate_gallery.py --write` — regenerate `GALLERY.md` (CI fails if it is stale).
4. Update the owning system's `README.md` stage table (with true maturity).
5. Update `README.md`'s status table if a system's maturity changed.
6. Add a `CHANGELOG.md` entry.
7. Add a review record to `_meta/review-log.md` if you changed a maturity label.
8. Update `PROJECT-STATUS.md` if the state, decisions, or next actions changed.

## Do not

- Invent benchmark results, test outcomes, or adoption claims.
- Mark a prompt `operational` because it is long.
- Run installs, deploys, or network publication from this repository — there is nothing to deploy.
- Change the meaning of an existing prompt's contract (artifact names, identifiers) without updating every reference and recording the migration.

## Where to look

| Question | File |
|----------|------|
| What exists and in what state? | `_meta/CATALOG.md` |
| What should I build next? | `_meta/ROADMAP-AND-BACKLOG.md` |
| What did the last agent decide? | `PROJECT-STATUS.md` §6–7 |
| How good is a prompt? | `_meta/quality-rubric.md` |
| How do systems compose? | `07-workflows/README.md` |
