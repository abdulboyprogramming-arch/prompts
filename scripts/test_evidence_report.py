#!/usr/bin/env python3
"""Regression tests for the published-count scan in `evidence_report.py`.

`--check` compared one generated file and nothing else, so the README, the
quickstart, the status page and five `_meta/` documents each restated a ratio
the registry had already left behind. Fourteen hand-written copies were stale
when the scan was written, and every one of them was in a file a reader is more
likely to read than the generated table.

The cases below pin the scan's shape rather than the current numbers:

  * a count that disagrees with the registry is reported, with file and line;
  * a count that agrees is not reported;
  * dated records are exempt, because correcting them would rewrite history;
  * a zeroth count, which is only ever the independent-run figure, is skipped,
    and that skip does not swallow an ordinary stale count.

Usage
-----
    python3 scripts/test_evidence_report.py

Exit code 0 means every case behaved as specified.
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_report  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def ok(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, condition, detail))


COUNTS = {"operational": 228, "operational_evaluated": 17}


class TempRepo:
    """A throwaway ROOT holding a fixed set of pages."""

    def __init__(self, pages: dict[str, str]):
        self.pages = pages

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        for rel, text in self.pages.items():
            path = os.path.join(self.root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        self.saved = evidence_report.ROOT
        evidence_report.ROOT = self.root
        return self

    def __exit__(self, *exc):
        evidence_report.ROOT = self.saved
        self.tmp.cleanup()
        return False


def scan(pages: dict[str, str]) -> list[str]:
    with TempRepo(pages):
        return evidence_report.published_claims(COUNTS)


def main() -> int:
    # A stale copy in a page a reader lands on.
    found = scan({"README.md": "The library says 14 of 228 prompts were run.\n"})
    ok("stale count in the README is reported", len(found) == 1, repr(found))
    ok("the report names file and line", found and found[0].startswith("README.md:1:"),
       repr(found))
    ok("the report quotes both numbers", found and "14 of 228" in found[0] and "17 of 228" in found[0],
       repr(found))

    # The current number is not a finding, wherever it appears.
    ok("current count passes", scan({"README.md": "17 of 228 prompts were run.\n"}) == [])
    ok("count in a _meta page is scanned too",
       len(scan({"_meta/publication-checklist.md": "14 of 228 executed\n"})) == 1)

    # Dated records: correcting these would falsify the record.
    ok("a dated evaluation is exempt",
       scan({"_meta/empirical-evaluation-09.md": "9 of 228 at the time.\n"}) == [])
    ok("the changelog is exempt", scan({"CHANGELOG.md": "4 of 228 in this release.\n"}) == [])
    ok("the review log is exempt", scan({"_meta/review-log.md": "library total 9 of 228\n"}) == [])

    # The one skip: zero counts the independent-run figure, a different metric
    # that happens to share the denominator.
    ok("a zeroth count is skipped", scan({"_meta/x.md": "Runs by another person: 0 of 228.\n"}) == [])
    ok("a stale non-zero count on a similar line is still reported",
       len(scan({"_meta/x.md": "Independent review covered 14 of 228\n"})) == 1)

    # The generated file is compared byte for byte, so scanning it would double-report.
    ok("the generated report is exempt",
       scan({"_meta/evidence-levels.md": "| executed | 14 |\n14 of 228\n"}) == [])

    # A different denominator is a different claim.
    ok("a count over another denominator is not flagged",
       scan({"README.md": "3 of 68 batches complete.\n"}) == [])

    passed = sum(1 for _, good, _ in RESULTS if good)
    for name, good, detail in RESULTS:
        print(f"{'PASS' if good else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not good else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
