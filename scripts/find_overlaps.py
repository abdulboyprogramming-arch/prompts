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

`--metric` may be given more than once. Every pair is scored on every signal in
the same pass, so `--metric shingle --metric combined` costs what one metric
costs: the second run is not a second read of 364 files. That is why the gate
list checks both signals in a single invocation.

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
import collections
from collections import defaultdict
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


BARS = {"shingle": 0.55, "vocab": 0.85, "structure": 0.80, "combined": 0.75}
FLOORS = {"shingle": 0.10, "vocab": 0.60, "structure": 0.60, "combined": 0.40}


def bars_for(metrics: list[str], ci_bar: float | None = None) -> dict[str, float]:
    """The failure bar per metric. A single explicit `--ci-bar` overrides the one metric."""
    if ci_bar is not None:
        return {metrics[0]: ci_bar}
    return {m: BARS[m] for m in metrics}


def failures_over(pairs: list[tuple], bars: dict[str, float]) -> list[tuple[str, float, float, str, str]]:
    """Every (metric, score, bar, a, b) that clears its bar, worst first.

    Pure, so the failure rule can be tested without a corpus: a pair that clears
    the bar on one signal and stays under it on another must report exactly one
    failure, and the metric must be named.
    """
    found: list[tuple[str, float, float, str, str]] = []
    for p in pairs:
        s = p[5] if len(p) > 5 else {}
        for metric, bar in bars.items():
            score = s.get(metric)
            if score is not None and score >= bar:
                found.append((metric, score, bar, p[3], p[4]))
    found.sort(key=lambda f: -f[1])
    return found


def shared_shingle_counts(keys: list[str], sh: dict[str, set[str]]) -> dict[tuple[int, int], int]:
    """How many 5-word shingles each document pair has in common, in one pass.

    Comparing every pair's shingle sets directly is the expensive part of this
    script: 66,066 pairs x ~460 shingles. Inverting the index and counting
    coincidences costs 0.02 s on the same corpus and gives identical counts,
    because a pair's intersection size is the number of shingles whose posting
    list contains both documents.
    """
    postings: dict[str, list[int]] = defaultdict(list)
    for i, key in enumerate(keys):
        for shingle in sh[key]:
            postings[shingle].append(i)
    counts: dict[tuple[int, int], int] = defaultdict(int)
    for docs in postings.values():
        if len(docs) > 1:
            for a, b in itertools.combinations(docs, 2):
                counts[(a, b)] += 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=None, help="minimum score to report (default: 0.10 shingle, 0.60 vocab, 0.60 structure)")
    ap.add_argument("--top", type=int, default=25, help="how many pairs to print")
    ap.add_argument("--check", action="store_true", help="exit 1 if any pair exceeds the CI bar")
    ap.add_argument("--metric", choices=("shingle", "vocab", "structure", "combined"), action="append",
                    default=None, metavar="METRIC",
                    help="which signal --check and the ranking use (default shingle); repeatable, "
                         "and repeating it costs nothing because every pair is scored on every signal anyway")
    ap.add_argument("--ci-bar", type=float, default=None, help="score that fails --check (default: 0.55 shingle, 0.85 vocab, 0.80 structure)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    metrics = args.metric or ["shingle"]
    if len(metrics) > 1 and args.ci_bar is not None:
        ap.error("--ci-bar applies to one metric; give it with a single --metric")
    bar = args.ci_bar if args.ci_bar is not None else {
        "shingle": 0.55, "vocab": 0.85, "structure": 0.80, "combined": 0.75,
    }[metrics[0]]
    floor = args.threshold if args.threshold is not None else min(FLOORS[m] for m in metrics)
    floors = {m: (args.threshold if args.threshold is not None else FLOORS[m]) for m in metrics}

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

    metric_set = set(metrics)
    keys = sorted(sh)
    shared = shared_shingle_counts(keys, sh)

    pairs = []
    for i, j in itertools.combinations(range(len(keys)), 2):
        a, b = keys[i], keys[j]
        s: dict[str, float] = {}
        # Structure is cheap (heading sets hold tens of members) and every
        # report prints it, so it is always computed even when only one other
        # metric decides the ranking.
        s["structure"] = jaccard(hd[a], hd[b])
        s["shingle"] = (shared.get((i, j), 0) / min(len(sh[a]), len(sh[b]))) if sh[a] and sh[b] else 0.0
        if "vocab" in metric_set or "combined" in metric_set:
            # For the combined metric, score = structure x vocabulary, so a pair
            # whose structure is already below the bar cannot clear it however
            # much vocabulary it shares. Skipping the vocabulary comparison for
            # those pairs is what makes this pass cheaper than two single-metric
            # passes, and it cannot change the result.
            if "vocab" in metric_set or s["structure"] >= floors["combined"]:
                s["vocab"] = containment(vb[a], vb[b])
                s["combined"] = s["structure"] * s["vocab"]
            else:
                # Structure alone rules it out; the exact vocabulary comparison
                # would be spent on a pair that cannot clear the bar.
                s["combined"] = 0.0
        keep = [m for m in metrics if s.get(m, 0.0) >= floors[m]]
        if not keep:
            continue
        # Every report prints all four signals, so a kept pair gets the ones the
        # ranking did not need.
        if "vocab" not in s:
            s["vocab"] = containment(vb[a], vb[b])
        if "combined" in metric_set:
            s["combined"] = s["structure"] * s["vocab"]
        s["shingle_jaccard"] = jaccard(sh[a], sh[b])
        best = max(s[m] for m in keep)
        pairs.append((best, s["shingle"], s["shingle_jaccard"], a, b, s))

    # Same order as before the optimisation: score, then the two supporting
    # signals, then the paths. A change in tie-break order would churn every
    # report that quotes the top pairs.
    pairs.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]), reverse=True)
    print_floor = floor
    label = " + ".join(metrics)

    if args.json:
        print(json.dumps(
            [{
                "score": round(p0[0], 3),
                "shingle_containment": round(p0[1], 3),
                "shingle_jaccard": round(p0[2], 3),
                "vocab_containment": round(p0[5].get("vocab", 0.0), 3),
                "structure_jaccard": round(p0[5].get("structure", 0.0), 3),
                "combined": round(p0[5].get("combined", 0.0), 3),
                "a": p0[3],
                "b": p0[4],
            } for p0 in pairs[:args.top]],
            indent=2,
        ))
    else:
        print(f"Compared {len(sh)} prompts across every pair.")
        print(f"Pairs at or above {label} {print_floor:.2f}: {len(pairs)}")
        print(f"Ranked by: {label}   (CI bar {bar:.2f})\n")
        if pairs:
            print(f"Highest {label} score: {pairs[0][0]:.2f}\n  {pairs[0][3]}\n  {pairs[0][4]}\n")
        else:
            print("No overlapping pairs at this threshold.")
        for p0 in pairs[:args.top]:
            s = p0[5]
            print(
                f"{p0[0]:5.2f} {label:9s} "
                f"shr {p0[1]:4.2f}  voc {s.get('vocab', 0.0):4.2f}  "
                f"str {s.get('structure', 0.0):4.2f}   {p0[3]}\n{'':48}{p0[4]}\n"
            )

    if args.check:
        failures = failures_over(pairs, bars_for(metrics, args.ci_bar))
        if failures:
            for metric, score, bar_value, a, b in failures[:10]:
                print(f"ERROR   {score:.2f} {metric} (bar {bar_value:.2f})  {a}  <->  {b}", file=sys.stderr)
            print(f"ERROR   {len(failures)} prompt pair(s) exceed "
                  f"{'a CI bar' if len(metrics) > 1 else f'{metrics[0]} {bar:.2f}'}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
