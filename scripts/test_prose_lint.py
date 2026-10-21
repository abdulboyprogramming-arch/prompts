#!/usr/bin/env python3
"""Regression tests for the prose lint.

A lint that is never tested is a lint that quietly stops matching. These fixtures
pin each detector, the false-positive cases that would make it unusable, and the
ratchet behaviour that lets a large corpus adopt it incrementally.

    python3 scripts/test_prose_lint.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lint_prose as L  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


def kinds(text: str) -> list[str]:
    return [f["kind"] for f in L.lint_text(text)]


def main() -> int:
    check("flags 'as appropriate'",
          "unactionable" in kinds("Choose a strategy as appropriate to the risk."))
    check("flags 'if necessary'",
          "unactionable" in kinds("Retry the request if necessary."))
    check("flags 'etc.' as an unfinished enumeration",
          "unactionable" in kinds("Record the name, version, licence, etc."))
    check("flags bare 'properly'",
          "unactionable" in kinds("Handle errors properly."))

    check("does not flag a concrete instruction",
          kinds("Run `pytest -q tests/unit` and paste the summary line.") == [])
    check("does not flag 'make sure to' when the sentence is concrete",
          "empty-intensifier" not in kinds("Make sure to run `python3 scripts/validate_library.py`."))
    check("flags an empty intensifier",
          "empty-intensifier" in kinds("Be careful with the migration."))
    check("does not flag a short sentence", "long-sentence" not in kinds("Write the report."))

    long_sentence = " ".join(["word"] * (L.MAX_SENTENCE_WORDS + 1)) + "."
    check("flags a sentence over the limit", "long-sentence" in kinds(long_sentence))
    at_limit = " ".join(["word"] * L.MAX_SENTENCE_WORDS) + "."
    check("does not flag a sentence at the limit", "long-sentence" not in kinds(at_limit))

    fenced = "```\nthis line is etc. and properly vague and should be ignored\n```\n"
    check("ignores fenced code", kinds(fenced) == [])

    n = len(L.lint_text("Record a, b, etc.\nRetry if necessary."))
    check("counts each finding once per line", n == 2, f"got {n}")

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
