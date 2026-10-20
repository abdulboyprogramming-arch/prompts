# PROMPT 03 — Audience, Jobs, and Structure

**Identifier:** DOC-P03
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** DOC-P01, DOC-P02
**Produces:** `AUDIENCE_GOALS.md`
**Inputs:** DOC_PRODUCTS, REPO_PATH (optional: SUPPORT_EVIDENCE)
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You turn "the docs should be better" into a structure that a reader can move through: who they are, what task they arrived with, where the path starts, and what they must be able to do when it ends.

Documentation fails structurally far more often than it fails stylistically. The usual cause: it is organised by the *system's* components (Installation, Configuration, Services, Modules) while readers arrive with *tasks* ("connect my app", "fix a failed payment", "add a field").

## 2. Objective and scope

**Produce:** `AUDIENCE_GOALS.md` — personas with evidence, the top jobs per persona, the task-based structure per document product, entry points, success measures, and the deliberate omissions.

Out of scope: writing prose (P06), ranking gaps by cost (P04).

## 3. Prerequisites and inputs

- `DOC_CONTEXT.md` (products, readers, completion tests) and `DOC_INVENTORY.md` (what exists, what is unverified).
- `{{DOC_PRODUCTS}}` restated for this stage; `{{REPO_PATH}}` for verifying claims about who the software serves.
- `{{SUPPORT_EVIDENCE}}` if available: support tickets, repeated questions, failed onboarding attempts — the only real evidence of what readers cannot do.

## 4. Workflow

1. **Derive personas from evidence, not imagination.** Sources: issue labels and questions, support tickets, onboarding records, PR review comments ("where is this documented?"), the audience named in `DOC_CONTEXT.md`. Where evidence is missing, say the persona is assumed.

2. **State each persona's entry point and first question.** A new engineer arrives at the README asking "how do I run this?"; an integrator arrives at the API reference asking "how do I authenticate?"; an on-call responder arrives at a runbook asking "what do I do right now?". If the entry point cannot be named, the structure is wrong.

3. **Express jobs as tasks with a completion test:** "run the project locally and reach a green test run from a clean checkout in under 30 minutes, without asking anyone". A job without a completion test cannot be designed for.

4. **Design the structure task-first**, and put concept material where the task needs it rather than in a "Concepts" chapter nobody reads first. For each product: ordered path, branch points (what to do if X), and prerequisites at the point of need.

5. **Assign each task to exactly one place.** Duplicated instructions decay differently — P02's duplication map is the input. Name the canonical page and make the others link to it.

6. **Set success measures that can be observed:** time to first successful run, number of steps, support questions per week for a topic, "no ambiguity" review by a reader who has never seen the system. Choose measures a human can actually collect; "improved satisfaction" is not one.

7. **Decide the reading paths** for the common journeys and write them as sequences of pages. These become the navigation and the acceptance test for completeness: a missing page is a broken path.

8. **State deliberate omissions**: what will not be documented (internal implementation detail, third-party products, deprecated versions), and where the reader is sent instead.

9. **Write `AUDIENCE_GOALS.md`:** persona table with evidence, jobs with completion tests, per-product structure, canonical page map, reading paths, success measures, omissions.

## 5. Decision rules and evidence standard

- **Task-first, component-second.** A structure organised by module forces the reader to reverse-engineer their own path.
- **One canonical page per instruction.** Links, not copies.
- **Every job has a completion test**, or it is a topic and belongs in reference material.
- **Assume a competent reader with no context**, not a beginner who needs encouragement or an expert who knows the jargon.
- **Personas without evidence are labelled assumed** — and must be re-checked with a real reader before the structure is locked.
- **A reading path is a test**: walking it reveals missing pages, wrong ordering, and hidden prerequisites.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Personas evidenced | source cited per persona | assumed ones labelled |
| Entry point named | per persona | URL or file path |
| Jobs have completion tests | table | observable outcome each |
| Structure is task-first | inspect | reader's order, not module order |
| One canonical page per task | duplication map applied | no instruction in two places |
| Paths walked | walk each path | no missing page, prerequisites at point of use |
| Measures collectable | inspect | a human could record them |

## 7. Failure handling

- **No evidence about readers** → build the structure from the product's interfaces (CLI flags, API surface, alerts) and label every persona assumed; validate against one real reader before writing.
- **Conflicting audiences for one document** (internal ops and external clients) → split the product; a document serving both serves neither.
- **A reading path requires a page that cannot exist yet** (feature unreleased) → mark it explicitly as unreleased; do not document planned behaviour as current. That is the most damaging documentation defect there is.
- **The existing structure is published and linked externally** → keep URLs stable, add redirects, and change navigation before moving pages.
- **Success measures would require instrumentation you do not have** → pick a proxy that a human collects (support questions, onboarding time reported by the new hire).

## 8. Security and authorisation

Risk class A: planning only. Persona descriptions must not contain customer names or personal data; use roles. Reading paths for on-call material may reference internal systems — keep hostnames and endpoints generic in artifacts that could be shared outside the engineering group.

## 9. Completion criteria

- [ ] Personas with evidence or an explicit "assumed" label.
- [ ] Entry point per persona.
- [ ] Jobs expressed as tasks with completion tests.
- [ ] Structure designed task-first per product.
- [ ] Canonical page map; no duplicated instructions.
- [ ] Reading paths walked and recorded.
- [ ] Success measures collectable.
- [ ] Omissions stated with where the reader is sent instead.

## 10. Deliverables and handover

Artifact: `AUDIENCE_GOALS.md`.

P04 receives: jobs, paths, and personas, to judge which *gaps* actually block a reader. P05 receives: the structure that the plan must populate.
