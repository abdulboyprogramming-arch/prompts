# Documentation

**Maturity: operational (v1.0.0).** Eight stages that take a documentation request — an SRS for a client, a handbook for new engineers, a runbook, a broken quickstart — and produce documents whose claims have been checked and whose exports have been rendered and read.

**Entry point:** [`P08-Orchestrator`](P08-Orchestrator/P08-Documentation-Orchestrator.md) routes by shape; start at [`P01-Context`](P01-Context/P01-Context-Scope.md) for a new document product.
**Execution mode:** planning
**Per stage:** planning (P01, P03, P05), diagnostic (P02, P04, P07), implementation (P06), orchestration (P08)
**Risk class:** A–B (P07 publishes, so its approval gate matters)

## Why this system exists

Documentation fails in two directions, and most guidance addresses neither:

- **Unreadable**: organised by system component when the reader arrives with a task, no prerequisites, no expected output, five minutes lost on every step.
- **Untrue**: commands that no longer run, endpoints that were renamed, an architecture diagram from two releases ago, a runbook whose mitigation no longer works — and, worst, a page that documents behaviour that was never built.

Untrue documentation is worse than none, because it is trusted. This system makes truth a gate: no document without a source of truth, no command that was not executed, no export that was not opened and read.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DOC-P01 | [Context & products](P01-Context/P01-Context-Scope.md) | Which documents, for which reader, from which source of truth, in which format | `DOC_CONTEXT.md` |
| DOC-P02 | [Inventory & truth audit](P02-Inventory/P02-Documentation-Inventory.md) | What exists, who owns it, and whether its claims still hold — checked, not assumed | `DOC_INVENTORY.md` |
| DOC-P03 | [Audience & structure](P03-Audience-Goals/P03-Audience-Goals.md) | Personas with evidence, jobs with completion tests, task-first structure | `AUDIENCE_GOALS.md` |
| DOC-P04 | [Gap analysis](P04-Gap-Analysis/P04-Gap-Analysis.md) | Gaps ranked by what happens to the reader, with evidence and a fix shape | `DOC_GAPS.md` |
| DOC-P05 | [Plan](P05-Plan/P05-Documentation-Plan.md) | Ordered deliverables, acceptance tests, owners, and the mechanism that keeps them true | `DOC_PLAN.md` |
| DOC-P06 | [Writing](P06-Writing/P06-Writing-Improvement.md) | Authoring per product type; every command executed or labelled unverified | documents + `DOC_IMPLEMENTATION_LOG.md` |
| DOC-P07 | [Review, export, publish](P07-Review/P07-Review-Validation.md) | Re-run the claims, build PDF/DOCX, inspect every page, record approval | `DOC_REVIEW.md` |
| DOC-P08 | [Orchestrator](P08-Orchestrator/P08-Documentation-Orchestrator.md) | Triage into five shapes; hold the source-of-truth and publication gates | `DOC_RUN.md` |

## Document products and what each must contain

| Product | Reader | Non-negotiable content | Forbidden content |
|---------|--------|------------------------|-------------------|
| SRS | Client, QA, engineering | Numbered testable requirements with a verification method, actors, non-functional targets, acceptance criteria, traceability, change log | Design decisions, implementation detail |
| Technical design / RFC | Engineering reviewers | Options with trade-offs, the decision and why, interfaces, failure modes, rollout and rollback | Marketing language, unresolved speculation presented as plan |
| ADR | Future engineers | One decision, context, consequences, status, supersession | Edits to accepted decisions |
| Engineer handbook | New engineers | A clean-machine setup that was executed, architecture map, where things live, first-week path, glossary | Aspirational process nobody follows |
| API reference | Integrators | Auth, errors, pagination, limits, versioning, an executed example — generated from the spec where possible | Hand-maintained copies of machine-readable facts |
| Runbook | On-call | Per alert: symptom, diagnosis with expected output, mitigation and its risk, verification, escalation | Guessed commands, credentials |
| Quickstart / user guide | Users | Shortest path to first success, prerequisites at point of use, expected output per step | Internal architecture |

## The rules

1. **No document without a source of truth.** Unknown behaviour is reconstructed first (`codebase-audit`, `project-recovery`), not guessed.
2. **Every command is executed or explicitly labelled unverified.**
3. **A requirement is testable or it is a wish.** "Shall be fast" is not a requirement.
4. **Task-first structure**; one canonical page per instruction; link, never copy.
5. **PDF and DOCX are build outputs.** They are generated from Markdown and then *opened and read* — build exit codes prove nothing about page 7.
6. **Delete wrong pages** instead of annotating them.
7. **Every document has an owner and a review trigger**, or it is scheduled for decay at creation.
8. **Never document unbuilt behaviour.** This is the highest-severity defect in the system.

## Export and delivery

The working source is Markdown in the repository. PDF/DOCX are produced for readers who need them (client sign-off, procurement, printing, tracked changes):

```bash
pandoc DOC.md -o DOC.pdf --pdf-engine=xelatex --toc --number-sections -V geometry:margin=2.5cm
pandoc DOC.md -o DOC.docx --reference-doc=reference.docx --toc
```

Both are then verified by P07: every page opened, code blocks intact, tables inside margins, contents matching headings, fonts covering the glyphs used, title and language set, outline present. A DOCX is opened in a real editor; a PDF is read, not just generated.

## Boundaries

- Runbooks for specific alerts: `04-process/observability-reliability/P04`.
- Release notes and versioning: `04-process/release-engineering/P02`.
- Reading and judging an existing *live site or endpoint* from outside: `05-scenarios/live-surface-audit/`.
- Verifying whether claimed work was actually done: `07-workflows/independent-verification.md`.

## What this system will not do

- Write marketing copy or product positioning.
- Guarantee the system matches the SRS. It can check that requirements are testable and that the document states what exists; verifying implementation is `codebase-audit` and `feature-completion`.
- Replace human acceptance for contractual documents. It produces the approval record; a person still signs.
