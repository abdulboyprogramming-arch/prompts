# Contributing

This repository is a curated library, not a collection bin. Contributions are judged on whether they make a competent engineer more effective, not on volume.

## Before you write

1. Read [`_meta/prompt-authoring-standard.md`](_meta/prompt-authoring-standard.md) — metadata block, maturity levels, required sections, writing rules.
2. Read [`_meta/taxonomy.md`](_meta/taxonomy.md) — where the content belongs and why folders exist.
3. Check [`_meta/CATALOG.md`](_meta/CATALOG.md) and [`_meta/ROADMAP-AND-BACKLOG.md`](_meta/ROADMAP-AND-BACKLOG.md) — the gap you are filling may already be planned or partly covered.
4. If you are an AI agent, also read [`AGENTS.md`](AGENTS.md).

## What makes a contribution acceptable

| Requirement | Why |
|-------------|-----|
| A real gap, stated | Duplicates dilute the library; near-duplicates are worse than one strong prompt |
| Complete metadata block | Enables the catalog, validation, and safety review |
| Declared inputs | `**Inputs:**` + `{{NAME}}` placeholders wherever the prompt needs configuration — see `_meta/prompt-inputs.md` |
| Maturity label that matches the content | A `skeleton` contribution is welcome; a dishonest `operational` one is not |
| Verification that can fail | Without it the prompt cannot be trusted |
| Failure handling | Real sessions get stuck; the prompt must say what to do |
| Risk class honesty | A read-only prompt must not carry hidden `C`/`D` actions |
| Discovery updated | System `README.md`, root `README.md` table, `_meta/CATALOG.md`, `GALLERY.md` |

## Adding a multi-stage system

1. Create the folder under the correct category, following the naming rules.
2. Add `README.md` with: purpose, when to use / when not to, stage table **with true maturity**, shared contracts, and what the system will not do.
3. Write stages at `draft` or better. Do not ship eight 20-line outlines and call it a system — that is exactly the failure mode this repository corrected.
4. Reference `00-core/` primitives instead of restating safety rules.
5. Include at least one worked example or state explicitly that none exists.
6. Update the root README status table, the category README, and the changelog.

## Improving an existing prompt

- Preserve the original intent and artifact names unless you are deliberately migrating them (then update every reference).
- Prefer adding verification and failure handling to restoring length.
- If you raise a maturity label, add a review record to `_meta/review-log.md` with the reason and the deductions.
- If you lower one, record why in `CHANGELOG.md`.

## Style

- Direct technical language. No marketing adjectives inside prompts.
- Concrete commands, paths, and pass conditions over advice.
- Mark uncertainty: `verified` / `inferred` / `unknown`.
- Do not instruct an agent to use tools or credentials it may not have.
- Keep prompts proportional: a 40-line task does not need 300 lines.

## Validation

```bash
python3 scripts/validate_library.py            # must exit 0
python3 scripts/validate_library.py --catalog  # regenerate the catalog
python3 scripts/generate_gallery.py --write    # regenerate GALLERY.md
python3 scripts/generate_gallery.py --check     # what CI runs
python3 scripts/find_overlaps.py --top 10      # is this prompt already written?
python3 scripts/new_prompt.py --system <dir> --identifier <ID> --title "<Title>"  # scaffold
```

A pull request that raises the validator's error count will not be merged. Warnings should be justified in the PR description.

## Review criteria

A contribution is reviewed against [`_meta/quality-rubric.md`](_meta/quality-rubric.md) at the tier matching its execution mode. The nine critical failure conditions block acceptance regardless of score:

1. Contradictory instructions.
2. Unbounded destructive autonomy.
3. Fabricated capability assumptions.
4. Missing acceptance criteria for mutating prompts.
5. Ambiguity between analysis and implementation.
6. Instructions to claim success without verification.
7. Incompatible workflow dependencies.
8. Materially incorrect technical guidance.
9. A maturity label that overstates the artifact.

## What we will not accept

- Prompt variants that differ only in tone.
- Framework-version-specific prompts that will be stale within months (appendices are fine).
- Claims of testing, adoption, or benchmark results that were not performed.
- Content copied from `archive/` without improvement and re-verification.
