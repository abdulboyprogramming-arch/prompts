# Empirical evaluation 10 — `git-operations` stage 1 and 2 executed as a system

**Prompts:** `GIT-P01` (`04-process/git-operations/P01-State/P01-Repository-State.md`, v1.0.0) and `GIT-P02` (`.../P02-Conflicts/P02-Conflict-Resolution.md`, v1.0.0)
**Date:** 2026-10-22 · **Method:** **real execution** on a purpose-built git fixture. Both stages ran in order, P02 consuming P01's artifact, exactly as the system declares.
**Evaluator:** the prompt's author. Conflict of interest recorded.

---

## 1. Fixture

`/tmp/gitops`, a Python project with one test, built before either run:

- `main` at `8842265`: renamed `send()` → `deliver()`.
- `feature` at `54f9827`, one commit that exists nowhere else: added `RETRY_BACKOFF`, raised `RETRY_LIMIT` to 5, and added a `certifi` line to the lockfile.
- one untracked file (`note.txt`), no remote, no upstreams, no in-progress operation.

The two intents are deliberately orthogonal (a rename and a capability), so a resolution that drops either is detectable by grep and by the test suite.

## 2. GIT-P01 — state and safety check

Artifact written: `.git-ops/STATE.md`, with branch/SHA, the untracked file, the **one commit that exists nowhere else**, absence of any in-progress operation, zero stashes, recorded SHAs, and the recommendation `proceed only after backup`.

Assertions, each a command run after the fact:

| Assertion | Result |
|---|---|
| Artifact exists | **pass** |
| In-progress operation correctly reported as none | **pass** — all six markers absent, verified independently |
| Unpushed commit identified | **pass** — `54f9827`, 1 commit, no upstream |
| Backup branch created and recorded | **pass** — `backup/main-20261022T…` → `8842265` |
| Recommendation matches the state | **pass** — `proceed only after backup` was the right call: losing `feature`'s commit would have been unrecoverable |

**Findings.**

| # | Severity | Finding |
|---|---|---|
| 1 | **Medium** | Step 8 offers `git stash create` as a snapshot for uncommitted work. That command returns a commit SHA **without storing it in the stash list**, so the object is unreachable from any ref and is garbage-collected after the expiry window. The prompt asks the operator to record "where the artifacts live", and for this option there is nowhere to look. A snapshot that silently disappears is worse than none, because it is relied on. |
| 2 | **Low** | Step 2 asks the operator to categorise "ignored-but-important files" and gives no test for importance. The run had one untracked text file and had to judge; another evaluator would have judged differently. |
| 3 | **Low** | Neither stage says where `.git-ops/` lives in the repository — committed, ignored, or local only. P02 consumes P01's artifact by path, so a user who commits it will have merge conflicts in it; a user who ignores it will lose it between machines. |

## 3. GIT-P02 — conflict resolution

Operation: `git merge feature` into `main` → `UU app/client.py`, auto-merges in `app/config.py` and `requirements.lock`.

The three-way read (`git diff :1: :2:`, `:1: :3:`) established the two intents in one sentence each, and the resolution composed them: `def deliver(url)` returning both `attempts` and `backoff`. Nothing was dropped.

| Assertion | Result |
|---|---|
| Conflict markers gone | **pass** — `grep -c "^<<<<<<<"` → 0 |
| Main's intent preserved (rename) | **pass** — `grep -rn "send(" app tests` → none |
| Feature's intent preserved (limit 5, backoff) | **pass** — config merged to `RETRY_LIMIT = 5`, `RETRY_BACKOFF = 2`; response includes `backoff` |
| Tests run, not described | **pass** — `python3 -m unittest discover -s tests` → `OK` |
| History not rewritten | **pass** — `feature` still at `54f9827`; merge commit `5bb9fa2` |
| Direction of "ours" stated | **pass** — recorded as main, in the artifact's first line |
| Generated file regenerated | **fail, and recorded as unverified** — no package manager in the fixture |

**Findings.**

| # | Severity | Finding |
|---|---|---|
| 1 | **High** | Step 5 requires lockfiles and generated files to be **regenerated, never hand-merged**, and the rule is unreachable in the case that actually happens: `requirements.lock` was **auto-merged by git with no conflict marker at all**, so step 2 (which keys on conflict type) never flagged it and step 5 never fired. The operator has to know to look. A lockfile merged by a text algorithm installs something neither branch intended, and nothing in the prompt says to check files that merged cleanly. |
| 2 | **Low** | The artifact's closing section ("needs the other author's confirmation") is optional in practice; the run produced it, and the fixture had no other author, so this was untested rather than passed. |
| 3 | **Low** | Step 7 requires `git merge --abort` to be shown to return to "the recorded pre-operation state — confirm the SHA matches P01's record", and P01's record is a path that may not be committed (finding 3 above). The two stages depend on each other for a fact neither pins down. |

## 4. Changes made

Both prompts to v1.1.0:

- **GIT-P01** step 8: `git stash create` replaced by `git stash push -m "pre-<operation>"` (stored and listed) or `git stash store` with the returned SHA; the artifact must record the stash ref, not just the SHA. Step 9 gains the location rule: `.git-ops/` is **local working state, added to `.git/info/exclude`, never committed**.
- **GIT-P02** step 2 gains a fifth column for **files changed by both sides that merged without conflict**, which must be checked against the generated-file list before the merge is committed; step 5 becomes: regenerate any generated file that either side touched, conflicted or not, or record it as unverified with the reason.
- **GIT-P02** §3 inherits the `.git-ops/` location rule so P01's artifact is findable by a second machine.

## 5. Retest

The lockfile rule was retested on the same fixture by re-creating the merge: with the revised step 2, the auto-merged lockfile appears in the checklist before `git commit`, and the run flags it (`regenerate or record unverified`). The stash fix was checked by running `git stash push -m "pre-test"` on a dirty tree and confirming `git stash list` shows the entry — the previous instruction's alternative would not have. The `.git-ops/` location rule was verified by adding it to `.git/info/exclude` and confirming `git status` no longer reports it.

## 6. What this run establishes, and what it does not

**Establishes:** the two stages compose — P02 read P01's artifact and the `.git-ops/` handoff worked; the conflict resolution procedure produced a result that preserved both intents and passed the test; two real defects were found, one of which (auto-merged generated files) will cause a wrong install in a real repository.

**Does not establish:** anything about a human using these prompts, a conflict in a language with no tests, a rebase (only a merge was run, and the direction rule matters most in a rebase), a semantic conflict that git cannot see and grep cannot find, or the system as a whole — stages 3, 4 and 5 were not executed. **This is two stages of a five-stage system, not an end-to-end system run**, and the release criteria record it as partial.

## 7. Limitations

- The fixture is synthetic, single-author (so no "reach the other author" path), single-language, and 5 files. A real repository would exercise file types the table lists and this run did not.
- No package manager, so the one instruction that failed could not be tested in its repaired form against a real lockfile.
- Agent-executed, agent-graded, author-written, in one context. The same limitation as the rest of batch 0 and B2's first entry.
