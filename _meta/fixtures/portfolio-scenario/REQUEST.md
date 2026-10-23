<!-- not-a-prompt -->

# Portfolio fixture — eleven wants, one product, two people

**Purpose:** a fixed input for running `PORTFOLIO-01` (Feature Portfolio Decision). It exists so the
desirable behaviour is visible in the output: candidates checked against the code before they are
ranked, each restated as a user problem, a non-empty *not now* list, and accounts treated as an
obligation rather than a feature.

**Why this request:** it is the shape of nearly every real one — a product that works, a list of
capabilities somebody wants, no ordering principle, and no statement of what the product is *for*.
The list is copied in spirit from `archive/legacy-txt-files/feature-portfolio-decision.txt`, which is
where this prompt came from.

---

## The user's request

> The app works but it feels thin. I want to add: PWA, sign in with Google or GitHub, a download for
> the analysis (PDF and CSV), dark/light/system theme, i18n, accessibility, and some device-specific
> advanced features. Also notifications when an analysis finishes, and a shareable public link.
> We are two people with about six weeks before we show this to anyone. Add as many as possible.

## The product, as the repository shows it

`app/` is a small Flask application. Its ground truth is deliberately uneven:

| Fact | Where it is visible |
|---|---|
| **Dark mode half exists** — CSS variables and a `data-theme` attribute are defined | `app/static/theme.css` |
| **A theme selector exists in the settings page** | `app/templates/settings.html` |
| **The preference is saved** to a cookie — and **read by nothing** | `app/routes/settings.py`; no template references the cookie |
| **CSV export exists for one report type only**; PDF is named in a comment as unstarted | `app/routes/export.py` |
| **There are no accounts at all** — reports are reached by an unguessable token in the URL | no user, session, or login code anywhere |
| **Accessibility defects**: an input with no label, a table with no header scope | `app/templates/report.html` |
| **No manifest, no service worker** | `app/static/` |
| **No i18n**: English strings inline, dates hardcoded `%d/%m/%Y` | `app/templates/report.html` |
| **No notifications and no shareable link** beyond the existing token URL | `app/routes/` |

## What a passing portfolio must contain

| # | Requirement | Why this request forces it |
|---|---|---|
| 1 | **Dark mode is reported as half-built**, with the missing step named (nothing reads the cookie) | proposing to build it from scratch wastes the work already done |
| 2 | **Export is scoped as finishing an existing route**, naming which report types are missing | the request says "a download"; one already exists |
| 3 | **Sign-in is recorded as having nothing to hold yet**, and as a data obligation rather than a feature | there is no per-user state; adding accounts changes the product's risk class |
| 4 | **Every candidate is restated as a user problem**, not a technology noun | "PWA" and "i18n" are not problems |
| 5 | **The *not now* list is non-empty, with a reason per item** | a portfolio that keeps everything is a list |
| 6 | **At most three items in *Now*, and *Next* sequenced behind its dependency** | two people, six weeks |
| 7 | **The accounts/analytics-data risk is named explicitly**: what is stored, where, for how long, who can read it, how it is deleted | the product analyses uploaded data; accounts would attach it to a person |
| 8 | **One item delivered end to end**: change, test, rollback, and the sentence a user would notice | the point of ranking is to finish something |

## Grading

`PASS` requires all eight. `FAIL` on any of: dark mode or export proposed as new work without checking
the tree; sign-in placed in *Now* without a data-obligation paragraph; a candidate left as a noun (no
user problem); an empty *not now*; more than three *Now* items; or no end-to-end slice.

**Grading source:** the table above is checked against the files under `app/`, not against memory. The
counts below were produced by reading the fixture:

```
$ grep -rl "data-theme" app/               -> app/static/theme.css
$ grep -rl "theme" app/routes/             -> app/routes/settings.py
$ grep -rl "cookie" app/templates/         -> (none)
$ grep -rli "login|password|session[" app/ -> (none)
$ grep -rn "PDF" app/                      -> app/routes/export.py:3 (a comment: not started)
```

The first line is the defect in one command: the custom property exists, the selector exists, and
**no template ever reads the cookie**, so choosing "Dark" saves a preference that changes nothing.
