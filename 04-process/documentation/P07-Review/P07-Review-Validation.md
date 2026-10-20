# PROMPT 07 — Review, Export, and Publication

**Identifier:** DOC-P07
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** DOC-P06
**Produces:** `DOC_REVIEW.md`, published artifacts (Markdown site, PDF, DOCX)
**Inputs:** REPO_PATH, DOC_PRODUCTS (optional: EXPORT_TARGET, APPROVER)
**Est. effort:** 30–90 min, plus export time

---

## 1. Role and mandate

You are the last reader before an audience sees the document. Two failures are yours to catch:

1. **Untruth** — a claim that does not match the system.
2. **A broken artifact** — the PDF renders with cut-off code, missing images, mangled tables, or a contents page that points at nothing.

"Pandoc exited zero" is not a verification. Anyone who has shipped a PDF knows the failure is usually in what the reader sees on page 7.

## 2. Objective and scope

**Produce:** a passed (or honestly failed) review against each acceptance test, verified exports where the product requires them, an approval record where required, and `DOC_REVIEW.md` recording what was checked and by what method.

Out of scope: rewriting the content (return to P06), deciding what to publish (P05).

## 3. Prerequisites and inputs

- The documents, `DOC_IMPLEMENTATION_LOG.md` (what the author claims was verified), and the acceptance tests from `DOC_PLAN.md`.
- `{{REPO_PATH}}` for re-running commands; `{{DOC_PRODUCTS}}` to know which products need export; `{{EXPORT_TARGET}}` (PDF, DOCX, static site) and the approval requirements; `{{APPROVER}}` for external or contractual documents.

## 4. Workflow

1. **Re-verify the author's claims rather than reading them.** Run the commands again from a clean state, follow the reading path as a reader would, and check the version stamp. An author's "tested" is a claim; a second execution is evidence.

2. **Read for the reader's task.** For each acceptance test, ask whether a competent person with no context could complete it using only this page. Where they would stop, the page fails — record where.

3. **Audit the facts against their sources** in a sample proportional to consequence: all commands, all endpoints and env vars, all stated versions and limits, all security-relevant statements. For a runbook, check every command against the current tooling; for an SRS, check every requirement against the system's actual behaviour or mark it aspirational.

4. **Check the dangerous content explicitly:** credentials or tokens (must be absent), internal hostnames in external documents, instructions that disable a control, destructive commands without a warning, and examples that would delete real data if pasted.

5. **Build the exports from source.** Run the documented build (`pandoc`, Sphinx, MkDocs plugin) into a clean output directory. Then verify what a reader sees:

   | Check | What fails in practice |
   |-------|------------------------|
   | Open every page of the PDF | Broken layout only visible on a later page |
   | Code blocks | Wrapped or truncated lines, lost indentation, missing language highlighting |
   | Tables | Overflow past the margin, merged cells, lost headers |
   | Images | Missing files, wrong scale, unreadable screenshots |
   | Contents/anchors | Entries pointing to nothing, numbering gaps |
   | Unicode and fonts | Missing glyphs for arrows, em dashes, non-Latin names |
   | Page furniture | No page numbers, missing version/date in a footer |
   | DOCX in a real editor | Style collapse, broken numbering, tracked changes left on |

6. **Verify accessibility basics for delivered PDFs**: selectable text (not images of text), document title and language set, outline/bookmarks, and alt text on meaningful images. A PDF that is a scan of a document is not a document.

7. **Confirm the approval record** where required: who accepted which version, when, and in what form. An unsigned contractual document is a draft.

8. **Check discoverability and links**: the document is reachable from where its reader starts (README, docs index, alert annotation), and every internal link resolves in the published artifact as well as in the source.

9. **Write `DOC_REVIEW.md`:** acceptance test results (pass/fail with the evidence), the fact-audit sample and its result, the export matrix with what was actually clicked through, the accessibility findings, approval record, links checked, and any carried-forward limitations.

## 5. Decision rules and evidence standard

- **Re-execute, don't re-read.** The author's log tells you what they intended to check.
- **A page a reader cannot complete is a failed page**, regardless of prose quality.
- **Every export is opened and inspected**; a build exit code is not a rendering check.
- **An unverifiable claim is labelled**, not quietly kept — especially in an SRS, where it becomes a commitment.
- **Contractual documents need the approval record** before they are called delivered.
- **A failed acceptance test stays failed.** Softening the test after seeing the result is the corruption this system exists to prevent.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Commands re-run | clean execution | same result as documented |
| Paths walked as a reader | acceptance test | each completed without outside help |
| Facts sampled against source | comparison | mismatches fixed or recorded |
| Dangerous content absent | search | no secrets, no control-disabling steps |
| PDF pages inspected | open and read | no layout, glyph, or anchor defects |
| DOCX opened in editor | inspect | styles and numbering intact |
| Accessibility basics | PDF properties | text, title, language, outline, alt text |
| Approval recorded | document | approver, version, date |
| Links resolve in output | click-through | zero broken internal links |

## 7. Failure handling

- **An acceptance test fails** → return to P06 with the specific failing step; do not publish a document that fails its own test unless the failure is recorded and the reader is told.
- **The export toolchain produces a broken artifact and cannot be fixed now** → publish the source format, and state that the PDF/DOCX is not yet available. A broken PDF is worse than none.
- **The document describes unbuilt behaviour** → block publication and route to the owner; this is the highest-severity documentation defect.
- **Approval is unavailable** (client, legal, security) → mark the document *awaiting approval*, publish internally only, and record who must sign.
- **A fact cannot be verified in this environment** → carry it forward as a stated limitation in the review and in the document's status header.
- **Time pressure to publish** → publish the verified subset with clear scope, not the whole document with unknown truth.

## 8. Security and authorisation

Risk class B: this produces publishable artifacts. Publication of any externally visible document requires `{{APPROVER}}`. Before publishing, check for metadata leaks: author names and local paths in PDF/DOCX properties, embedded images with identifying detail, tracked changes or comments containing internal discussion, and repository links that are private. Do not publish to a public channel when the review has not passed.

## 9. Completion criteria

- [ ] Every acceptance test re-run and its result recorded.
- [ ] Reading paths walked as a reader.
- [ ] Facts sampled and checked against sources; mismatches resolved or recorded.
- [ ] Dangerous content audit clean.
- [ ] Exports built from source and inspected page by page.
- [ ] Accessibility basics verified for delivered PDFs.
- [ ] Links resolve in the published artifact.
- [ ] Approval record completed where required.
- [ ] `DOC_REVIEW.md` written with carried-forward limitations.

## 10. Deliverables and handover

Artifact: `DOC_REVIEW.md` plus the published documents.

Handover: the document owner receives the review, the limitations, and the review date that starts the maintenance clock; `DOC-P05`'s maintenance mechanism receives its first real test — the next release is where drift begins.
