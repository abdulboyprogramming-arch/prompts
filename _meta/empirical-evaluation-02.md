# Empirical Evaluation 02 — `CHAT-DEBUG` Conversational Debugging

**Date:** 2026-10-20
**Prompt under test:** `00-core/conversational/CHAT-DEBUG.md` v1.0.0
**Evaluator:** the author of the prompt (conflict of interest stated below)
**Method:** tabletop walkthrough against a constructed fixture — **not** a live user session
**Result:** three real prompt defects found and fixed in v1.1.0

---

## What this evaluation is, and is not

`DBG-01` was executed against a running fixture: the prompt's steps were followed and a defect was genuinely fixed. This evaluation is weaker, and says so.

**What happened:** a fixture was built (a small sync script, an error log, a hidden second connection). A tabletop session was then run against it — the user turns were written by the evaluator, and the prompt's steps were followed as written to see what the prompt would have demanded at each turn.

**What this can show:** whether the prompt's instructions are followable, whether they force a discriminating experiment, and — the point of the exercise — whether they resist a premature conclusion when the pasted code is innocent.

**What this cannot show:** whether a real user would answer the questions, whether a real model follows the steps faithfully, or whether the prompt improves outcomes. A tabletop tests the *instrument*, not the *operator*.

**Conflict of interest:** the evaluator wrote the prompt. A second evaluator would remove it; none was available, which is the same limitation recorded in `empirical-evaluation-01.md`.

---

## The fixture

A nightly job syncs a supplier catalogue into a local `prices` table. The user pastes the sync function and one traceback. Not shown to the model: a module-level audit connection opened earlier in `main()` that performs an `INSERT` and never commits.

```python
def sync(client, db):
    cursor = None
    while True:
        page = fetch_page(client, cursor)          # HTTP call
        for item in page["items"]:
            row = db.execute("SELECT id, price FROM prices WHERE sku = ?", (item["sku"],)).fetchone()
            if row and row[1] == item["price"]:
                continue
            if row:
                db.execute("UPDATE prices SET price = ? WHERE sku = ?", (item["price"], item["sku"]))
            else:
                db.execute("INSERT INTO prices (sku, price) VALUES (?, ?)", (item["sku"], item["price"]))
        cursor = page.get("next_cursor")
        if not cursor:
            break
    db.commit()
    return seen
```

```
File "/srv/app/sync.py", line 33, in sync
    db.commit()
sqlite3.OperationalError: database is locked
```

The point of the fixture: **the visible code contains no defect.** It is inefficient — it holds a write transaction across network calls — but that inefficiency is not what produces this error at `commit()`. The cause is outside the paste. A prompt that hunts for a bug in the pasted lines will find one and be wrong.

---

## Walkthrough against v1.0.0

| Prompt step | What it demanded | What happened in the tabletop |
|---|---|---|
| 1 — defect statement | When / observed / expected / since | Worked. "Nightly sync fails at commit since Tuesday" became precise in one exchange. |
| 2 — read the error | Class, message, deepest own-code frame | Worked, and revealed the limits: the traceback has **one** frame in user code, and the message names a resource, not a cause. |
| 3 — exclusive hypotheses | At most five, each with a discriminator | Produced four: (a) another process holds the write lock; (b) this connection never enabled WAL and a reader blocks the writer; (c) a second connection in-process is uncommitted; (d) the loop holds the transaction so long that contention becomes certain. All four are legitimate and mutually exclusive. |
| 4 — rank by priors | Commonness, recent change, determinism, abruptness | **Gap found.** In SQLite, `database is locked` at `commit()` most often means *another writer or an uncommitted second connection*, not a defect in the code shown. The prompt had no instruction to prioritise "something else holds the resource", so the natural next move was to critique the pasted loop — which is innocent. |
| 5–6 — one experiment, exact command | A single discriminating test | Worked once hypothesis (c) was on the list: `lsof`/`sqlite3` on the file plus a search for `connect(` in the process start-up would have found the second connection. Before (c) existed, the most attractive experiment was "refactor the loop", which changes several variables and proves nothing. |
| 7 — ledger | Confident / reported / eliminated / open / next | **Gap found.** The ledger had no slot for a finding located outside the paste, so the discovery of the second connection would have been recorded as `OPEN` indefinitely. |
| 8 — symptom vs cause | Distinguish mitigation from fix | Worked. Calling `db.commit()` per item would have made the error disappear and multiplied the lock contention — the prompt's framing caught this. |
| 9 — prove by prediction | State implied behaviours | Worked, and was decisive: the second-connection hypothesis predicts the failure stops the moment a report job runs alone, and that no input to `sync` can trigger it. |
| 10 — know when to stop | Escalate after three non-discriminating experiments | **Partial gap.** The stop rule counts experiments, but the relevant stopping condition here is different: the search has moved outside what the user can paste. That is not a count, it is a scope change. |

## Defects found and fixed

| # | Defect | Fix in v1.1.0 |
|---|---|---|
| 1 | No instruction to establish **what else touches the same resource** before theorising about the paste. The prompt inherited the assumption that the bug is in the sent code. | New workflow step 2b: identify other holders of the lock, port, file, pool, or limit, and prefer the hypothesis that explains the failure without requiring a defect in the visible lines. |
| 2 | The ledger could not represent a finding outside the paste, so such a finding stayed `OPEN` and looked unresolved. | Ledger gained `CONTRADICTION:` and `OUT OF SCOPE (needs access):` lines. |
| 3 | No rule for a user claim that conflicts with evidence ("we bumped nothing", while a version differs). | Decision rule: a contradiction is evidence — record both and test the difference rather than accepting the reassuring account. |

Two smaller additions followed from the same session: the failure-handling rule for **the pasted code looks correct** ("this function is fine, and something else holds the lock" is a valid answer), and two completion criteria covering the shared resource and recorded contradictions.

## What the run cost

About forty minutes of construction and walkthrough. The three defects were found in the step where the tabletop diverged from what the prompt would have asked for — steps 4, 7, and 10 — which is the value of running the prompt against a fixture whose answer is known.

## What this does not prove

- **That a real model follows the new step 2b.** It is instruction, not enforcement.
- **That the fixture generalises.** Locks are one shape of "the defect is elsewhere"; a database error is unusually friendly to this lesson because the error message names the resource.
- **That chat debugging works.** The method is sound and the prompt is now better; the outcome in a real conversation remains unmeasured.

## Note for the library

This is the second recorded execution, and the first of a conversational prompt. The evidence registry (`_meta/evidence.json`) records it with the limitation stated: a tabletop by the author. `CHAT-MODE`, `CHAT-REVIEW`, and `CHAT-DESIGN` remain unexecuted — `CHAT-MODE` is the most testable of the three, because two people can run the same chat task and compare outputs.
