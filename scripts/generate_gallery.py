#!/usr/bin/env python3
"""Generate GALLERY.md — a human-facing index of every prompt with a one-line purpose.

The gallery answers "which of these 260 prompts do I want?" without opening files:
each row links directly to the prompt and states what it is for. It is generated
from the prompt files themselves, so it cannot drift from the library.

Purpose text, in order of preference
------------------------------------
1. A `**Gallery:** ...` metadata line in the prompt (explicit override).
2. The first concrete line of the "Objective" section (bullet or paragraph),
   skipping role prose that begins "You are".
3. The prompt's `Produces:` metadata.
4. The first non-heading paragraph of the file.

Usage
-----
    python3 scripts/generate_gallery.py --write    # regenerate GALLERY.md
    python3 scripts/generate_gallery.py --check     # exit 1 if GALLERY.md is stale

Stdlib only. Safe to run in CI. `--check` is what keeps the promise that the
gallery is updated whenever a prompt is added.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import textwrap
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_library import ROOT, Doc, is_archive, load  # noqa: E402

OUT = os.path.join(ROOT, "GALLERY.md")
MAX_PURPOSE = 165

AREA_TITLES = {
    "00-core": "00-core — foundations every prompt assumes",
    "01-contribution": "01-contribution — contributing to open source",
    "02-engineering": "02-engineering — building, auditing, and recovering code",
    "03-domains": "03-domains — domain-specific engineering",
    "04-process": "04-process — delivering software responsibly",
    "05-scenarios": "05-scenarios — single-session, high-urgency situations",
    "06-interactive": "06-interactive — conversations that clarify a request",
    "07-workflows": "07-workflows — multi-system procedures",
}

AREA_BLURB = {
    "00-core": "Rules and protocols that apply to every other prompt.",
    "01-contribution": "Stage systems for contributing to an unfamiliar project.",
    "02-engineering": "Work on an existing codebase: audit, repair, complete, upgrade.",
    "03-domains": "Stack-specific practice: data, AI, and the domains still being built out.",
    "04-process": "The lifecycle around code: testing, release, observability, dependency and governance.",
    "05-scenarios": "One prompt, one session, one pressing situation.",
    "06-interactive": "Use when the request is vague and needs to be scoped first.",
    "07-workflows": "Composed sequences that route between systems and stop at human gates.",
}


def _clean(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" \t-—|*_")


def _first_sentence(text: str) -> str:
    text = text.strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return (m.group(1) if m else text).strip()


def _section(lines: list[str], pattern: str) -> list[str]:
    """Return the body lines of the first H2 whose title matches `pattern`."""
    h2 = [(i, ln[3:].strip()) for i, ln in enumerate(lines) if ln.startswith("## ")]
    for pos, (idx, title) in enumerate(h2):
        if re.search(pattern, title, re.I):
            end = h2[pos + 1][0] if pos + 1 < len(h2) else len(lines)
            return lines[idx + 1:end]
    return []


REJECT_PREFIXES = (
    "you are", "you will", "you must", "do not", "don't", "never", "out of scope",
    "this prompt is", "this stage", "in this stage", "before you", "if you",
    "see ", "scope:", "note:", "warning:", "rule:", "constraint:", "however",
)


def _pick_line(body: list[str]) -> str:
    """Choose the sentence that best states what the prompt is for.

    Role prose ("You are ...") and prohibitions ("Do not ...") are rejected: they
    describe the agent, not the job. Concrete bullets are preferred over such prose.
    """
    bullets, paras, buf = [], [], []
    for raw in body:
        line = raw.strip()
        if not line or line.startswith(("---", "|", "**Identifier", "#")):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if line.startswith(("- ", "* ")):
            bullets.append(_clean(line[2:]))
            continue
        if re.match(r"^\d+[.)]\s+", line):
            bullets.append(_clean(re.sub(r"^\d+[.)]\s+", "", line)))
            continue
        if line.startswith("```"):
            continue
        buf.append(line)
    if buf:
        paras.append(" ".join(buf))

    label_only = re.compile(r"^[A-Z][A-Za-z /&()-]{0,28}:$")

    def usable(text: str) -> bool:
        low = _clean(text).lower()
        if not low or low.startswith(REJECT_PREFIXES):
            return False
        # A bare label such as "Sequence:" or "Answer:" is structure, not purpose.
        return not label_only.match(_clean(text).strip())

    candidates = [p for p in paras if usable(p)] + [b for b in bullets if usable(b)]
    if not candidates:
        return ""
    # A three-word fragment ("Nothing is on fire.") says nothing about the job;
    # prefer the first candidate that actually describes it.
    for cand in candidates:
        sentence = _first_sentence(_clean(cand))
        if len(sentence) >= 30:
            return sentence
    return max((_first_sentence(_clean(c)) for c in candidates), key=len)


def purpose(doc: Doc) -> str:
    explicit = doc.meta.get("Gallery") or doc.meta.get("Use when")
    if explicit:
        return _clean(explicit)[:MAX_PURPOSE]

    lines = doc.text.splitlines()
    h2 = [ln[3:].strip() for ln in lines if ln.startswith("## ")]
    body = (
        _section(lines, r"objective|mission|purpose|goal|what this")
        or _section(lines, r"^\s*2\.")
    )
    text = _pick_line(body)
    if not text and h2:
        text = _pick_line(_section(lines, re.escape(h2[0])))
    produces = _clean(doc.meta.get("Produces", ""))
    if not text and produces and not produces.lower().startswith(("see ", "none")):
        if len(produces) > 3:
            head = produces[0].lower() if produces[1:2].islower() else produces[0]
            text = "Produces " + head + produces[1:]
        else:
            text = produces
    if not text:
        # first paragraph before any H2
        pre = []
        for line in lines[1:]:
            if line.startswith("## "):
                break
            if line.startswith("**") or not line.strip() or line.startswith("#"):
                continue
            if line.strip() == "---":
                break
            pre.append(line.strip())
        text = _first_sentence(_clean(" ".join(pre)))

    m_label = re.match(r"^(answer|produce|prove|establish|execute|implement|clarify|turn|build|plan|assess|deliverable|sequence)\s*:\s*(.*)$",
                       text, flags=re.I | re.S)
    if m_label:
        label, rest = m_label.group(1).lower(), m_label.group(2).strip()
        if label == "sequence":
            text = rest[0].upper() + rest[1:] if rest else text
        elif label == "answer" or re.match(r"^(what|which|who|how|why|when|where)\b", rest, re.I):
            text = "Answers: " + rest
        else:
            text = rest[0].upper() + rest[1:] if rest else text
    if not text:
        title = _title(doc).lower()
        system = doc.rel.split(os.sep)[-3] if len(doc.rel.split(os.sep)) >= 3 else ""
        if "orchestrator" in title or "orchestrat" in title:
            text = f"Runs the {system.replace('-', ' ')} system end to end: gates, routing, and final acceptance." if system else "Runs the system end to end: gates, routing, and final acceptance."
    text = re.sub(r"\s*\bthat can:\s*$", "", text)
    text = text.rstrip(":;, ")
    if len(text) > MAX_PURPOSE:
        cut = text[:MAX_PURPOSE].rsplit(" ", 1)[0]
        text = cut.rstrip(",;:") + "…"
    return text.replace("|", "/")


def _title(doc: Doc) -> str:
    raw = doc.text.splitlines()[0].lstrip("# ").strip() if doc.text else doc.rel
    raw = re.sub(r"^PROMPT\s+\d+\s*[—–-]\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s+Prompt$", "", raw)
    return _clean(raw).replace("|", "/")


def _natural(text: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text)]


def _sort_key(d: Doc):
    return (_natural(d.identifier or ""), d.rel)


def _system_key(rel: str) -> str:
    parts = rel.split(os.sep)
    return os.sep.join(parts[:-2]) if len(parts) >= 3 else parts[0]


def _system_blurb(rel: str) -> str:
    """First descriptive line of the system README, minus maturity boilerplate."""
    readme = os.path.join(ROOT, os.path.dirname(rel), "README.md")
    if not os.path.exists(readme):
        return ""
    with open(readme, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    for line in lines[1:]:
        line = line.strip()
        if not line or line.startswith(("#", "---", "|", "**Maturity", ">", "**Entry")):
            continue
        line = re.sub(r"^\*\*Maturity[^*]*\*\*\s*", "", line)
        return _first_sentence(_clean(line))
    return ""


def _anchor(text: str) -> str:
    """GitHub-style anchor: lowercase, drop punctuation, each space becomes a hyphen."""
    a = text.lower()
    a = re.sub(r"[^\w\s-]", "", a)
    return a.strip().replace(" ", "-")


TOOLING_DIRS = ("_meta",)


def _is_reference(rel: str) -> bool:
    """Foundational documents in 00-core: prompts in substance, reference in form."""
    return rel.startswith("00-core" + os.sep) and os.path.basename(rel) != "README.md"


def build_gallery(docs: list[Doc]) -> str:
    systems: dict[str, list[Doc]] = defaultdict(list)
    references: list[Doc] = []
    for d in docs:
        if is_archive(d.rel) or d.rel.split(os.sep)[0] in TOOLING_DIRS:
            continue
        if d.is_prompt:
            systems[_system_key(d.rel)].append(d)
        elif _is_reference(d.rel):
            references.append(d)

    by_area: dict[str, list[str]] = defaultdict(list)
    for key in sorted(systems):
        by_area[key.split(os.sep)[0]].append(key)

    total = sum(len(v) for v in systems.values())
    by_mat = defaultdict(int)
    for members in systems.values():
        for d in members:
            by_mat[d.maturity or "unlabelled"] += 1

    out: list[str] = [
        "# Prompt Gallery",
        "",
        "<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/generate_gallery.py --write -->",
        "",
        f"Every prompt in the library — **{total}** of them — with a direct link and the situation it is for,"
        + (f" plus **{len(references)}** foundational reference documents." if references else "."),
        "Generated from the prompt files, so it cannot drift from them; CI fails if this file is stale.",
        "",
        "**Reading the columns**",
        "",
        "| Column | Meaning |",
        "|---|---|",
        "| **ID** | Stable identifier used in cross-references and the catalog |",
        "| **Prompt** | Direct link to the file |",
        "| **Use it for** | The situation, taken from the prompt's own objective (or its author's `Gallery:` line) |",
        "| **Maturity** | `operational` = complete and reviewable; `draft` = usable with supervision; `skeleton` = outline, not runnable |",
        "| **Risk** | A = read-only, B = branch changes, C = shared environments, D = destructive |",
        "",
        "**Browse by area**",
        "",
        "| Area | Prompts | What it is for |",
        "|---|---:|---|",
    ]
    for area in sorted(by_area):
        n = sum(len(systems[k]) for k in by_area[area])
        title = AREA_TITLES.get(area, area)
        out.append(f"| [{title}](#{_anchor(title)}) | {n} | {AREA_BLURB.get(area, '')} |")
    out += [
        "",
        f"*Maturity across the library: "
        + ", ".join(f"{by_mat[m]} {m}" for m in ("operational", "draft", "skeleton") if by_mat[m])
        + f", {total} total.*",
        "",
        "---",
        "",
    ]

    for area in sorted(by_area):
        area_title = AREA_TITLES.get(area, area)
        out += [f"## {area_title}", "", AREA_BLURB.get(area, ""), ""]
        for key in by_area[area]:
            members = sorted(systems[key], key=_sort_key)
            name = key.split(os.sep, 1)[1] if os.sep in key else "All prompts in this area"
            out.append(f"### {name} · {len(members)} prompt{'s' if len(members) != 1 else ''}")
            blurb = "" if key == key.split(os.sep)[0] else _system_blurb(members[0].rel)
            if blurb:
                out += ["", f"*{blurb}*"]
            out += [
                "",
                "| ID | Prompt | Use it for | Maturity | Risk |",
                "|---|---|---|---|---|",
            ]
            for d in members:
                ident = d.identifier or "—"
                mat = d.maturity or "—"
                risk = (d.meta.get("Risk class") or "—").strip()[:1]
                p = purpose(d) or "—"
                out.append(
                    f"| `{ident}` | [{_title(d)}]({d.rel}) | {p} | {mat} | {risk} |"
                )
            out.append("")
        out.append("")

    if references:
        out += [
            "## 00-core — reference documents",
            "",
            "Foundational rules that the systems above assume. These are written as short reference",
            "documents rather than staged prompts, so they carry no identifier or maturity label.",
            "",
            "| Document | Use it for | Risk |",
            "|---|---|---|",
        ]
        for d in sorted(references, key=_sort_key):
            title = _title(d)
            p = purpose(d) or "—"
            risk = (d.meta.get("Risk class") or "A").strip()[:1]
            out.append(f"| [{title}]({d.rel}) | {p} | {risk} |")
        out.append("")

    out += [
        "---",
        "",
        "## Keeping this file current",
        "",
        "This gallery is generated, not maintained by hand. Whenever a prompt is added, renamed,",
        "or its objective changes:",
        "",
        "```bash",
        "python3 scripts/generate_gallery.py --write   # regenerate",
        "python3 scripts/generate_gallery.py --check   # what CI runs",
        "```",
        "",
        "CI fails when `GALLERY.md` no longer matches the library. To control the wording of a row,",
        "add a `**Gallery:** one line describing when to use this` metadata line to the prompt;",
        "the generator prefers it over the extracted objective.",
        "",
        "Related indexes: [`README.md`](README.md) routes by situation, [`_meta/CATALOG.md`](_meta/CATALOG.md)",
        "lists metadata for tooling, and [`_meta/coverage-matrix.md`](_meta/coverage-matrix.md) tracks what is",
        "covered — and what is not.",
        "",
    ]
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text if text.endswith("\n") else text + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="write GALLERY.md")
    ap.add_argument("--check", action="store_true", help="exit 1 if GALLERY.md is stale")
    ap.add_argument("--quiet", action="store_true", help="suppress the summary line")
    args = ap.parse_args()

    if not (args.write or args.check):
        ap.print_help()
        return 2

    docs = load(ROOT)
    rendered = build_gallery(docs)
    current = ""
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            current = fh.read()

    if args.check:
        if rendered == current:
            if not args.quiet:
                print("GALLERY.md is up to date.")
            return 0
        print("ERROR   GALLERY.md is stale. Run: python3 scripts/generate_gallery.py --write", file=sys.stderr)
        return 1

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    if not args.quiet:
        prompts = sum(1 for d in docs if d.is_prompt and not is_archive(d.rel) and d.rel.split(os.sep)[0] not in TOOLING_DIRS)
        print(f"GALLERY.md written: {prompts} prompts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
