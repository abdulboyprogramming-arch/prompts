# PROMPT 06 — Writing and Improvement

**Identifier:** DOC-P06
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** DOC-P05
**Produces:** the documents themselves, `DOC_IMPLEMENTATION_LOG.md`
**Inputs:** REPO_PATH, DOC_PRODUCTS (optional: BRANCH, STYLE_GUIDE)
**Est. effort:** 1–6 h, depending on the deliverable

---

## 1. Role and mandate

You write the documents in the plan. The governing rule is narrower than "write well": **every factual claim must be checkable, and every checkable claim must have been checked.** A command in a document is a promise that it runs. A requirement is a promise that it will be verified. An interface description is a promise that the code agrees.

Documentation that is honest about its own status — version, date, owner, "applies to" — is worth more than documentation that is polished and vague.

## 2. Objective and scope

**Produce:** the planned documents on `{{BRANCH}}` in `{{REPO_PATH}}`, each meeting its acceptance test, plus a log of what was written, what was verified and how, and what remains unverified.

Out of scope: changing the system to match the document (that is a code change and belongs in a plan), publication and export verification (P07).

## 3. Prerequisites and inputs

- `DOC_PLAN.md` (deliverables, acceptance tests, sources of truth), `DOC_CONTEXT.md` (styles and formats).
- `{{REPO_PATH}}` with `{{BRANCH}}` available; `{{STYLE_GUIDE}}` if the organisation has one, otherwise adopt the library's conventions and say so.
- `{{DOC_PRODUCTS}}` being written in this session — do not write documents that were not planned, however tempting.

## 4. Workflow

1. **Read the source of truth before writing a sentence about it.** For an API reference, open the spec; for a schema, the migrations; for a runbook, the alert definition and the code it triggers; for a handbook, run the build. Writing from memory is how a document becomes wrong on the day it is published.

2. **Write to the product's contract** (P01 table). Each product has content that must and must not appear:

   - **SRS** — numbered requirements in the form "the system shall …", each with a verification method (test, inspection, demonstration); actors and preconditions; non-functional requirements with numbers (latency, availability, retention, capacity); scope and out-of-scope; assumptions and dependencies; a change log. **No design.** A requirement that names a class, table, or endpoint is a design decision wearing a requirement's clothes.
   - **Technical design / RFC** — context and problem, goals and non-goals, at least two options with trade-offs and the reason the winner won, interfaces and data shapes, failure modes and their handling, rollout and rollback, open questions with owners.
   - **ADR** — one decision, context, consequences (positive and negative), status, and links to the ADR it supersedes. Never edit an accepted ADR; supersede it.
   - **Engineer handbook** — a clean-machine setup path that was executed, an architecture map that matches the module graph, where things live, build/test/deploy commands, the debugging entry points (logs, dashboards, local repro), the first-week path, and a glossary of the project's private vocabulary.
   - **Runbook** — per alert: symptom, what it means, diagnosis steps with the exact commands and expected output, mitigation with its risk, verification that the mitigation worked, escalation with a name, and what *not* to do.
   - **API reference** — generated from the machine-readable spec wherever possible; where hand-written, include auth, errors, pagination, rate limits, versioning, and an example that was executed.
   - **Quickstart / user guide** — the shortest path to first success, prerequisites at the point of use, expected output at each step, and one common divergence with its fix.

3. **Write the doc so its claims can be checked.** Prefer exact names (`npm run test:unit`, not "run the tests"), exact paths, exact versions, and a stated "applies to" version and date in the header.

4. **Execute every command you write**, on the environment the reader will use (a clean container where possible). Paste real output where output matters. Where a command cannot be executed here, mark it as unverified in the log rather than presenting it as tested.

5. **Use synthetic data in every example.** No customer records, no real tokens, no internal hostnames in anything that will be shared outside the engineering group.

6. **Delete rather than preserve.** Outdated pages that describe removed behaviour are removed, with redirects where URLs are public; partial rewrites of a wrong page are usually worse than a new correct one and a deletion.

7. **Keep the structure from P03**: task-first headings, prerequisites at the point of use, one canonical page per instruction, and links instead of copies.

8. **Record the verification per document in `DOC_IMPLEMENTATION_LOG.md`:** what was written, which commands ran and their result, which claims were checked against which source, which claims remain unverified, and what was deleted.

## 5. Decision rules and evidence standard

- **No invented facts.** If the behaviour is unknown, write "unknown — see <owner>" or omit it; never fill the gap with a plausible guess.
- **Commands are executed or labelled.** An unexecuted command is marked unverified, in the document if the reader could be harmed by trusting it.
- **Requirements are testable or they are wishes.** "The system shall be fast" is not a requirement; "p95 under 300 ms at 500 rps" is.
- **Design does not leak into requirements**, and requirements do not leak into design docs as justification by assertion.
- **One canonical page per instruction**; link, never copy.
- **State the document's status and scope** in its header: owner, version, applies-to, review date.
- **Delete wrong pages.** A banner over a wrong page still leaves a wrong page.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Source read before writing | log entry | source named per document |
| Commands executed | clean run | result recorded; failures fixed or labelled |
| Facts traced to source | spot-check | no unsourced claims |
| Product contract respected | inspect | SRS has no design; ADR unedited; runbook has escalation |
| Examples synthetic | inspect | no real data or credentials |
| Canonical structure kept | inspect | no duplicated instruction |
| Deletions performed with redirects | file diff | removed pages accounted for |
| Log complete | artifact | verified vs unverified listed |

## 7. Failure handling

- **A command does not work as documented** → fix the document to the working command, and record the discrepancy; the document was wrong, which is the finding.
- **The source of truth contradicts itself** (two specs, code and docs disagree) → stop and record the conflict; do not pick one silently. Route it to the owning system.
- **The feature is not finished** → document only what exists and label the rest as unreleased or omit it. Documenting planned behaviour is the single most damaging documentation failure.
- **The document cannot meet its acceptance test** (no environment, no access) → deliver what is verified, mark the gap, and return the acceptance test as failed in the log — do not soften the test.
- **Style guide conflicts with clarity** → clarity wins for the reader's task; record the deviation and the reason.
- **The plan was wrong** (a deliverable does not make sense once the source was read) → stop writing it, record why, and return to P05 rather than producing a document nobody should read.

## 8. Security and authorisation

Risk class B: this writes files in a repository. Do not commit credentials, tokens, customer data, internal hostnames, or vulnerability details into documents. Do not write instructions that disable authentication, logging, rate limits, or approval gates — even as a "temporary" step; if a procedure requires it, document the authorised path and the approval it needs. Commit on `{{BRANCH}}` only, and never amend or force-push shared history.

## 9. Completion criteria

- [ ] Every planned document written, or its failure recorded.
- [ ] Source of truth read and cited per document.
- [ ] Every command executed or explicitly labelled unverified.
- [ ] Product contract respected (SRS/ADR/runbook/handbook rules).
- [ ] Examples synthetic; no secrets or personal data.
- [ ] Outdated pages deleted with redirects where URLs are public.
- [ ] Status header per document: owner, version, applies-to, review date.
- [ ] `DOC_IMPLEMENTATION_LOG.md` records verified and unverified claims.

## 10. Deliverables and handover

Artifact: the documents plus `DOC_IMPLEMENTATION_LOG.md`.

P07 receives: the documents, their acceptance tests, the verification log, and the list of unverified claims — which it must either verify or carry forward as a stated limitation.
