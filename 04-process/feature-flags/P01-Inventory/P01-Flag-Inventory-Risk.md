# PROMPT 01 — Flag Inventory and Risk

**Identifier:** FF-P01
**System:** 04-process/feature-flags
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.flags/FLAG_INVENTORY.md`
**Inputs:** REPO_PATH (optional: FLAG_PROVIDER, TARGET_SERVICE)
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You are auditing the runtime switches that decide what the production system actually does. A feature flag is a branch that lives outside the code review process: it changes behaviour without a deploy, and it accumulates. Your job is to make the set visible, classify it by *purpose*, and rank it by the harm it can cause when it is wrong, stale, or flipped by the wrong person.

You do not change flags, delete code, or recommend a rollout in this stage. You produce the map everything else depends on.

## 2. Objective and scope

**Produce:** a complete inventory of runtime switches with, per flag: identifier, type, owner, age, default state, exposure, where it is read, and risk class — plus a ranked risk list and an honest statement of what you could not see.

Out of scope: designing new flags (P02), rollouts (P03), flipping one during an incident (P04), removal (P05).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` read-only, with flag reads in code (SDK calls, config keys, env-var lookups) searchable.
- `{{FLAG_PROVIDER}}` if a flag service is used (LaunchDarkly, Unleash, Flagsmith, Split, internal) — for the console list and audit log. Without console access, inventory from code and mark provider-side targeting as unverifiable.
- `{{TARGET_SERVICE}}` if the repository hosts several deployables; otherwise inventory all.

## 4. Workflow

1. **Enumerate from three sources and reconcile them.** Code (grep for the SDK and config lookups), provider console (flag list with creation dates), and configuration (env vars, YAML, database rows). Every disagreement is a finding: a flag in the console that no code reads is dead configuration; a flag read in code that the console does not define is either a typo or an env-var path with different semantics.

2. **Classify by purpose, not by name.** The name is a hint, the usage site is the truth:

   | Type | What it looks like | Expected lifetime |
   |------|--------------------|-------------------|
   | Release | New path behind a flag, old path still reachable | Days to weeks |
   | Operational / kill-switch | Disables a dependency, expensive path, or risky feature under load | Long-lived, with a named operator |
   | Permission / entitlement | Gates a capability per tenant or plan | Permanent — this is product logic, not a flag |
   | Experiment | Splits traffic to measure an outcome | Fixed by the experiment's end date |
   | Migration / coexistence | Old and new implementation run side by side | Until the migration completes |

   A "release" flag older than its stated removal date, or a "permission" flag implemented as a boolean in a flag service, is a finding — the second is a security boundary stored in the wrong system, editable by whoever has console access.

3. **Record per flag:** identifier, type, owner (from blame, CODEOWNERS, or the provider's metadata), created date, age, default state, whether the default is safe when the provider is unreachable, number of read sites, whether both states are tested, and last-evaluated timestamp if available.

4. **Audit the kill-switches specifically.** For every operational flag, answer: who can flip it, what happens to in-flight work, does the off-path actually restore the old behaviour (or only stop *new* work), and has it been exercised? A kill-switch that has never been flipped is a hope, not a control.

5. **Find the orphan categories.** Flags with no owner, flags whose code path no longer references them, flags with an age beyond their type's expected lifetime, and flags whose two paths have diverged so far that the "off" path no longer builds the product's current shape.

6. **Rank by consequence**, using: blast radius if flipped unintentionally, the cost of the stale path (complexity, dead tests, security surface), whether the flag guards data-destructive behaviour, and whether both states are tested. State the ranking rule you used.

7. **Write `.flags/FLAG_INVENTORY.md`:** the table, the type summary with counts and median ages, the risk-ranked list with one-line consequences, the kill-switch audit, the reconciliation discrepancies, and the coverage statement (what was invisible: provider targeting rules, flags evaluated only in mobile clients, flags in services outside this repository).

## 5. Decision rules and evidence standard

- **A flag you cannot see is not an absent flag.** State the blind spots: client-side defaults, provider-side targeting, other repositories. Never write "all flags" unless the reconciliation actually closed.
- **Age is evidence, not a verdict.** An old operational kill-switch is correct; an old release flag is debt. Judge against the type.
- **Do not classify by name.** `enable_v2_checkout` may be a permission gate. Read the call site.
- **Both-states-tested is a fact to verify**, not to assume: does a test run with the flag off?
- **Default state is a safety property.** If the default is `true` and the provider is unreachable, the risky path is on during an outage.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Inventory reconciled | code count vs console count | every difference explained |
| Types assigned from usage | read each call site | no type derived from the name alone |
| Kill-switches audited | per-flag answers | operator, off-path effect, exercise history recorded |
| Orphans found | age vs type, unread flags | each listed with consequence |
| Defaults captured | config inspection | safety of the unreachable case stated |
| Blind spots stated | review | named, not implied |
| Ranking rule stated | read-through | consequence-based, applied consistently |

## 7. Failure handling

- **No provider access** → inventory from code, mark targeting as unverifiable, and state that the risk ranking is code-based only. Do not skip the stage: code inventory still finds orphans and untested states.
- **Thousands of flags** → sample deliberately: all operational and permission flags, all flags guarding destructive paths, and a random 10% of the rest with the sampling policy written down. Never present a sample as a census.
- **Flag reads are indirect** (wrapped in a helper, loaded from a config service) → follow the helper once and document the indirection; then use the helper as the search key.
- **Ambiguous purpose** → record both candidate types and the evidence for each; the owner resolves it in P02 rather than you guessing.
- **The repository is a library with no runtime** → stop and say so; flags belong to deployments, and the correct scope is the consuming services.

## 8. Security and authorisation

Risk class A: read-only. Do not evaluate flags in production, do not call provider APIs with write scopes, and never paste real targeting rules containing customer identifiers into the artifact. If a flag turns out to be an authorisation control, record that as a finding and notify the security owner rather than describing how it could be bypassed in a shared document.

## 9. Completion criteria

- [ ] Three sources enumerated and reconciled, differences explained.
- [ ] Every flag typed by usage site.
- [ ] Per-flag record complete: owner, age, default, read sites, test states.
- [ ] Kill-switches audited for operator, off-path effect, exercise history.
- [ ] Orphans and over-age flags listed with consequences.
- [ ] Risk ranking applied with a stated rule.
- [ ] Blind spots and sampling stated.
- [ ] `.flags/FLAG_INVENTORY.md` written.

## 10. Deliverables and handover

Artifact: `.flags/FLAG_INVENTORY.md`.

P02 receives: the inventory and the risk ranking, to decide what must be redesigned, what needs an owner or expiry, and which flags must never be removed because they are product logic in disguise.
