#!/usr/bin/env python3
"""Regression tests for the validator's system-README maturity rules.

The rule added in 2.16.0 was verified against real repository cases at the
time, which is evidence that it worked once — not that it keeps working. These
fixtures pin the behaviour:

  * `**Status:** Operational` over skeleton stages  -> error
  * `**Maturity: operational` over skeleton stages  -> error
  * prose "Operational" when most stages are skeleton and the README does not
    declare itself mixed                              -> error
  * the same prose with a "Mixed" declaration          -> no error
  * a genuinely operational system                     -> no error

Usage
-----
    python3 scripts/test_validator.py

Exit code 0 means every case behaved as specified.
"""

from __future__ import annotations

import os
import sys
import tempfile
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import check_system_readmes, load  # noqa: E402


STAGE = """# PROMPT {n} — Stage {n}

**Identifier:** TST-P0{n}
**System:** testcase/system
**Version:** 1.0.0
**Maturity:** {maturity}
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none
**Produces:** nothing
**Inputs:** TARGET_PATH
**Est. effort:** 1 min

## 1. Role and mandate

You review `{{{{TARGET_PATH}}}}` and report what you find.

## 2. Objective and scope

Produce a report. Out of scope: everything else.

## 3. Prerequisites and inputs

- `{{{{TARGET_PATH}}}}` exists.

## 4. Workflow

1. Read the path.

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
- [ ] Report written.

## 10. Deliverables and handover

Deliver the report; the next stage reads it.
"""


def build(root: str, readme: str, stages: list[str]) -> list:
    system = os.path.join(root, "testcase", "system")
    os.makedirs(system, exist_ok=True)
    with open(os.path.join(system, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(textwrap.dedent(readme))
    for i, maturity in enumerate(stages, start=1):
        stage_dir = os.path.join(system, f"P0{i}-Stage")
        os.makedirs(stage_dir, exist_ok=True)
        with open(os.path.join(stage_dir, f"P0{i}-Stage.md"), "w", encoding="utf-8") as fh:
            fh.write(STAGE.format(n=i, maturity=maturity))
    return load(root)


CASES = [
    (
        "status-claim over skeletons is an error",
        "**Status:** Operational — a fine system.\n\n## Stages\n\n| ID | Stage |\n|----|-------|\n",
        ["skeleton", "skeleton"],
        True,
    ),
    (
        "maturity-claim over skeletons is an error",
        "**Maturity: operational (v1.0.0).** Two stages.\n\n## Stages\n\n| ID | Stage |\n|----|-------|\n",
        ["skeleton", "skeleton"],
        True,
    ),
    (
        "prose claim with mostly skeletons is an error",
        "# System\n\n- **general/** — Operational multi-stage contribution system\n",
        ["skeleton", "skeleton"],
        True,
    ),
    (
        "prose claim with a Mixed declaration is allowed",
        "# System\n\n**Status:** Mixed — 1 operational, 1 skeleton.\n\n- **general/** — Operational stages where marked\n",
        ["skeleton", "operational"],
        False,
    ),
    (
        "fully operational system passes",
        "**Maturity: operational (v1.0.0).** Two stages.\n",
        ["operational", "operational"],
        False,
    ),
    (
        "one skeleton among many operational passes the status claim",
        "**Status:** Operational — one stage outstanding.\n",
        ["operational", "operational", "skeleton"],
        True,
    ),
]


def main() -> int:
    failures = 0
    for name, readme, stages, expect_error in CASES:
        with tempfile.TemporaryDirectory() as root:
            docs = build(root, readme, stages)
            errors = [e for e in check_system_readmes(docs) if "README.md" in e]
        got_error = bool(errors)
        ok = got_error == expect_error
        status = "ok  " if ok else "FAIL"
        print(f"{status} {name} (expected {'error' if expect_error else 'no error'})")
        if not ok:
            failures += 1
            for e in errors:
                print(f"       got: {e}")
    total = len(CASES)
    print(f"\n{total - failures}/{total} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
