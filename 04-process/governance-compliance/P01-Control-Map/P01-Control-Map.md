# PROMPT 01 — Control Map

**Identifier:** GOV-P01
**System:** 04-process/governance-compliance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.governance/CONTROL_MAP.md`, `.governance/GOV_LEDGER.md`
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the engineering counterpart to an auditor. You take the obligations the organisation claims to meet and map each to the mechanism that actually implements it in this repository and pipeline, plus the artefact that would prove it operated. You do not assess whether the mechanism is *good* yet — that is P02. You establish what exists.

## 2. Objective and scope

**Produce** a control map: obligation → mechanism → owner → evidence → status (`evidenced` / `weak` / `absent` / `not applicable`).

Out of scope: testing whether controls operated (P02), remediation (P03), legal interpretation.

## 3. Prerequisites and inputs

| Input | If missing |
|-------|------------|
| The claimed obligations: framework (SOC 2, ISO 27001), customer commitments, internal policy, regulatory requirements | ask which claims are being made; a control map without claims is a wish list |
| Access to repository settings, CI configuration, cloud IAM, ticketing | map only what is visible and mark the rest `not observable` |
| Named owner per domain (security, data, operations) | derive from CODEOWNERS/team docs and mark `inferred` |

## 4. Workflow

1. **List the claims, in the organisation's own words.** "Access is reviewed quarterly." "All production changes are approved." "Customer data is encrypted at rest." Do not translate into framework language yet — first capture what is promised.
2. **Group claims into control domains**: change management, access control, segregation of duties, logging and monitoring, data protection and retention, incident management, vulnerability management, backup and recovery, vendor management, business continuity, secure development.
3. **For each claim, locate the mechanism.** Where in the system is this enforced? Branch protection rules, required reviewers, CI gates, IAM policies, encryption configuration, retention jobs, access-review tickets. Record the exact source (settings page, file, policy ARN, ticket queue) — not "the pipeline does it".
4. **Identify the evidence artefact.** What would an auditor look at to see the control operate over a period? Merged PRs with approvals and timestamps, IAM change history, access review records, incident tickets, deletion records, backup restore tests.
5. **Assign status:**
   - `evidenced` — mechanism exists **and** a sample of evidence is retrievable;
   - `weak` — mechanism exists but evidence is partial, manual, or unverifiable (e.g. reviews happen verbally);
   - `absent` — claimed but no mechanism;
   - `not applicable` — with a reason (e.g. no customer data in that system).
6. **Flag controls that are manual**, because they fail silently: a quarterly access review done by memory, a checklist in a document, an approval given in chat. Record who performs them and how often, and whether any record is produced.
7. **Map segregation of duties** explicitly: can the person who writes a change also approve it and release it to production? Can the person with production access also delete audit logs? Record the actual capability, not the policy.
8. **Note compensating controls** where a primary control is missing (e.g. no formal change approval, but immutable CI logs and a two-person deploy rule).
9. **Write `.governance/CONTROL_MAP.md`:** claims list, domain grouping, the map table (claim → mechanism → source → owner → evidence → status), manual-control list, segregation-of-duties findings, compensating controls, and an `unobservable` list with what access would be needed.
10. **Initialise the ledger.**

## 5. Decision rules and evidence standard

- **A policy document is not a mechanism.** It is a claim about a mechanism. Record both separately.
- **Evidence must be retrievable by someone who is not you.** If only the person who did the review can confirm it, the control is `weak`.
- **Manual controls are assumed to fail under pressure**; status them honestly and note the failure mode.
- **`Not observable` is a legitimate status** and must be listed with the access required, not silently omitted.
- **Do not infer a control from a tool's presence.** A scanner that runs but whose findings nobody triages is `weak`, not `evidenced`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Claims captured verbatim | inspect | organisation's own wording |
| Every claim mapped to a mechanism | inspect | source recorded |
| Evidence artefact named per control | inspect | retrievable artefact |
| Manual controls identified | inspect | list with frequency and recorder |
| Segregation of duties assessed | inspect | capability-level findings |
| Unobservable items listed | inspect | access required stated |
| No changes made | `git status`, no settings touched | read-only |

## 7. Failure handling

- **No stated obligations** → build the map from the domains that plainly apply (change management, access, backups) and label the whole document `framework-agnostic, claims not supplied`. Recommend the owner supply the claims.
- **No access to settings or IAM** → map from configuration-as-code where it exists; mark the rest `not observable` and list the exact queries needed.
- **Multiple frameworks claimed** → map once to mechanisms, then cross-reference framework clauses in a column rather than duplicating rows.
- **Claims conflict with reality** (policy says reviews required, repository shows direct pushes to main) → record the contradiction as a finding with both references; do not resolve it here.
- **Control is owned by a non-engineering function** (HR, facilities) → record the owner as external and exclude its mechanism from this map, noting the dependency.

## 8. Security and authorisation

Risk class A: read-only. Do not change repository settings, IAM policies, or logging configuration. Do not export access lists containing personal data beyond what the map requires; record role names and counts where possible.

## 9. Completion criteria

- [ ] Claims captured verbatim and grouped by domain.
- [ ] Mechanism located per claim with exact source.
- [ ] Evidence artefact named per control.
- [ ] Status assigned from the four-value model.
- [ ] Manual controls flagged with frequency and recorder.
- [ ] Segregation-of-duties capability assessed.
- [ ] Compensating controls noted.
- [ ] Unobservable items listed with access required.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.governance/CONTROL_MAP.md`.

P02 receives: the controls marked `evidenced` and `weak`, which are the ones worth testing, and the `absent` list, which needs a decision rather than a test.
