#!/usr/bin/env python3
"""Check that prompts compose: dependencies resolve, and artifacts flow along them.

`validate_library.py` proves each prompt is well formed *in isolation* — metadata,
sections, links, inputs. It cannot see the property that makes this library a
library rather than 364 separate documents: **a stage's artifact is the next
stage's input, and the name in `Produces:` is the token that carries it.**

A system of prompts fails in a specific way when that breaks. Stage 1 writes
`.flags/ROLLOUT_LOG.md`; stage 5 says "the rollout evidence" and never names the
file. Each prompt is individually correct, and an agent running the sequence has
to invent the mapping — which is where artifacts get re-derived, re-named, and
silently diverge.

What this checks
----------------
**Hard (exit 1):**
1. A `Depends on:` identifier that does not exist. Judged from the part of the
   line outside parentheses, so "none (companion: GEN-P02)" is not a dependency.
2. Two non-orchestrator stages in one system claiming to *produce* the same
   artifact. Two writers of one file is a race, not a sequence. Words such as
   `updates` and `appends` do not count as ownership.
3. A cycle in the dependency graph of one system.

**Reported, not failed:**
4. An upstream artifact that the downstream stage never names, either as a file
   or as a placeholder stem. The most common real defect in this library, and
   the count is printed so it can burn down rather than be forgotten.
5. A system whose first stage produces nothing.

Usage
-----
    python3 scripts/check_prompt_contract.py            # gates + summary
    python3 scripts/check_prompt_contract.py --report   # per-system detail
    python3 scripts/check_prompt_contract.py --write-report   # _meta/conformance-report.md

Stdlib only. Safe to run in CI.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import ROOT, Doc, is_archive, load  # noqa: E402

# An artifact reference in `Produces:` or in prose. Backticked, with an extension,
# optionally in a dotted directory (`.flags/ROLLOUT_LOG.md`).
ARTIFACT = re.compile(r"`([.A-Za-z0-9_/-]+\.(?:md|json|ya?ml|csv|txt))`")
# A claim of ownership, as opposed to a mention: "updates X" is not "produces X".
UPDATE_WORD = re.compile(r"\b(update|updates|updated|append|appends|refresh|refreshes|revise|revises)\b", re.I)
ORCHESTRATOR = re.compile(r"orchestrat", re.I)
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")


def system_key(rel: str) -> str:
    parts = rel.split(os.sep)
    return os.sep.join(parts[:-2]) if len(parts) >= 3 else parts[0]


def identifiers(docs: list[Doc]) -> dict[str, Doc]:
    return {d.identifier: d for d in docs if d.identifier}


def produces(doc: Doc) -> set[str]:
    raw = doc.meta.get("Produces") or ""
    out: set[str] = set()
    # Split on commas so a single "updates" marker only disclaims its own clause.
    for clause in re.split(r",|;", raw):
        if UPDATE_WORD.search(clause):
            continue
        for m in ARTIFACT.findall(clause):
            out.add(os.path.basename(m))
    return out


def dependency_tokens(doc: Doc) -> set[str]:
    """Identifiers named in `Depends on:`, whether or not they exist.

    Returning only the ones that resolve would make the "unknown dependency"
    check unfalsifiable: it would always pass. Tokens are recognised by shape —
    a hyphenated identifier (`DBG-01`, `CHAT-MODE`) or a bare `P01`-style stage
    number — and parenthetical prose is dropped first, so "none (companion:
    GEN-P02)" is not a dependency.
    """
    raw = doc.meta.get("Depends on") or ""
    outside = re.sub(r"\([^)]*\)", " ", raw)
    tokens = re.findall(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b|\bP\d{1,2}\b", outside)
    return set(tokens)


def dependencies(doc: Doc, known: dict[str, Doc]) -> set[str]:
    """The subset of `dependency_tokens` that exists in the library."""
    return {t for t in dependency_tokens(doc) if t in known}


def is_orchestrator(doc: Doc, path_hint: str) -> bool:
    return bool(ORCHESTRATOR.search(doc.text.splitlines()[0] if doc.text else "") or ORCHESTRATOR.search(path_hint))


def check(docs: list[Doc]) -> tuple[list[str], list[str], dict[str, dict]]:
    prompts = [d for d in docs if d.is_prompt and not is_archive(d.rel)]
    known = identifiers(prompts)

    errors: list[str] = []
    notes: list[str] = []
    systems: dict[str, list[Doc]] = defaultdict(list)
    for d in prompts:
        systems[system_key(d.rel)].append(d)

    # 1. Dependencies resolve.
    for d in prompts:
        for ident in sorted(dependency_tokens(d) - set(known)):
            errors.append(f"{d.rel}: depends on '{ident}', which is not a prompt in the library")

    # 2 and 3, per system.
    report: dict[str, dict] = {}
    for system, members in sorted(systems.items()):
        owners: dict[str, list[str]] = defaultdict(list)
        for d in members:
            if is_orchestrator(d, d.rel):
                continue
            for art in produces(d):
                owners[art].append(d.identifier or d.rel)
        collisions = {a: who for a, who in owners.items() if len(who) > 1}
        for art, who in sorted(collisions.items()):
            errors.append(
                f"{system}: {art} is claimed as produced by {', '.join(sorted(who))} — "
                "two writers of one artifact is a race; one stage should say 'updates' instead"
            )

        graph = {d.identifier: dependencies(d, known) & {m.identifier for m in members} for d in members if d.identifier}
        cycles = find_cycles(graph)
        for cycle in cycles:
            errors.append(f"{system}: dependency cycle {' → '.join(cycle)}")

        # 4. Artifact flow: does a downstream stage name what its upstream produces?
        flow_total = 0
        unreferenced: list[tuple[str, str, str]] = []
        weak: list[tuple[str, str, str]] = []
        for d in members:
            for up_id in sorted(dependencies(d, known)):
                up = known.get(up_id)
                if up is None or system_key(up.rel) != system:
                    continue
                arts = produces(up)
                if not arts:
                    continue
                flow_total += 1
                body = d.text.upper()
                joined = ", ".join(sorted(arts))
                if not any(a.rsplit(".", 1)[0] in body for a in arts):
                    unreferenced.append((d.identifier or d.rel, up_id, joined))
                    continue
                # A stem match is not a citation. `{{SELECTED_WORK}}` is an input
                # placeholder, not the file `SELECTED_WORK.md`, and "the plan" is
                # not `PLAN.md`. Placeholders are stripped before the strict test
                # so an input name shared with a filename cannot pass for a
                # reference to it.
                stripped = PLACEHOLDER.sub("", body)
                if not any(a.upper() in stripped for a in arts):
                    weak.append((d.identifier or d.rel, up_id, joined))

        # 5. A system whose entry stage produces nothing.
        first = members[0]
        first_id = first.identifier or ""
        if (
            len(members) > 1
            and re.search(r"(^|-)P0?1$", first_id)
            and not produces(first)
            and not is_orchestrator(first, first.rel)
        ):
            notes.append(f"{system}: entry stage {first.identifier or first.rel} produces no artifact")

        report[system] = {
            "stages": len(members),
            "artifacts": len(owners),
            "collisions": collisions,
            "cycles": cycles,
            "flow_links": flow_total,
            "unreferenced": unreferenced,
            "weak": weak,
        }

    return errors, notes, report


def find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Return one representative path per cycle, with the repeated node included."""
    seen: list[list[str]] = []
    for start in sorted(graph):
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            for nxt in sorted(graph.get(node, ())):
                if nxt == start:
                    seen.append(path + [start])
                elif nxt not in path and nxt in graph:
                    stack.append((nxt, path + [nxt]))
    # Deduplicate rotations of the same cycle.
    unique: list[list[str]] = []
    for cycle in seen:
        body = cycle[:-1]
        if not any(set(body) == set(u[:-1]) for u in unique):
            unique.append(cycle)
    return unique


def render_report(report: dict[str, dict]) -> str:
    total_flow = sum(r["flow_links"] for r in report.values())
    total_links = sum(len(r["unreferenced"]) for r in report.values())
    total_weak = sum(len(r["weak"]) for r in report.values())
    lines = [
        "# Conformance Report — how the prompts compose",
        "",
        "**Generated by `scripts/check_prompt_contract.py --write-report`. Do not edit by hand.**",
        "",
        "This report answers a different question from the validator. The validator asks whether each",
        "prompt is well formed on its own; this asks whether one stage's artifact is the next stage's",
        "input, which is the property that makes a sequence of prompts a system rather than a folder.",
        "",
        "## Summary",
        "",
        "| Measure | Value |",
        "|---------|------:|",
        f"| Systems with more than one stage | {sum(1 for r in report.values() if r['stages'] > 1)} |",
        f"| Dependency links between stages in a system | {total_flow} |",
        f"| Links where the downstream stage never names the upstream artifact | **{total_links}** |",
        f"| Links that mention it only by stem, never as a filename | {total_weak} |",
        f"| Links that cite the upstream filename | {total_flow - total_links - total_weak} |",
        "",
        "The second row is the library's real integration claim. The third is what is left of it: a",
        "link where the downstream prompt says *\"the rollout evidence\"* instead of naming",
        "`.flags/ROLLOUT_LOG.md` leaves an agent to invent the mapping, and invented mappings are where",
        "artifacts get re-derived under a second name.",
        "",
        "The fourth row is the honest middle. A stem match is not a citation: `{{SELECTED_WORK}}` is an",
        "input placeholder, and \"the plan\" is not `PLAN.md`. Those links are counted separately rather",
        "than as satisfied, because the number that matters is the last row — how many stages could be",
        "handed the artifact without anyone guessing its name.",
        "",
        "## Per system",
        "",
        "| System | Stages | Artifacts | Flow links | Filename cited | Stem only | No artifact |",
        "|--------|-------:|----------:|-----------:|---------------:|----------:|------------:|",
    ]
    for system, r in sorted(report.items()):
        if r["stages"] < 2:
            continue
        lines.append(
            f"| `{system}` | {r['stages']} | {r['artifacts']} | {r['flow_links']} | "
            f"{r['flow_links'] - len(r['unreferenced']) - len(r['weak'])} | {len(r['weak'])} | {len(r['unreferenced'])} |"
        )
    lines += ["", "## The specific links that name no artifact", ""]
    lines.append("Grouped by system. Each row is a stage, the stage it depends on, and the artifact")
    lines.append("that stage produces but this one never mentions.")
    lines.append("")
    for system, r in sorted(report.items()):
        if not r["unreferenced"]:
            continue
        lines.append(f"### `{system}`")
        lines.append("")
        lines.append("| Stage | Depends on | Artifact not named |")
        lines.append("|-------|------------|--------------------|")
        for stage, up, arts in r["unreferenced"]:
            lines.append(f"| `{stage}` | `{up}` | `{arts}` |")
        lines.append("")
    lines += ["## The links that name the artifact only by stem", ""]
    lines.append("Each of these mentions something that matches a filename's stem — often a `{{PLACEHOLDER}}`")
    lines.append("that happens to share it — but never the filename itself. Cheap to fix, and worth fixing")
    lines.append("before the prompts are run back to back.")
    lines.append("")
    for system, r in sorted(report.items()):
        if not r["weak"]:
            continue
        lines.append(f"### `{system}`")
        lines.append("")
        lines.append("| Stage | Depends on | Artifact matched by stem only |")
        lines.append("|-------|------------|-------------------------------|")
        for stage, up, arts in r["weak"]:
            lines.append(f"| `{stage}` | `{up}` | `{arts}` |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true", help="print per-system detail")
    ap.add_argument("--write-report", action="store_true", help="write _meta/conformance-report.md")
    ap.add_argument("--check-report", action="store_true", help="fail if _meta/conformance-report.md is stale")
    args = ap.parse_args()

    docs = load(ROOT)
    errors, notes, report = check(docs)

    for e in errors:
        print(f"ERROR   {e}")
    for n in notes:
        print(f"NOTE    {n}")

    links = sum(r["flow_links"] for r in report.values())
    unnamed = sum(len(r["unreferenced"]) for r in report.values())
    weak = sum(len(r["weak"]) for r in report.values())
    cited = links - unnamed - weak
    print()
    print(f"{sum(1 for r in report.values() if r['stages'] > 1)} multi-stage systems; "
          f"{links} dependency links; {cited} cite the upstream filename, {weak} mention it only by "
          f"stem, {unnamed} name no artifact ({_pct(unnamed, links)}).")
    print(f"Links that do not cite a filename: {unnamed + weak} of {links} ({_pct(unnamed + weak, links)}).")
    print(f"Result: {len(errors)} error(s).")

    if args.report:
        for system, r in sorted(report.items()):
            if r["stages"] < 2:
                continue
            print()
            print(f"{system}  ({r['stages']} stages, {r['artifacts']} artifacts, "
                  f"{len(r['weak'])} stem-only, {len(r['unreferenced'])} unnamed)")
            for stage, up, arts in r["unreferenced"]:
                print(f"   {stage} ← {up}   [not named: {arts}]")
            for stage, up, arts in r["weak"]:
                print(f"   {stage} ← {up}   [stem only: {arts}]")

    out = os.path.join(ROOT, "_meta", "conformance-report.md")
    rendered = render_report(report)

    if args.write_report:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(rendered)
        print(f"Report written to {os.path.relpath(out, ROOT)}")

    if args.check_report:
        current = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
        if current != rendered:
            print(f"ERROR   {os.path.relpath(out, ROOT)} is stale — run: "
                  "python3 scripts/check_prompt_contract.py --write-report")
            return 1

    return 1 if errors else 0


def _pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f}%" if d else "n/a"


if __name__ == "__main__":
    sys.exit(main())
