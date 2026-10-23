<!-- not-a-prompt -->

# Rewrite 04 — "add many more features… as many as possible"

**Source:** [`../process7(chat2).txt`](../process7%28chat2%29.txt) — 1 paragraph plus a copy-paste marker
**Status:** archive rewrite. **This is the most important rewrite in the folder**, because the original
instructs the exact behaviour the current library forbids.
**Closest library prompts:** `02-engineering/feature-design-suggestion/` (a system, still skeleton) and
`04-process/project-management/P02-Goals/P02-Goals-Success-Criteria.md` for the goal and non-goal frame.

---

## 1. The original, verbatim

> Add many more features and improvements....as man as possible adding all possible features and
> implementations for this kind of this software that ever exist in the world. Add PWA, ability for user
> to create account or sign in with google or github, download analysis or report, white/dark/system
> default mode, i18n, a11y, device-specific advanced or improved unique features, ...etc.
>
> [ PROMPT FROM PROCESS 5]

## 2. What it was trying to say

*"This product feels thin. I want it to be competitive — to have the things users expect: it installs
like an app, people can sign in with an account they already have, they can take their results out,
it respects their theme and their language and their accessibility needs. Tell me which of these to do
and in what order, and make the product feel finished rather than demo-shaped."*

That is a legitimate and common instinct. The problem is not the ambition; it is that the instruction
**cannot be executed, cannot be finished, and cannot be judged** — and following it would damage the
product.

## 3. Why the original fails as a prompt

| Defect | What actually happens |
|---|---|
| **"as many as possible… all possible features… that ever exist in the world"** | no stopping condition, so the run never converges: the agent keeps generating features, and the product grows while its quality per feature falls |
| **eleven capabilities in one sentence, unranked** | they have wildly different cost and risk. Sign-in adds a user table, a session, a reset flow, a password policy and a privacy obligation. Dark mode is a CSS variable. Treating them as one request guarantees the expensive ones are half-done |
| **no reason attached to any of them** | "PWA" is a platform, not a user problem. Without the problem, the cheapest correct answer might be "no" — and the prompt has made "no" unreachable |
| **the list ends in "…etc."** | the scope is explicitly open-ended. There is no state of the world in which this ask is complete |
| **no state of the product first** | nothing says what exists, so the agent cannot tell a missing capability from an existing one |
| **it contradicts this repository's own rules** | `../README.md` says these files "instruct agents in ways the current library forbids (unbounded autonomy, *add every possible feature*)". This is that sentence |

The specific danger is **accounts and sign-in**. Of the eleven items, that one introduces personal data,
a credential store, a reset flow, and a legal obligation. It is the item most likely to be implemented
first (it sounds foundational) and worst to implement badly.

## 4. The rewritten prompt

> **Role.** You are deciding what this product should build next — and, just as importantly, what it
> should not. Every item on the list below is a candidate, not a commitment. Your output is a ranked
> **portfolio** with a reason per row and an explicit *not now* list.
>
> **Inputs.** `{{REPO_PATH}}`, `{{PRODUCT_GOAL}}` — what the product is for and who uses it,
> `{{CONSTRAINT}}` — team size and the next date that matters, and `{{CANDIDATES}}` — the list the user
> gave. If `{{PRODUCT_GOAL}}` is missing, ask for it; a feature list without a goal has no ordering
> principle and will be sorted by effort instead, which is the wrong sort.
>
> **Step 1 — establish what exists.** For each candidate, find whether some version of it is already
> present (a partial theme toggle, a settings page, a half-built auth route). Report the evidence.
> **Never propose building something the repository already does** — that is the most common waste in
> this kind of request.
>
> **Step 2 — restate each candidate as a user problem.** Not "PWA" but *"a returning user on a phone
> browser cannot get back to their saved work without re-typing a URL"*. A candidate that cannot be
> restated as a problem is either a platform decision or a preference; label it as one and move on.
>
> **Step 3 — score each on four axes, and show the scores.** *User value* (how many users, how often),
> *cost* (days of work, and whether it needs new infrastructure), *risk* (what it can break, and whether
> it adds a security or privacy obligation), *reversibility* (how hard it is to undo). Two sentences of
> justification per row, no more.
>
> **Step 4 — the three buckets.** **Now** (high value, low risk, reversible) — at most three items.
> **Next** (valuable but expensive, or dependent on *Now*) — sequenced behind its dependency.
> **Not now** — with the reason: *"no user has asked for it"*, *"the product has no accounts, so sign-in
> has nothing to hold"*, *"it is a platform, and there is no problem it solves yet"*.
>
> **Step 5 — name the trap.** If any candidate adds **accounts, personal data, or a payment**, say so
> explicitly and treat it as a separate decision with its own risk class: what will be stored, where,
> for how long, who can read it, and what the deletion path is. This is not a feature; it is an
> obligation with a UI. **Do not fold it into a batch of "improvements".**
>
> **Step 6 — the first slice, end to end.** One item from *Now*, taken all the way: the change, the
> test, the rollback, and the one sentence a user would notice. A finished small thing beats six
> half-finished ones, and the portfolio exists to make that choice visible.
>
> **Failure handling.** No stated product goal → produce the problem statements only, and stop; ranking
> without a goal is arbitrary. All candidates expensive → rank by reversibility and propose the cheapest
> reversible one. A candidate the user insists on that the analysis ranks last → implement it, but put
> the cost and the risk in the record first, so the decision is theirs and is written down.
>
> **Done when:** every candidate has a bucket and a reason, the *not now* list is non-empty, any
> data-collecting item has its own risk paragraph, and one item is delivered end to end.

### The specific list, decided rather than repeated

| Candidate | The user's framing | What it actually is | Where it usually belongs |
|---|---|---|---|
| PWA | "add PWA" | a delivery mechanism; useful only if returning users exist | *Next*, after the product has returning users |
| Sign-in with Google/GitHub | "ability to sign in" | personal data + a credential dependency + a deletion obligation | **its own decision**, and *not now* until there is per-user state worth protecting |
| Download analysis/report | "download analysis" | the cheapest real value on the list — it makes existing work portable | **Now** |
| Dark/light/system | "default mode" | a preference; small, reversible, user-visible | **Now** |
| i18n | "i18n" | doubles the text surface and adds a translation owner forever | *Next*, and only for languages users actually ask for |
| a11y | "a11y" | not a feature — a floor. If it is missing, it is a defect | **Now**, as a defect, not a feature |
| "device-specific advanced features" | "unique features" | an invitation to build something no one asked for | *Not now*, until a device-specific problem is named |

That table is the answer to the original request. The user asked for all of them; the useful response
is that **two are worth doing this month, one is a defect rather than a feature, one is a legal
obligation in disguise, and four are speculation.**

## 5. Does the library cover this now?

**Partly — and this is a real gap.** The frame exists (`04-process/project-management/P02-Goals` for
goals and non-goals; `05-scenarios/feature-sunset/` for the opposite decision), and `HACK-01` forces
scope cuts in writing. What does not exist is a prompt for **deciding between candidate features**:
`02-engineering/feature-design-suggestion/` designs a feature once it has been chosen, and its seven
stages are still skeletons.

Recorded honestly: the rewrite above is the best available statement of the decision, and promoting it
into `02-engineering/feature-design-suggestion/` as a "portfolio" stage would need its own evidence, not
just this text.
