# Handoff Contract

**Identifier:** WF-HANDOFF
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** planning
**Risk class:** A
**Depends on:** none
**Produces:** the handoff block appended to any stage artifact

---

## 1. Role and mandate

This is the shared format every stage of every workflow uses to pass state forward. It exists so a later stage — or a later session, or a different agent — can continue without re-reading the whole conversation.

## 2. Objective and scope

Define one compact block that carries: what was done, what is true now, what is uncertain, what is next, and what authority exists. It does not replace the stage artifact; it summarises and points to it.

## 3. Prerequisites and inputs

- A completed stage artifact.
- The stage's completion criteria, honestly assessed.

## 4. Workflow

Append this block to the stage artifact, filled in factually:

```markdown
## Handoff
- Stage: <identifier> (<name>) — status: complete | partial | blocked
- Repository state: commit <sha>, branch <name>, tree clean|dirty
- Artifacts: <path> (what it answers)
- Established facts: <3–6 bullets a later stage can rely on>
- Decisions made: <decision → reason>
- Assumptions: <assumption → impact if wrong>
- Open questions: <question → who can answer → what it blocks>
- Not done / not verified: <explicit list>
- Constraints in force: risk class <A–D>; <specific prohibitions established earlier>
- Recommended next stage: <identifier> — because <reason>
- If blocked: <smallest action needed from the user>
```

## 5. Decision rules and evidence standard

- **Facts only.** "Established facts" must be verifiable from the artifact; opinions belong in the artifact's findings, not here.
- **Assumptions are liabilities.** Every assumption states what changes if it is wrong.
- **"Not done" is mandatory and may not be empty without a reason.** Write `none` only when the stage's completion criteria were fully met.
- **Carry constraints forward verbatim.** A later stage that needs more authority must ask; it cannot inherit it silently.
- **Point, do not duplicate.** Reference artifacts by path; do not restate their content.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| All fields present | inspect | no blanks; `none` is explicit |
| Facts traceable | sample 3 bullets | resolvable in the artifact |
| Status honest | compare to stage completion criteria | matches |
| Next stage exists | check identifier | real and appropriate |
| Constraints listed | inspect | prohibitions carried forward |

## 7. Failure handling

- **Stage partial** → status `partial`, list exactly what remains, and state whether the next stage can start or must wait.
- **Stage blocked** → status `blocked`, name the blocker class (context, tooling, decision, safety), and give the smallest user action.
- **Contradiction with an earlier handoff** → record it explicitly as a contradiction rather than overwriting the earlier claim; the resolving stage records the decision.

## 8. Security and authorisation

The block must not contain secret values, tokens, personal data, or private URLs with embedded credentials. Record that a secret exists and where it is managed, never the value.

## 9. Completion criteria

- [ ] Block appended to the artifact.
- [ ] Status accurate.
- [ ] Facts, decisions, assumptions, open questions, and not-done list populated.
- [ ] Constraints in force listed.
- [ ] Next stage named with a reason.

## 10. Deliverables and handover

The handoff block itself. The next stage consumes it as its input contract and verifies the facts it depends on before acting.
