#!/usr/bin/env python3
"""Run every gate in the order CI runs them, with one summary at the end.

The repository has nine checks and they drifted between three places: the CI
workflow, the contributor guide, and a paragraph in the publication checklist.
A contributor could not tell which list was authoritative, and a check added to
one list was not added to the others.

This script is the single source. CI calls it, `CONTRIBUTING.md` points at it,
and a local run is the same run the pull request will get.

    python3 scripts/check_all.py            # run every gate
    python3 scripts/check_all.py --fix      # regenerate the generated files first
    python3 scripts/check_all.py --quick    # skip the duplicate detector, the slow one

Exit status is 0 only when every gate passes. Output is one line per gate, then a
summary naming the failures, so a failing run can be read in a few seconds.

Why this is not a shell one-liner
---------------------------------
`--fix` has to regenerate in dependency order: the catalog and gallery read the
prompt files, the task index reads the prompts, and the evidence report reads the
registry. Running them alphabetically produces a stale file that the next check
then fails, which looks like a flaky build.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (gate name, argv, whether --quick skips it)
GATES: list[tuple[str, list[str], bool]] = [
    ("validator self-tests", ["scripts/test_validator.py"], False),
    ("validator", ["scripts/validate_library.py"], False),
    ("overlap self-tests", ["scripts/test_overlaps.py"], False),
    ("prose-lint self-tests", ["scripts/test_prose_lint.py"], False),
    ("prose lint", ["scripts/lint_prose.py", "--check"], False),
    ("task-index self-tests", ["scripts/test_task_index.py"], False),
    ("contract self-tests", ["scripts/test_contract.py"], False),
    ("prompt contracts", ["scripts/check_prompt_contract.py", "--check-report"], False),
    ("gallery current", ["scripts/generate_gallery.py", "--check", "--quiet"], False),
    ("task index current", ["scripts/generate_task_index.py", "--check"], False),
    ("evidence report current", ["scripts/evidence_report.py", "--check"], False),
    ("duplicate detector (shingle)", ["scripts/find_overlaps.py", "--check", "--top", "5"], True),
    ("duplicate detector (combined)", ["scripts/find_overlaps.py", "--check", "--metric", "combined", "--top", "5"], True),
]

# Regeneration, in dependency order. --fix runs this before the gates.
REGENERATE: list[tuple[str, list[str]]] = [
    ("catalog", ["scripts/validate_library.py", "--catalog"]),
    ("gallery", ["scripts/generate_gallery.py", "--write"]),
    ("task index", ["scripts/generate_task_index.py", "--write"]),
    ("evidence report", ["scripts/evidence_report.py", "--write"]),
    ("conformance report", ["scripts/check_prompt_contract.py", "--write-report"]),
]


CATALOG = os.path.join("_meta", "CATALOG.md")


def catalog_is_current() -> tuple[bool, str]:
    """`--catalog` rewrites the file, so currency means "the rewrite changes nothing"."""
    path = os.path.join(ROOT, CATALOG)
    before = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    code, out = run(["scripts/validate_library.py", "--catalog"])
    if code != 0:
        return False, out
    after = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if before != after:
        open(path, "w", encoding="utf-8").write(before)  # leave the tree as we found it
        return False, f"{CATALOG} was stale; run: python3 scripts/validate_library.py --catalog"
    return True, ""


def run(argv: list[str]) -> tuple[int, str]:
    proc = subprocess.run([PY] + argv, cwd=ROOT, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true", help="regenerate the generated files before checking")
    ap.add_argument("--quick", action="store_true", help="skip the duplicate detector")
    ap.add_argument("--verbose", action="store_true", help="print each gate's output, not just its status")
    args = ap.parse_args()

    if args.fix:
        for name, argv in REGENERATE:
            code, out = run(argv)
            status = "ok" if code == 0 else "FAILED"
            print(f"  regenerate {name}: {status}")
            if code != 0:
                print(out.rstrip())
                return code
        print()

    failures: list[str] = []
    ok, out = catalog_is_current()
    print(f"  {'PASS' if ok else 'FAIL'}  catalog current")
    if not ok:
        failures.append("catalog current")
        print(f"          {out.strip().splitlines()[-1] if out.strip() else ''}")

    for name, argv, skippable in GATES:
        if args.quick and skippable:
            print(f"  SKIP  {name}")
            continue
        code, out = run(argv)
        print(f"  {'PASS' if code == 0 else 'FAIL'}  {name}")
        if code != 0:
            failures.append(name)
            if args.verbose:
                print(out.rstrip())
            else:
                tail = [ln for ln in out.strip().splitlines() if ln.strip()][-3:]
                for line in tail:
                    print(f"          {line}")

    print()
    if failures:
        print(f"{len(failures)} gate(s) failed: {', '.join(failures)}")
        print("Run with --verbose for the full output of each failing gate.")
        return 1
    print("All gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
