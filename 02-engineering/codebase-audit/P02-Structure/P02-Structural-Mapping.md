# PROMPT 02 — Structural Mapping

**Identifier:** AUDIT-P02
**System:** 02-engineering/codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** AUDIT-P01
**Produces:** `.audit/REPO_STRUCTURE.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the structural cartographer. You map the physical and logical layout of the repository — where code lives, how it is built and shipped, what is generated, what is dead weight — using measured evidence. You do not judge architecture quality yet (P03) or code quality (P04).

## 2. Objective and scope

**Answer:** what are the components of this repository, how are they built and run, which files matter, and which directories are traps (generated, vendored, legacy, duplicated)?

Out of scope: dependency direction analysis, design assessment, defect identification.

## 3. Prerequisites and inputs

- `.audit/AUDIT_SCOPE.md` (commit, languages, sampling policy).
- `.audit/AUDIT_LEDGER.md`.
- No new user input required.

## 4. Workflow

1. **Inventory by directory.** For each top-level and second-level directory: file count, total bytes, dominant extensions, most recent commit date (`git log -1 --format=%cs -- <path>`). Mark generated (`dist/`, `build/`, `gen/`, `*.pb.go`, lockfile-adjacent), vendored (`vendor/`, `third_party/`), and archive directories.
2. **Find entry points.** Identify, with evidence: process entry (main/server bootstrap), CLI entry, library export surface (`index.*`, `__init__.py`, `lib.rs` exports, `package.json` `exports`/`main`), scheduled jobs, message consumers, and test entry.
3. **Map the build and ship path.** Build command → artifacts → packaging → publish/deploy definitions (CI workflows, Dockerfiles, chart manifests). Note where the documented command differs from CI's actual command; the CI is the truth.
4. **Locate configuration and environment surfaces.** Config loaders, `.env` files, feature flags, secrets indirection. Never record secret values.
5. **Measure hot spots.** Top 20 files by (a) size, (b) churn (`git log --since=12.months --name-only | sort | uniq -c | sort -rn | head -20`) if history exists. Churn × size is the candidate hot-spot list for P04.
6. **Detect duplication and drift.** Same-named files in multiple trees, copied utility modules, two competing test frameworks, multiple lockfiles, mixed package managers.
7. **Write `.audit/REPO_STRUCTURE.md`** with: directory table (path, files, bytes, role, notes), entry-point table, build/ship path (ordered steps with file references), configuration surfaces, hot-spot list, duplication/drift list, and explicit coverage limits (what you sampled vs read fully).
8. **Update the ledger** with P02 status and open questions.

## 5. Decision rules and evidence standard

- Counts must come from commands, not impressions; paste the command in the artifact.
- A directory is "generated" only if there is a generator config or a header marker. Otherwise label `possibly generated — unconfirmed`.
- Entry points require a code reference (file:line) showing registration or invocation.
- If the repository has no meaningful structure (flat dump of files), say so — that is itself a finding candidate for P07.
- For monorepos, produce the same table per workspace and then a cross-workspace summary.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Numbers reproducible | re-run two counts from the artifact | identical results |
| Entry points real | open each referenced file:line | registration/invocation visible |
| Build path matches CI | compare artifact's build steps with CI config | no undocumented step |
| Coverage limits stated | inspect artifact | non-empty section |
| No source mutation | `git status --porcelain` | only `.audit/` changes |

## 7. Failure handling

- **Shallow clone / no history** → skip churn analysis, record `history unavailable`, use size and import fan-in as substitutes.
- **Binary-heavy repository** → report byte shares, exclude binaries from code analysis, note the limitation.
- **Generated code dominates** → identify the generator and audit that, not the output; say so explicitly.
- **No CI** → record "no automated build/ship path"; this becomes an S3/S2 finding candidate depending on the project's maturity.

## 8. Security and authorisation

Risk class B, artifacts only. Do not open `.env*`, key files, or credential stores beyond confirming their existence. Do not run build commands that deploy or publish.

## 9. Completion criteria

- [ ] Directory inventory with measured counts and roles.
- [ ] Entry points identified with file:line evidence.
- [ ] Build/ship path documented and reconciled with CI.
- [ ] Hot-spot list produced (churn and/or size).
- [ ] Duplication/drift observations listed.
- [ ] Coverage limits explicit.
- [ ] Ledger updated.

## 10. Deliverables and handover

Artifact: `.audit/REPO_STRUCTURE.md`.

P03 receives: subsystem candidates, entry points, hot-spot files, build/ship path, and the list of areas excluded from analysis.
