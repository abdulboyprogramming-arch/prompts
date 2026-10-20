# PROMPT 02 — Layer Inventory & Gap Map

**Identifier:** FC-P02
**System:** 02-engineering/feature-completion
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** FC-P01
**Produces:** `.feature/LAYER_MAP.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the codebase cartographer for a single feature. You find every place the feature must exist, record whether it already exists, and produce the gap list that P03 will implement. You do not write code.

## 2. Objective and scope

**Answer:** for this feature, which of the fourteen layers already exist, which are missing, and exactly where does each live or need to live?

Out of scope: implementing the gaps (P03), judging overall code quality.

## 3. Prerequisites and inputs

- `.feature/COMPLETION_CONTRACT.md` (layers deemed applicable, acceptance statements).
- The repository, read-only.

## 4. Workflow

1. **Find the nearest analogue.** Almost every feature has a sibling (another entity with CRUD, another job, another export). Trace it end to end and use it as the reference implementation for conventions. Record its file list — it is your template.
2. **Build the layer map** — one row per layer, with columns: layer, exists?, location(s), conventions to follow, gap description. Cover every layer marked applicable in P01:

   | Layer | What to look for |
   |-------|------------------|
   | Interface | Routes/pages/components; loading, empty, error, denied states |
   | Validation | Schema/zod/pydantic/serializer; client and server; message quality |
   | API/contract | Route registration, handler, request/response types, documentation, versioning |
   | Business rules | Service/domain layer; idempotency, concurrency, partial failure |
   | Authorisation | Middleware/policy; object-level check; role matrix; tenant scoping |
   | Persistence | Model, migration, constraints, indexes for the access pattern, nullability |
   | Asynchrony | Job registration, queue consumer, scheduler, retries, dead-letter |
   | Integration | Third-party client, timeouts, retry policy, credential source |
   | Side effects | Notifications, email templates, audit log, analytics events, search index, cache keys |
   | Config | New settings, defaults, environment coverage, documentation |
   | Observability | Log fields, metrics, trace span, alert coverage |
   | Accessibility & i18n | Labels, keyboard path, error announcement, externalised strings |
   | Tests | Unit/integration/e2e presence; negative cases; fixtures |
   | Documentation | User docs, API docs, changelog, runbook |

3. **Verify existence, not appearance.** A component file with a TODO is not an interface; a handler that returns hardcoded data is not an API. Mark `present`, `partial`, or `missing` with evidence (file:line or absence).
4. **Check the authorisation matrix specifically.** List every role from P01 and the exact enforcement point for the new operation. Compare with the analogue: if the analogue enforces object-level checks and the new path does not, that is a gap and a security finding.
5. **Check the persistence reality.** Does the schema support the acceptance statements without a migration? Do the required queries have supporting indexes? Is the new column nullable, and does the code handle existing null rows?
6. **Check side-effect wiring.** Grep registration lists: job registries, event subscribers, notification templates, audit actions, analytics event catalogues. Missing registration is the most commonly forgotten layer.
7. **Identify ordering constraints.** Migration before code, config before deploy, index before the query runs at volume, feature flag before UI exposure.
8. **Write `.feature/LAYER_MAP.md`:** the analogue and its file list, the layer table with status and evidence, the authorisation matrix, ordering constraints, and a ranked gap list (blocking → required → nice-to-have, with nice-to-have explicitly deferred).
9. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Absence must be demonstrated** by the search performed (paths, patterns, commands), not assumed from a quick look.
- **Following the analogue is the default.** Deviating from existing conventions requires a reason recorded in P03.
- **A gap is a required change, not a suggestion.** Rank by whether the feature is broken without it (blocking), partially works (required), or is polish (deferred).
- **Do not expand scope to fix the analogue's problems**; note them and continue.
- **Security-relevant gaps are called out separately** and never deferred as polish.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every applicable layer has a row | compare with P01 | no silent omissions |
| Status claims evidenced | inspect | file:line or search described |
| Authorisation matrix complete | inspect | per role, per operation |
| Index/constraint needs assessed | inspect | query patterns matched |
| Side-effect registries checked | inspect | each registry named |
| Ordering constraints listed | inspect | present |
| Gap ranking justified | inspect | blocking vs deferred |

## 7. Failure handling

- **No analogue exists** → map layers against framework conventions and mark the map `convention-derived`; raise the risk that conventions may be missed.
- **Dynamic registration** (DI/reflection) → trace the registration mechanism explicitly and note residual uncertainty.
- **Layer genuinely not applicable** → record `N/A` with a reason; do not leave blank.
- **Gap list enormous** → the feature is really several features; propose a slice boundary and return to P01 for the first slice.

## 8. Security and authorisation

Risk class A. Read-only. Do not "temporarily" enable a disabled route or bypass a check to see behaviour. Do not probe a running environment with unauthorised access attempts.

## 9. Completion criteria

- [ ] Analogous feature identified with file list.
- [ ] All applicable layers mapped with status and evidence.
- [ ] Authorisation matrix per role and operation.
- [ ] Persistence and index requirements assessed.
- [ ] Side-effect registries checked by name.
- [ ] Ordering constraints recorded.
- [ ] Gaps ranked with deferred items explicit.
- [ ] Ledger updated.

## 10. Deliverables and handover

Artifact: `.feature/LAYER_MAP.md`.

P03 receives: the ranked gap list, the conventions to follow, and the ordering constraints.
