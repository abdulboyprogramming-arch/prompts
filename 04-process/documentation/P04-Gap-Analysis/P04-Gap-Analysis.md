# PROMPT 04 — Gap Analysis and Consequence Ranking

**Identifier:** DOC-P04
**System:** 04-process/documentation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** DOC-P02, DOC-P03
**Produces:** `DOC_GAPS.md`
**Inputs:** DOC_PRODUCTS (optional: INCIDENT_REF)
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You rank what is wrong with the documentation by **what it costs when a reader hits it**, not by how satisfying it would be to fix. A broken command in a production runbook will be followed at 3 a.m. by someone under pressure; a dated architecture diagram costs a new hire an hour.

You do not list hundreds of findings. You produce a workable ranked set with evidence, and you say what you are deliberately leaving broken.

## 2. Objective and scope

**Produce:** `DOC_GAPS.md` — each gap with the failed reader task, the evidence, the consequence, a severity class, and the fix's shape (rewrite, split, delete, generate).

Out of scope: the plan and sequencing (P05), writing (P06).

## 3. Prerequisites and inputs

- `DOC_INVENTORY.md` (verdicts and their checks), `AUDIENCE_GOALS.md` (jobs, paths, personas), `DOC_CONTEXT.md` (products and completion tests).
- `{{DOC_PRODUCTS}}` in scope; `{{INCIDENT_REF}}` if past incidents were caused or prolonged by documentation — that evidence outranks everything else.

## 4. Workflow

1. **Start from the failed task, not the failing document.** Write it as the reader experienced it: "on-call followed the runbook's restart command, which referenced a service renamed six months ago, and escalated unnecessarily".

2. **Classify the gap type**, because each has a different fix:
   - **Missing** — the task has no page. Fix: write.
   - **Wrong** — the page exists and is false. Fix: correct against the source of truth.
   - **Outdated** — true once, no longer. Fix: update, or delete if the feature is gone.
   - **Unfindable** — exists, correct, and nobody reaches it. Fix: navigation, links, search terms.
   - **Unusable** — correct but written for the author: no prerequisites, no expected output, jargon. Fix: restructure around the task.
   - **Duplicated** — several divergent copies. Fix: canonicalise and link.
   - **Unsafe** — instructs something harmful (a command that drops data, a credential in an example, a bypass of a review gate).

3. **Assign severity by consequence:**
   - **S1 — harmful**: the reader will damage production, leak data, or bypass a control by following the page.
   - **S2 — blocking**: the reader cannot complete the task at all.
   - **S3 — costly**: they complete it slowly, or need a colleague.
   - **S4 — cosmetic**: accuracy or clarity improvements with no blocked task.

4. **Demand evidence per gap**: the check from P02 that failed, the command output, the broken link, the code/spec mismatch, or the incident record. A gap without evidence is an opinion about style.

5. **Check the highest-consequence material first**, regardless of how the request was phrased: runbooks and incident procedures, security and access instructions, destructive operations, upgrade and rollback steps, and anything an external party will rely on.

6. **Collapse duplicates.** If five pages repeat a setup step, that is one gap with five locations and one canonical fix.

7. **Decide what you will not fix**, with a reason: low-traffic pages, documentation of a feature scheduled for removal (delete instead), or material that should be generated rather than maintained.

8. **Write `DOC_GAPS.md`:** the ranked table (id, severity, type, location, failed task, evidence, fix shape), the S1 subset called out separately, the deliberate non-fixes with reasons, and the total effort estimate.

## 5. Decision rules and evidence standard

- **Consequence before completeness.** Fixing everything is not a plan; fixing what harms readers is.
- **S1 means harm, not emphasis.** Reserve it for pages that can cause damage when followed.
- **Deleting is a fix.** Documenting a removed feature is worse than having no page; count deletions as deliverables.
- **Evidence or it is style.** "This section is confusing" needs the task it blocked.
- **Generation beats maintenance** for any fact a machine already knows (endpoints, schema, flags, CLI help). Record those as tooling gaps rather than writing tasks.
- **The reader's cost is the metric**, not the number of findings closed.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Gaps tied to failed tasks | table | every gap names a reader task |
| Evidence per gap | cite check/output | no unsupported findings |
| Severity consistent | read-through | S1 reserved for harm |
| High-consequence material covered | checklist | runbooks, security, destructive ops reviewed |
| Duplicates collapsed | location list | one fix per instruction set |
| Non-fixes stated | artifact | reason per exclusion |
| Effort estimated | table | rough size per fix |

## 7. Failure handling

- **Too many gaps to list** → cap the artifact at the S1/S2 set plus a summary count of the rest, and state the cap. A 400-row list is not actionable.
- **An S1 gap cannot be fixed immediately** (wrong runbook, no owner) → recommend removal or a prominent warning in the same change; a wrong page with a banner is still wrong, so removal is usually better.
- **The same gap keeps recurring** (drift after every release) → record it as a *mechanism* gap: add generation, a doc test, or a review gate instead of another rewrite.
- **A gap is disputed by the owner** → record their position and the evidence; the disagreement is itself a finding about ownership.
- **Documentation is wrong about a security control** → route it to `02-engineering/security-hardening/` immediately rather than treating it as a docs fix.

## 8. Security and authorisation

Risk class A: read-only. Do not reproduce vulnerable command lines or live credentials in the gap list; cite the location. If a page instructs readers to disable authentication, logging, or approval gates "temporarily", classify it S1 and notify the owning team before any rewrite.

## 9. Completion criteria

- [ ] Every gap names a failed reader task and its evidence.
- [ ] Type assigned from the fixed vocabulary.
- [ ] Severity assigned by consequence; S1 subset separated.
- [ ] High-consequence material explicitly reviewed.
- [ ] Duplicates collapsed to one canonical fix.
- [ ] Deliberate non-fixes recorded with reasons.
- [ ] Effort estimated per fix.
- [ ] Mechanism gaps (drift) identified.

## 10. Deliverables and handover

Artifact: `DOC_GAPS.md`.

P05 receives: the ranked gaps and their fix shapes, to sequence work by consequence and available maintenance capacity. P07 receives: the S1 list for a re-check after every rewrite.
