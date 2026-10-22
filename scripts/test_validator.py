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
from validate_library import (  # noqa: E402
    MIN_BODY,
    check,
    check_community,
    check_documented_counts,
    check_readme_counts,
    check_risk_class,
    check_stated_totals,
    check_system_readmes,
    load,
)


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


COUNT_CASES = [
    (
        "a README row that matches the tree passes",
        "| [`testcase/system/`](testcase/system/README.md) | 2 | operational |\n",
        2,
        False,
    ),
    (
        "a README row that is one short is an error",
        "| [`testcase/system/`](testcase/system/README.md) | 1 | operational |\n",
        2,
        True,
    ),
    (
        "a README row naming a directory with no prompts is an error",
        "| [`testcase/empty/`](testcase/empty/README.md) | 1 | operational |\n",
        2,
        True,
    ),
    (
        "a row for a different directory is checked against that directory, not this one",
        "| [`testcase/other/`](testcase/other/README.md) | 1 | operational |\n"
        "| [`testcase/system/`](testcase/system/README.md) | 2 | operational |\n",
        2,
        True,
    ),
]


DOC_CASES = [
    (
        "a maturity line that matches the tree passes",
        ["operational", "operational", "skeleton"],
        "- Maturity: **2 operational**, **0 draft**, **1 skeleton**.\n",
        False,
    ),
    (
        "a maturity line that is stale is an error",
        ["operational", "operational", "skeleton"],
        "- Maturity: **1 operational**, **0 draft**, **1 skeleton**.\n",
        True,
    ),
    (
        "the error names the file and both numbers",
        ["operational", "operational", "skeleton"],
        "- Maturity: **9 operational**, **0 draft**, **1 skeleton**.\n",
        True,
    ),
    (
        "a document with no maturity line is ignored, not failed",
        ["operational"],
        "# Notes\n\nNo counts here.\n",
        False,
    ),
    (
        "prose elsewhere in the document is checked too, not just the maturity line",
        ["operational", "operational"],
        "- Maturity: **2 operational**, **0 draft**, **0 skeleton**.\n"
        "The honest summary says 1 operational prompt.\n",
        True,
    ),
    (
        "prose that matches the tree passes",
        ["operational", "operational"],
        "- Maturity: **2 operational**, **0 draft**, **0 skeleton**.\n"
        "Two operational prompts, and one of them is executed.\n",
        False,
    ),
    (
        "a bare 'N prompts carry that label' is a count and is checked",
        ["operational", "operational"],
        "- Maturity: **2 operational**, **0 draft**, **0 skeleton**.\n"
        "Every prompt declares a maturity, and 5 prompts carry that label.\n",
        True,
    ),
    (
        "a stale triplet is reported once, not twice",
        ["operational", "operational", "skeleton"],
        "- Maturity: **1 operational**, **0 draft**, **1 skeleton**.\n",
        True,
    ),
]


TOTAL_CASES = [
    (
        "a file total that matches the scan passes",
        {"PROJECT-STATUS.md": "**3 Markdown files**, **2 prompt files**.\n"},
        False,
    ),
    (
        "a stale Markdown file total is an error",
        {"PROJECT-STATUS.md": "**458 Markdown files**, **2 prompt files**.\n"},
        True,
    ),
    (
        "a stale prompt total is an error",
        {"QUICKSTART.md": "All 362 prompts, plus 3 prompt files.\n"},
        True,
    ),
    (
        "a subset claim is not a total and is not checked",
        {"PROJECT-STATUS.md": "228 prompts carry that label; 3 Markdown files.\n"},
        False,
    ),
    (
        "an unchecked document is ignored",
        {"CHANGELOG.md": "Old release: 457 Markdown files.\n"},
        False,
    ),
]


COMMUNITY_CASES = [
    (
        "all community files present and linked passes",
        {"LICENSE": "MIT", "CONTRIBUTING.md": "See CODE_OF_CONDUCT.md and SECURITY.md.",
         ".github/CODE_OF_CONDUCT.md": "x", ".github/SECURITY.md": "y",
         "README.md": "Read CONTRIBUTING.md."},
        False,
    ),
    (
        "a missing code of conduct is an error",
        {"LICENSE": "MIT", "CONTRIBUTING.md": "See CODE_OF_CONDUCT.md and SECURITY.md.",
         ".github/SECURITY.md": "y", "README.md": "Read CONTRIBUTING.md."},
        True,
    ),
    (
        "a conduct policy nobody links is an error",
        {"LICENSE": "MIT", "CONTRIBUTING.md": "Nothing here.", ".github/CODE_OF_CONDUCT.md": "x",
         ".github/SECURITY.md": "y", "README.md": "Read CONTRIBUTING.md."},
        True,
    ),
    (
        "a README that never points at CONTRIBUTING is an error",
        {"LICENSE": "MIT", "CONTRIBUTING.md": "See CODE_OF_CONDUCT.md and SECURITY.md.",
         ".github/CODE_OF_CONDUCT.md": "x", ".github/SECURITY.md": "y", "README.md": "Hello."},
        True,
    ),
]


RISK_CASES = [
    (
        "a risk-class-A prompt that invites a destructive action is an error",
        "A",
        "\nThe operator will deploy the release to production.\n",
        True,
    ),
    (
        "the same sentence under risk class B is allowed",
        "B",
        "\nThe operator will deploy the release to production.\n",
        False,
    ),
    (
        "a negated destructive action under risk class A is allowed",
        "A",
        "\nYou must not deploy to production; report instead.\n",
        False,
    ),
    (
        "a risk-class-A prompt with no destructive verb passes",
        "A",
        "\nRead the tree and write a report.\n",
        False,
    ),
    (
        "the message tells the author how to resolve it",
        "A",
        "\nThe operator will deploy the release to production.\n",
        True,
    ),
]


def risk_doc(root: str, risk: str, extra: str):
    """One prompt with a given risk class, plus whatever the case appends."""
    system = os.path.join(root, "testcase", "system")
    os.makedirs(system, exist_ok=True)
    body = STAGE.format(n=1, maturity="operational").replace("**Risk class:** A", f"**Risk class:** {risk}")
    path = os.path.join(system, "P01-Stage.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body + extra)
    docs = load(root)
    return next(d for d in docs if d.rel.endswith("P01-Stage.md"))



# --- Whole-document rules -------------------------------------------------------------
# These rules live inside `check()`, which also compares the tree against the status
# documents. A fixture therefore builds a throwaway tree and keeps only the messages whose
# path starts with `sys/`, so a claim in the real README cannot colour the result.

PROMPT = """\
# A prompt

**Identifier:** {ident}
**System:** testcase/system
**Version:** 1.0.0
**Maturity:** {maturity}
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none
**Produces:** nothing
**Inputs:** {inputs}
{tail}
"""

BODY = "Read `{{TARGET}}` and report what you find. " + "Body sentence for the stage. " * 60

REQUIRED_TAIL = """\
## 6. Verification

- run it and record the result.

## 7. Failure handling

- if it cannot run, say so.

## 8. Completion criteria

- [ ] done.
"""


def prompt_messages(root: str, ident="AA-P01", maturity="operational",
                    inputs="TARGET", tail="", files=None):
    """Write one prompt (or an explicit file map) into a tree and return its messages."""
    os.makedirs(os.path.join(root, "sys", "P01"), exist_ok=True)
    text = PROMPT.format(ident=ident, maturity=maturity, inputs=inputs, tail=tail)
    with open(os.path.join(root, "sys", "P01", "P01-A.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    for rel, content in (files or {}).items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    errors, warnings = check(load(root))
    mine = lambda xs: [x for x in xs if x.startswith("sys/")]
    return mine(errors), mine(warnings)



# (name, kwargs for prompt_messages, expect_error, expect_warning)
DOC_CASES_PROMPT = [
    (
        "a marker at the start of a line is an error, not a warning",
        dict(tail=BODY + "\n## 6. Verification\n\nTODO: fill this in\n" + REQUIRED_TAIL),
        True, False,
    ),
    (
        "a bulleted marker is an error",
        dict(tail=BODY + "\n- FIXME: revisit this stage\n" + REQUIRED_TAIL),
        True, False,
    ),
    (
        "the bracketed markdown-checkbox form is still caught",
        dict(tail=BODY + "\n[TODO] finish the handover\n" + REQUIRED_TAIL),
        True, False,
    ),
    (
        "the word in prose is not a marker and must not be flagged",
        dict(tail=BODY + "\nA component file with a TODO is not an interface.\n" + REQUIRED_TAIL),
        False, False,
    ),
    (
        "a sentence naming TODO comments mid-line is not a marker",
        dict(tail=BODY + "\nSearch for TODO comments in the diff.\n" + REQUIRED_TAIL),
        False, False,
    ),
    (
        "an empty required section is an error, not a heading that satisfies the rule",
        dict(tail=BODY + "\n## 6. Verification\n\n## 7. Failure handling\n\n- nothing.\n\n"
             "## 8. Completion criteria\n\n- [ ] done.\n"),
        True, False,
    ),
    (
        "an empty non-required section stays a warning",
        dict(tail=BODY + REQUIRED_TAIL + "\n## 9. Related\n\n## 10. Notes\n\nText.\n"),
        False, True,
    ),
    (
        "a body shorter than the minimum cannot be labelled operational",
        dict(tail="Short, but it names `{{TARGET}}`.\n"),
        True, False,
    ),
    (
        "a duplicate identifier is an error naming both files",
        dict(tail=BODY + REQUIRED_TAIL,
             files={"sys/P02/P02-B.md": PROMPT.format(
            ident="AA-P01", maturity="operational", inputs="TARGET",
            tail=BODY + REQUIRED_TAIL)}),
        True, False,
    ),
    (
        "a broken relative link is an error",
        dict(tail=BODY + "\nSee [gone](nope.md).\n" + REQUIRED_TAIL),
        True, False,
    ),
    (
        "an undeclared placeholder is an error",
        dict(tail=BODY + "\nUse {{NOT_DECLARED}} here.\n" + REQUIRED_TAIL),
        True, False,
    ),
    (
        "an input declared but never used is a warning, not an error",
        dict(inputs="TARGET UNUSED_INPUT", tail=BODY + REQUIRED_TAIL),
        False, True,
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
    for name, readme_text, stage_count, expect_error in COUNT_CASES:
        with tempfile.TemporaryDirectory() as root:
            docs = build(root, "**Maturity: operational (v1.0.0).** Two stages.\n",
                         ["operational"] * stage_count)
            errors = check_readme_counts(docs, readme_text)
        got_error = bool(errors)
        ok = got_error == expect_error
        status = "ok  " if ok else "FAIL"
        print(f"{status} {name} (expected {'error' if expect_error else 'no error'})")
        if not ok:
            failures += 1
            for e in errors:
                print(f"       got: {e}")
    for name, stages, text, expect_error in DOC_CASES:
        with tempfile.TemporaryDirectory() as root:
            docs = build(root, "**Maturity: operational (v1.0.0).** Two stages.\n", stages)
            errors = check_documented_counts(docs, {"PROJECT-STATUS.md": text})
        got_error = bool(errors)
        ok = got_error == expect_error
        status = "ok  " if ok else "FAIL"
        print(f"{status} {name} (expected {'error' if expect_error else 'no error'})")
        if not ok:
            failures += 1
            for e in errors:
                print(f"       got: {e}")
        elif name == "a stale triplet is reported once, not twice" and len(errors) != 1:
            failures += 1
            print(f"       expected one error, got {len(errors)}")
        elif name.startswith("the error names"):
            if "PROJECT-STATUS.md" not in errors[0] or "tree has 2 / 0 / 1" not in errors[0]:
                failures += 1
                print("       detail missing from the message")

    # The stated-totals rule counts the docs it is given, so the fixtures supply a
    # document list and read their claims against it.
    for name, texts, expect_error in TOTAL_CASES:
        errors = check_stated_totals([], texts, totals={"files": 3, "prompts": 2})
        got_error = bool(errors)
        good = got_error == expect_error
        print(f"{'ok  ' if good else 'FAIL'} {name} (expected {'error' if expect_error else 'no error'})")
        if not good:
            failures += 1
            for e in errors:
                print(f"       got: {e}")

    for name, texts, expect_error in COMMUNITY_CASES:
        errors = check_community([], texts)
        got_error = bool(errors)
        good = got_error == expect_error
        print(f"{'ok  ' if good else 'FAIL'} {name} (expected {'error' if expect_error else 'no error'})")
        if not good:
            failures += 1
            for e in errors:
                print(f"       got: {e}")

    # The risk rule was a warning until 2.28.1, so check_all.py passed with a
    # read-only prompt inviting a deploy. These fixtures pin the blocking behaviour.
    for name, risk, extra, expect_error in RISK_CASES:
        with tempfile.TemporaryDirectory() as root:
            doc = risk_doc(root, risk, extra)
            errors = check_risk_class(doc)
        got_error = bool(errors)
        good = got_error == expect_error
        print(f"{'ok  ' if good else 'FAIL'} {name} (expected {'error' if expect_error else 'no error'})")
        if not good:
            failures += 1
            for e in errors:
                print(f"       got: {e}")
        elif name.startswith("the message tells"):
            if "without forbidding it" not in errors[0] or "raise the class" not in errors[0]:
                failures += 1
                print("       detail missing from the message")


    # Whole-document rules. GAPS.md G-01..G-07: three of these could not stop a build
    # and four had no fixture at all.
    for name, kwargs, expect_error, expect_warning in DOC_CASES_PROMPT:
        with tempfile.TemporaryDirectory() as root:
            errors, warnings = prompt_messages(root, **kwargs)
        good = bool(errors) == expect_error and bool(warnings) == expect_warning
        print(f"{'ok  ' if good else 'FAIL'} {name} "
              f"(expected {'error' if expect_error else 'no error'}, "
              f"{'warning' if expect_warning else 'no warning'})")
        if not good:
            failures += 1
            for e in errors:
                print(f"       error: {e}")
            for w in warnings:
                print(f"       warning: {w}")

    total = (len(CASES) + len(COUNT_CASES) + len(DOC_CASES) + len(TOTAL_CASES)
             + len(COMMUNITY_CASES) + len(RISK_CASES) + len(DOC_CASES_PROMPT))
    print(f"\n{total - failures}/{total} cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
