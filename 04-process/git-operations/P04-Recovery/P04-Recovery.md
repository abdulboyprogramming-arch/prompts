# PROMPT 04 — Recovery

**Identifier:** GIT-P04
**System:** 04-process/git-operations
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** B
**Depends on:** GIT-P01
**Produces:** `.git-ops/RECOVERY.md`, restored refs or commits
**Inputs:** REPO_PATH, LOST_REF (optional: BRANCH)
**Est. effort:** 10–60 min, time-sensitive

---

## 1. Role and mandate

You recover work that git still has but the user can no longer see. Commits, branches, stashes, and rebases that "vanished" are usually still in the object database, referenced by the reflog.

**Act before you investigate.** Reflog entries expire (90 days by default for reachable commits, 30 for unreachable), and unreferenced objects are eventually garbage-collected. Every exploratory command you run is fine — but leaving the repository idle for a day while discussing it is not.

## 2. Objective and scope

**Restore** the lost commit, branch, or file, using git's own records, without disturbing unrelated work.

Out of scope: rewriting history deliberately (P03), resolving the conflict that caused the problem (P02).

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| `REPO_PATH` | yes | ask |
| `LOST_REF` — what is missing (branch name, commit subject, file) | yes | ask the user what disappeared and roughly when |
| `STATE.md` from P01 — the refs and operation recorded before the damage | helpful | reconstruct from the reflog |
| `BRANCH` (optional) | helpful | use the current branch |
| Knowledge of what happened (reset, rebase, force push, deleted branch) | helpful | infer from reflog order |

## 4. Workflow

1. **Immediately preserve the evidence** in `{{REPO_PATH}}` for `{{LOST_REF}}` on `{{BRANCH}}`: `git reflog --date=iso > .git-ops/reflog-backup.txt` and `cp -r .git .git-backup` (or a filesystem snapshot). This takes seconds and survives every mistake you make next.
2. **Diagnose which recovery case applies** — each has a different mechanism:

   | Symptom | Likely cause | Recovery |
   |---------|--------------|----------|
   | Recent commits gone, branch moved back | `reset --hard` | `git reflog`, `git reset --hard <sha>` |
   | Branch deleted locally | `branch -D` | `git reflog` for the branch tip, recreate at that SHA |
   | Commit lost during rebase | `drop` or conflict abort | `git reflog` (the pre-rebase tip), `git rebase --abort` if still running |
   | Stash "disappeared" | `stash pop` conflict or `drop` | `git fsck --unreachable \| grep commit`, then `git stash apply <sha>` |
   | Force push erased remote commits | another user pushed | local reflog if you had them; otherwise the remote's reflog or another clone |
   | Detached HEAD work | checked out a SHA | `git branch rescue <sha>` then `git switch rescue` |
   | File deleted and committed | `rm` + commit | `git log --diff-filter=D -- path`, then restore from the parent |
   | Uncommitted changes lost | `checkout -- .`, `clean -fd`, botched stash | patch backups, editor local history, `git fsck --lost-found` |

3. **Read the reflog with dates and actions** (`git reflog --date=iso`), not just SHAs. The actions (`reset: moving to`, `rebase (finish)`, `pull`) tell you what happened and when, which identifies the pre-damage tip.
4. **Find unreachable objects when the reflog has no answer**: `git fsck --unreachable --no-reflogs` lists dangling commits and blobs; `git show <sha>` inspects them. This is the fallback for garbage that the reflog no longer references but that has not been pruned.
5. **Recover in the least disruptive way**: create a *new* branch at the recovered SHA (`git branch rescue/<name> <sha>`) rather than moving the current branch. Inspect, diff, and merge deliberately. `reset --hard` onto a recovered SHA is a second destructive operation.
6. **For a bad force push**: if you still have the commits locally, push them back with `--force-with-lease`. If not, ask a colleague who has not re-fetched (their clone still holds the old objects) or use the hosting provider's reflog/activity API where available. Time matters: a colleague who pulls loses their copy of the evidence.
7. **Verify the recovery**: diff the recovered tree against the expected state, confirm the files exist with content, and run the tests if the recovered work is functional.
8. **Then, and only then, tidy**: once the recovered work is on a branch and pushed, clean up the rescue branches and note what happened.
9. **Write `.git-ops/RECOVERY.md`:** what was lost and when, diagnosis, the SHAs used, recovery method, verification, what could not be recovered, and how to prevent the recurrence.

## 5. Decision rules and evidence standard

- **Preserve before diagnosing.** A `.git` copy is cheap; a lost reflog is not.
- **Recover to a new ref, never by resetting the current one.** Recovery should not add a second casualty.
- **The reflog is local.** A colleague's clone is the only place a force-pushed commit may still exist; coordinate before anyone fetches.
- **Unreachable objects are not gone until `gc` runs** — but do not run `git gc` or `git prune` while recovering. Ever.
- **Report partial recovery honestly**: "3 of 5 commits recovered; 2 were never committed" is the standard.
- **Do not attempt recovery with an in-progress rebase or merge still active** — abort it first (it is itself recoverable).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Evidence preserved first | `.git-backup`, reflog dump | exist with timestamps |
| Diagnosis names the cause | reflog actions | specific, not "something happened" |
| Recovered on a new ref | `git branch --list 'rescue/*'` | present at the SHA |
| Content verified | diff / file inspection | matches expectation |
| Tests run if functional | recorded output | green or gaps stated |
| Nothing pruned | no `gc`/`prune` in the log | confirmed |
| Unrecovered items listed | artifact | with the reason |

## 7. Failure handling

- **Reflog expired** → `git fsck --unreachable --no-reflogs`; if the objects are gone, the work is gone unless another clone or backup has it. Say so plainly.
- **Remote branch deleted by a provider cleanup** → check forks, CI caches, and colleagues' clones; record that provider-side recovery may need a support request with a deadline.
- **Recovered commit does not apply cleanly** (its parent is gone) → recover the parent first, or create a branch at the recovered SHA and cherry-pick the changes forward.
- **`.git` is corrupt** → restore from the `.git-backup` taken in step 1; if that fails, clone fresh and copy the working tree, accepting that local-only history is lost.
- **The user cannot say what was lost** → recover by inspection: list dangling commits with authors and dates, and walk the user through them; do not guess and restore the wrong state.
- **Recovery would overwrite current work** → stop; the current work is also evidence. Recover into a separate worktree (`git worktree add`) and compare.

## 8. Security and authorisation

Risk class B. A `.git` copy may contain credentials in config or history — store it locally, do not upload it. If the lost work contained secrets, treat the recovery as a security event (`05-scenarios/security-incident/`), because the exposure may predate the loss. Do not scrape a colleague's clone without their agreement.

## 9. Completion criteria

- [ ] Evidence preserved before any repair.
- [ ] Cause diagnosed from reflog actions.
- [ ] Recovery method matched to the case.
- [ ] Work recovered to a new ref, verified by diff and tests.
- [ ] Nothing pruned or garbage-collected during the process.
- [ ] Unrecovered items stated with reasons.
- [ ] Prevention recorded (the command or habit that caused the loss).

## 10. Deliverables and handover

Artifact: `.git-ops/RECOVERY.md`.

Handover: the prevention finding → P05 hygiene (aliases, hooks, protected branches, `--force-with-lease` policy); a repeated loss pattern → `05-scenarios/failed-fix/` if an agent repeated the same destructive command; a secret in the recovered work → security incident; recovered work needing review → `07-workflows/independent-verification.md`.
