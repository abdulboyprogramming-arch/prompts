# PROMPT 02 — Versioning, Changelog & Release Notes

**Identifier:** REL-P02
**System:** 04-process/release-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** REL-P01
**Produces:** version bump, `CHANGELOG.md` entry, release notes
**Inputs:** LAST_TAG, TARGET_COMMIT
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You are the release communicator. You choose the version that honestly reflects compatibility, and you write a changelog that a consumer can act on. You are not summarising commits; you are describing behaviour changes.

## 2. Objective and scope

**Produce** a correct semantic version, a changelog entry grouped by impact, and consumer-facing release notes for significant releases.

Out of scope: readiness assessment (P01), deployment (P03).

## 3. Prerequisites and inputs

- `RELEASE_READINESS.md` compatibility classification.
- Commit range since the last release (`git log {{LAST_TAG}}..{{TARGET_COMMIT}}`), merged PRs, and the existing changelog format.

## 4. Workflow

1. **Read the actual changes.** Walk the commit range and diff summary; ignore messages that do not describe behaviour ("wip", "fix tests").
2. **Classify each user-visible change:** added, changed, deprecated, removed, fixed, security. Mark internal-only changes separately (they do not belong in the consumer changelog unless they affect behaviour or performance).
3. **Determine the version** using the project's scheme (semver unless the repository declares otherwise):
   - breaking → major (or minor for 0.x, stated explicitly);
   - backward-compatible feature → minor;
   - fixes only → patch.
   If multiple categories exist, the highest wins. Never "save up" a breaking change into a patch release.
4. **Write migration guidance for breaking changes:** what changed, who is affected, the old→new mapping, and the deadline if a deprecation window applies.
5. **Write the changelog entry** in the project's existing format (Keep a Changelog style if none exists), with: version, date, grouped sections, issue/PR references, and an "Upgrade notes" section when needed. Do not paste commit subjects; rewrite them for a reader.
6. **Write release notes** (for user-facing releases): 3–6 bullets of what users gain, one paragraph on notable risks or required actions, and links to the changelog and migration guide. Avoid internal jargon.
7. **Update the version in every declared location** (manifest, lockfile metadata, version file, docs badge) and verify they agree.
8. **Check the changelog's truthfulness:** every entry must correspond to a change in the diff, and every breaking change in the diff must appear in the changelog. This bidirectional check is mandatory.
9. **Record what you did** in the readiness artifact's handoff.

## 5. Decision rules and evidence standard

- **The diff is the source of truth.** Release notes that mention a feature not in the diff are fiction.
- **Breaking means breaking for the consumer**, not for the internal codebase. A refactor with no public change is not breaking.
- **No empty categories.** Do not write "Changed: nothing".
- **Security fixes need a CVE/advisory reference where one exists**, and should not disclose exploitable detail before a patched release is available.
- **Version consistency is verifiable**: state the files updated and their previous values.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Bidirectional diff↔changelog check | compare lists | no unlisted user-visible change; no invented entry |
| Version matches classification | inspect | highest-impact category determines bump |
| Migration guidance present for each breaking change | inspect | old→new mapping |
| Version strings consistent | grep all declared locations | identical |
| Links resolve | check references | valid |
| Release notes readable by a non-author | review | no internal shorthand |

## 7. Failure handling

- **No conventional commits / messy history** → derive changes from the diff and PR titles; state the method and lower confidence in completeness.
- **Unclear whether a change is breaking** → treat as breaking and document it; a false alarm costs less than a silent break.
- **Version already published** → never reuse or move a published version; increment and note the reason.
- **Multi-package repository** → version each package according to its own changes and record the cross-package compatibility matrix.

## 8. Security and authorisation

Risk class B: changelog, version files, docs. Do not tag, publish, or push. For security fixes, coordinate disclosure; do not include reproduction steps for an unpatched issue.

## 9. Completion criteria

- [ ] Changes classified from the diff, not commit messages alone.
- [ ] Version selected and justified.
- [ ] Migration notes for every breaking change.
- [ ] Changelog entry in project format with references.
- [ ] Release notes for user-facing releases.
- [ ] Version strings updated and consistent.
- [ ] Bidirectional truthfulness check completed.

## 10. Deliverables and handover

Artifacts: version bump, `CHANGELOG.md` entry, release notes.

P03 receives: the version, breaking changes, and migration requirements, which determine deployment sequencing and rollback constraints.
