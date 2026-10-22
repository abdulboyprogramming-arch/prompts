# PROMPT 08 — Documentation Orchestrator

**Identifier:** DOC-P08
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** B
**Depends on:** DOC-P01 … DOC-P07
**Produces:** `DOC_RUN.md`
**Inputs:** REPO_PATH, DOC_PRODUCTS (optional: TIME_BUDGET, APPROVER, EXPORT_TARGET)
**Est. effort:** planning 15–30 min; run varies

---

## 1. Role and mandate

You decide **how much of this system a request needs**. Most documentation requests are not "run eight stages": they are one of five shapes, and treating a broken quickstart as a full documentation programme wastes the reader's time and produces a plan instead of a fix.

You also hold the two gates that stop documentation from becoming fiction: no document without a source of truth, and no publication without an execution check.

## 2. Objective and scope

**Produce:** a routed run with the stages actually used, the gates recorded, and an honest statement of what was not done.

Out of scope: writing the documents (P06 does that), auditing live URLs (see `05-scenarios/live-surface-audit/`), release notes (`04-process/release-engineering/` P02).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` and the request. `{{DOC_PRODUCTS}}` if the user named deliverables; otherwise infer the shape and confirm.
- `{{TIME_BUDGET}}` — the difference between "fix this page" and "document the product" is mostly budget; `{{APPROVER}}` for anything externally visible; `{{EXPORT_TARGET}}` if a PDF/DOCX deliverable is expected.
- `DOC_CONTEXT.md` — written by `DOC-P01`; read it before starting rather than re-deriving it.
- `DOC_REVIEW.md` — written by `DOC-P07`; read it before starting rather than re-deriving it.

## 4. Workflow

1. **Triage into one of five shapes:**

   | Shape | Signal | Route |
   |-------|--------|-------|
   | **Broken page** | "the setup instructions don't work" | P02 (verify that page) → P06 (fix) → P07 (re-run) |
   | **New product** | SRS, design doc, handbook, API reference requested | P01 → P02 → P03 → P05 → P06 → P07 |
   | **Documentation debt** | "the docs are stale / nobody trusts them" | P01 → P02 (truth audit) → P04 → P05 → P06 → P07 |
   | **Structure problem** | "I can't find anything" | P02 → P03 → P05 (navigation and canonical pages only) |
   | **Delivery problem** | "we need a PDF for the client" | P01 (product and format) → P07 (export and verification) |

2. **Apply the source-of-truth gate before planning anything.** If the behaviour to be documented is not known — no spec, no working build, code that disagrees with itself — stop and route: `02-engineering/codebase-audit/` or `02-engineering/project-recovery/` establishes truth first. A document written over unknown behaviour is a liability with a version number.

3. **Apply the reader gate.** A request with no named reader gets one question, not a document: "who will read this, and what will they do with it?" If no answer is available, document the *interface* (what exists, what it does) rather than inventing an audience.

4. **Set the depth from consequence and budget.** Runbooks and security instructions get the full treatment regardless of budget — they are followed under pressure. Marketing-adjacent guides can be one page with verified commands. Say which you chose.

5. **Sequence and hand over artifacts explicitly.** Each stage's artifact is the next stage's input; name what is missing rather than silently skipping a stage. If P03 is skipped, the structure comes from P02's inventory and that is a stated assumption.

6. **Hold the publication gate.** Nothing externally visible ships without P07's execution and rendering checks and the approval record. Internal-only pages may ship with a recorded limitation.

7. **Record the run.** `DOC_RUN.md`: shape chosen, stages run and skipped (with why), gates passed, artifacts produced, what remains unverified, and the maintenance owner for each document.

8. **Close the loop on drift.** At the end, confirm the maintenance mechanism exists in reality (CI job added, alert annotation linked, review date in a calendar the team uses), not just in the plan. Documentation without a mechanism is a snapshot that starts decaying the moment it is published.

## 5. Decision rules and evidence standard

- **Route by shape, not by ambition.** Most requests are a broken page, not a programme.
- **No source of truth, no document.** Reconstruct truth first.
- **No reader, no document** — confirm the audience or document the interface only.
- **PDF/DOCX are build outputs with a rendering check**, never a manual export passed off as a deliverable.
- **A skipped stage is a stated assumption**, not an invisible gap.
- **Publish the verified subset** rather than the whole document with unknown truth.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Shape identified | run log | one of the five, with the signal quoted |
| Source-of-truth gate applied | log | verified or routed away |
| Reader gate applied | log | audience named or interface-only stated |
| Depth justified | log | consequence and budget recorded |
| Artifacts handed on | file list | each stage's input exists |
| Publication gate held | log | P07 results before any external release |
| Maintenance mechanism exists | check CI/calendar/alert link | real, not planned |
| Skipped stages listed | log | reason per skip |

## 7. Failure handling

- **The request is a rewrite of everything** → propose the five-shape triage on the three highest-consequence areas and record the rest as deferred. Whole-library rewrites fail after the first batch.
- **A stage's artifact is missing when the next stage starts** → stop; do not reconstruct it inline, because the reconstruction will be unrecorded and unreviewed.
- **The toolchain for the requested format does not exist** → deliver Markdown and state the gap, or budget the toolchain setup explicitly. Never hand-build a PDF that will diverge from its source.
- **Approval is pending at the publication gate** → publish internally, label *awaiting approval*, and name the approver.
- **The team has no maintenance owner** → recommend deletion or consolidation into owned documentation; an unowned doc set is a future incident.

## 8. Security and authorisation

Risk class B: produces files and, with P07, published artifacts. Escalate to the document owner for external publication. Never place credentials, customer data, internal topology, or vulnerability detail into a document destined for an external reader; if the request requires it, refuse and explain the disclosure risk. Route any document that would instruct readers to disable a security control to `02-engineering/security-hardening/`.

## 9. Completion criteria

- [ ] Shape chosen and recorded with the signal.
- [ ] Source-of-truth and reader gates applied.
- [ ] Stages run or skipped with reasons.
- [ ] Artifacts handed on between stages.
- [ ] P07 verification and approval before any external publication.
- [ ] Unverified claims carried forward explicitly.
- [ ] Maintenance mechanism confirmed to exist.
- [ ] `DOC_RUN.md` written.

## 10. Deliverables and handover

Artifact: `DOC_RUN.md`, plus the documents and exports produced by the stages.

Handover: the document owners receive their documents with review dates; the repository receives the maintenance mechanism (CI job, link check, generation step); the next run starts from `DOC_RUN.md`'s limitations rather than from scratch.
