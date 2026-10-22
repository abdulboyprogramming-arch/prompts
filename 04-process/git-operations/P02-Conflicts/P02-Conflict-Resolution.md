# PROMPT 02 — Conflict Resolution

**Identifier:** GIT-P02
**System:** 04-process/git-operations
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** GIT-P01
**Produces:** `.git-ops/CONFLICTS.md`, resolved merge/rebase
**Inputs:** REPO_PATH, BRANCH, BASE_REF
**Est. effort:** 20–90 min

---

## 1. Role and mandate

You resolve conflicts by understanding both sides' intent, not by picking a side. The failure this stage exists to prevent is the one that looks like success: the conflict markers are gone, the build passes, and a colleague's change has silently vanished.

## 2. Objective and scope

**Resolve** every conflict with a justified decision per hunk, then prove the result preserves both intents by building and testing.

Out of scope: deciding that one branch should win wholesale (that is a product decision), rewriting history (P03).

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| `REPO_PATH`, `BRANCH`, `BASE_REF` | yes | the merge target is unknown; ask |
| `.git-ops/STATE.md` from P01: the operation in progress (merge, rebase, cherry-pick) | yes | run P01 first |
| Build and test commands | yes | conflicts cannot be validated without them |
| A way to reach the other author | recommended | record it as a risk; semantic conflicts may need them |

## 4. Workflow

1. **Identify the operation and its direction** in `{{REPO_PATH}}`, with `{{BRANCH}}` replaying onto or merging with `{{BASE_REF}}`. A merge conflict and a rebase conflict are not the same: in a merge, "ours" is your branch; in a rebase, "ours" is the upstream you are replaying onto. Getting this backwards is the most common cause of lost work.
2. **List every conflicted file by type**, because each needs a different method:

   | Type | Signal | Method |
   |------|--------|--------|
   | Textual, both edited | `UU` | Hunk-by-hunk, intent-based |
   | Modify/delete | `UD`, `DU` | Decide whether the file should exist; check both sides' commits |
   | Both added | `AA` | Merge contents or choose; usually both intents matter |
   | Rename + edit | rename detected | Move to the new path, apply the edit |
   | Binary | `UU` on binary | Choose one (cannot merge); record why |
   | Submodule | gitlink diff | Point to the correct commit; check it exists |
   | Generated/lock file | lockfiles, snapshots | Regenerate from source; never hand-merge |

3. **For each textual conflict, read the three commits**: `git log --merge -p <file>` and `git diff :1:file :2:file` / `:3:file`. State each side's intent in one sentence before editing. If you cannot state the intent, you are not ready to resolve.
4. **Resolve with intent, not preference.** Keep both behaviours where they compose; where they genuinely conflict, choose with a stated reason and flag it for review. Never resolve by "taking ours" across a file, and never delete a hunk you do not understand.
5. **Handle lockfiles and generated files by regeneration**: take either version, then run the package manager/build to produce the correct resolved file. Hand-merging a lockfile produces a file that installs differently than either branch intended.
6. **Check for semantic conflicts that git cannot see**: two branches that each compile but contradict each other (one renames a field, the other uses the old name; one changes a default, the other relies on it). Search for the symbols involved across the merged result.
7. **Complete the operation**: `git add` resolved paths; for a merge `git commit` (with the default message plus a note on non-obvious decisions); for a rebase `git rebase --continue`; if it becomes unmanageable, `git merge --abort` or `git rebase --abort` returns to the recorded pre-operation state — confirm the SHA matches P01's record.
8. **Verify behaviour, not just the absence of markers**: build, type-check, run the tests, and run the specific tests covering both changed areas. If the suite is weak here, say so and list what is unverified.
9. **Write `.git-ops/CONFLICTS.md`:** operation and direction, per-file type and resolution with the reason, semantic conflicts found, deletions kept (and why), regeneration performed, verification results, and anything needing the other author's confirmation.

## 5. Decision rules and evidence standard

- **Know which side "ours" means before resolving.** State it in the artifact.
- **No wholesale resolution.** `git checkout --ours .` on a conflicted tree is a data-loss operation wearing a convenience flag.
- **Every discarded hunk needs a stated reason** in the log.
- **Both intents usually survive.** If they cannot, the conflict is a design disagreement — escalate it rather than silently choosing.
- **A conflict-free tree is not a working system.** Build and test before declaring resolution.
- **Abort is a legitimate outcome**, and cheap: it returns to a known state. Repeatedly continuing through a rebase you do not understand is how commits disappear.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Operation and direction recorded | inspect | merge vs rebase, and which side is ours |
| Every conflicted file classified | `git status` | no unclassified file |
| Each resolution has a reason | artifact | per file, per discarded hunk |
| No markers remain | `grep -rn '<<<<<<<\\|>>>>>>>'` | zero hits |
| Lockfiles regenerated | package manager run | no hand-merge |
| Semantic conflicts searched | symbol search | addressed or listed |
| Build and tests pass | recorded output | green, or gaps stated |
| Abort path confirmed | P01 SHA comparison | unchanged base |

## 7. Failure handling

- **Conflict is in generated code** (protobuf, schema types, bundled assets) → regenerate from the source definition; never merge the output.
- **The other side deleted what you edited** → read both commits; decide whether the deletion was intentional (often it is a removal of dead code). If unclear, restore the file and flag it — losing a deletion is cheaper than losing a feature.
- **Rebase produces conflicts at every commit** → the branch has diverged structurally; abort and use a merge, or squash and re-apply intentionally. Record the choice.
- **Conflict in a binary or vendored artefact** → choose one version, record why, and check whether the artefact should be in the repository at all.
- **Verification fails and the cause is the merge** → do not "fix forward" inside the conflict resolution; abort, resolve on a fresh branch with the failing test as the first reproduction.
- **You cannot reach the author and the intent is ambiguous** → stop, record the specific question, and leave the operation in progress rather than guessing; a stopped merge preserves both sides.

## 8. Security and authorisation

Risk class B: repository-local changes. Do not resolve a conflict by disabling a security control (removing an auth check, weakening a validation) to make the tests pass — if both sides touched security logic, escalate to a reviewer. Do not commit secret material that appeared in either side; see `00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`.

## 9. Completion criteria

- [ ] Operation and direction identified and recorded.
- [ ] Every conflicted file classified by type.
- [ ] Intent stated for both sides before each resolution.
- [ ] Resolutions justified, including discarded hunks.
- [ ] Generated files regenerated, not merged.
- [ ] Semantic conflicts searched and addressed or listed.
- [ ] Build and tests executed with results recorded.
- [ ] Any question for the other author recorded.
- [ ] Abort state verified against P01.

## 10. Deliverables and handover

Artifact: `.git-ops/CONFLICTS.md`.

Handover: unclear semantics → the other author with the specific question; a design disagreement → `02-engineering/architecture-review/`; missing test coverage exposed by the conflict → `04-process/testing-qa/`; a lockfile conflict that recurs → P05 hygiene (commit lockfile policy).
