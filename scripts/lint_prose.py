#!/usr/bin/env python3
"""Prose lint for prompt files: the defects a structural validator cannot see.

`validate_library.py` proves that a prompt *has* a verification section. It cannot
see that the section says "verify it works properly". This script reads for the
failure modes that make a prompt unusable in practice:

1. **Unactionable qualifiers** — "as appropriate", "if necessary", "handle errors
   properly". Each one delegates a decision back to the model, which is exactly
   what a prompt exists to prevent.
2. **Run-on instructions** — sentences over 55 words, which readers (human and
   model) skim rather than follow.
3. **Empty intensifiers in rules** — "be careful", "make sure to", "ensure that
   the code is good" without saying what good means.

Adoption model: a **ratchet that has closed**. When these rules were written the
library already contained the phrases, and failing the build on all of them would
have blocked every change; `--check` therefore compares against a recorded
baseline rather than zero. The corpus was then burned down to **zero findings**
(v2.22.0), so the baseline file records `0` and the ratchet is now a hard gate:
any new unactionable phrase or 56-word sentence fails CI. `--write-baseline` still
exists, but raising the number is now a decision that needs a reason in the commit.

Usage
-----
    python3 scripts/lint_prose.py                 # summary by file, worst first
    python3 scripts/lint_prose.py --file <path>   # one file, with line numbers
    python3 scripts/lint_prose.py --check         # exit 1 if findings exceed baseline
    python3 scripts/lint_prose.py --write-baseline
    python3 scripts/lint_prose.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import ROOT, is_archive, load  # noqa: E402

BASELINE = os.path.join(ROOT, "_meta", "prose-lint-baseline.json")
MAX_SENTENCE_WORDS = 55

# Phrases that hand a decision back to the reader. Ordered longest-first so the
# reported match is the whole phrase rather than its first word.
UNACTIONABLE = [
    "as appropriate",
    "as needed",
    "if necessary",
    "if needed",
    "where appropriate",
    "when appropriate",
    "handle errors properly",
    "handle appropriately",
    "use best practices",
    "follow best practices",
    "industry best practices",
    "and so on",
    "etc.",
    "and the like",
    "various things",
    "somehow",
    "in some way",
    "to some extent",
    "as required",
    "reasonable amount",
    "properly",
    "adequately",
    "suitably",
    "judiciously",
    "where possible",
]

# Intensifiers that assert care instead of specifying it. Only flagged when the
# sentence does not also contain a concrete instruction (a command, a path, or a
# number), because "make sure to run pytest -q" is actionable.
EMPTY_INTENSIFIERS = [
    "be careful",
    "make sure to",
    "make sure that",
    "ensure that the",
    "be thorough",
    "take care to",
    "be diligent",
]

CONCRETE = re.compile(r"(`[^`]+`|/[a-z0-9_.-]+/|\b\d+\b|run |execute |paste |record |write )", re.IGNORECASE)


def split_sentences(text: str) -> list[str]:
    # Deliberately crude: prompts are prose with lists, not literature.
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def lint_text(text: str) -> list[dict]:
    findings: list[dict] = []
    lines = text.splitlines()
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        low = line.lower()
        for phrase in UNACTIONABLE:
            if phrase in low:
                findings.append({
                    "line": i,
                    "kind": "unactionable",
                    "match": phrase,
                    "text": line.strip()[:160],
                })
        if any(p in low for p in EMPTY_INTENSIFIERS) and not CONCRETE.search(line):
            findings.append({
                "line": i,
                "kind": "empty-intensifier",
                "match": next(p for p in EMPTY_INTENSIFIERS if p in low),
                "text": line.strip()[:160],
            })
        for sentence in split_sentences(line):
            words = sentence.split()
            if len(words) > MAX_SENTENCE_WORDS:
                findings.append({
                    "line": i,
                    "kind": "long-sentence",
                    "match": f"{len(words)} words",
                    "text": sentence[:160],
                })
    return findings


def collect() -> tuple[dict[str, list[dict]], int]:
    """Return findings per file, and how many files were actually read.

    The second value exists because the summary used to report `len(per_file)` as
    "across N prompt files" — the number of files *with* findings. On a clean corpus
    that printed "0 findings across 0 prompt files", which reads like a gate that
    scanned nothing. A gate's summary should say what it scanned, not only what it
    found.
    """
    docs = load(ROOT)
    out: dict[str, list[dict]] = {}
    scanned = 0
    for d in docs:
        if not d.is_prompt or is_archive(d.rel) or d.rel.split(os.sep)[0] in {"_meta", "archive"}:
            continue
        scanned += 1
        findings = lint_text(d.text)
        if findings:
            out[d.rel.replace(os.sep, "/")] = findings
    return out, scanned


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="lint one file (path relative to the repository root)")
    ap.add_argument("--check", action="store_true", help="exit 1 if findings exceed the baseline")
    ap.add_argument("--write-baseline", action="store_true", help="record the current totals as the baseline")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--top", type=int, default=20, help="how many files to list")
    args = ap.parse_args()

    if args.file:
        path = os.path.join(ROOT, args.file)
        if not os.path.exists(path):
            print(f"ERROR   no such file: {args.file}", file=sys.stderr)
            return 1
        findings = lint_text(open(path, encoding="utf-8").read())
        for f in findings:
            print(f"{args.file}:{f['line']}  {f['kind']}: {f['match']}")
            print(f"    {f['text']}")
        print(f"\n{len(findings)} finding(s)")
        return 0

    per_file, scanned = collect()
    total = sum(len(v) for v in per_file.values())
    kinds: dict[str, int] = {}
    for fs in per_file.values():
        for f in fs:
            kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1

    if args.write_baseline:
        with open(BASELINE, "w", encoding="utf-8") as fh:
            json.dump({"total": total, "by_kind": kinds}, fh, indent=2)
            fh.write("\n")
        print(f"Baseline written: {total} findings ({kinds})")
        return 0

    baseline = {"total": 0}
    if os.path.exists(BASELINE):
        baseline = json.load(open(BASELINE, encoding="utf-8"))

    if args.json:
        print(json.dumps({
            "total": total,
            "baseline": baseline.get("total", 0),
            "by_kind": kinds,
            "scanned": scanned,
            "files": {k: len(v) for k, v in sorted(per_file.items(), key=lambda kv: -len(kv[1]))[:args.top]},
        }, indent=2))
    else:
        print(f"{total} findings across {scanned} prompt files (baseline {baseline.get('total', 0)})")
        print("  " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items(), key=lambda kv: -kv[1])))
        print()
        for rel, fs in sorted(per_file.items(), key=lambda kv: -len(kv[1]))[:args.top]:
            print(f"{len(fs):4d}  {rel}")
            for f in fs[:3]:
                print(f"        L{f['line']} {f['kind']}: {f['match']}")

    if args.check:
        allowed = baseline.get("total", 0)
        if total > allowed:
            print(
                f"\nERROR   prose lint regressed: {total} findings, baseline {allowed}. "
                f"Fix the new findings, or run --write-baseline if the increase is justified.",
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
