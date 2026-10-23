# Feature Portfolio Decision

**Identifier:** PORTFOLIO-01
**System:** 02-engineering/feature-portfolio
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — analysis and a written decision; nothing in the repository is changed
**Depends on:** none (`FD-P01` in `02-engineering/feature-design-suggestion/` takes the chosen item as its context; `04-process/project-management/P02-Goals` produces the goal this prompt needs if none exists)
**Produces:** `PORTFOLIO.md` — a scored table, three buckets, and a *not now* register
**Inputs:** REPO_PATH, PRODUCT_GOAL, CANDIDATES, CONSTRAINT (optional: DATA_CLASS)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are deciding what this product builds next — and, just as importantly, what it does not. Every item
on the candidate list is a candidate, not a commitment. Your output is a ranked portfolio with a reason
per row and an explicit *not now* list that someone can defend in six months.

The failure this prevents is the one every product has: a list of wanted capabilities arrives, it is
sorted by effort or by whoever asked loudest, everything is kept, and nothing is finished. The list is
not the problem. The absence of an ordering principle is.

## 2. Objective and scope

**Produce:** `PORTFOLIO.md` containing, in this order — what already exists, a user problem per
candidate, a four-axis score per candidate, three buckets (*Now*, *Next*, *Not now*), an obligations
paragraph for anything that stores data or moves money, and one slice carried to done.

**Out of scope:** designing the chosen feature (`FD-P01` does that), estimating in story points, and
any ranking that requires information you were not given — a missing goal stops this prompt, it does
not get guessed at.

## 3. Prerequisites and inputs

| Input | Required | What it is |
|---|---|---|
| `{{REPO_PATH}}` | yes | the repository, so "we already have that" is checked rather than assumed |
| `{{PRODUCT_GOAL}}` | yes | what the product is for and who uses it. **If absent, stop after step 1 and ask.** A feature list without a goal has no ordering principle, and will be sorted by effort, which is the wrong sort |
| `{{CANDIDATES}}` | yes | the list, in the words of whoever asked for it. Do not tidy it before step 2 — the nouns are evidence of what is actually wanted |
| `{{CONSTRAINT}}` | yes | team size, and the next date that matters. Capacity is what makes *Now* three items and not eleven: "two people, six weeks" is a constraint; "soon" is not |
| `{{DATA_CLASS}}` | optional | what the product already stores about people, if anything. Without it, step 6 has to establish it from the schema |

## 4. Workflow

1. **Establish what exists, per candidate, with evidence.** For each item, find whether some version of
   it is already present: a half-wired settings control, a route that returns one of the two formats
   asked for, a table that already has the column. Cite the file. **Never propose building something
   the repository already does** — it is the most common waste in this kind of request, and the only
   defence is reading the tree.

2. **Restate each candidate as a user problem.** Not "PWA" but *"a returning user on a phone browser
   cannot get back to their saved work without re-typing a URL"*. A candidate that cannot be restated
   as a problem is either a platform decision or a preference; label it as one and move on. Keep the
   user's original noun beside your restatement, so the translation is visible and arguable.

3. **Score each on four axes, and show the scores.** *User value* (how many users, how often); *cost*
   (days of work, and whether it needs new infrastructure); *risk* (what it can break, and whether it
   adds a security or privacy obligation); *reversibility* (how hard it is to undo). Two sentences of
   justification per row, no more. A score without a justification is an opinion with a number on it.

4. **Sort into three buckets, and make *Not now* non-empty.**
   - **Now** — high value, low risk, reversible. **At most three items**, and the limit is not
     negotiable: a *Now* of eleven is the list you started with.
   - **Next** — valuable but expensive, or dependent on a *Now* item. Each row names **what it is
     waiting for**.
   - **Not now** — with a reason from this set: *no user has asked for it*; *the product has no
     accounts, so sign-in has nothing to hold*; *it is a platform decision with no problem behind it*;
     *the obligation it creates is larger than the value*.

5. **Name the trap.** If any candidate adds **accounts, personal data, or a payment**, say so explicitly
   and treat it as a separate decision with its own risk class: **what will be stored, where, for how
   long, who can read it, and what the deletion path is.** That is not a feature; it is an obligation
   with a UI. Do not fold it into a batch of "improvements", and do not let it into *Now* on the
   strength of being wanted.

6. **Check the claim against the code before you write the sentence.** If you say "there is no
   authentication", show the search that returns nothing. If you say "export is half-built", name the
   route and the format that is missing. A portfolio's credibility is its citations; one invented fact
   discredits every other row.

7. **Deliver the first slice end to end.** One item from *Now*, taken all the way: the change, the test
   that would fail without it, the rollback, and the one sentence a user would notice. A finished small
   thing beats six half-finished ones, and the portfolio exists to make that choice visible.

8. **Write `PORTFOLIO.md`** with the sections in §2, and hand the chosen item to `FD-P01`.

## 5. Decision rules and evidence standard

- **The repository decides what is new work.** A candidate that exists in part is scoped down, not
  rebuilt.
- **A candidate is a hypothesis about a problem.** If the problem cannot be stated, the candidate is a
  preference — say so, and rank it as one.
- **Capacity is an input, not a discovery.** Three *Now* items for a two-person team with six weeks is
  a decision; eleven is a wish list.
- **Risk is about the obligation, not the code.** Accounts, personal data, and payments change what the
  product owes people.
- **Every "we do not have X" is a search result**, quoted.
- **A *Not now* without a reason is a *Later*, and *Later* is how lists stay lists.**

## 6. Verification

| Check | Method | Pass condition |
|---|---|---|
| Every candidate accounted for | Compare table to `{{CANDIDATES}}` | One row per candidate, none dropped |
| Existing work found | File citations per candidate | Each "already exists" claim names a file |
| Problem restatements | Read the second column | No row is a bare technology noun |
| Scores justified | Read the rows | Two sentences per row; four axes present |
| *Now* is small | Count | Three items or fewer |
| *Next* has dependencies | Read the rows | Each names what it waits for |
| *Not now* has reasons | Count and read | Non-empty; every row has a reason from §4.4 |
| Obligations named | Search the output | Stored data, location, retention, readers, deletion path all present if any candidate touches data |
| Slice is real | Read the last section | Change, test, rollback, user-visible sentence |

## 7. Failure handling

- **`{{PRODUCT_GOAL}}` missing or contested** → produce the problem statements only, and stop. Ranking
  without a goal is arbitrary, and an invented goal is worse.
- **Every candidate is expensive** → rank by reversibility and propose the cheapest reversible one.
  Shipping something undoable beats waiting for something perfect.
- **The user insists on an item the analysis ranks last** → build it, but write the cost and the risk
  into the portfolio first, so the decision is theirs and is on the record.
- **Two candidates are the same thing** (a shareable link and a public URL) → merge them and say so;
  a list that counts one idea twice ranks it twice.
- **The repository contradicts the request** (the feature exists, or the product cannot support it) →
  the repository wins; report the contradiction as the finding.

## 8. Security and authorisation

Risk class A: read-only analysis. Reading a repository may expose secrets in configuration — record
their location, never their values. If the candidate list implies collecting personal data, the
obligations paragraph is mandatory, not optional, and it must name the deletion path: a product that
cannot delete what it stores has not decided to store it, it has deferred the decision.

## 9. Completion criteria

- [ ] Every candidate has a row, a user problem, four scores with justification, and a bucket.
- [ ] *Not now* is non-empty and every reason comes from §4.4.
- [ ] *Now* holds three items or fewer.
- [ ] Every "already exists" / "does not exist" claim cites a file or a search.
- [ ] Any data-storing candidate has the five-part obligations paragraph.
- [ ] One slice is specified with change, test, rollback, and user-visible outcome.
- [ ] `PORTFOLIO.md` is written and the chosen item is named for `FD-P01`.

## 10. Handoff

The single *Now* item goes to `02-engineering/feature-design-suggestion/` (`FD-P01`) with the problem
statement from step 2 as its input. The *Not now* register is kept: it is the answer the next time the
same list arrives, and the reason it will not have to be re-argued.

## 11. Testing and known limitations

- **Executed** against the fixture in `_meta/fixtures/portfolio-scenario/` (eleven wants, two people,
  a repository with a half-wired theme control and a single-format export route). Record:
  `_meta/empirical-evaluation-20.md`. v0.1.0 scored 0 of 8; this version scored 8 of 8 on the same
  fixture.
- **Author-run.** One desk execution by the author, no second reader. The fixture's ground truth is
  checked by command against the files, but the score is a judgement.
- **Not tested:** a genuine multi-stakeholder argument, and a product with real accounts. The
  obligations paragraph is designed for that case and has not been exercised against it.
