## What this changes

<!-- One paragraph. Which prompts, systems, or tools, and why. -->

## Type

- [ ] New prompt or system
- [ ] Promotion (skeleton/draft → operational)
- [ ] Correction (broken link, stale claim, factual error)
- [ ] Tooling (`scripts/`)
- [ ] Documentation / meta only

## The library's own bar

- [ ] `python3 scripts/validate_library.py` → **0 errors / 0 warnings**
- [ ] `python3 scripts/validate_library.py --catalog` run, `_meta/CATALOG.md` committed if it changed
- [ ] `python3 scripts/generate_gallery.py --write` run, `GALLERY.md` committed if it changed
- [ ] `python3 scripts/find_overlaps.py --check` clean
- [ ] Any promoter: metadata updated (Version, Maturity), `Est. effort` present, `Inputs:` declared **and used** as `{{PLACEHOLDER}}`s
- [ ] Any promoter: verification table, failure handling, completion criteria are real, not headings
- [ ] Indexes updated: system `README.md`, root `README.md` table, `CHANGELOG.md`, `_meta/review-log.md`, `PROJECT-STATUS.md` if counts changed
- [ ] No new claim exceeds what the files do (this is the rule the validator exists to enforce)

## Evidence

<!-- For a promotion: what you checked and how. For a tooling change: the fixture that proves the new rule fires. "Reviewed" alone is not evidence. -->

## Honest limits

<!-- What this change does NOT do. Every merged change should be able to state one. -->
