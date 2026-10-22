#!/usr/bin/env python3
"""Regression tests for the prompt-contract checks.

The contract checks are the only ones that look *across* prompts, so they are the
ones most able to pass while being wrong. Each fixture here is a small system in
a temporary directory, and each case pins one rule that the real library depends
on:

  * a dependency on a non-existent identifier is an error
  * an identifier named only in parentheses is not a dependency
  * two stages claiming to produce one artifact is an error, unless one says
    "updates" or is an orchestrator
  * a cycle in a system's dependency graph is an error
  * an upstream artifact the downstream stage never names is reported, not
    failed — it is debt, and the count is the point

Usage
-----
    python3 scripts/test_contract.py
"""

from __future__ import annotations

import os
import sys
import tempfile
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_prompt_contract import check, find_cycles  # noqa: E402
from validate_library import load  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def ok(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))


STAGE = """# PROMPT {n} — {title}

**Identifier:** {ident}
**System:** {system}
**Version:** {version}
**Maturity:** {maturity}
**Execution mode:** planning
**Risk class:** A
**Depends on:** {depends}
**Produces:** {produces}
**Inputs:** TARGET_PATH

---

## 1. Role and mandate

You handle `{{{{TARGET_PATH}}}}` and record what you find in the artifacts named above.

## 2. Objective and scope

Produce the artifacts. Out of scope: everything else.

## 3. Prerequisites and inputs

- `{{{{TARGET_PATH}}}}` exists.
{extra}
## 4. Workflow

1. Read the path and write the artifact.

## 5. Decision rules and evidence standard

- Evidence over assertion.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Read | Inspect | Path was read |

## 7. Failure handling

- **Path missing** → stop and say so.

## 8. Security and authorisation

Risk class A: read-only.

## 9. Completion criteria

- [ ] Path read.

## 10. Deliverables and handover

Deliver the artifact; the next stage reads it.
"""


def build(root: str, system: str, stages: list[dict]) -> list:
    folder = os.path.join(root, *system.split("/"))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# Test system\n\n**Status:** Mixed.\n")
    for i, stage in enumerate(stages, start=1):
        d = os.path.join(folder, f"P0{i}-Stage")
        os.makedirs(d, exist_ok=True)
        text = STAGE.format(
            n=i,
            title=stage.get("title", f"Stage {i}"),
            ident=stage["ident"],
            system=system,
            version=stage.get("version", "1.0.0"),
            maturity=stage.get("maturity", "operational"),
            depends=stage.get("depends", "none"),
            produces=stage.get("produces", f"`ART_{i}.md`"),
            extra=stage.get("extra", ""),
        )
        with open(os.path.join(d, f"P0{i}-Stage.md"), "w", encoding="utf-8") as fh:
            fh.write(textwrap.dedent(text))
    return load(root)


def errors_for(stages: list[dict]) -> tuple[list[str], dict]:
    with tempfile.TemporaryDirectory() as root:
        docs = build(root, "testcase/system", stages)
        errors, _, report = check(docs)
    return errors, report


def main() -> int:
    # A clean two-stage chain: no errors, and no unnamed artifact.
    errors, report = errors_for([
        {"ident": "TST-P01", "produces": "`ART_1.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "extra": "- `ART_1.md` — from `TST-P01`.\n"},
    ])
    ok("a clean chain passes", errors == [], str(errors))
    ok("the chain counts one flow link", report["testcase/system"]["flow_links"] == 1)
    ok("a named upstream artifact is not reported",
       report["testcase/system"]["unreferenced"] == [],
       str(report["testcase/system"]["unreferenced"]))

    # An unnamed upstream artifact is reported, not failed.
    errors, report = errors_for([
        {"ident": "TST-P01", "produces": "`ART_1.md`"},
        {"ident": "TST-P02", "depends": "TST-P01"},
    ])
    ok("an unnamed upstream artifact does not fail the check", errors == [], str(errors))
    ok("an unnamed upstream artifact is reported",
       len(report["testcase/system"]["unreferenced"]) == 1)

    # A dependency on something that does not exist.
    errors, _ = errors_for([
        {"ident": "TST-P01", "depends": "GHOST-P99"},
    ])
    ok("a dependency on a missing identifier is an error", len(errors) == 1, str(errors))

    # Parenthetical mentions are not dependencies.
    errors, _ = errors_for([
        {"ident": "TST-P01", "depends": "none (companion: GHOST-P99)"},
    ])
    ok("a parenthetical identifier is not a dependency", errors == [], str(errors))

    # Two writers of one artifact.
    errors, _ = errors_for([
        {"ident": "TST-P01", "produces": "`SAME.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "produces": "`SAME.md`"},
    ])
    ok("two stages producing one artifact is an error",
       any("SAME.md" in e for e in errors), str(errors))

    # ... unless the second says it updates the file.
    errors, _ = errors_for([
        {"ident": "TST-P01", "produces": "`SAME.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "produces": "`OTHER.md`, plus updates to `SAME.md`"},
    ])
    ok("an 'updates' claim is not ownership", errors == [], str(errors))

    # ... or is an orchestrator.
    errors, _ = errors_for([
        {"ident": "TST-P01", "produces": "`SAME.md`"},
        {"ident": "TST-P02", "title": "Orchestrator", "depends": "TST-P01", "produces": "`SAME.md`"},
    ])
    ok("an orchestrator may restate its stages' artifacts", errors == [], str(errors))

    # Cycles.
    errors, _ = errors_for([
        {"ident": "TST-P01", "depends": "TST-P02"},
        {"ident": "TST-P02", "depends": "TST-P01"},
    ])
    ok("a two-stage cycle is an error", any("cycle" in e for e in errors), str(errors))
    ok("a cycle is reported once, not once per rotation",
       sum(1 for e in errors if "cycle" in e) == 1, str(errors))

    ok("find_cycles reaches a three-stage cycle",
       find_cycles({"A": {"B"}, "B": {"C"}, "C": {"A"}}) != [])
    ok("find_cycles ignores a DAG", find_cycles({"A": {"B"}, "B": set()}) == [])

    # A stem match is not a citation: a placeholder that shares the stem, or the
    # plain word, must not count as naming the file.
    _, report = errors_for([
        {"ident": "TST-P01", "produces": "`SELECTED_WORK.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "extra": "- `{{SELECTED_WORK}}` — the selection.\n"},
    ])
    r = report["testcase/system"]
    ok("a placeholder sharing a filename's stem is not a citation",
       len(r["weak"]) == 1 and r["unreferenced"] == [], str(r["weak"]))

    _, report = errors_for([
        {"ident": "TST-P01", "produces": "`PLAN.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "extra": "- The plan is agreed.\n"},
    ])
    r = report["testcase/system"]
    ok("a prose mention of the stem is not a citation", len(r["weak"]) == 1, str(r["weak"]))

    _, report = errors_for([
        {"ident": "TST-P01", "produces": "`PLAN.md`"},
        {"ident": "TST-P02", "depends": "TST-P01", "extra": "- Read `PLAN.md` before starting.\n"},
    ])
    r = report["testcase/system"]
    ok("naming the filename counts as a citation",
       r["weak"] == [] and r["unreferenced"] == [], f"{r['weak']} {r['unreferenced']}")

    # The stem test is why loose matching is not enough in the other direction
    # either: "PLAN" matches the word "planning" in the template's own header.
    _, report = errors_for([
        {"ident": "TST-P01", "produces": "`PLAN.md`"},
        {"ident": "TST-P02", "depends": "TST-P01"},
    ])
    r = report["testcase/system"]
    ok("a substring of an unrelated word is not a citation", len(r["weak"]) == 1, str(r["weak"]))

    _, report = errors_for([
        {"ident": "TST-P01", "produces": "`INVENTORY.md`"},
        {"ident": "TST-P02", "depends": "TST-P01"},
    ])
    r = report["testcase/system"]
    ok("an artifact mentioned nowhere is reported, not failed",
       len(r["unreferenced"]) == 1, str(r["unreferenced"]))

    passed = sum(1 for _, good, _ in RESULTS if good)
    for name, good, detail in RESULTS:
        print(f"{'PASS' if good else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not good else ""))
    print(f"\n{passed}/{len(RESULTS)} cases passed")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
