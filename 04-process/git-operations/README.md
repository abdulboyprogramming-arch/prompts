# Git Operations & History Safety

**Maturity: operational (v1.0.0).** Five stages for the situations that break agents and engineers alike: conflicts, history surgery, and recovery from a repository that now looks wrong.

**Entry point:** triage below, then [`P01-State/P01-State-Safety-Check.md`](P01-State/P01-State-Safety-Check.md)
**Execution mode:** implementation
**Per stage:** diagnostic (P01, P05), specialised (P04), implementation (P02, P03)
**Risk class:** A–D. Local-only operations are B; rewriting **shared** history is D.

## Why this system exists

Until 2.7.0 this library treated git in only two ways: a **prohibition** ("never force-push", "never rewrite history") and a **publication** prompt that pushes commits. Neither helps at the moment the problem occurs:

- A merge conflict in a 40-file rename — and the agent resolves it by taking "ours" for everything, silently discarding a colleague's work.
- An interactive rebase that drops a commit, and nobody knows it is recoverable because `reflog` is never mentioned.
- A history rewrite that never needed to happen, erasing three colleagues' commits — recoverable only if you act before the objects are garbage-collected, and only if you know the remote also has a reflog.
- A secret committed six months ago, and the team believes deleting it in a new commit removed it.
- A branch strategy argument that gets re-litigated every quarter because no decision was recorded.

Git is the substrate every other prompt in this library operates on. A wrong `reset --hard` destroys more work, faster, than any other single command an agent can run.

## Triage — which stage do you need?

| Situation | Stage | Risk |
|-----------|-------|------|
| Something looks wrong and I am about to run a destructive command | [P01 State check](P01-State/P01-State-Safety-Check.md) — **always first** | A |
| Merge or rebase stopped with conflicts | [P02 Conflicts](P02-Conflicts/P02-Conflict-Resolution.md) | B |
| I need cleaner commits, a squashed branch, or to remove a file from history | [P03 History repair](P03-History/P03-History-Repair.md) | B local / **D shared** |
| Commits, branches, or a stash vanished; a history rewrite went wrong | [P04 Recovery](P04-Recovery/P04-Recovery.md) — **time-critical** | B |
| We keep arguing about branching, merging, or commit conventions | [P05 Hygiene](P05-Hygiene/P05-Hygiene-Collaboration.md) | A |

**If the repository is still broken and you are unsure which stage applies, run P01.** It is read-only and it answers "what state am I actually in", which is the question every other stage depends on.

## The five rules

1. **Never run a destructive git command before P01.** Do not run any of `reset --hard`, `clean -fd`, `checkout -- .`, `branch -D`, a plain force push, or `rebase` until P01 has told you what is at stake — each can discard work that is the only copy.
2. **Uncommitted work is backed up before anything risky** — a stash *and* a patch file *and* a branch, because each can fail independently.
3. **Shared history is other people's work.** Rewriting it requires an explicit decision by the owner, advance notice, and `--force-with-lease`, never `--force`.
4. **A resolved conflict is not a resolved conflict until it builds and the tests pass** — textual resolution is the easy half.
5. **Recovery is time-sensitive.** Reflog entries expire; unreferenced objects are garbage-collected. Act before investigating at leisure.

## Related material

- Publishing commits and opening PRs: `01-contribution/open-source/general-agent/P13-Git-Publication/`.
- Reading history to understand a codebase: `general-agent/P06-Git-History-Conventions/`.
- Secrets in history: `00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md` (this system handles the purge; rotation comes first and is not optional).
- Per-change safety for refactors and releases: `02-engineering/refactoring/` P04, `04-process/release-engineering/` P03.

## What this system will not do

- Rescue work that was never committed anywhere. Git only recovers objects that once existed.
- Recover a secret that has been pushed: purging history removes it from the repository, not from whoever cloned or scraped it.
- Decide your branching model. P05 records and operationalises a decision; it does not impose one.
