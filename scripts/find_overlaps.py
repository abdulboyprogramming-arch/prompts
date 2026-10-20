#!/usr/bin/env python3
"""Find near-duplicate prompts — the redundancy that dilutes a prompt library.

Volume is not coverage. Two prompts that say the same thing in different words
make the library harder to choose from and impossible to maintain: a fix lands
in one and not the other.

Method
------
1. Strip metadata, code fences, headings and boilerplate sections that every
   prompt shares (verification tables, completion-criteria checklists).
2. Tokenise to lowercase words, dropping stopwords and short tokens.
3. Build 5-word shingles (overlapping) and compare prompts pairwise.
4. Report two numbers:
   - **Jaccard** — overall similarity of the two documents.
   - **containment** — what share of the *smaller* prompt appears in the larger;
     this is what catches "template copied into three systems".

Usage
-----
    python3 scripts/find_overlaps.py                  # report top pairs
    python3 scripts/find_overlaps.py --threshold 0.3  # stricter
    python3 scripts/find_overlaps.py --check          # exit 1 if any pair is above a high bar
    python3 scripts/find_overlaps.py --json           # machine-readable

`--check` uses a deliberately high threshold (0.55 containment) so CI fails only
on genuine duplication, not on prompts that legitimately share a vocabulary.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import ROOT, is_archive, load  # noqa: E402

SHINGLE = 5
BOILERPLATE_HEADINGS = (
    "verification",
    "completion criteria",
    "deliverables",
    "failure handling",
    "security and authorisation",
    "prerequisites",
)

STOPWORDS = set("""
a an the and or if then than that this these those is are was were be been being
to of in on for with without by from as at into over under not no nor but so such
it its their there here we you your our they them he she his her i me my
must should may can could would will shall do does did done make made use used
using per each any all more most less least other same own only also just
""".split())


def body(text: str) -> str:
    """Prompt body without metadata, code fences, or shared boilerplate sections."""
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    skip_section = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            title = line.lstrip("# ").strip().lower()
            skip_section = any(title.startswith(h) for h in BOILERPLATE_HEADINGS)
            continue
        if skip_section:
            continue
        if re.match(r"^\*\*[A-Z][a-zA-Z /-]{1,30}:\*\*", line.strip()):
            continue
        out.append(line)
    return "\n".join(out)


def shingles(text: str) -> set[str]:
    words = [w for w in re.findall(r"[a-z0-9_]+", text.lower()) if w not in STOPWORDS and len(w) > 2]
    if len(words) < SHINGLE:
        return set()
    return {" ".join(words[i:i + SHINGLE]) for i in range(len(words) - SHINGLE + 1)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=0.10, help="minimum containment to report (default 0.10)")
    ap.add_argument("--top", type=int, default=25, help="how many pairs to print")
    ap.add_argument("--check", action="store_true", help="exit 1 if any pair exceeds the CI bar")
    ap.add_argument("--ci-bar", type=float, default=0.55, help="containment that fails --check")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    docs = load(ROOT)
    prompts = [d for d in docs if d.is_prompt and not is_archive(d.rel) and d.rel.split(os.sep)[0] != "_meta"]
    sh: dict[str, set[str]] = {}
    for d in prompts:
        s = shingles(body(d.text))
        if s:
            sh[d.rel] = s

    pairs = []
    for a, b in itertools.combinations(sorted(sh), 2):
        sa, sb = sh[a], sh[b]
        shared = len(sa & sb)
        if not shared:
            continue
        containment = shared / min(len(sa), len(sb))
        if containment < args.threshold:
            continue
        jaccard = shared / len(sa | sb)
        pairs.append((containment, jaccard, a, b))

    pairs.sort(reverse=True)

    if args.json:
        print(json.dumps(
            [{"containment": round(c, 3), "jaccard": round(j, 3), "a": a, "b": b} for c, j, a, b in pairs[:args.top]],
            indent=2,
        ))
    else:
        print(f"Compared {len(sh)} prompts with at least one {SHINGLE}-word shingle.")
        print(f"Pairs at or above containment {args.threshold:.2f}: {len(pairs)}\n")
        if pairs:
            c, j, a, b = pairs[0]
            print(f"Highest containment: {c:.2f} ({j:.2f} jaccard)\n  {a}\n  {b}\n")
        else:
            print("No overlapping pairs at this threshold.")
        for c, j, a, b in pairs[:args.top]:
            print(f"{c:5.2f} contained  {j:5.2f} jaccard   {a}\n{'':30}{b}\n")

    if args.check:
        worst = [p for p in pairs if p[0] >= args.ci_bar]
        if worst:
            print(f"ERROR   {len(worst)} prompt pair(s) exceed containment {args.ci_bar:.2f}", file=sys.stderr)
            for c, _, a, b in worst[:10]:
                print(f"  {c:.2f}  {a}  <->  {b}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
