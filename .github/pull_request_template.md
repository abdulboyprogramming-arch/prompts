## What this changes

<!-- One paragraph. Which prompts, systems, or tools, and why. -->

## Type

- [ ] New prompt or system
- [ ] Promotion (skeleton/draft → operational)
- [ ] Correction (broken link, stale claim, factual error)
- [ ] Tooling (`scripts/`)
- [ ] Documentation / meta only

## The library's own bar

- [ ] `python3 scripts/check_all.py` passes — it regenerates nothing, so the generated files must already be committed
- [ ] New prompt: it has a home in `scripts/generate_task_index.py`, and `TASKS.md` is regenerated
- [ ] Counts updated wherever they appear (`README.md`, `PROJECT-STATUS.md`, `QUICKSTART.md`, `_meta/publication-checklist.md`)
- [ ] Any promoter: metadata updated (Version, Maturity), `Est. effort` present, `Inputs:` declared **and used** as `{{PLACEHOLDER}}`s
- [ ] Any promoter: verification table, failure handling, completion criteria are real, not headings
- [ ] Indexes updated: system `README.md`, root `README.md` table, `CHANGELOG.md`, `_meta/review-log.md`, `PROJECT-STATUS.md` if counts changed
- [ ] No new claim exceeds what the files do (this is the rule the validator exists to enforce)

## Evidence

<!-- For a promotion: what you checked and how. For a tooling change: the fixture that proves the new rule fires. "Reviewed" alone is not evidence. -->

## Honest limits

<!-- What this change does NOT do. Every merged change should be able to state one. -->
