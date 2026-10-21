#!/usr/bin/env python3
"""Regression tests for the near-duplicate detector.

`find_overlaps.py` decides what counts as a duplicate, and a detector that is
never exercised is indistinguishable from one that checks nothing. These
fixtures pin the behaviour that matters:

- identical documents score 1.0 on every signal;
- unrelated documents score 0;
- reordered content keeps vocabulary overlap but loses shingle overlap, which is
  why the vocabulary metric exists;
- a clone with different nouns keeps structure at 1.0 and vocabulary high, which
  is why the combined metric exists;
- the shared boilerplate every prompt in this repository carries is stripped, so
  two prompts are not called duplicates because both have a Verification section.

Run it before changing any metric or threshold:

    python3 scripts/test_overlaps.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import find_overlaps as fo  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


SECTIONS = """
## Role and mandate
You are a specialist reviewing a system for a specific failure class.

## Workflow
1. Enumerate the assets that matter and record where each one is evidenced.
2. Inspect the configuration rather than the documentation.

## Verification
Run the checks and record the results.

## Completion criteria
- Every asset has an owner.
"""


def doc(objective: str, body: str) -> str:
    return f"""# PROMPT 01 — Example

**Identifier:** TEST-01
**System:** test
**Version:** 1.0.0

## Role and mandate
{objective}

{body}
"""


def main() -> int:
    a = doc("You audit backups and prove restores work.", SECTIONS)
    b = doc("You audit backups and prove restores work.", SECTIONS)
    c = doc("You review colour contrast against WCAG for portal screens.", """
## Workflow
1. Measure contrast ratios for every text and non-text element on the portal.
2. Record the ratio, the pair, and the failing threshold in a table.

## Completion criteria
- Each contrast failure is listed with its measured ratio.
""")
    # Same sentences, different order: shingles drop, vocabulary does not.
    reordered = doc("You audit backups and prove restores work.", """
2. Inspect the configuration rather than the documentation.
1. Enumerate the assets that matter and record where each one is evidenced.
""")
    # A reworded clone: same structure, same vocabulary, different sentence order
    # and enough rewording that the 5-word shingle signal collapses. This is the
    # duplicate a reader misses and a shingle-only detector never reports.
    clone = doc("You audit backups and prove restores work.", """
## Workflow
Record where each asset is evidenced, then enumerate the assets that matter.
Inspect the configuration; do not inspect the documentation.

## Verification
Checks are run, and the results are recorded.

## Completion criteria
- Each asset has an owner.
""")

    check("identical shingle containment is 1.0", fo.containment(fo.shingles(fo.body(a)), fo.shingles(fo.body(b))) == 1.0)
    check("identical vocabulary containment is 1.0", fo.containment(fo.vocabulary(fo.body(a)), fo.vocabulary(fo.body(b))) == 1.0)
    check("identical structure jaccard is 1.0", fo.jaccard(fo.headings(a), fo.headings(b)) == 1.0)

    unrel_shr = fo.containment(fo.shingles(fo.body(a)), fo.shingles(fo.body(c)))
    unrel_voc = fo.containment(fo.vocabulary(fo.body(a)), fo.vocabulary(fo.body(c)))
    check("unrelated prompts score below the reporting floor", unrel_shr < 0.10 and unrel_voc < 0.60,
          f"shingle={unrel_shr:.2f} vocab={unrel_voc:.2f}")

    reord_shr = fo.containment(fo.shingles(fo.body(a)), fo.shingles(fo.body(reordered)))
    reord_voc = fo.containment(fo.vocabulary(fo.body(a)), fo.vocabulary(fo.body(reordered)))
    check("reordered content loses shingle overlap", reord_shr < 0.60, f"shingle={reord_shr:.2f}")
    check("reordered content keeps vocabulary overlap", reord_voc > reord_shr, f"vocab={reord_voc:.2f}")

    clone_str = fo.jaccard(fo.headings(a), fo.headings(clone))
    clone_voc = fo.containment(fo.vocabulary(fo.body(a)), fo.vocabulary(fo.body(clone)))
    clone_shr = fo.containment(fo.shingles(fo.body(a)), fo.shingles(fo.body(clone)))
    check("a clone keeps structure at 1.0", clone_str == 1.0, f"structure={clone_str:.2f}")
    check("a clone keeps vocabulary high", clone_voc >= 0.40, f"vocab={clone_voc:.2f}")
    check("a clone defeats the shingle metric", clone_shr < 0.20, f"shingle={clone_shr:.2f}")
    check("the combined metric catches the clone", clone_str * clone_voc >= 0.40,
          f"combined={clone_str * clone_voc:.2f}")

    h = fo.headings(a)
    check("boilerplate headings are stripped", not any(x.startswith("verification") for x in h), str(sorted(h)))
    check("numbered headings normalise", "workflow" in h and "1. workflow" not in h, str(sorted(h)))
    check("metadata block is not body text", "identifier" not in fo.body(a).lower())

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
