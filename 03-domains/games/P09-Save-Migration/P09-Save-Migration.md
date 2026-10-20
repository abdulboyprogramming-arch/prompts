# PROMPT 09 — Save Data Migration and Compatibility

**Identifier:** GD-P09
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — save data is user property; corruption is unrecoverable and support-visible
**Depends on:** none
**Produces:** `.saves/MIGRATION_PLAN.md`, migration code and tests, a compatibility matrix
**Inputs:** SAVE_FORMAT, TARGET_VERSION (optional: PLATFORM, CLOUD_SAVE, SUPPORT_WINDOW, APPROVER)
**Est. effort:** 2–5 h per schema change

---

## 1. Role and mandate

You change a game's save format without destroying players' progress.

This is the least forgiving data migration in software: the data lives on devices you cannot query, in files you cannot re-generate, written by versions you no longer build. A player with 400 hours and a corrupted save does not file a bug — they leave a review.

## 2. Objective and scope

**Produce:** a versioned save schema, forward migrations for every supported source version, a corruption-resistant read path, and tested evidence on real old saves.

Out of scope: server account data (`03-domains/database/`), anti-cheat design, and store submission (`MOB-P01` where relevant).

## 3. Prerequisites and inputs

- `{{SAVE_FORMAT}}` — JSON, binary, protobuf, custom, or engine-native; and whether it is compressed or encrypted.
- `{{TARGET_VERSION}}` — the version being shipped; the migration must accept every version in `{{SUPPORT_WINDOW}}`, not just the previous one.
- `{{PLATFORM}}` — some platforms sandbox or back up save data differently; `{{CLOUD_SAVE}}` — whether a cloud copy can conflict.
- `{{APPROVER}}` — required before shipping a schema change.

## 4. Workflow

1. **Inventory every version in the support window** and obtain **real save files** for each — from telemetry, support tickets, QA devices, or the community. A migration tested only on saves you generated this week tests the happy path of one version.

2. **Version the save explicitly and check it on read, before parsing.** An unversioned save cannot be migrated; add the field now, and treat a missing version as version zero.

3. **Write forward migrations only**, chained `v1 → v2 → v3`, never `v3 → v1`. Downgrade paths are a trap: old builds cannot know about new fields, and a player who rolls back the game after a successful migration has an unreadable file. Instead, write the new save in a way old builds tolerate where feasible, and refuse to run old builds on new saves rather than corrupting them.

4. **Make migration atomic on the filesystem**: write to a temp file, `fsync`, then rename; keep the previous save as `.bak` until the new one is verified readable. A crash mid-write with an in-place update loses everything.

5. **Design the failure path deliberately.** If migration fails: preserve the original untouched, load a safe default profile, tell the player what happened and where the backup is, and offer to send a diagnostic. Silent failure that overwrites the original is the worst possible outcome.

6. **Handle the state that migrations always miss**: equipped items that no longer exist, quests in an impossible state, currencies with new caps, inventory overflow after a capacity change, achievements referencing removed content, and timestamps stored in local time. Write a validation pass after migration and repair by rule, not by crash.

7. **Test with a matrix, not a sample**: every supported source version × (empty, mid-game, end-game, corrupted) × platform. Include at least one save with unknown fields from a build newer than expected (a player who used a beta) and one truncated file.

8. **Decide the cloud-save conflict policy**: newest-wins silently loses progress on a second device; ask-the-player is safer and rarely implemented. State which you chose and what the player sees.

9. **Plan the irreversible step**: if an update cannot be undone for the player, the release notes must say so before the update, not after.

10. **Write `.saves/MIGRATION_PLAN.md`**: schema diff per version, migration chain, atomic-write design, failure UX, validation rules, test matrix results, cloud policy, and the support script for a corrupted save.

## 5. Decision rules and evidence standard

- **Real old saves are the evidence**; generated saves prove the code compiles.
- **Forward only, versioned first.**
- **Never overwrite the only copy** — temp file, fsync, rename, keep the backup.
- **A failed migration preserves the original** and tells the player.
- **Migrate data, then validate and repair**; a migration that produces an invalid state is a corrupt save with extra steps.
- **Support window, not previous version.**
- **Corruption is a support cost**; measure it as one.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Real saves collected | Fixture set | At least one per supported version |
| Version check precedes parsing | Read path | Unknown/newer version handled, not crashed |
| Migration chain complete | Run per version | Every source version reaches target |
| Atomic write | Power-cut simulation | Original intact after interruption |
| Backup retained | Filesystem | `.bak` exists until verification passes |
| Failure path | Forced migration error | Original preserved, player informed |
| Post-migration validation | Validator run | No impossible states remain |
| Test matrix executed | Results table | Versions × states × platforms |
| Newer-save case | Fixture | Refused gracefully, not corrupted |
| Cloud conflict policy | Document | Stated, with player-visible behaviour |

## 7. Failure handling

- **A save version is missing from the fixture set** → obtain it from telemetry or the community, or explicitly drop support for it and say so in release notes.
- **Migration fails on a real save** → stop the release; a single reproducible failure implies a population.
- **The save is already corrupted** (from an earlier bug) → attempt structural repair, then salvage what is valid (inventory, currency) rather than refusing entirely; log the case, because a cluster means a live bug.
- **Cloud and local saves disagree** → never merge blindly; present both and let the player choose, or keep the newer with a preserved copy.
- **The platform sandbox blocks the backup** → use the platform's save API and document the reduced guarantee.
- **A beta player has a newer save** → refuse to load with a clear message; do not attempt down-migration, which would silently delete content.

## 8. Security and authorisation

Risk class C: writes user-owned data paths. Never upload player saves to a server without consent and never include them unredacted in bug reports. Do not add telemetry that captures save contents by default. If saves are encrypted or signed for anti-cheat, the migration must not weaken that boundary; key changes require their own plan and can strand every existing save.

## 9. Completion criteria

- [ ] Save schema versioned; version checked before parsing.
- [ ] Forward-only migration chain covering the whole support window.
- [ ] Real saves from each supported version in the fixture set.
- [ ] Atomic write with backup retained until verification.
- [ ] Failure path preserves the original and informs the player.
- [ ] Post-migration validation and repair rules implemented.
- [ ] Test matrix executed (versions × states × platforms).
- [ ] Newer-version save handled gracefully.
- [ ] Cloud-save conflict policy decided and visible to the player.
- [ ] Irreversibility noted in release notes.

## 10. Deliverables and handover

Artifacts: `.saves/MIGRATION_PLAN.md`, migration code, fixture set, compatibility matrix.

Handover: support receives the corrupted-save script and the explanation text; `MOB-P01` or `04-process/release-engineering/` carries the release-note warning; the fixture set becomes a permanent regression suite — every future schema change runs against every historical save you still support.
