# PROMPT 03 — History Repair

**Identifier:** GIT-P03
**System:** 04-process/git-operations
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D when history is shared; B when local and unpublished
**Depends on:** GIT-P01 (shared-status assessment required)
**Produces:** `.git-ops/HISTORY_REPAIR.md`, rewritten branch or cleanup commits
**Inputs:** REPO_PATH, BRANCH, BASE_REF (optional: SHARED_HISTORY, APPROVER)
**Est. effort:** 20–120 min

---

## 1. Role and mandate

You are performing history surgery: squashing, rewording, reordering, splitting, dropping commits, removing files or secrets, or correcting authorship. These operations rewrite commits, and rewritten commits are **different commits** — anyone who has the old ones will diverge.

Your first job is not the rebase. It is establishing whether the history is shared, because that single fact changes the operation from a tidy-up into an event requiring authorisation and coordination.

## 2. Objective and scope

**Produce** the intended history with the least destructive method, on a branch whose safety has been established.

Out of scope: recovering already-lost commits (P04), deciding branch policy (P05), rotating a leaked secret (that happens *before* any purge, and is not optional).

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| `REPO_PATH`, `BRANCH` | yes | ask; never guess the branch |
| `SHARED_HISTORY` — whether others have these commits | **yes** | determine it: remote branch exists? others pushed? run `git log @{u}..HEAD` and ask | 
| `APPROVER` for a shared rewrite | required when shared | stop; a shared rewrite without authorisation is not a technical decision |
| A backup reference and the reflog SHA from P01's `.git-ops/STATE.md` | yes | take them now |

## 4. Workflow

1. **Classify the rewrite by blast radius**, working in `{{REPO_PATH}}` on `{{BRANCH}}`, given that `SHARED_HISTORY` is `{{SHARED_HISTORY}}` and the authorised approver is `{{APPROVER}}`:

   | Situation | Method | Risk |
   |-----------|--------|------|
   | Unpushed local commits: squash, reword, reorder, split | interactive rebase | B |
   | Unpushed commit already amended wrongly | `git commit --amend` / reflog restore | B |
   | Pushed branch nobody else has pulled | rebase + `push --force-with-lease` | C |
   | Shared branch (merged into main, or others branching from it) | **do not rewrite**; add a corrective commit | D |
   | File or secret must leave all history | `git filter-repo` on a coordinated clone | D |
   | Wrong author/email on recent commits | rebase with `--exec`, or `filter-repo --mailmap` if widespread | C |

2. **For a shared branch, prefer a revert over a rewrite.** A corrective commit preserves everyone's history and is auditable. Reserve rewriting for cases where the content must not exist (secrets, large binaries, legal removal) and where the owner has authorised it.
3. **Back up before touching anything** in `{{REPO_PATH}}`: `git branch backup/{{BRANCH}}-<timestamp>` at the current tip, plus the reflog SHA in `.git-ops/HISTORY_REPAIR.md`. Record how to restore: `git reset --hard backup/...`.
4. **Perform the smallest operation that achieves the goal.** Reword one commit rather than rebasing the branch; fix one file rather than rewriting history.
5. **Interactive rebase procedure**: `git rebase -i {{BASE_REF}}`, mark commits `pick`/`reword`/`edit`/`squash`/`fixup`/`drop`. After each stop: make the change, `git add`, `git rebase --continue`. If a commit is dropped deliberately, **state it in the artifact** — a silently dropped commit is indistinguishable from a lost one.
6. **For a secret in history**, the order is mandatory:
   1. **Rotate the credential now**, before anything else; history rewriting does not un-leak it.
   2. Assess exposure: was the branch ever pushed? For how long? Who could clone it?
   3. Purge with `git filter-repo` (not `filter-branch`) on a fresh clone, coordinated with the owner.
   4. Force-push with lease, notify every collaborator to re-clone (not pull), and invalidate any forks/caches you know of.
   5. Record that removal is incomplete by nature: clones, caches, CI logs, and provider snapshots may retain it.
7. **Rewriting shared history, when authorised**: announce a freeze window, confirm every collaborator's state, perform the rewrite, `push --force-with-lease` (never plain `--force`), then verify the remote's tip matches your local tip, and tell everyone to re-clone or reset to the new tip. Record the old and new SHAs.
8. **Verify the result**: `git log --oneline` against the intended list, `git diff backup/...` for *content* equality where the change was meant to be content-preserving, and the test suite if any commit's content changed.
9. **Write `.git-ops/HISTORY_REPAIR.md`:** classification, shared-status evidence, authorisation, backup refs and restore command, operations performed with old→new SHAs, commits dropped (with reason), verification, collaborator instructions, and residual risks.

## 5. Decision rules and evidence standard

- **Never rewrite shared history without an explicit decision by the owner.** Technical feasibility is not authorisation.
- **`--force-with-lease` always; `--force` never.** Plain force overwrites work pushed since you last fetched.
- **Backup branch before the first rebase command**, because `reflog` is local, expires, and is useless to a colleague.
- **Content-preserving rewrites must be proven content-preserving** by diffing against the backup.
- **A dropped commit is a decision to delete work.** Name it.
- **Secret purging does not undo disclosure.** Say so in the artifact; the rotation is what limits the damage.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Shared status evidenced | remote branch + recent authors | stated with basis |
| Authorisation recorded (if shared) | approver name | present |
| Backup ref exists | `git branch --list 'backup/*'` | points at pre-rewrite tip |
| Restore command documented | artifact | tested or explicit |
| Old→new SHAs recorded | `git log` comparison | every rewritten commit mapped |
| Content preserved where intended | `git diff backup/...` | empty, or explained |
| Force push used lease | command log | `--force-with-lease` |
| Remote tip matches local | `git ls-remote` | equal SHAs |
| Collaborators instructed | message/draft | re-clone guidance stated |

## 7. Failure handling

- **Rebase produces conflicts** → resolve per P02, or abort; the pre-rewrite backup remains valid until the operation completes.
- **A commit disappears unexpectedly** → stop, do not continue the rebase; `git reflog` and the backup branch identify the lost commit, and P04 recovers it.
- **Someone pushed during the rewrite** → the lease will (correctly) reject the push; re-fetch, inspect their commits, and redo the rewrite including them, or abort.
- **The branch is protected** → the push will fail; do not disable protection to force it. Escalate: protection exists for this reason.
- **`filter-repo` changed more than expected** → restore from the backup clone, verify with `git diff`, and re-run with narrower paths. Never run it on a repository without a full backup clone.
- **You discover the rewrite is unnecessary** → stop; a corrective commit is almost always cheaper than the coordination a rewrite costs.

## 8. Security and authorisation

Risk class D for shared history. This prompt rewrites published commits, deletes content, and can destroy colleagues' work. Requirements: owner approval recorded, a backup branch, a lease-based push, and notification. Never publish a rewritten branch by deleting and re-pushing the remote branch as a shortcut. Never purge a secret without rotating it first.

## 9. Completion criteria

- [ ] Rewrite classified by blast radius.
- [ ] Shared status evidenced; authorisation recorded where shared.
- [ ] Backup branch and restore command documented.
- [ ] Smallest sufficient operation chosen.
- [ ] Operations recorded with old→new SHA mapping.
- [ ] Dropped commits named with reasons.
- [ ] Secrets rotated before any purge; exposure assessed.
- [ ] Content preservation verified against the backup.
- [ ] Force-with-lease used; remote tip verified.
- [ ] Collaborator instructions issued; residual risks stated.

## 10. Deliverables and handover

Artifact: `.git-ops/HISTORY_REPAIR.md`.

Handover: a leaked secret → `05-scenarios/security-incident/` for disclosure decisions, with rotation already done; recurring history problems → P05 hygiene (commit granularity, branch model, hooks); lost commits during the operation → P04 immediately; the recorded decision → the team's conventions document.
