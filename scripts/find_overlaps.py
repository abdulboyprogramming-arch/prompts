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
4. Report up to four numbers per pair:
   - **shingle containment** — what share of the smaller prompt's 5-word
     sequences appears in the larger; catches copy-paste and template reuse.
   - **shingle jaccard** — overall similarity, symmetric.
   - **vocabulary containment** — order-insensitive overlap of content words.
     Catches the same content reordered or lightly rewritten, which shingles miss.
   - **structure similarity** — Jaccard over section headings. Catches a prompt
     that was cloned structurally and then re-worded, the hardest duplicate to
     see by reading.
   - **combined** (`structure × vocabulary`) — the useful form of the previous
     two. Structure alone is near 1.0 for every pair, because every prompt in
     this library follows one template; multiplied by vocabulary overlap it
     separates "house style" from "same prompt with different nouns".

All four metrics answer a different question, and none of them detects a
**paraphrase with different vocabulary**; that remains a human judgement, and
this tool's job is to make the reading list short rather than to replace it.

Usage
-----
    python3 scripts/find_overlaps.py                  # report top pairs
    python3 scripts/find_overlaps.py --threshold 0.3  # stricter
    python3 scripts/find_overlaps.py --check          # exit 1 if any pair is above a high bar
    python3 scripts/find_overlaps.py --metric vocab --top 10
    python3 scripts/find_overlaps.py --json           # machine-readable

`--check` uses a deliberately high threshold so CI fails only on genuine
duplication, not on prompts that legitimately share a vocabulary. The default
metric is shingle containment (0.55). `--metric vocab` uses 0.85, and
`--metric structure` uses 0.80, because those signals run higher for prompts in
the same system by design. `--metric combined` uses 0.75 — identical structure
*and* three quarters of the content words — which is a clone rather than a
variant. The combined metric ranks the library's own skeleton families highest,
which is correct: `01-contribution` holds several parallel variants of the same
stage sequence, and they are legitimately similar and legitimately duplicated.
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


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9_]+", text.lower()) if w not in STOPWORDS and len(w) > 2]


def shingles(text: str) -> set[str]:
    ws = words(text)
    if len(ws) < SHINGLE:
        return set()
    return {" ".join(ws[i:i + SHINGLE]) for i in range(len(ws) - SHINGLE + 1)}


def vocabulary(text: str) -> set[str]:
    """Content words as a set — order-insensitive overlap."""
    return set(words(text))


def headings(text: str) -> set[str]:
    """Section headings, normalised, minus the boilerplate every prompt shares."""
    out = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        title = re.sub(r"[^a-z0-9 ]", "", line.lstrip("# ").strip().lower())
        title = " ".join(title.split())
        if not title or any(title.startswith(h) for h in BOILERPLATE_HEADINGS):
            continue
        # Drop the leading section number, so "1. Workflow" == "Workflow".
        out.add(re.sub(r"^[0-9]+\s*", "", title))
    return out


def containment(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=None, help="minimum score to report (default: 0.10 shingle, 0.60 vocab, 0.60 structure)")
    ap.add_argument("--top", type=int, default=25, help="how many pairs to print")
    ap.add_argument("--check", action="store_true", help="exit 1 if any pair exceeds the CI bar")
    ap.add_argument("--metric", choices=("shingle", "vocab", "structure", "combined"), default="shingle",
                    help="which signal --check and the ranking use (default shingle)")
    ap.add_argument("--ci-bar", type=float, default=None, help="score that fails --check (default: 0.55 shingle, 0.85 vocab, 0.80 structure)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    bar = args.ci_bar if args.ci_bar is not None else {
        "shingle": 0.55, "vocab": 0.85, "structure": 0.80, "combined": 0.75,
    }[args.metric]
    floor = args.threshold if args.threshold is not None else {
        "shingle": 0.10, "vocab": 0.60, "structure": 0.60, "combined": 0.40,
    }[args.metric]

    docs = load(ROOT)
    prompts = [d for d in docs if d.is_prompt and not is_archive(d.rel) and d.rel.split(os.sep)[0] != "_meta"]
    sh: dict[str, set[str]] = {}
    vb: dict[str, set[str]] = {}
    hd: dict[str, set[str]] = {}
    for d in prompts:
        b = body(d.text)
        sh[d.rel] = shingles(b)
        vb[d.rel] = vocabulary(b)
        hd[d.rel] = headings(d.text)

    def metric_value(a: str, b: str) -> float:
        if args.metric == "vocab":
            return containment(vb[a], vb[b])
        if args.metric == "structure":
            return jaccard(hd[a], hd[b])
        if args.metric == "combined":
            return jaccard(hd[a], hd[b]) * containment(vb[a], vb[b])
        return containment(sh[a], sh[b])

    # Every pair is scored on every metric: the point of a second signal is to
    # catch the pairs the first one misses, so it cannot be pre-filtered by it.
    pairs = []
    for a, b in itertools.combinations(sorted(sh), 2):
        if a == b:
            continue
        score = metric_value(a, b)
        if score < floor:
            continue
        pairs.append((score, containment(sh[a], sh[b]), jaccard(sh[a], sh[b]), a, b))

    pairs.sort(reverse=True)
    print_floor = floor

    if args.json:
        print(json.dumps(
            [{
                "score": round(s0, 3),
                "shingle_containment": round(c, 3),
                "shingle_jaccard": round(j, 3),
                "vocab_containment": round(containment(vb[a], vb[b]), 3),
                "structure_jaccard": round(jaccard(hd[a], hd[b]), 3),
                "a": a,
                "b": b,
            } for s0, c, j, a, b in pairs[:args.top]],
            indent=2,
        ))
    else:
        print(f"Compared {len(sh)} prompts across every pair.")
        print(f"Pairs at or above {args.metric} {print_floor:.2f}: {len(pairs)}")
        print(f"Ranked by: {args.metric}   (CI bar {bar:.2f})\n")
        if pairs:
            s0, c, j, a, b = pairs[0]
            print(f"Highest {args.metric} score: {s0:.2f}\n  {a}\n  {b}\n")
        else:
            print("No overlapping pairs at this threshold.")
        for s0, c, j, a, b in pairs[:args.top]:
            print(
                f"{s0:5.2f} {args.metric:9s} "
                f"shr {c:4.2f}  voc {containment(vb[a], vb[b]):4.2f}  "
                f"str {jaccard(hd[a], hd[b]):4.2f}   {a}\n{'':48}{b}\n"
            )

    if args.check:
        worst = [p for p in pairs if p[0] >= bar]
        if worst:
            print(f"ERROR   {len(worst)} prompt pair(s) exceed {args.metric} {bar:.2f}", file=sys.stderr)
            for s0, _, _, a, b in worst[:10]:
                print(f"  {s0:.2f}  {a}  <->  {b}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
