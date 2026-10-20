# PROMPT 01 — State & Safety Check

**Identifier:** GIT-P01
**System:** 04-process/git-operations
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage; run before any destructive command)
**Produces:** `.git-ops/STATE.md`
**Inputs:** REPO_PATH, BRANCH (optional: BASE_REF)
**Est. effort:** 5–15 min

---

## 1. Role and mandate

You are the engineer establishing what state the repository is actually in before anything risky happens. Engineers and agents routinely destroy work because they acted on an assumed state: they thought the tree was clean, they thought the branch was pushed, they thought no rebase was in progress.

This stage is read-only and deliberately short. Its value is that it runs *before* the command that cannot be undone.

## 2. Objective and scope

**Answer:** what is uncommitted, unpushed, in progress, recoverable, and shared — for `{{REPO_PATH}}` on `{{BRANCH}}`.

Out of scope: fixing anything, resolving conflicts (P02), rewriting history (P03).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| `REPO_PATH` | user | use the current directory and say so in the output |
| `BRANCH` | user | read it from `git rev-parse --abbrev-ref HEAD` and record it |
| `BASE_REF` (optional) | user | default to the branch's upstream, or to `origin/main` if there is none |
| Whether the branch is shared | user | infer from remotes and recent pushers, and mark `assumed` |

## 4. Workflow

1. **Record the basics verbatim:** current branch, HEAD SHA, upstream branch, ahead/behind counts, and whether the repository is a worktree or a clone.
2. **Inventory uncommitted work in `{{REPO_PATH}}`**: `git status --porcelain=v1 -uall`. Categorise staged, unstaged, untracked, and ignored-but-important files. Count them; a clean tree is a finding worth stating explicitly.
3. **Inventory unpushed work**: commits ahead of upstream (`git log --oneline @{u}..HEAD`), plus any local branches with no upstream (`git for-each-ref --format='%(refname:short) %(upstream:short)'`). These commits may exist *nowhere else*.
4. **Detect an operation in progress** — this is the step that prevents damage:
   - `.git/MERGE_HEAD` → merge in progress
   - `.git/rebase-merge` or `.git/rebase-apply` → rebase in progress
   - `.git/CHERRY_PICK_HEAD` → cherry-pick in progress
   - `.git/BISECT_LOG` → bisect in progress
   - `.git/REVERT_HEAD` → revert in progress
   If any exists, **stop and say so**; every later command behaves differently.
5. **Check for stashes** (`git stash list`) and for worktrees (`git worktree list`), because work may live in a different checkout than the one you are looking at.
6. **Establish recoverability** relative to `{{BASE_REF}}`: `git reflog -n 20` on `{{BRANCH}}`, and note that reflog entries are local and expire (default 90 days for reachable, 30 for unreachable). Record the current SHA of every branch that might be moved.
7. **Establish what is shared**: which branches exist on the remote, who pushed recently (`git log --format='%an %ae' --since='2 weeks'`), and whether protected-branch rules exist. Anything shared changes the risk class of P03 from B to D.
8. **Take a safety snapshot before recommending any operation** — cheap and reversible:
   - `git stash create` (or `git stash push -m "pre-<operation>"`) for uncommitted work;
   - `git diff > /tmp/pre-<operation>.patch` and `git diff --cached >>` for a file-level copy;
   - `git branch backup/<branch>-<timestamp>` for the current commit.
   Record the exact commands used and where the artifacts live.
9. **Write `.git-ops/STATE.md`:** branch/SHA/upstream, working tree inventory, unpushed commits, in-progress operation, stashes and worktrees, reflog snapshot with expiry, shared-status assessment, safety snapshots taken, and a recommendation (`safe to proceed` / `proceed only after backup` / `stop — resolve the in-progress operation first`).

## 5. Decision rules and evidence standard

- **Never assume a clean tree.** Print it.
- **Unpushed commits are the highest-risk asset in the repository.** If they exist, no history-changing command runs until they are backed up.
- **An in-progress operation is a stop sign**, not a detail: `git rebase --abort` may be the right move, but it must be a decision, not a side effect.
- **Backups are three-way when work is uncommitted**: stash, patch file, and a branch. Each can fail (a stash conflict, a diff that omits untracked files, a branch created from the wrong ref).
- **Shared status changes the rules**, so establish it here rather than discovering it during a history rewrite; never assume a branch is local-only.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Branch, SHA, upstream recorded | `git rev-parse`, `git status -sb` | exact values in the artifact |
| Working tree inventoried | `git status --porcelain -uall` | counts per category |
| Unpushed commits listed | `git log @{u}..HEAD` | every commit named |
| In-progress operation detected | check the five marker files | stated, even if none |
| Stashes and worktrees listed | `git stash list`, `git worktree list` | complete |
| Reflog snapshot taken | `git reflog -n 20` | SHAs recorded |
| Shared status assessed | remote branches + recent authors | stated with basis |
| Backups taken where needed | commands + paths | recorded |

## 7. Failure handling

- **No `.git` directory** → the path is not a repository or is a subdirectory of one; locate the root with `git rev-parse --show-toplevel` and re-run there.
- **Detached HEAD with uncommitted work** → record the SHA, create a branch immediately if the work matters, and say so; a detached HEAD is the most common way work is lost.
- **Shallow clone or single-branch clone** → note it; history-based investigation (`bisect`, `log -S`) will be incomplete.
- **Repository in a corrupt or locked state** (`.git/index.lock` present) → do not delete the lock blindly; check for a running git process first, then record it and stop.
- **Huge untracked directories** (build output, `node_modules`) → distinguish genuinely untracked source from generated noise before counting it as work at risk.

## 8. Security and authorisation

Risk class A: read-only. Do not run any command that writes to the repository (including `stash push`, which mutates) without saying so — `git stash create` and `git diff` are the read-only forms. Never print remote URLs that embed credentials; redact them to `https://<redacted>@host/path`.

## 9. Completion criteria

- [ ] Branch, HEAD SHA, upstream, ahead/behind recorded.
- [ ] Working tree inventoried by category.
- [ ] Unpushed commits listed.
- [ ] In-progress operation checked and stated.
- [ ] Stashes and worktrees listed.
- [ ] Reflog snapshot recorded with expiry noted.
- [ ] Shared-status assessment with its basis.
- [ ] Safety backups taken where work is at risk.
- [ ] Explicit recommendation issued.

## 10. Deliverables and handover

Artifact: `.git-ops/STATE.md`.

Handover: `proceed` → P02/P03 with the backups named. `Resolve first` → the in-progress operation's own stage (P02 for a stopped merge/rebase, P04 for a bisect or unexpected state). `Shared` → P03 must obtain approver-level authorisation before any rewrite.
