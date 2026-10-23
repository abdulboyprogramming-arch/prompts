#!/usr/bin/env python3
"""Generate TASKS.md — the library indexed by the problem the reader has.

`GALLERY.md` is organised the way the repository is organised: by area and system.
That is the right shape for maintainers and the wrong shape for a visitor, who
arrives with a situation ("the deploy broke", "I inherited this codebase") and does
not know which of 362 prompts belongs to it.

This generator inverts the index. A task is a question a person asks; each task
declares the homes — directories — that answer it. The result is deterministic and
checked in CI, and it carries one enforced property:

    every prompt in the library is reachable from at least one task.

A prompt added without a home fails `--check` with the list of unrouted files, so
the index cannot silently fall behind the library. That property is the reason this
file is generated rather than written by hand.

How rows are chosen
-------------------
Within a task, `operational` and `draft` prompts are listed individually — they are
the material a reader can actually run. `skeleton` prompts are counted and left to
the gallery, because a 149-row wall of outlines would bury the useful rows. The
count is stated, never hidden: a task with four runnable prompts and eleven
outlines says so.

Usage
-----
    python3 scripts/generate_task_index.py --write   # regenerate TASKS.md
    python3 scripts/generate_task_index.py --check   # exit 1 if stale or unrouted

Stdlib only. Safe to run in CI.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gallery import purpose  # noqa: E402
from validate_library import ROOT, Doc, is_archive, load  # noqa: E402

OUT = os.path.join(ROOT, "TASKS.md")

# A task is (question, one-line orientation, homes, start-here note).
# `homes` are directory prefixes relative to the repository root; a prompt belongs
# to a task when its path starts with one of them. Prefix matching is deliberately
# coarse — it is auditable by eye, and the coverage check catches anything missed.
#
# Homes may overlap across tasks, and that is deliberate: a prompt answers more than
# one situation, and a reader who arrives from either side should find it. If the
# same directory appears under two tasks, check that both descriptions are true of
# it — a row that appears twice under a description that only fits once is worse
# than a missing row, because it looks like coverage.
TASKS: list[tuple[str, str, list[str], str]] = [
    (
        "Something is broken right now",
        "Diagnosis first, mitigation second, cause third. Every prompt here forbids the reverse order.",
        [
            "05-scenarios/debugging",
            "05-scenarios/failed-fix",
            "05-scenarios/flaky-tests",
            "05-scenarios/incident-response",
            "05-scenarios/security-incident",
            "05-scenarios/data-loss",
            "05-scenarios/disaster-recovery",
            "05-scenarios/performance-investigation",
            "05-scenarios/incident-communications",
            "05-scenarios/ai-output-verification",
            "05-scenarios/background-jobs",
            "05-scenarios/quick-fixes",
            "00-core/conversational/CHAT-DEBUG.md",
            "00-core/conversational/CHAT-MODE.md",
        ],
        "Start with `DBG-01` if the failure is reproducible in a repository you can run. "
        "Start with `CHAT-DEBUG` if all you have is a pasted error. "
        "Start with `JOBS-01` if what stopped is scheduled work and nothing threw.",
    ),
    (
        "I have to work in a codebase I have never seen",
        "Reconnaissance, then orientation, then a first contribution that survives review.",
        [
            "05-scenarios/onboarding",
            "05-scenarios/legacy-code",
            "01-contribution/open-source",
            "01-contribution/web",
            "01-contribution/web3",
            "01-contribution/packages-libraries",
            "01-contribution/language-design",
            "02-engineering/codebase-audit",
        ],
        "`ONBOARD-01` produces the orientation document; the `01-contribution` systems take it from there.",
    ),
    (
        "I need to change existing code without breaking it",
        "Safety net, smallest change, evidence that nothing else moved — and a decision about which change is worth making.",
        [
            "02-engineering/refactoring",
            "02-engineering/feature-completion",
            "02-engineering/feature-design-suggestion",
            "02-engineering/feature-portfolio",
            "02-engineering/rewriting-migration",
            "02-engineering/project-recovery",
            "05-scenarios/quick-fixes",
        ],
        "`02-engineering/feature-portfolio/` when the list is longer than the capacity and something has to be said no to; "
        "`05-scenarios/quick-fixes/` when the change is small; `02-engineering/refactoring/` when it is not.",
    ),
    (
        "I am starting something from nothing",
        "Scope, architecture, then a scaffold whose first commit a stranger can run.",
        [
            "02-engineering/from-scratch",
            "02-engineering/patterns-strategies-methods",
            "02-engineering/architecture-review",
            "05-scenarios/hackathon-sprint",
            "00-core/conversational/CHAT-DESIGN.md",
        ],
        "`02-engineering/from-scratch/` for a project; `05-scenarios/hackathon-sprint/` when the deadline is days, not months.",
    ),
    (
        "I need to know whether this codebase is healthy",
        "Audit and measurement, with the difference between 'no evidence of a problem' and 'evidence of no problem' kept explicit.",
        [
            "02-engineering/codebase-audit",
            "02-engineering/performance",
            "02-engineering/security-hardening",
            "05-scenarios/live-surface-audit",
            "05-scenarios/monorepo",
            "02-engineering/access-review",
            "02-engineering/tenancy-audit",
            "02-engineering/secrets-rotation",
            "02-engineering/time-correctness",
        ],
        "`02-engineering/codebase-audit/` is the general instrument; the scenarios answer one question each.",
    ),
    (
        "I am shipping a release",
        "Deployment, flags, supply chain, and the verification that the release is what you think it is.",
        [
            "04-process/release-engineering",
            "04-process/feature-flags",
            "04-process/dependency-management",
            "04-process/git-operations",
            "05-scenarios/deployment-target",
            "05-scenarios/platform-migration",
            "05-scenarios/infrastructure-as-code",
            "05-scenarios/feature-sunset",
            "05-scenarios/third-party-integration",
        ],
        "`04-process/release-engineering/` runs the sequence; the scenarios cover the decisions around it.",
    ),
    (
        "I need confidence that the tests mean something",
        "Test strategy, the fixtures that make it real, and triage for the tests that fail intermittently.",
        [
            "04-process/testing-qa",
            "05-scenarios/test-data",
            "05-scenarios/flaky-tests",
            "05-scenarios/build-performance",
        ],
        "`04-process/testing-qa/` sets the risk map before any test is written.",
    ),
    (
        "I have to review a change, or get mine reviewed",
        "A review that states what it did not see, and a pull request a maintainer can act on.",
        [
            "04-process/code-review",
            "05-scenarios/pr-authoring",
            "04-process/git-operations",
            "00-core/conversational/CHAT-REVIEW.md",
            "00-core/conversational/CHAT-MODE.md",
        ],
        "`04-process/code-review/` with repository access; `CHAT-REVIEW` when the diff arrives as a paste.",
    ),
    (
        "I am handing over a system, or taking one over",
        "What the receiver can do unaided, not what the sender explained.",
        [
            "04-process/handover",
            "05-scenarios/onboarding",
            "04-process/documentation",
            "00-core/conversational/CHAT-HANDOFF.md",
        ],
        "`04-process/handover/` for a person; `05-scenarios/on-call-handover/` for a rota change at speed.",
    ),
    (
        "Something costs too much or runs too slowly",
        "Measurement before optimisation, in money and in milliseconds.",
        [
            "03-domains/cost-engineering",
            "05-scenarios/performance-budget",
            "05-scenarios/build-performance",
            "05-scenarios/capacity-planning",
            "05-scenarios/usage-metering",
            "02-engineering/performance",
        ],
        "`05-scenarios/performance-investigation/` when it is slow now; `03-domains/cost-engineering/` when the invoice is the symptom.",
    ),
    (
        "I need to move or delete data",
        "Migrations and deletions that can be verified, not merely executed.",
        [
            "05-scenarios/data-migration",
            "05-scenarios/data-residency",
            "05-scenarios/data-loss",
            "04-process/privacy-requests",
            "03-domains/database",
        ],
        "`05-scenarios/data-migration/` for movement; `04-process/privacy-requests/` when the request is a legal obligation.",
    ),
    (
        "I am building with AI or agents",
        "Agent contracts, evaluation, permissions, and the context an agent needs to be useful rather than confident.",
        [
            "03-domains/ai-agentic",
            "04-process/agent-context",
            "00-core/agent-orchestration",
            "00-core/system-prompts",
            "00-core/safety-and-security",
            "05-scenarios/ai-output-verification",
        ],
        "`00-core/` states the rules the agent systems assume; `03-domains/ai-agentic/` builds the product.",
    ),
    (
        "I am building a game",
        "Vertical slice first, then systems, then content — with a playable build at every stage boundary.",
        ["03-domains/games"],
        "`03-domains/games/` runs the ten stages end to end.",
    ),
    (
        "I am building on a blockchain",
        "Contract-level discipline: invariants, access control, upgrade paths, and the audit trail a reviewer expects.",
        [
            "03-domains/web3",
            "01-contribution/web3",
            "03-domains/payments",
        ],
        "`03-domains/web3/` for a new protocol; `01-contribution/web3/` to contribute to an existing one.",
    ),
    (
        "I am building a specific kind of application",
        "Backend, frontend, mobile, desktop, embedded, data, or ML — each with its own failure modes.",
        [
            "03-domains/backend",
            "03-domains/frontend",
            "03-domains/mobile",
            "03-domains/desktop-cli",
            "03-domains/embedded-iot",
            "03-domains/data-engineering",
            "03-domains/data-ml-ai",
            "03-domains/devops-infra",
        ],
        "Pick the directory for your stack; each is a staged system with the same shape.",
    ),
    (
        "I need to answer someone outside engineering",
        "Compliance, vendors, contracts, and the evidence that survives an auditor who asks for a date and a sample.",
        [
            "04-process/governance-compliance",
            "04-process/licence-compliance",
            "04-process/standards-conformance",
            "04-process/accessibility-audit",
            "05-scenarios/vendor-due-diligence",
            "05-scenarios/supply-chain",
            "05-scenarios/abuse-prevention",
            "05-scenarios/client-secrets",
            "05-scenarios/email-deliverability",
            "05-scenarios/file-uploads",
            "05-scenarios/localization",
        ],
        "`04-process/governance-compliance/` maps a requirement to a practice and a piece of dated evidence.",
    ),
    (
        "I have to operate this in production",
        "Instrumentation, alerting, runbooks, and the handover that decides whether an on-call engineer can act alone.",
        [
            "04-process/observability-reliability",
            "05-scenarios/operational-readiness",
            "05-scenarios/on-call-handover",
            "05-scenarios/environment-parity",
            "05-scenarios/dev-environment",
            "05-scenarios/infrastructure-as-code",
            "05-scenarios/capacity-planning",
        ],
        "`05-scenarios/operational-readiness/` before launch; `04-process/observability-reliability/` once it is live.",
    ),
    (
        "I am running the work, not just the code",
        "Process design, decommissioning, and the improvement cycle that survives a busy quarter.",
        [
            "04-process/project-management",
            "04-process/research-and-development",
            "04-process/systems-building-improvement",
            "04-process/decommissioning",
            "05-scenarios/automation",
            "05-scenarios/background-jobs",
        ],
        "`04-process/systems-building-improvement/` for the process; `04-process/project-management/` for the plan.",
    ),
    (
        "I am writing a prompt, or setting up an agent",
        "The meta level: how a prompt is built, routed, and kept honest about what it cannot do.",
        [
            "00-core/prompt-engineering",
            "00-core/inputs",
            "06-interactive",
            "00-core/conversational/CHAT-SELECT.md",
        ],
        "`00-core/prompt-engineering/` writes the prompt; `06-interactive/` gathers the context it needs first.",
    ),
    (
        "The work spans several systems",
        "Composed procedures with named human gates and a handoff contract between stages.",
        ["07-workflows"],
        "`07-workflows/` sequences the other systems; start from the README's routing table.",
    ),
    (
        "I only have a chat window",
        "What survives when there is no repository, no shell, and no way to run a test.",
        ["00-core/conversational"],
        "`CHAT-MODE` adapts any other prompt; the three task prompts are already written for chat.",
    ),
]

GALLERY_ANCHORS = {
    "00-core": "00-core--foundations-every-prompt-assumes",
    "01-contribution": "01-contribution--contributing-to-open-source",
    "02-engineering": "02-engineering--building-auditing-and-recovering-code",
    "03-domains": "03-domains--domain-specific-engineering",
    "04-process": "04-process--delivering-software-responsibly",
    "05-scenarios": "05-scenarios--single-session-high-urgency-situations",
    "06-interactive": "06-interactive--conversations-that-clarify-a-request",
    "07-workflows": "07-workflows--multi-system-procedures",
}


def _title(doc: Doc) -> str:
    raw = doc.text.splitlines()[0].lstrip("# ").strip() if doc.text else doc.rel
    raw = re.sub(r"^PROMPT\s+\d+\s*[—–-]\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s+Prompt$", "", raw)
    return re.sub(r"\s+", " ", raw).replace("|", "/").strip()


def _clip(text: str, limit: int = 130) -> str:
    """Cut at a word boundary; a mid-word cut reads as a rendering bug."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return cut + "…"


def _natural(text: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text)]


def _key(doc: Doc):
    return (_natural(doc.identifier or ""), doc.rel)


def _home(rel: str) -> str:
    return "/".join(rel.split("/")[:-1])


def _matches(rel: str, home: str) -> bool:
    """A home is a directory prefix, or an exact file when it ends in `.md`."""
    if home.endswith(".md"):
        return rel == home
    here = _home(rel)
    return here == home or here.startswith(home + "/")


def route(docs: list[Doc]) -> tuple[dict[int, list[Doc]], list[Doc]]:
    """Assign each prompt to the tasks whose homes contain it; return unrouted ones."""
    prompts = [
        d
        for d in docs
        if d.is_prompt and not is_archive(d.rel) and not d.rel.startswith("_meta" + os.sep)
    ]
    routed: dict[int, list[Doc]] = {i: [] for i in range(len(TASKS))}
    assigned: set[str] = set()
    for doc in prompts:
        for i, (_, _, homes, _) in enumerate(TASKS):
            if any(_matches(doc.rel, h) for h in homes):
                routed[i].append(doc)
                assigned.add(doc.rel)
    unrouted = sorted((d for d in prompts if d.rel not in assigned), key=_key)
    return routed, unrouted


def build(docs: list[Doc]) -> tuple[str, list[Doc]]:
    routed, unrouted = route(docs)
    total = sum(len(v) for v in routed.values())
    uniq = len({d.rel for v in routed.values() for d in v})
    operational = sum(1 for v in routed.values() for d in v if d.maturity == "operational")
    out: list[str] = [
        "# Tasks — start from the problem, not the folder tree",
        "",
        "<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/generate_task_index.py --write -->",
        "",
        f"**{uniq} prompts**, indexed by the situation you are in. Each task lists the prompts that are",
        "**runnable** — `operational` and `draft`. The `skeleton` outlines are counted per task and linked",
        "to the gallery, because a wall of outlines would bury the rows that work today.",
        "",
        "Generated from the prompt files and checked in CI, so it cannot drift. Every prompt in the",
        "library is reachable from at least one task: a prompt added without a home fails the build.",
        "",
        "| | |",
        "|---|---|",
        f"| Prompts indexed | {uniq} |",
        f"| Rows listed individually | {total} (a prompt can answer more than one task) |",
        f"| Of those, `operational` | {operational} |",
        "",
        "Not sure which task is yours? [`QUICKSTART.md`](QUICKSTART.md) routes five common situations,",
        "[`06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md`](06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md)",
        "asks three questions, and [`GALLERY.md`](GALLERY.md) is the complete flat list.",
        "",
        "---",
        "",
    ]

    for i, (question, blurb, homes, start) in enumerate(TASKS):
        members = sorted(routed[i], key=_key)
        runnable = [d for d in members if d.maturity in ("operational", "draft")]
        skeletons = [d for d in members if d.maturity not in ("operational", "draft")]
        areas = sorted({d.rel.split("/")[0] for d in members})
        out += [f"## {question}", "", blurb, ""]
        if start:
            out += [f"**Start here.** {start}", ""]
        if runnable:
            out += [
                "| ID | Prompt | Where | Use it for | Maturity |",
                "|---|---|---|---|---|",
            ]
            for d in sorted(runnable, key=lambda x: (_home(x.rel), _key(x))):
                ident = d.identifier or "—"
                use = _clip(purpose(d) or "—")
                leaf = _home(d.rel).split("/")[-1]
                out.append(
                    f"| `{ident}` | [{_title(d)}]({d.rel}) | `{leaf}` | {use} | {d.maturity} |"
                )
            out.append("")
        if skeletons:
            links = ", ".join(
                f"[{a}](GALLERY.md#{GALLERY_ANCHORS[a]})" for a in areas if a in GALLERY_ANCHORS
            )
            out += [
                f"*Plus **{len(skeletons)}** `skeleton` prompt{'s' if len(skeletons) != 1 else ''} in these homes — "
                f"a defensible stage sequence without verification or failure handling. Use them to structure a "
                f"human-led session, not to drive an agent: {links}.*",
                "",
            ]
        out.append("")

    out += [
        "---",
        "",
        "## How this index stays honest",
        "",
        "`scripts/generate_task_index.py` reads the prompt files, assigns each to the tasks whose homes",
        "contain it, and fails when a prompt belongs to none of them. Two rules follow from that:",
        "",
        "1. **A new prompt needs a home.** Add its directory to a task in the generator; the build stops",
        "   until you do. The index cannot quietly fall behind the library.",
        "2. **Maturity is not rounded up.** A task that lists four runnable prompts and eleven outlines",
        "   says exactly that, because the counts come from the same metadata the validator checks.",
        "",
        "Related: [`GALLERY.md`](GALLERY.md) by area · [`_meta/CATALOG.md`](_meta/CATALOG.md) for tooling ·",
        "[`_meta/coverage-matrix.md`](_meta/coverage-matrix.md) for what is covered and what is not.",
        "",
    ]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return (text if text.endswith("\n") else text + "\n"), unrouted


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="write TASKS.md")
    ap.add_argument("--check", action="store_true", help="exit 1 if TASKS.md is stale or a prompt is unrouted")
    args = ap.parse_args()
    if not (args.write or args.check):
        ap.print_help()
        return 2

    rendered, unrouted = build(load(ROOT))
    if unrouted:
        print(f"ERROR   {len(unrouted)} prompt(s) belong to no task — add their directory to TASKS:", file=sys.stderr)
        for d in unrouted:
            print(f"        {d.rel}", file=sys.stderr)
        return 1

    current = ""
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            current = fh.read()

    if args.check:
        if current != rendered:
            print("ERROR   TASKS.md is stale — run: python3 scripts/generate_task_index.py --write", file=sys.stderr)
            return 1
        print("TASKS.md is up to date.")
        return 0

    if current == rendered:
        print("TASKS.md already up to date; nothing written.")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    print(f"TASKS.md written: {len(TASKS)} tasks, {len(rendered.splitlines())} lines.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
