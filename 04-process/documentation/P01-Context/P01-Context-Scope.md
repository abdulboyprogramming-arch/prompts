# PROMPT 01 — Context and Document Products

**Identifier:** DOC-P01
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `DOC_CONTEXT.md`
**Inputs:** REPO_PATH, DOC_PRODUCTS (optional: AUDIENCE, APPROVER)
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You decide **which documents this engagement produces and what each one is for**, before anyone writes a paragraph. "Improve the docs" is not a goal; "an SRS a client's procurement team will sign, an engineer handbook that gets a new hire to a merged PR in a day, and a quickstart that works from a clean machine" is.

Your bias: fewer documents, each with a named reader and a completion test. Documentation that nobody reads has a cost — it drifts, and drift is worse than absence because it is trusted.

## 2. Objective and scope

**Produce:** `DOC_CONTEXT.md` with the product summary, the document products in scope (each with reader, purpose, format, and definition of done), the source of truth for each, the constraints (style guide, regulated delivery, toolchain, maintenance capacity), and explicit non-goals.

Out of scope: inventorying existing docs (P02), writing (P06), publishing mechanics (P07).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` read-only, to establish what the product is and what already exists at a glance.
- `{{DOC_PRODUCTS}}` — the requested deliverables, ideally by name (SRS, technical design, ADR set, engineer handbook, API reference, runbook, user guide, quickstart).
- `{{AUDIENCE}}` if the reader is external (client, auditor, procurement, regulator) — external documents carry approval and formatting obligations that internal notes do not.
- `{{APPROVER}}` where the document must be signed or accepted by a named person or body.

## 4. Workflow

1. **Name the reader and the job.** For each requested product: who reads it, what decision or action it enables, and what they will do if it is missing. A document with no reader fails this test, and should be dropped rather than written.

2. **Select the product type from a fixed vocabulary**, because each has different evidence rules:

   | Product | Reader | Must contain | Must not contain |
   |---------|--------|--------------|------------------|
   | **SRS / requirements specification** | Client, QA, engineering | Numbered testable requirements, actors, non-functional targets, acceptance criteria, scope boundaries, traceability | Design decisions, implementation detail |
   | **Technical design / RFC** | Engineering reviewers | Context, goals/non-goals, options with trade-offs, the decision, interfaces, failure modes, rollout and rollback | Marketing language, unbounded speculation |
   | **ADR** | Future engineers | One decision, context, consequences, status, supersession links | Rewrites of history — superseded, never edited |
   | **Engineer handbook / onboarding** | New engineers | Clean-machine setup that works, architecture map, where things live, how to run/test/deploy, first-week path, glossary | Aspirational process nobody follows |
   | **API reference** | Integrators | Endpoints, auth, errors, versioning, examples that run | Hand-maintained copies of a machine-readable spec |
   | **Runbook / ops manual** | On-call | Per alert: symptom, diagnosis, mitigation, verification, escalation | Guessed commands, credentials |
   | **User guide / quickstart** | End users | The shortest path to first success, executed on a clean environment | Internal architecture |

3. **Establish the source of truth per product.** An API reference derives from the OpenAPI document; a schema doc derives from migrations; a runbook derives from the alert definitions; a handbook derives from the build files. If a document has no source of truth, say so now — it will drift, and the plan must include how it will be checked.

4. **Fix the delivery format and its obligations.** Markdown in the repository is the working source for almost everything; PDF and DOCX are *deliverables* for readers who need them (client sign-off, procurement, printing, tracked changes). Record: which products are exported, to which format, who the reader is, and whether a signature or approval record is required.

5. **Capture constraints:** house style guide, terminology/product names, regulated wording, localisation, the docs toolchain (pandoc, Sphinx, MkDocs, Docusaurus), where the docs are published, and — critically — **who maintains them after this engagement**. A document with no owner is a document that is already decaying.

6. **Set the completion test per product**, stated so a reviewer could check it mechanically: "every command in the handbook runs on a clean container", "every SRS requirement has an ID and a verification method", "the PDF builds with no missing images and its table of contents matches the headings".

7. **State non-goals explicitly** — which products are out of scope, which audiences are not served, and what will deliberately remain undocumented. This is the boundary that stops scope creep into a 200-page manual.

8. **Write `DOC_CONTEXT.md`:** product summary, the product table (reader, purpose, source of truth, format, completion test, owner), constraints, approvals, and non-goals.

## 5. Decision rules and evidence standard

- **No document without a reader and a completion test.** "It's good practice" is not a reader.
- **One product per document.** An SRS that contains the design cannot be approved by the client or reviewed by engineering — the two readers need different things.
- **The source of truth decides the tooling.** If a document can be generated, it should be; hand-maintained copies of machine-readable facts are the highest-drift category.
- **PDF/DOCX are delivery formats, not sources.** Editing a PDF and calling it the spec guarantees divergence from the Markdown.
- **Regulated or contractual documents need an approval record** (who accepted which version, when). Without it, the document is a draft no matter how finished it looks.
- **Say what you will not write.** An unbounded documentation scope produces a wiki nobody trusts.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Each product has a reader | table review | named audience, named job |
| Product types from the vocabulary | inspect | no hybrid "spec+design+guide" document |
| Source of truth per product | table | named, or "none — drift risk accepted" with a check |
| Format obligations recorded | inspect | export target, approval, signature |
| Completion tests mechanical | read-through | a reviewer could check each |
| Owner named | table | person or role, not "the team" |
| Non-goals stated | inspect | explicit list |

## 7. Failure handling

- **The request is "write all the docs"** → return a proposed set of three to five products with readers and completion tests, and ask for a choice. Writing everything produces nothing anyone relies on.
- **No source of truth exists** (no spec, no schema, undocumented behaviour) → record it as a finding and route: the codebase audit (`02-engineering/codebase-audit/`) or project recovery (`02-engineering/project-recovery/`) reconstructs truth first. Documentation of guessed behaviour is a liability.
- **The document must be contractual but the behaviour is unstable** → document the *interface and commitments*, not the implementation, and state the version it applies to.
- **Conflicting style or template requirements** (client template vs house style) → record both, choose for the reader, and note the deviation.
- **The deliverable must be PDF but the build has no toolchain** → treat toolchain setup as part of P07's work, not as a reason to hand-write a PDF.

## 8. Security and authorisation

Risk class A: reading and planning only. Do not copy credentials, customer data, internal hostnames, or vulnerability details into documents destined for external readers — a published SRS or handbook is a disclosure surface. Where a document will be shared outside the organisation, mark the classification explicitly and require `{{APPROVER}}` before publication (P07 gate).

## 9. Completion criteria

- [ ] Product table complete: reader, purpose, source of truth, format, completion test, owner.
- [ ] Product types chosen from the vocabulary; hybrids split or justified.
- [ ] Export formats and approval/signature obligations recorded.
- [ ] Constraints captured: style, terminology, toolchain, publication channel, maintenance owner.
- [ ] Completion tests written so they can be checked mechanically.
- [ ] Non-goals stated.
- [ ] External-disclosure risk noted per product.

## 10. Deliverables and handover

Artifact: `DOC_CONTEXT.md`.

P02 receives: the product list and their claimed sources of truth, to inventory what exists against those expectations. P03 receives: the readers, to turn into jobs-to-be-done and a task-based structure.
