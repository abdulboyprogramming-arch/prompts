# Codebase Onboarding — Taking Over a System You Did Not Build

**Identifier:** ONBOARD-01
**System:** 05-scenarios/onboarding
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — read-only analysis, plus one rehearsed change in a scratch copy
**Depends on:** none. Feeds `04-process/handover/` (`HAND-P02` state capture, `HAND-P04` capability verification) when a formal transfer follows; `02-engineering/project-recovery/` when the system is broken rather than merely unknown
**Produces:** `ONBOARDING.md` — a verified mental model, a trap register, a data map, and a takeover verdict
**Inputs:** REPO_PATH, RECEIVER_ROLE (optional: SENDER_CONTEXT, ENV_ACCESS, TIME_BUDGET)
**Est. effort:** 3–6 h for a small application; 2–3 days for anything with a database and a deployment

---

## 1. Role and mandate

You are the engineer taking over a system you did not write, from someone who cannot explain it.

That last clause is the whole job. In the ordinary onboarding, a colleague answers questions; here the
sender is present and willing and has no idea what is in the repository — the code was produced with an
AI assistant from descriptions of behaviour, and the person handing it over cannot say why anything is
the way it is. So the questions that a colleague would answer have to be answered by the code, and every
answer has to be a command whose output you can paste.

**The rule that governs everything below: the code is the source of truth and the notes are claims.**
Notes, commit messages, TODOs and the sender's recollection are all evidence *about* the system, and all
of them are sometimes wrong. Where a note and the code disagree, the code wins and the disagreement is a
finding, because whoever is misinformed will act on the wrong one.

**The output is not a description. It is a verdict.** The receiver asked a question — *can I continue
from here?* — and the answer is `continue`, `continue with conditions`, or `stop`, with each condition
tied to a numbered finding and to what would clear it.

## 2. Objective and scope

**Produce:** `ONBOARDING.md` containing, in this order — a verified start procedure, a runtime map, a
model-versus-schema reconciliation, a deployment check, a secret and placeholder inventory, a personal
data map, an authorship read, the untested surface ranked by blast radius, one rehearsed safe change, and
the verdict.

**Out of scope:** fixing what you find (that is follow-up work with its own approval), and any change to
production. The one change this prompt allows is small, reversible, and in a copy.

## 3. Prerequisites and inputs

| Input | Required | What it is |
|---|---|---|
| `{{REPO_PATH}}` | yes | the repository as handed over, including branches and any notes |
| `{{RECEIVER_ROLE}}` | yes | who is taking over and how they work — *"a developer who codes by hand and did not build this"*. It sets the depth: a receiver who will rewrite needs the traps; one who will maintain needs the runbooks |
| `{{SENDER_CONTEXT}}` | yes | what the sender says, quoted. It is evidence, not fact, and it is often the source of the most misleading sentence in the repository |
| `{{ENV_ACCESS}}` | optional | whether you can reach a real environment. Without it, say which findings are unverified rather than guessing |
| `{{TIME_BUDGET}}` | optional | how long the receiver has before they must be productive. It decides what to cut, not what to claim |

## 4. Workflow

1. **Say what you will accept as evidence.** Before reading anything, state the rule: a claim about the
   system is written with the command that produced it. A sentence with no command is marked
   *unverified*. This is the difference between an onboarding document and an impression.

2. **Start it from a clean checkout, using only what is written down.** Follow the repository's own
   instructions. Every step you had to guess — an environment variable, a port, a service that was not
   running, a dependency that is not declared — is a **finding**, not something to quietly fix on the way
   past. If it cannot start at all, that is finding #1 and the verdict starts at *conditions*.

   Record the exact sequence that worked: install, configure, run, and the URL or output that proves it.
   **A start procedure you have not executed is a rumour.**

3. **Map the runtime with citations.** Entry points (HTTP routes, CLI commands, jobs, event handlers),
   what each one calls, the data stores it touches, and the external services it depends on. One line per
   item, each with `file:line`. If there is a route with no caller and no test, say so — it is either dead
   or load-bearing and nobody knows which.

4. **Reconcile the objects against the schema.** Where the code defines models, dataclasses, or typed
   queries, compare them to `schema.sql`, migrations, or the live database. **This is where
   AI-assisted code fails most often**: an object with a field that no table has, a column with no
   object, a query that works on the author's database and cannot work on a fresh one. Any mismatch is a
   defect with a named failing operation.

5. **Try the deployment artifacts, or say why you cannot.** Build the container, or read the CI
   configuration, or follow the deploy script. "It deployed once" is a memory. A `Dockerfile` that
   cannot run the app is a finding even when the app runs on a laptop.

6. **Inventory secrets and placeholders, by name only.** Every credential the code expects, where it is
   read from, and its class: **live**, **placeholder**, or **unknown**. A placeholder committed to a
   repository that was ever public is one careless commit from a live key — report it as a finding with
   the rotation question attached, and never paste the value.

7. **Map the personal data.** What the system collects about people, where it lands (table, file, bucket,
   third party), who can read it, how long it stays, and how it is deleted. The sender cannot answer this
   and it is the question most likely to become a legal one. If the answer is "emails in `users` and
   nothing deletes them", that is the finding.

8. **Read the authorship.** What does the code say about how it was built? Duplicated helpers with
   different behaviour, two implementations of the same function with one commented out, a declared
   dependency that is never imported, wholesale patterns applied inconsistently, notes that describe work
   that was never finished. This is not blame — it tells the receiver **what to trust and what to
   distrust**, which is the difference between inheriting a system and inheriting a guess.

9. **Rank the untested surface by blast radius.** Name what has no test at all, then the three paths where
   a defect would cost the most — money, personal data, data loss, or silent wrongness. "No tests" is a
   fact; "no tests on the payment path" is a risk.

10. **Make one small change, and roll it back.** Choose the smallest real change that proves the
    development loop works — a config value, a log line, a route that returns one more field. Run the
    tests that exist (if none, run the app and exercise the path by hand). Then revert it and confirm you
    are back where you started. **A receiver who has not reverted something does not know the way back.**
    In a copy, never in production.

11. **Write the verdict.** One of three, with the reasons numbered against the findings:
    - **Continue** — the system starts, the loop works, no finding is a live hazard.
    - **Continue with conditions** — list each condition, the finding it answers, who owns it, and what
      evidence clears it. Most takeovers land here, and that is not a failure.
    - **Stop** — a live credential, personal data with no owner or deletion path, or a system that cannot
      be run from the repository at all. Say which.

12. **Write `ONBOARDING.md`** with the sections above, and hand the conditions to whoever owns the work.

## 5. Decision rules and evidence standard

- **The code is the source of truth; notes, comments and recollection are claims.** State the
  disagreement rather than resolving it silently.
- **An unexecuted instruction is a rumour.** Start, build, deploy and revert are procedures to be run,
  not to be transcribed.
- **An absence is the finding.** `grep` printing nothing where a column should be is exactly as much
  evidence as grep printing a line.
- **Blame is not a category.** The authorship section exists to say what to trust, not who to be annoyed
  with. AI-assisted code is not worse code; it is code whose author cannot explain it, which changes what
  must be written down.
- **Every finding has a consequence**: what breaks, for whom, and how you would notice. A finding without
  a consequence is a style note.
- **The verdict is about the evidence, not the vibes.** "It feels fine" is what the prompt exists to
  replace.

## 6. Verification

| Check | Method | Pass condition |
|---|---|---|
| Start procedure works | clean checkout, follow only the written steps | app runs; every guessed step is listed as a finding |
| Runtime map is complete | cross-check routes/entry points against the code | every entry point has a `file:line` and its store |
| Model/schema reconciled | diff objects against schema or live database | every mismatch named with the failing operation, or "none found" after checking |
| Deployment artifact exercised | build, or documented reason it could not be | result recorded, not assumed |
| Secrets inventoried | search + read | every expected credential named and classified; no value quoted |
| Personal data mapped | schema + code paths | collected, stored, readable-by, retained, deletion — all five |
| Authorship read | diff of duplicates, dead deps, comments | at least the duplicated and abandoned code named |
| Untested surface ranked | search for tests | absence stated and the three highest-blast-radius paths named |
| Change made and reverted | run it | both directions observed, evidence quoted |
| Verdict issued | read the last section | one of three, conditions numbered against findings |

## 7. Failure handling

- **The application cannot start, and the cause is not in the repository** (a missing service, a private
  package, a database that only exists on someone's laptop) → finding #1, verdict *continue with
  conditions*, and name the exact missing thing. Do not substitute a guess for the missing service.
- **There is no schema and no migrations** (the database exists only in production) → dump the schema
  read-only if authorised; otherwise record it as the largest single unknown, because every query in the
  codebase is a claim about a structure nobody has written down.
- **A credential looks live** → do not test it, do not paste it, and stop the corresponding line of
  investigation: report it, recommend rotation, and continue elsewhere.
- **The sender's notes contradict the code** → report both, quote the note, cite the line. The receiver
  needs to know which document lied, not just which is right.
- **The repository is too large to read in the budget** → follow the money and the personal data first,
  then the entry points on the critical path; say explicitly what was not read. A partial map with its
  edges stated is useful; a complete-sounding map that skipped the payment path is not.
- **The system is broken rather than unknown** → this is `02-engineering/project-recovery/`, which
  preserves and repairs. Say so, and hand over the findings already gathered.

## 8. Security and authorisation

Risk class A: read-only, plus one reverted change in a copy. Do not test credentials, do not connect to
production with write access, and do not export personal data to your own machine — count records, do not
copy them. Quote secret **names** and locations, never values; if a value appears in a note or a commit,
report its presence without reproducing it. The change in step 10 is confined to a scratch copy or a
feature branch with no deployment.

## 9. Completion criteria

- [ ] Start procedure executed and written; every guessed prerequisite listed as a finding.
- [ ] Runtime map with `file:line` for every entry point.
- [ ] Model/schema reconciliation done, with mismatches named or "none" after checking.
- [ ] Deployment artifact exercised, or the reason it could not be recorded.
- [ ] Secrets named and classified; no value quoted.
- [ ] Personal data map complete: collected, stored, readable-by, retention, deletion.
- [ ] Authorship read: duplicated code, abandoned implementations, dead dependencies named.
- [ ] Untested surface ranked, with the three highest-blast-radius paths.
- [ ] One change made and reverted, with evidence.
- [ ] Verdict issued, with conditions numbered against findings.
- [ ] `ONBOARDING.md` written.

## 10. Handoff

Conditions that are engineering work go to the system that owns them (`project-recovery` for repair,
`security-hardening` for credential and access findings, `04-process/documentation/` when the gap is the
document rather than the code). If a formal transfer follows — access, revocation, acceptance — continue
in `04-process/handover/`, whose `HAND-P04` tests the receiver against the same evidence this prompt
produces.

## 11. Testing and known limitations

- **Executed** against `_meta/fixtures/takeover-scenario/` — a six-file Flask app built "with an AI",
  handed over by a sender who cannot answer questions, with a hardcoded key placeholder, a schema that
  disagrees with its models, a Dockerfile that cannot run, no tests, and personal data. Record:
  `_meta/empirical-evaluation-21.md`. The previous version (v0.1.0, a skeleton) scored **0 of 9**; this
  version scored **9 of 9** on the same fixture.
- **Author-run, and the fixture is small.** Reading six files is not reading six hundred. The failure mode
  this prompt most needs to survive — a large repository and a tight budget — is handled by the *cut in
  this order* rule in §7 and has not been exercised.
- **Not tested:** a real takeover with a live environment, where the deployment check can actually build
  and the change can be deployed and rolled back end to end.
