# PROMPT 05 — Documentation Plan

**Identifier:** DOC-P05
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** DOC-P04
**Produces:** `DOC_PLAN.md`
**Inputs:** DOC_PRODUCTS, TIME_BUDGET (optional: APPROVER, CHANGE_WINDOW)
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You convert a ranked gap list into a plan that can be executed and then *maintained*. Most documentation plans fail after delivery, not during it: the pages are written, nobody owns them, and within two releases they describe a system that no longer exists.

Your plan therefore has two halves — what will be written, and **what will keep it true**.

## 2. Objective and scope

**Produce:** `DOC_PLAN.md` — ordered deliverables with acceptance tests, per-item owner and review date, the maintenance mechanism per document class, the export/publish path, and the explicit deferrals.

Out of scope: writing the documents (P06), running the review and export (P07).

## 3. Prerequisites and inputs

- `DOC_GAPS.md` (ranked), `AUDIENCE_GOALS.md` (structure and paths), `DOC_CONTEXT.md` (products, formats, owners).
- `{{DOC_PRODUCTS}}` in scope, `{{TIME_BUDGET}}` for the effort available; `{{APPROVER}}` where acceptance or publication requires sign-off; `{{CHANGE_WINDOW}}` if documents must be released with a specific version.

## 4. Workflow

1. **Sequence by consequence, then by path.** All S1 gaps first (harmful instructions), then the gaps that break a reading path, then the rest. A path that is 80% complete is unusable; finish paths.

2. **Group work by canonical document**, not by gap id. Five gaps in one runbook are one rewrite with five acceptance points.

3. **Write an acceptance test per deliverable**, phrased so P07 can run it: "a clean container reaches a green test run using only this page", "every SRS requirement has an ID, a verification method, and no design content", "the PDF builds from the Markdown source and its contents page matches the headings".

4. **Assign ownership and a review date now.** One named owner per document; a review cadence tied to a trigger (each release, each schema change, each incident) rather than a vague "quarterly". A document with no owner is scheduled for decay at creation.

5. **Choose the maintenance mechanism per document class, and state its limits:**

   | Class | Mechanism | What it cannot catch |
   |-------|-----------|----------------------|
   | Reference generated from a spec/schema/CLI | Build-time generation in CI | Specs that are themselves stale |
   | Quickstart / handbook | Executed in CI on a clean container | Steps a human must do (DNS, DNS-like manual approvals) |
   | Runbook | Linked from the alert; exercised in a game day | Alerts whose definitions change silently |
   | Design doc / ADR | Immutable once accepted, superseded by a new one | Decisions that are never revisited |
   | SRS / contractual | Version stamp + approval record + change log | Behaviour changed without a spec change |

6. **Plan the export and publication path.** Which products are exported to PDF or DOCX, from what source, with which tool (`pandoc` with a reference document, Sphinx, MkDocs PDF plugin), where the output is stored, and who verifies the rendered result. Treat the export as a build artifact with a check, not a manual "save as".

7. **Account for the cost of removal.** Each deleted page needs redirects where URLs are public, and a note in the changelog where readers will look for it.

8. **State deferrals and refusals explicitly**: what will not be written, why, and what a reader should do instead. Plans that silently omit work are discovered by the reader, not the author.

9. **Write `DOC_PLAN.md`:** ordered table (id, deliverable, gaps closed, acceptance test, owner, review date, effort), the maintenance matrix, export/publication path, dependencies, deferrals, and the definition of done for the whole engagement.

## 5. Decision rules and evidence standard

- **No deliverable without an acceptance test and an owner.**
- **Finish paths, don't average them.** Partial paths cost readers more than absent ones because they signal completeness.
- **Maintenance is part of the deliverable.** A plan without a mechanism is a plan to be wrong in six months.
- **Generated beats hand-maintained** whenever the source of truth is machine-readable. Budget the generator, not the transcription.
- **PDF/DOCX are build outputs.** Plan the toolchain and a rendering check, not a manual conversion.
- **Say what you are not doing**, with the reader's fallback.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| S1 gaps scheduled first | table order | all S1 in the first batch |
| Acceptance tests runnable | read-through | P07 could execute each |
| Owner and review date per item | table | no blanks |
| Maintenance mechanism per class | matrix | mechanism + stated blind spot |
| Export path defined | inspect | tool, source, output location, verifier |
| Deferrals stated | artifact | reason and fallback |
| Whole-engagement done defined | inspect | measurable |

## 7. Failure handling

- **Effort exceeds the budget** → cut by consequence and *delete* rather than half-write the remainder; record the cut so it is visible.
- **No owner available for a document** → propose deletion or merge into a document that has one. Unowned documentation is a liability, not an asset.
- **A document must be contractual but behaviour is still moving** → plan the version stamp, the change log, and an explicit "applies to version X" line.
- **The PDF toolchain is unavailable or unreliable** → say so before writing; a manually maintained PDF will diverge from its Markdown source, and the plan should either fix the toolchain or choose a format the toolchain can produce.
- **Approval dependency blocks a path** (legal, client sign-off) → sequence the dependent documents after it and mark the path as blocked, not "in progress".

## 8. Security and authorisation

Risk class A: planning. Any document destined for external readers needs the `{{APPROVER}}` gate in its acceptance test. Plans must not include copying production data, customer records, or internal credentials into examples; specify synthetic data instead.

## 9. Completion criteria

- [ ] Ordered deliverables with the gaps each closes.
- [ ] Acceptance test per deliverable, executable by P07.
- [ ] Owner and review trigger per document.
- [ ] Maintenance mechanism and blind spot per document class.
- [ ] Export/publication path with a rendering check.
- [ ] Removal costs (redirects, changelog notes) accounted for.
- [ ] Deferrals and refusals stated with fallbacks.
- [ ] Engagement definition of done written.

## 10. Deliverables and handover

Artifact: `DOC_PLAN.md`.

P06 receives: the ordered deliverables, their acceptance tests, and the source of truth for each. P07 receives: the acceptance tests and the export path, to verify rather than assume.
