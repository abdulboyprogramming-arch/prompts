#!/usr/bin/env python3
"""Validate the prompt library and (optionally) regenerate its catalog.

Checks
------
1. Metadata block present, parseable, and internally consistent.
2. Identifier uniqueness and format.
3. Semantic-version rules tied to maturity (skeleton -> major 0).
4. Underdeveloped content that claims maturity beyond `skeleton`.
5. Broken relative Markdown links.
6. Duplicate / missing H1, empty sections, leftover placeholders.
7. Risk-class honesty: destructive verbs in a read-only prompt.
8. Status overclaim: a system README that advertises Operational while every
   stage in that system is still a skeleton.

Usage
-----
    python3 scripts/validate_library.py            # validate
    python3 scripts/validate_library.py --quiet     # errors only
    python3 scripts/validate_library.py --catalog    # validate + write _meta/CATALOG.md

Exit code 1 if any error is found, else 0. Warnings never fail the build.

Stdlib only. No network access. Safe to run in CI.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "archive", "__pycache__", ".github"}
ARCHIVE_DIRS = {"archive"}
TOOLING_DIRS = {"_meta"}  # standards, templates, and generated indexes — not prompts

MATURITY = {"skeleton", "draft", "operational", "canonical"}
MODES = {
    "diagnostic", "planning", "implementation", "audit-remediation",
    "autonomous-completion", "research", "continuous-improvement",
    "orchestration", "specialised",
}
RISK = {"A", "B", "C", "D"}

REQUIRED_KEYS = ["Identifier", "Version", "Maturity", "Execution mode", "Risk class"]
RECOMMENDED_KEYS = ["System", "Depends on", "Produces"]

ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(-[A-Z0-9]+)*$")
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
META_RE = re.compile(r"^\*\*([A-Za-z][A-Za-z /&-]*?):\*\*\s*(.+?)\s*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")

# Minimum developed body length (after the metadata block) for non-skeleton prompts.
MIN_BODY = 1200
# A prompt below this is treated as an outline regardless of its label.
OUTLINE_BODY = 900

REQUIRED_SECTIONS = [
    ("verification", ("verification", "validat")),
    ("completion criteria", ("completion criteria", "definition of done", "done when")),
    ("failure handling", ("failure", "recovery", "when blocked")),
]

DESTRUCTIVE = re.compile(
    r"\b(git push|force[- ]push|deploy (?:to|the|this|it)\b|"
    r"publish(?:ing)? to|drop table|delete (?:the )?(?:database|bucket)|rm -rf|"
    r"revoke (?:the )?(?:key|token|access)|rotate (?:the )?(?:key|secret))",
    re.IGNORECASE,
)
INPUT_NAME = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\b")
PLACEHOLDER = re.compile(r"\{\{\s*([^{}]*?)\s*\}\}")
STATUS_OVERCLAIM = re.compile(r"(production-ready|status:\s*\**\s*operational|complete and ready)", re.IGNORECASE)


@dataclass
class Doc:
    path: str
    rel: str
    text: str
    meta: dict[str, str] = field(default_factory=dict)
    maturity: str | None = None
    identifier: str | None = None
    body_len: int = 0
    is_prompt: bool = False


def iter_markdown(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                full = os.path.join(dirpath, name)
                yield full, os.path.relpath(full, root)


def parse_meta(text: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    prose_lines = []
    in_fence = False
    for line in text.splitlines()[:60]:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            prose_lines.append(line)
    for line in prose_lines[:40]:
        m = META_RE.match(line.strip())
        if m:
            key = " ".join(m.group(1).split())
            if key not in meta:
                meta[key] = m.group(2).strip()
    return meta


def load(root: str) -> list[Doc]:
    docs = []
    for full, rel in iter_markdown(root):
        with open(full, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        meta = parse_meta(text)
        body = re.sub(r"^#.*$", "", text, count=1, flags=re.MULTILINE)
        doc = Doc(path=full, rel=rel, text=text, meta=meta, body_len=len(body.strip()))
        doc.identifier = meta.get("Identifier")
        doc.maturity = (meta.get("Maturity") or "").strip().lower() or None
        doc.is_prompt = bool(doc.identifier) or bool(
            re.search(r"(^|/)(P\d{2}-[^/]+)/[^/]*\.md$", rel)
        )
        docs.append(doc)
    return docs


def is_archive(rel: str) -> bool:
    return rel.split(os.sep)[0] in ARCHIVE_DIRS


TOP_LEVEL_DOCS = {"README.md", "AGENTS.md", "CHANGELOG.md", "CONTRIBUTING.md", "PROJECT-STATUS.md", "GALLERY.md", "QUICKSTART.md", "TASKS.md"}


def strip_fences(text: str) -> str:
    """Drop fenced code blocks so example placeholders are never validated."""
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def check_inputs(doc: Doc) -> tuple[list[str], list[str]]:
    """A declared `Inputs:` list must agree with the {{PLACEHOLDER}}s in the body."""
    errors: list[str] = []
    warnings: list[str] = []
    declared_raw = doc.meta.get("Inputs")
    body = strip_fences(doc.text)

    used = set()
    for raw in PLACEHOLDER.findall(body):
        if not re.fullmatch(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*", raw):
            errors.append(f"{doc.rel}: malformed placeholder '{{{{{raw}}}}}' — use UPPER_SNAKE_CASE")
            continue
        used.add(raw)

    declared = set(INPUT_NAME.findall(declared_raw)) if declared_raw else set()
    if declared_raw:
        for token in re.split(r"[,\n]", declared_raw.replace("(", ",").replace(")", ",")):
            token = re.sub(r"^\s*optional\s*:\s*", "", token).strip()
            if token and re.fullmatch(r"[a-z][a-z0-9_]*", token):
                errors.append(f"{doc.rel}: input '{token}' should be UPPER_SNAKE_CASE")

    for name in sorted(used - declared):
        errors.append(f"{doc.rel}: placeholder {{{{{name}}}}} is not declared in `**Inputs:**`")
    for name in sorted(declared - used):
        warnings.append(f"{doc.rel}: input {name} is declared but never used as a placeholder")
    return errors, warnings


README_CLAIM = re.compile(
    r"^\s*\*\*(?:Status|Maturity):?\s*\**\s*(Operational|Production-ready)\b",
    re.IGNORECASE | re.MULTILINE,
)
# A README that says "Operational" anywhere in prose while most of its stages are
# outlines is the same overclaim in a different sentence.
README_PROSE_CLAIM = re.compile(r"\bOperational\b")
SYSTEM_README = re.compile(r"^(?:[^/]+)/(?:[^/]+)/README\.md$")


def check_system_readmes(docs: list[Doc]) -> list[str]:
    """A system README may not claim more maturity than its own stage prompts have."""
    errors: list[str] = []
    by_system: dict[str, list[Doc]] = {}
    for d in docs:
        if not d.is_prompt or d.maturity is None:
            continue
        parts = d.rel.split(os.sep)
        if len(parts) < 3:
            continue
        by_system.setdefault(os.sep.join(parts[:2]), []).append(d)

    for d in docs:
        if not SYSTEM_README.match(d.rel):
            continue
        claim = README_CLAIM.search(d.text)
        prose = README_PROSE_CLAIM.search(d.text)
        declares_mixed = re.search(r"\bmixed\b", d.text, re.IGNORECASE)
        if declares_mixed and claim is None:
            continue
        if not claim and not prose:
            continue
        system = os.sep.join(d.rel.split(os.sep)[:2])
        stages = by_system.get(system, [])
        if not stages:
            continue
        weak = [s for s in stages if s.maturity in ("skeleton", "draft")]
        if not weak or declares_mixed:
            continue
        if claim is not None:
            errors.append(
                f"{d.rel}: claims {claim.group(1)} but {len(weak)} of {len(stages)} stage prompts in "
                f"{system}/ are skeleton/draft (e.g. {weak[0].rel}); the README overclaims"
            )
        elif prose and len(weak) > len(stages) / 2:
            errors.append(
                f"{d.rel}: prose claims 'Operational' but {len(weak)} of {len(stages)} stage prompts in "
                f"{system}/ are skeleton/draft; state the real maturity or mark the system mixed"
            )
    return errors

def check(docs: list[Doc]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids: dict[str, str] = {}

    for d in docs:
        if is_archive(d.rel):
            continue
        if d.is_prompt:
            for key in REQUIRED_KEYS:
                if key not in d.meta:
                    errors.append(f"{d.rel}: missing metadata key '{key}'")
            for key in RECOMMENDED_KEYS:
                if key not in d.meta:
                    warnings.append(f"{d.rel}: recommended metadata key '{key}' absent")

        ident = d.identifier
        if ident:
            if not ID_RE.match(ident):
                errors.append(f"{d.rel}: identifier '{ident}' does not match {ID_RE.pattern}")
            elif ident in ids:
                errors.append(f"{d.rel}: duplicate identifier '{ident}' (also in {ids[ident]})")
            else:
                ids[ident] = d.rel

        version = d.meta.get("Version", "")
        if d.is_prompt and version:
            m = SEMVER_RE.match(version)
            if not m:
                errors.append(f"{d.rel}: version '{version}' is not semver")
            elif d.maturity == "skeleton" and m.group(1) != "0":
                errors.append(
                    f"{d.rel}: skeleton prompt declares version {version}; skeletons must be 0.x"
                )

        if d.is_prompt and d.maturity:
            if d.maturity not in MATURITY:
                errors.append(f"{d.rel}: maturity '{d.maturity}' not in {sorted(MATURITY)}")
            elif d.maturity != "skeleton":
                if d.body_len < MIN_BODY:
                    errors.append(
                        f"{d.rel}: labelled '{d.maturity}' but body is only "
                        f"{d.body_len} chars (< {MIN_BODY}); label is an overclaim"
                    )
                low = d.text.lower()
                for label, needles in REQUIRED_SECTIONS:
                    if not any(n in low for n in needles):
                        errors.append(f"{d.rel}: '{d.maturity}' prompt lacks a {label} section")
            elif d.body_len > 4000:
                warnings.append(
                    f"{d.rel}: skeleton is unusually developed ({d.body_len} chars); "
                    "consider promoting it to draft"
                )

        mode = d.meta.get("Execution mode")
        if mode:
            primary = mode.split(",")[0].strip().lower()
            if primary not in MODES:
                errors.append(f"{d.rel}: execution mode '{primary}' not in {sorted(MODES)}")
        risk = d.meta.get("Risk class")
        if risk:
            code = risk.strip().upper()[:1]
            if code not in RISK:
                errors.append(f"{d.rel}: risk class '{risk}' not in A/B/C/D")
            elif code == "A":
                hit = None
                for m in DESTRUCTIVE.finditer(d.text):
                    sent_start = d.text.rfind(". ", 0, m.start())
                    sentence = d.text[max(0, sent_start):m.end()].lower()
                    if not re.search(r"\b(do not|never|must not|avoid|without|not)\b", sentence):
                        hit = m
                        break
                if hit:
                    warnings.append(
                        f"{d.rel}: risk class A but text mentions '{hit.group(0)}'; "
                        "confirm the action is gated or raise the class"
                    )

        # Structure (ignore fenced code blocks so templates/examples do not count)
        prose = []
        in_fence = False
        for ln in d.text.splitlines():
            if ln.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                prose.append(ln)
        h1 = [ln for ln in prose if ln.startswith("# ")]
        if len(h1) == 0:
            errors.append(f"{d.rel}: no H1 title")
        elif len(h1) > 1:
            warnings.append(f"{d.rel}: {len(h1)} H1 headings; keep exactly one")

        for m in LINK_RE.finditer(d.text):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(d.path), target))
            if not os.path.exists(resolved):
                errors.append(f"{d.rel}: broken relative link -> {target}")

        # Backticked repo paths that look like document references must exist.
        for span in re.findall(r"`([0-9]{2}-[a-z0-9-]+/[A-Za-z0-9_./-]+\.md)`", d.text):
            if not os.path.exists(os.path.join(ROOT, span)):
                warnings.append(f"{d.rel}: referenced path does not exist -> {span}")

        if d.is_prompt and not is_archive(d.rel):
            for token in ("[TODO", "TBD", "lorem ipsum", "<insert"):
                if token.lower() in d.text.lower():
                    warnings.append(f"{d.rel}: placeholder token '{token}' present")

        # Empty sections (a deeper sub-heading means the section has content)
        lines = d.text.splitlines()
        for i, ln in enumerate(lines):
            m = H2_RE.match(ln)
            if not m:
                continue
            level = len(ln) - len(ln.lstrip("#"))
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                warnings.append(f"{d.rel}: empty section '{m.group(1)}'")
                continue
            nxt = lines[j]
            if nxt.strip() == "---":
                warnings.append(f"{d.rel}: empty section '{m.group(1)}'")
            elif nxt.startswith("#"):
                nlevel = len(nxt) - len(nxt.lstrip("#"))
                if nlevel <= level:
                    warnings.append(f"{d.rel}: empty section '{m.group(1)}'")

    # Status-overclaim check per system folder (two levels below a top category).
    systems: dict[str, list[Doc]] = defaultdict(list)
    for d in docs:
        parts = d.rel.split(os.sep)
        if len(parts) >= 4 and re.match(r"\d{2}-", parts[0]):
            systems[os.sep.join(parts[:3])].append(d)
    for sysdir, members in systems.items():
        readme = next((m for m in members if m.rel.endswith("README.md")), None)
        stages = [m for m in members if m.is_prompt]
        if not readme or not stages:
            continue
        maturities = {s.maturity for s in stages}
        if maturities == {"skeleton"} and STATUS_OVERCLAIM.search(readme.text):
            word = STATUS_OVERCLAIM.search(readme.text).group(0)
            errors.append(
                f"{readme.rel}: advertises '{word}' while all "
                f"{len(stages)} stages are skeleton"
            )

    errors.extend(check_readme_counts(docs))
    errors.extend(check_documented_counts(docs))

    for d in docs:
        if d.is_prompt and d.rel.split(os.sep)[0] not in TOOLING_DIRS:
            e, w = check_inputs(d)
            errors.extend(e)
            warnings.extend(w)

    for d in docs:
        if is_archive(d.rel) or d.is_prompt:
            continue
        parts = d.rel.split(os.sep)
        if parts[0] in TOOLING_DIRS:
            continue
        if os.path.basename(d.rel) in {"README.md", "INDEX.md"} or d.rel in TOP_LEVEL_DOCS:
            continue
        if parts[0] == "00-core":
            continue  # reference documents, listed in the gallery's 00-core section
        if "<!-- not-a-prompt -->" in d.text:
            continue
        errors.append(
            f"{d.rel}: not a prompt (no Identifier) and not an allowed document — "
            "it will be missing from the catalog and gallery. Add a metadata block, "
            "or mark it `<!-- not-a-prompt -->` if it is supporting material."
        )

    return errors, warnings


# A row in the README's per-system table looks like:
#   | [`02-engineering/codebase-audit/`](02-engineering/codebase-audit/README.md) | 9 | operational |
README_COUNT_ROW = re.compile(r"^\|\s*\[`([A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*)/`\]\([^)]*\)\s*\|\s*(\d+)\s*\|", re.M)


def check_readme_counts(docs: list[Doc], readme_text: str | None = None) -> list[str]:
    """The README's system table must agree with the number of prompts on disk.

    This is the count that drifts most quietly. It drifted twice in one release:
    `03-domains/ai-agentic/` said 5 while holding 7, and `07-workflows/` said 12
    while holding 13. Neither is a lie anyone types; both are what happens when a
    prompt is added and the table is not revisited. Because the table is the first
    quantitative claim a reader meets, a stale row is a small, avoidable
    inaccuracy in the document that asks to be trusted.
    """
    text = readme_text
    if text is None:
        readme_path = os.path.join(ROOT, "README.md")
        if not os.path.exists(readme_path):
            return []
        with open(readme_path, encoding="utf-8") as fh:
            text = fh.read()

    errors: list[str] = []
    for prefix, claimed in README_COUNT_ROW.findall(text):
        actual = sum(
            1
            for d in docs
            if d.is_prompt
            and not is_archive(d.rel)
            and d.rel.replace(os.sep, "/").startswith(prefix + "/")
        )
        if int(claimed) != actual:
            errors.append(
                f"README.md: table says {claimed} prompts under {prefix}/ but {actual} exist — "
                "update the row (and the maturity in the same row) to match the tree"
            )
    return errors


# Maturity lines restated in prose. Each is a hand-maintained sentence, and each
# drifted every time a batch promoted a prompt: the number of `operational`
# prompts moved from 213 to 228 during one release, and four documents had to be
# edited by hand each time. A hand-maintained count beside a generated one is a
# claim waiting to become false.
DOC_MATURITY_LINES = [
    (
        "PROJECT-STATUS.md",
        re.compile(r"\*\*(\d+) operational\*\*,\s*\*\*(\d+) draft\*\*,\s*\*\*(\d+) skeleton\*\*"),
    ),
    (
        os.path.join("_meta", "publication-checklist.md"),
        re.compile(r"(\d+) operational, (\d+) draft, (\d+) skeleton"),
    ),
]


def check_documented_counts(
    docs: list[Doc], texts: dict[str, str] | None = None
) -> list[str]:
    """Prose counts must match the tree, in the same way the README table must.

    The generated files cannot drift: CI fails if they are stale. The documents a
    reader actually arrives through can, and did — a maturity line that says 213
    while the tree holds 228 is the quiet kind of wrong, because it looks like a
    measurement.

    `texts` maps a path to its content so tests can supply fixtures instead of
    reading the working tree.
    """
    prompts = [
        d
        for d in docs
        if d.is_prompt and not is_archive(d.rel) and d.rel.split(os.sep)[0] not in TOOLING_DIRS
    ]
    counts: dict[str, int] = {"operational": 0, "draft": 0, "skeleton": 0}
    for d in prompts:
        if d.maturity in counts:
            counts[d.maturity] += 1

    errors: list[str] = []
    for rel, pattern in DOC_MATURITY_LINES:
        if texts is not None:
            text = texts.get(rel)
        else:
            path = os.path.join(ROOT, rel)
            text = None
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
        if text is None:
            continue
        for op, dr, sk in pattern.findall(text):
            claimed = (int(op), int(dr), int(sk))
            actual = (counts["operational"], counts["draft"], counts["skeleton"])
            if claimed != actual:
                errors.append(
                    f"{rel}: says {op} operational / {dr} draft / {sk} skeleton but the tree "
                    f"has {actual[0]} / {actual[1]} / {actual[2]} — update the line"
                )
    return errors


def build_catalog(docs: list[Doc]) -> str:
    systems: dict[str, list[Doc]] = defaultdict(list)
    for d in docs:
        if not d.is_prompt or is_archive(d.rel) or d.rel.split(os.sep)[0] in TOOLING_DIRS:
            continue
        parts = d.rel.split(os.sep)
        key = os.sep.join(parts[:-2]) if len(parts) >= 3 else parts[0]
        systems[key].append(d)

    lines = [
        "# Catalog",
        "",
        "<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/validate_library.py --catalog -->",
        "",
        "Every prompt in the library, grouped by system, with its declared maturity,",
        "execution mode, and risk class. `skeleton` rows are structural outlines and",
        "are not ready to run. See `_meta/prompt-authoring-standard.md`.",
        "",
    ]
    counts = defaultdict(int)
    for key in sorted(systems):
        members = sorted(systems[key], key=lambda d: d.rel)
        lines.append(f"## `{key}`")
        lines.append("")
        lines.append("| ID | Stage | Maturity | Mode | Risk | File |")
        lines.append("|----|-------|----------|------|------|------|")
        for d in members:
            ident = d.identifier or "—"
            title = d.text.splitlines()[0].lstrip("# ").strip() if d.text else ""
            title = title[:60].replace("|", "/")
            mat = d.maturity or "—"
            counts[mat] += 1
            mode = (d.meta.get("Execution mode") or "—").split(",")[0].strip()
            risk = (d.meta.get("Risk class") or "—").strip()[:1]
            lines.append(f"| `{ident}` | {title} | {mat} | {mode} | {risk} | [{os.path.basename(d.rel)}](../{d.rel}) |")
        lines.append("")

    total = sum(counts.values())
    totals = (f"**Totals:** {total} prompts — " + ", ".join(
        f"{counts.get(m, 0)} {m}" for m in ("canonical", "operational", "draft", "skeleton")) + ".")
    # Insert after the introductory prose block, before the first system heading.
    insert_at = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))
    lines[insert_at:insert_at] = [totals, ""]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print errors only")
    ap.add_argument("--catalog", action="store_true", help="write _meta/CATALOG.md")
    args = ap.parse_args()

    docs = load(ROOT)
    errors, warnings = check(docs)
    errors = errors + check_system_readmes(docs)

    for e in errors:
        print(f"ERROR   {e}")
    if not args.quiet:
        for w in warnings:
            print(f"WARNING {w}")

    prompts = [
        d for d in docs
        if d.is_prompt and not is_archive(d.rel) and d.rel.split(os.sep)[0] not in TOOLING_DIRS
    ]
    by_mat = defaultdict(int)
    for d in prompts:
        by_mat[d.maturity or "unlabelled"] += 1

    print()
    print(f"Scanned {len(docs)} Markdown files; {len(prompts)} prompt files.")
    print("Maturity:", ", ".join(f"{k}={v}" for k, v in sorted(by_mat.items())))
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s).")

    if args.catalog:
        out = os.path.join(ROOT, "_meta", "CATALOG.md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(build_catalog(docs))
        print(f"Catalog written to {os.path.relpath(out, ROOT)}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
