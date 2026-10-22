#!/usr/bin/env python3
"""Regression tests for the gate list itself.

`scripts/check_all.py` is the single source of truth for what "validated"
means in this repository, and until now it was the only script with no tests.
That is the wrong one to leave untested: a defect in the runner either hides a
failing gate or, as happened here, corrupts the working tree while reporting
that a gate failed.

The cases below pin three things:

  * the catalog check leaves the tree exactly as it found it, whether the
    validator passed, failed, or rewrote the file on its way out;
  * a catalog that does not exist is restored by deleting it, not by leaving an
    empty file where a generated one used to be;
  * every gate names a script that exists, and no gate name is duplicated.

The catalog cases drive a fake `run`, so they test the runner's own logic
without needing a broken repository to point it at.

Usage
-----
    python3 scripts/test_check_all.py

Exit code 0 means every case behaved as specified.
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_all  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def ok(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, condition, detail))


class TempRepo:
    """A throwaway ROOT with a catalog file, and a scripted stand-in for `run`."""

    def __init__(self, initial: str | None):
        self.dir = tempfile.TemporaryDirectory()
        self.root = self.dir.name
        os.makedirs(os.path.join(self.root, "_meta"), exist_ok=True)
        self.path = os.path.join(self.root, check_all.CATALOG)
        if initial is not None:
            with open(self.path, "w", encoding="utf-8") as fh:
                fh.write(initial)
        self._saved = (check_all.ROOT, check_all.run)

    def script(self, code: int, write: str | None) -> None:
        """Replace `run` so that the fake validator returns `code` and optionally writes."""

        def fake_run(argv):  # noqa: ANN001
            if write is not None:
                with open(self.path, "w", encoding="utf-8") as fh:
                    fh.write(write)
            return code, "pretend output"

        check_all.ROOT = self.root
        check_all.run = fake_run

    def read(self) -> str | None:
        if not os.path.exists(self.path):
            return None
        with open(self.path, encoding="utf-8") as fh:
            return fh.read()

    def __enter__(self) -> "TempRepo":
        return self

    def __exit__(self, *exc) -> None:  # noqa: ANN002
        check_all.ROOT, check_all.run = self._saved
        self.dir.cleanup()


def main() -> int:
    # A failing validator that rewrites the catalog must not leave the rewrite behind.
    with TempRepo("ORIGINAL\n") as repo:
        repo.script(code=1, write="BROKEN REWRITE\n")
        current, _ = check_all.catalog_is_current()
        ok("a failing validator reports the catalog as not current", current is False)
        ok("a failing validator leaves the catalog unchanged", repo.read() == "ORIGINAL\n",
           repr(repo.read()))

    # A passing validator whose rewrite is identical is current, and still untouched.
    with TempRepo("SAME\n") as repo:
        repo.script(code=0, write="SAME\n")
        current, _ = check_all.catalog_is_current()
        ok("an identical rewrite is current", current is True, str(current))
        ok("an identical rewrite leaves the file alone", repo.read() == "SAME\n")

    # A passing validator whose rewrite differs is stale, and the tree is restored.
    with TempRepo("OLD\n") as repo:
        repo.script(code=0, write="NEW\n")
        current, message = check_all.catalog_is_current()
        ok("a differing rewrite is reported stale", current is False)
        ok("the stale message names the file", check_all.CATALOG in message, message)
        ok("a stale catalog is restored before returning", repo.read() == "OLD\n",
           repr(repo.read()))

    # A missing catalog must stay missing: writing "" would create an empty generated file.
    with TempRepo(None) as repo:
        repo.script(code=1, write="CREATED BY FAILING RUN\n")
        check_all.catalog_is_current()
        ok("a catalog that did not exist is removed again", repo.read() is None,
           repr(repo.read()))

    # The gate list itself: every script it names exists, and names are unique.
    missing = [
        argv[0]
        for _, argv, _ in check_all.GATES
        if not os.path.exists(os.path.join(check_all.ROOT, argv[0]))
    ] + [
        argv[0]
        for _, argv in check_all.REGENERATE
        if not os.path.exists(os.path.join(check_all.ROOT, argv[0]))
    ]
    ok("every gate names a script that exists", not missing, ", ".join(sorted(set(missing))))

    names = [name for name, _, _ in check_all.GATES]
    ok("no gate name is duplicated", len(names) == len(set(names)),
       ", ".join(sorted({n for n in names if names.count(n) > 1})))

    passed = sum(1 for _, good, _ in RESULTS if good)
    for name, good, detail in RESULTS:
        print(f"{'PASS' if good else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not good else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
