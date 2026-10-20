#!/usr/bin/env python3
"""Scaffold a new prompt with the metadata and section skeleton the library requires.

Adding a prompt by hand is where standards erode: a missing `Risk class`, a
`Version: 1.0.0` on a skeleton, or a section list borrowed from memory. This
script writes the structure, refuses the mistakes the validator would catch
later, and prints the two commands that keep the indexes honest.

Usage
-----
    python3 scripts/new_prompt.py --system 02-engineering/refactoring \\
        --identifier REF-P08 --title "Post-Refactor Review" --mode diagnostic

    python3 scripts/new_prompt.py --list-systems

The file is created under `<system>/P<NN>-<Title-Slug>/<P<NN>-<Title-Slug>.md`,
matching the repository convention. Existing files are never overwritten.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import MODES, RISK, ROOT  # noqa: E402

TEMPLATE = """# PROMPT {nn} — {title}

**Identifier:** {identifier}
**System:** {system}
**Version:** {version}
**Maturity:** {maturity}
**Execution mode:** {mode}
**Risk class:** {risk}
**Depends on:** {depends}
**Produces:** {produces}{inputs_line}
**Est. effort:** {effort}

---

## 1. Role and mandate

You are the {role}. {mandate}

## 2. Objective and scope

**{verb}** {objective}

Out of scope: {out_of_scope}

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| {input1} | {source1} | {fallback1} |
| {input2} | {source2} | {fallback2} |

## 4. Workflow

1. {step1}
2. {step2}
3. {step3}
4. {step4}
5. {step5}
6. Write `{artifact}` with the findings, the evidence, and what remains unresolved.

## 5. Decision rules and evidence standard

- {rule1}
- {rule2}
- Report uncertainty as verified / inferred / unknown rather than presenting a guess as a finding.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| {check1} | {method1} | {pass1} |
| {check2} | {method2} | {pass2} |
| No unauthorised changes | `git status` | clean |

## 7. Failure handling

- **{failure1}** → {response1}
- **{failure2}** → {response2}

## 8. Security and authorisation

Risk class {risk}. {security}

## 9. Completion criteria

- [ ] {criterion1}
- [ ] {criterion2}
- [ ] `{artifact}` written with evidence and open questions.

## 10. Deliverables and handover

Artifact: `{artifact}`.

Handover: {handover}
"""

DEFAULTS = {
    "role": "engineer responsible for this stage",
    "mandate": "Replace this paragraph with the specific mandate, including what you must not do.",
    "verb": "Produce",
    "objective": "replace this with one observable outcome this stage is accountable for.",
    "out_of_scope": "the next stage's work.",
    "input1": "The request or artifact from the previous stage",
    "source1": "previous stage",
    "fallback1": "ask; do not invent the input",
    "input2": "The code or system under examination",
    "source2": "repository",
    "fallback2": "state the limitation explicitly",
    "step1": "Establish the starting state and record it before changing anything.",
    "step2": "Do the smallest unit of work that produces observable progress.",
    "step3": "Verify that unit against an explicit criterion.",
    "step4": "Record the result, including anything that failed and why.",
    "step5": "Stop at the boundary of this stage; route the rest to the next one.",
    "rule1": "Every claim needs evidence; state how it was obtained.",
    "rule2": "Do not exceed the risk class of this stage.",
    "check1": "Output exists and is complete",
    "method1": "inspect",
    "pass1": "all required sections present",
    "check2": "Claims traceable to evidence",
    "method2": "spot-check two claims",
    "pass2": "each cites a source",
    "failure1": "A required input is missing",
    "response1": "stop and state exactly what is needed; do not substitute a guess",
    "failure2": "The work exceeds the stage boundary",
    "response2": "record it and hand off; do not expand scope silently",
    "security": "Describe what may be read, changed, or executed, and what needs approval.",
    "criterion1": "The stage's outcome is observable and recorded",
    "criterion2": "Failures and unresolved items are listed",
    "handover": "route findings to the owning system and remaining work to the next stage.",
}


def slug(title: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--system", help="path relative to the repository root, e.g. 02-engineering/refactoring")
    ap.add_argument("--identifier", help="unique identifier, e.g. REF-P08")
    ap.add_argument("--title", help="human title, e.g. 'Post-Refactor Review'")
    ap.add_argument("--mode", default="diagnostic", help=f"one of: {', '.join(sorted(MODES))}")
    ap.add_argument("--risk", default="A", help="A/B/C/D")
    ap.add_argument("--maturity", default="skeleton", help="skeleton|draft|operational|canonical")
    ap.add_argument("--produces", default="a written record of this stage's output")
    ap.add_argument("--depends", default="the previous stage in this system")
    ap.add_argument("--effort", default="30–60 min")
    ap.add_argument("--inputs", default="", help="comma-separated UPPER_SNAKE inputs; must be used as {{NAME}} in the body")
    ap.add_argument("--list-systems", action="store_true", help="show systems that already contain prompts")
    ap.add_argument("--force-path", help="override the computed directory (relative to the repository root)")
    args = ap.parse_args()

    if args.list_systems:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "__")) and d not in {"archive", "_meta"})
            if any(f.startswith("P") and f.endswith(".md") for f in filenames) or any(
                re.match(r"P\d{2}-", d) for d in dirnames
            ):
                print(os.path.relpath(dirpath, ROOT))
        return 0

    missing = [f for f in ("system", "identifier", "title") if not getattr(args, f)]
    if missing:
        ap.error("missing required: " + ", ".join("--" + m for m in missing))

    if not os.path.isdir(os.path.join(ROOT, args.system)):
        ap.error(f"system directory does not exist: {args.system}")
    if args.mode not in MODES:
        ap.error(f"--mode must be one of: {', '.join(sorted(MODES))}")
    if args.risk not in RISK:
        ap.error("--risk must be one of A, B, C, D")

    number = re.search(r"-P(\d+)", args.identifier)
    if not number:
        ap.error("--identifier should end with -P<number> (e.g. REF-P08) so the folder can be numbered")
    nn = number.group(1)

    if args.force_path:
        folder = os.path.join(ROOT, args.force_path)
        filename = os.path.basename(args.force_path)
    else:
        base = f"P{nn}-{slug(args.title)}"
        folder = os.path.join(ROOT, args.system, base)
        filename = f"P{nn}-{slug(args.title)}.md"
    path = folder if filename.endswith(".md") and args.force_path else os.path.join(folder, filename)

    if os.path.exists(path):
        print(f"ERROR   refusing to overwrite {os.path.relpath(path, ROOT)}", file=sys.stderr)
        return 1

    version = "0.1.0" if args.maturity == "skeleton" else "1.0.0"
    artifact = f".{slug(args.system.split('/')[-1])}/{args.identifier}.md"

    inputs_line = f"\n**Inputs:** {args.inputs}" if args.inputs else ""
    content = TEMPLATE.format(
        nn=nn,
        title=args.title,
        identifier=args.identifier,
        system=args.system,
        version=version,
        maturity=args.maturity,
        mode=args.mode,
        risk=args.risk,
        depends=args.depends,
        produces=args.produces,
        effort=args.effort,
        inputs_line=inputs_line,
        artifact=artifact,
        **DEFAULTS,
    )

    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    rel = os.path.relpath(path, ROOT)
    print(f"Created {rel}\n")
    print("The placeholder text is marked inline — a skeleton may keep it, an operational")
    print("prompt may not. Before opening a pull request:\n")
    print("  python3 scripts/validate_library.py --catalog")
    print("  python3 scripts/generate_gallery.py --write")
    print("  python3 scripts/find_overlaps.py --top 10")
    print("\nThen add the stage to the system README table and a CHANGELOG entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
