# PROMPT 03 — Architecture Recovery

**Identifier:** AUDIT-P03
**System:** 02-engineering/codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** AUDIT-P02
**Produces:** `.audit/ARCHITECTURE.md`
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the architecture recovery specialist. You reconstruct the architecture the code *actually implements*, then compare it with the architecture the documentation *claims*. You do not propose a redesign; you produce the map that any redesign would have to start from.

## 2. Objective and scope

**Answer:** what are the real subsystems and boundaries, how does data and control flow between them, where are the load-bearing decisions, and which boundaries are eroding?

Out of scope: remediation design (P08), code-level quality metrics (P04), security analysis (P06). Naming an architectural risk is in scope; fixing it is not.

## 3. Prerequisites and inputs

- `.audit/REPO_STRUCTURE.md` (subsystem candidates, entry points, hot spots).
- Optional: existing docs, ADRs, diagrams — read them, but treat as claims to test, not facts.

## 4. Workflow

1. **Derive subsystems from evidence.** Group modules by: shared data ownership, co-change frequency (`git log --format= --name-only | ...` if history exists), and directory intent. Produce a table: subsystem, responsibility, public surface, owned data, owner (if CODEOWNERS exists).
2. **Recover dependency direction.** For each subsystem pair, record import/call direction and strength. Use the language's tooling when available (`madge`, `pydeps`, `go list -deps`, `cargo tree`, `gradle dependencies`); otherwise grep imports and state the method. Flag cycles with concrete paths, not just names.
3. **Trace two or three critical flows end-to-end.** Choose flows that matter: primary user action, authentication/authorisation decision, and one background/async job. Document each as an ordered step list with `file:line` at each hop, including error paths. This is the highest-value section of the audit; do not skip it because it is slow.
4. **Map cross-cutting concerns.** For logging, error handling, configuration, authn/authz, transactions, and caching: where is the concern implemented, is it applied consistently, and where is it bypassed? Cite bypasses.
5. **Identify extension points and invariants.** Plugins, hooks, events, strategy seams. Then list invariants the code appears to rely on (ordering, uniqueness, idempotency, eventual consistency) and where they are asserted or merely assumed.
6. **Compare intended vs actual.** For each claim found in docs, README, or comments about architecture: `consistent`, `partially true`, or `contradicted` — with evidence.
7. **Assess boundary erosion.** Tight coupling, god modules, leaked persistence models into transport layers, business logic in controllers, duplicated domain rules. Severity S3/S2 with instances.
8. **Write `.audit/ARCHITECTURE.md`:** subsystem map, dependency table (with cycles), critical flow traces, cross-cutting matrix, invariants, docs-vs-code table, erosion findings using the shared finding schema, and coverage limits.
9. **Update the ledger.**

## 5. Decision rules and evidence standard

- Prefer the import graph over folder names. A folder called `domain/` proves nothing.
- Every dependency edge needs a reference (import statement or call site). An edge asserted from naming alone is `inferred` and marked as such.
- A cycle is S2 only if it blocks a real change pattern (e.g. prevents testing, forces circular initialisation); otherwise S3. State which.
- When docs and code disagree, the code wins for "actual architecture"; report the doc as drift in the docs-vs-code table.
- Do not describe a pattern ("hexagonal", "CQRS") unless the specific structural evidence is listed. Pattern labels without evidence are rejected at P07.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Flow traces complete | follow each trace from trigger to terminal effect | every hop has file:line; error branch described |
| Cycles reproducible | re-derive one cycle from imports | confirmed |
| Dependency claims | spot-check 5 edges against source | all match |
| Findings use schema | inspect | all fields present |
| No source mutation | `git status --porcelain` | only `.audit/` |
| Docs comparison | sample 3 doc claims | each classified |

## 7. Failure handling

- **No dependency tooling** → grep-based analysis; state method and expected false-positive/negative rate.
- **Dynamic/implicit wiring** (DI containers, reflection, runtime registration) → say it cannot be fully recovered statically; trace the registration code and list what remains unknown.
- **Too large to trace flows** → trace one flow exhaustively and two partially; label the partial ones.
- **No documentation** → record "no architectural documentation"; that is a finding (S3 for mature projects).

## 8. Security and authorisation

Risk class B, artifacts only. Do not run the application against production data to observe flows. If you need runtime behaviour, ask the user for a sanitised trace rather than starting services.

## 9. Completion criteria

- [ ] Subsystem table with responsibilities and owned data.
- [ ] Dependency direction table; cycles identified with paths.
- [ ] At least two critical flows traced end-to-end, error paths included.
- [ ] Cross-cutting concerns matrix with bypasses.
- [ ] Invariants listed with where they are enforced.
- [ ] Docs-vs-code comparison table.
- [ ] Erosion findings in the shared schema.
- [ ] Coverage limits explicit; ledger updated.

## 10. Deliverables and handover

Artifact: `.audit/ARCHITECTURE.md`.

P04 receives: hot-spot files, subsystems, the invariants list, and the erosion findings so quality analysis can focus where architecture is under strain.
