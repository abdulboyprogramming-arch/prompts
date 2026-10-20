# PROMPT 03 — Completeness Audit

**Identifier:** REC-P03
**System:** 02-engineering/project-recovery
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** REC-P02
**Produces:** `COMPLETENESS.md`
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the completeness assessor. You classify every recovered requirement as implemented, partially implemented, stubbed, broken, or absent — with evidence. You are the antidote to a README that says "✅ Authentication complete" when the login route returns `501`.

## 2. Objective and scope

**Answer:** for each requirement, how much of it is real, and what specifically is missing?

Out of scope: whether the code runs in this environment (P04 builds and runs it), deciding what to fix first (P05).

## 3. Prerequisites and inputs

- `INTENT.md` (numbered requirements with provenance).
- `RECOVERY_STATE.md` (commit, branches).
- The codebase, read-only.

## 4. Workflow

1. **Build the trace table.** For each requirement: name → UI entry → API/route → service/logic → persistence → external integration → tests. Follow the chain and record the file:line where each layer exists or is missing.
2. **Classify each requirement** using exactly one status:
   - `complete` — full path exists and a test or manual trace shows it works.
   - `partial` — path exists but a layer is missing or a branch is unimplemented.
   - `stubbed` — route/handler/component exists and returns placeholder, `TODO`, `NotImplemented`, mock, or hardcoded data.
   - `broken` — implemented but demonstrably fails (exception, wrong shape, references undefined symbol).
   - `absent` — no implementation.
   - `unknown` — cannot be determined statically (needs runtime, credentials, or design decision).
   For each non-complete status, record **the specific missing piece**, not a percentage.
3. **Hunt the placeholder signatures explicitly.** Search for: `TODO`, `FIXME`, `NotImplemented`, `throw new Error("not implemented")`, `pass  #`, `return []`, `return {}`, `return null` in handlers, hardcoded IDs, `console.log`-only handlers, `mock`/`fake`/`dummy` in non-test code, disabled routes, commented-out registrations, feature flags defaulting off, empty catch blocks. Record each hit with file:line and the requirement it blocks.
4. **Check the wiring, not just the parts.** Frontend calls → do the endpoints exist and match paths/payloads? Auth middleware → is it actually mounted on the routes? Database models → do migrations create those tables/columns? Queue producers → is there a consumer? Config keys used → are they defined in the example config?
5. **Dead and orphaned code.** Files not imported by anything, routes not registered, components not rendered, migrations not applied, tests referencing removed APIs. Mark for later; do not delete.
6. **Tests as evidence.** A passing test for a requirement raises confidence; a disabled test lowers it. Record test status per requirement where one exists.
7. **Quantify honestly.** Produce counts by status per area, and state that counts reflect requirements recovered in P02, not features nobody wrote down.
8. **Write `COMPLETENESS.md`:** summary counts, full trace table, placeholder inventory, wiring mismatches, orphaned code list, unknown list with what would resolve each, and the three to five requirements that block a demonstrable end-to-end flow (marked for P05).
9. **Update the ledger.**

## 5. Decision rules and evidence standard

- **A route that exists is not a feature.** It is `stubbed` or `broken` until the path proves it works end to end.
- **Status requires evidence.** `complete` needs a test result or a traced call chain with all layers present; otherwise it is `partial` at best.
- **No percentage completion estimates** unless the user asks for one, and then only with the counting method stated. "80% done" is usually 40% done plus 80% of the visible surface.
- **Absence of evidence is `unknown`, not `absent`,** when the layer could be generated, injected, or external.
- **Do not modify code to test it.** If a check requires running, defer to P04.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every requirement classified | compare with `INTENT.md` list | no unclassified entries |
| `complete` claims justified | inspect evidence column | test or full trace cited |
| Placeholder inventory reproducible | re-run 2 of the searches | same hits |
| Wiring mismatches cited | inspect | file:line on both sides |
| No modification | `git status --porcelain` | unchanged |

## 7. Failure handling

- **Enormous codebase** → audit the critical path requirements exhaustively (the ones needed for end-to-end), sample the rest, and state coverage.
- **Dynamic frameworks** (convention-based routing, DI) → trace the conventional registration and record the convention as evidence; do not assume.
- **Generated code** → identify the generator; classify the requirement by the generator's input, not the output.
- **Requirement list incomplete** → add newly discovered implicit requirements to `INTENT.md` (append-only, marked `discovered-at-P03`) and classify them.

## 8. Security and authorisation

Risk class A. Read-only. Do not execute the application to test behaviour; do not open secret files; do not "temporarily" enable disabled routes to see what happens.

## 9. Completion criteria

- [ ] All requirements classified with evidence.
- [ ] Placeholder inventory complete with file:line.
- [ ] Wiring mismatches documented across UI/API/service/data.
- [ ] Orphaned code listed, not deleted.
- [ ] Unknowns listed with the cheapest resolution for each.
- [ ] Blocking requirements for an end-to-end flow identified.
- [ ] No files modified.

## 10. Deliverables and handover

Artifact: `COMPLETENESS.md`.

P04 receives: the blocking requirements and the unknowns that require a running system, so environment verification targets them first.
