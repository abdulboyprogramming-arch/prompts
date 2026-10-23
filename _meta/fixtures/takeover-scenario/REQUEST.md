<!-- not-a-prompt -->

# Takeover fixture — an app someone built with an AI, handed to a person who codes by hand

**Purpose:** a fixed input for running `ONBOARD-01` (Codebase Onboarding). It exists so the desirable
behaviour is visible in the output: the system reconstructed from the code rather than from a story, the
traps found and named, the run instructions verified by running them, and a verdict about whether the
receiver can continue without asking anyone.

**Why this fixture:** the commonest handover in 2026 is not agency-to-client. It is a founder, analyst,
or designer who built a working product with an AI assistant, has no mental model of the code, cannot
answer questions about it, and is handing it to a developer who works by hand. The sender is present and
willing — and has no idea what is in the repository.

**The sender's message, verbatim:**

> This is my app. I built it with Claude over about three weeks. It runs on my laptop and I have
> deployed it once but I don't remember how. There are some notes in docs/. I want you to take it over
> and keep going — I can't answer technical questions, I just described what I wanted and it built it.
> I need to know it's safe for a real developer to continue.

## The repository

`app/` — six Python files, a schema, a Dockerfile, no tests, no README. Its ground truth is deliberately
uneven; each fact below is checked by the command beside it.

| # | Fact | Command that shows it |
|---|---|---|
| 1 | The entry point is `python -m app.main` from the repository root, and it **requires** `APP_ENV` and `DATABASE_URL` — without them it exits with a message | `grep -n "APP_ENV\|DATABASE_URL" app/config.py` |
| 2 | A **hardcoded payment key placeholder** sits in `config.py` | `grep -n "PAYMENTS_KEY" app/config.py` |
| 3 | `schema.sql` creates `reports` **without** `user_id`; `models.py` has `user_id` — the report query cannot work against a fresh database | `grep -n "user_id" app/schema.sql app/models.py` |
| 4 | The **Dockerfile cannot run** the app: `CMD python app/main.py` breaks the package-relative imports | `grep -n "CMD" app/Dockerfile` |
| 5 | `requests` is declared and **never imported**; `psycopg2` is declared and used | `grep -rn "import requests" app/ ; grep -n "requirements" -A5 app/requirements.txt` |
| 6 | **No tests exist** | `find . -name "test*" -o -name "*_test.py"` |
| 7 | User **email addresses are stored** in `users`, so the app holds personal data | `grep -n "email" app/models.py app/schema.sql` |
| 8 | **AI authorship is visible** in the code: `_fmt_date` is duplicated in two modules with different formats, and a commented-out second implementation of `export` sits beside the live one | `grep -rn "_fmt_date\|# def export" app/` |
| 9 | The builder's notes are scraps, not documentation | `cat docs/notes.txt` |

## What a passing onboarding must contain

| # | Requirement | Why this repository forces it |
|---|---|---|
| 1 | **Start-up instructions that work from a clean checkout**, with the two required variables named | the app exits without them and nothing says so |
| 2 | **The hardcoded key reported as a finding**, not as a config line | a placeholder in a repo that has been public is one commit away from a real one |
| 3 | **The schema/model mismatch identified as a defect**, with the failing query named | it is the reason the app "sometimes doesn't show reports" |
| 4 | **The Dockerfile defect identified**, with what breaks and why | "it deployed once" and cannot do it again |
| 5 | **The absence of tests stated, with the three riskiest untested paths named** | upload, export, payment webhook |
| 6 | **A data-flow map saying where personal data enters and where it lands** | email addresses in `users` |
| 7 | **An authorship section**: what the code says about how it was built, and which patterns are AI-shaped (duplication, two implementations, dead dependency) | the receiver has to decide what to keep |
| 8 | **A first safe change with a rollback, actually performed or explicitly rehearsed** | "safe to continue" is a claim that needs a test |
| 9 | **A verdict** — continue, continue with conditions, or stop — tied to the evidence above | the sender asked exactly this question |

## Grading

`PASS` requires all nine. `FAIL` on any of: no runnable start instructions; the key, the schema mismatch or
the Dockerfile defect missed; tests claimed rather than their absence noted; no data-flow map; no
authorship section; no first change; or a verdict without conditions.

**Grading source:** the commands above are the grading, and the receiver is expected to run them. Each
one was run against the fixture when it was written, and its output is what the table says — the trap in
this fixture is that `grep user_id app/schema.sql` prints **nothing**, and an absence is the easiest
thing for a reader to skim past.
