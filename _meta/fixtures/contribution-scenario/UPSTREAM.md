<!-- not-a-prompt -->

# Contribution fixture — a synthetic upstream with five planted traps

**Purpose:** a fixed upstream for running `INT-P02` (Contribution Intake). The files below are the
upstream's rules, written out so that every trap is discoverable by reading and every finding can be
graded against this text rather than against an opinion.

**Why synthetic:** a real project's rules change, and a real project would have to be interrogated
over the network on every run. The fixture is the same technique used for `ml-churn`
([`../ml-churn/`](../ml-churn/)): plant known defects, then measure whether the procedure finds them.

---

## The upstream: `acme/ledgerkit`

A GPL-3.0 accounting library. The relevant files, quoted in full.

### `CONTRIBUTING.md` (excerpt)

> **Before you write code, open an issue.** Every pull request must reference an issue that a
> maintainer has labelled `accepted`. We close PRs without `accepted` issues without review — not
> because the work is bad, but because we cannot review work we did not ask for.
>
> **Sign-off is mandatory.** Every commit needs `Signed-off-by:` matching the author (the DCO, not a
> CLA). If your employer owns your work, get written permission first; we cannot accept a sign-off
> you are not entitled to give.
>
> **Scope.** `ledgerkit` is a library, not a framework. We do not accept new runtime dependencies.
> A change that adds one is closed with a pointer to the plugins repository.
>
> **Tests.** `make check` runs the full suite (unit, property-based, and a Postgres integration pass
> in Docker). PRs that do not run `make check` locally are usually red in CI for formatting alone.
>
> **Formatting.** `gofmt` and `goimports` are enforced by CI. LF endings only; a CRLF diff is rejected
> automatically.

### `LICENSE` (first line)

> GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

### `.github/ISSUE_TEMPLATE/bug.md`

> Before filing: search existing issues. Reproductions without the `make check` output for the failing
> case are closed.

### Recent commits on `main`

> `fix(ledger): reject negative reversals  Signed-off-by: A. Maintainer <a@acme.example>`
> `docs: clarify rounding  Signed-off-by: B. Maintainer <b@acme.example>`

---

## The user's request (what `INT-P02` receives)

> I want to contribute to `acme/ledgerkit`. I'm going to add `decimal.js` as a dependency so rounding
> works in the browser build, and I'll send it as one PR with the tests. I don't have an issue open —
> figured the PR speaks for itself. My employer pays me to write code, so I'll sign off under my work
> email. Fork is set up, I'll run `npm test` before I push.

## The five planted traps

| # | Trap | What the intake must notice |
|---|---|---|
| 1 | **No `accepted` issue** | the project closes unreviewed PRs without one; the change is unwelcome before it is hard |
| 2 | **Adding a runtime dependency** | explicitly refused by `CONTRIBUTING.md`; the correct destination is the plugins repository |
| 3 | **Sign-off under an employer email** | the DCO requires the signer be entitled to give it — an authority question, not a formatting one |
| 4 | **`npm test`** | the suite is `make check` (Go, plus a Docker Postgres pass); the stated command would validate nothing |
| 5 | **GPL-3.0 upstream** | a GPL library constrains downstream distribution; whether the contributor's use is compatible is a question for their employer, and it must be raised rather than assumed |

## Grading

`PASS` requires all five, plus:

- the licence position stated (compatible / incompatible / unknown for the contributor's case), not
  omitted;
- the test command corrected with a source;
- at least one candidate task that the project *does* want, or an explicit statement that this one is
  not welcome — not a rewrite of the refused task into a vague "improve documentation" suggestion.

`FAIL` on: any trap missed, any rule asserted without a source, or a brief that recommends proceeding
with the refused change.
