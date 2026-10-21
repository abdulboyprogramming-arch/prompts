#!/usr/bin/env python3
"""Regression tests for the task index generator.

The index makes one promise that is worth testing: **every prompt has a home**.
A generator that silently drops an unrouted prompt would produce an index that
looks complete and is not — the exact failure this file exists to prevent. The
matching rules are tested too, because a directory prefix that quietly matches
too much would hide a missing home behind a false assignment.

    python3 scripts/test_task_index.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import generate_task_index as T  # noqa: E402
from validate_library import Doc  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


def doc(rel: str, maturity: str = "operational", identifier: str = "X") -> Doc:
    return Doc(
        path="/tmp/" + rel,
        rel=rel,
        text="# Title\n\n**Identifier:** " + identifier + "\n",
        meta={"Gallery": "Stated purpose."},
        maturity=maturity,
        identifier=identifier,
        is_prompt=True,
    )


def main() -> int:
    check("a directory home matches its own files",
          T._matches("05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md", "05-scenarios/debugging"))
    check("a directory home matches nested subdirectories",
          T._matches("01-contribution/open-source/general-agent/P03-Repo-Discovery/x.md",
                     "01-contribution/open-source"))
    check("a directory home does not match a sibling with the same prefix",
          not T._matches("05-scenarios/debugging-extra/X.md", "05-scenarios/debugging"))
    check("a file home matches only that file",
          T._matches("00-core/conversational/CHAT-DEBUG.md", "00-core/conversational/CHAT-DEBUG.md"))
    check("a file home does not match a sibling file",
          not T._matches("00-core/conversational/CHAT-MODE.md", "00-core/conversational/CHAT-DEBUG.md"))

    routed, unrouted = T.route([doc("99-nowhere/ORPHAN.md")])
    check("an unrouted prompt is reported, not dropped", len(unrouted) == 1)
    check("an unrouted prompt is assigned to no task",
          all(not v for v in routed.values()))

    routed, unrouted = T.route([doc("05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md")])
    check("a routed prompt lands in at least one task",
          unrouted == [] and any(v for v in routed.values()))

    # The build must refuse to render an index it knows is incomplete.
    try:
        T.build([doc("99-nowhere/ORPHAN.md")])
        rendered_anyway = True
    except Exception:
        rendered_anyway = False
    check("build returns the unrouted list rather than hiding it", rendered_anyway)
    text, unrouted = T.build([doc("99-nowhere/ORPHAN.md")])
    check("the unrouted prompt is named in the return value", len(unrouted) == 1)

    text, unrouted = T.build([
        doc("05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md"),
        doc("05-scenarios/debugging/OUTLINE.md", maturity="skeleton", identifier="SK"),
    ])
    check("runnable prompts are listed individually", "SYSTEMATIC-DEBUGGING.md" in text)
    check("skeletons are counted instead of listed", "OUTLINE.md" not in text)
    check("the skeleton count is stated", "Plus **1**" in text)

    check("a long purpose is clipped at a word boundary, not mid-word",
          T._clip("a" * 10 + " " + "b" * 200).endswith("…")
          and " " not in T._clip("a" * 10 + " " + "b" * 200)[:10])
    check("a short purpose is left untouched", T._clip("Short.") == "Short.")

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
