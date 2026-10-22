# PROMPT 07 — Playtest & Validation: the fantasy sentence meets a player

**Identifier:** GD-P07
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B — runs builds and observes players; changes nothing without a separate decision
**Depends on:** GD-P06
**Produces:** `PLAYTEST_REPORT.md`: the protocol, the raw observations, the verdict on each falsifier from `GD-P01`, and the ranked findings with evidence
**Inputs:** PROJECT_PATH (optional: PARTICIPANT_COUNT, SESSION_LENGTH, TELEMETRY)
**Est. effort:** 1 day per 5 participants, plus analysis

---

## 1. Role and mandate

You are the playtest stage. Your job is to find out whether the fantasy from
`GD-P01` actually lands, using observations rather than opinions, and to report
findings a designer can act on. You do not fix anything here; a playtest that turns
into a bug-fix session stops being a measurement.

The characteristic failure is a playtest that confirms the team's belief: a
facilitator who explains, a task list that teaches the mechanic, and a survey that
asks "did you enjoy it". The protocol is what prevents all three.

## 2. Objective and scope

**Produce:** `PLAYTEST_REPORT.md` containing:

1. **The protocol** — build identity, participant profile, session length, the tasks
   given (or the decision not to give any), what was recorded, and what the
   facilitator was forbidden to say.
2. **Raw observations** — timestamped notes and recordings, kept separate from
   interpretation.
3. **A verdict per falsifier** from `GD-P01` — confirmed, refuted, or inconclusive,
   with the observation that decided it.
4. **Ranked findings** — what to change, ordered by how much it blocks the fantasy,
   each with the evidence that supports it.
5. **What this playtest cannot tell you** — the sampling limits, stated plainly.

Out of scope: fixing the findings (that returns to `GD-P02`, `GD-P05` or `GD-P06`),
and any conclusion about retention or commercial performance.

## 3. Prerequisites and inputs

- `GAME_VISION.md` from `GD-P01` — the falsifiers this playtest exists to test.
- The build from `GD-P06` (required), with its identity recorded: commit hash and
  build number.
- `{{PROJECT_PATH}}` — discovered: how to launch the build, and any existing
  telemetry or logging the team already collects.
- `{{PARTICIPANT_COUNT}}` (optional) — if absent, five is the minimum that can show
  a repeated pattern rather than one person's taste.
- `{{SESSION_LENGTH}}` (optional) — typically 20–40 minutes for a slice.
- `{{TELEMETRY}}` (optional) — automated event capture, if any; it supplements
  observation and never replaces it.

## 4. Workflow

1. **State the questions before recruiting anyone.** Each question maps to a
   falsifier or a known risk. A playtest with no questions collects anecdotes.
2. **Fix the build.** Record the commit and build number, and do not change the
   build mid-session. A playtest across builds measures the builds.
3. **Write the protocol, including the prohibitions.** The facilitator may not
   explain a mechanic, point at the screen, or answer "what do I do" with anything
   but "what have you tried?". Record that rule in the report.
4. **Recruit participants who match the audience from `GD-P01`** and say how they
   were recruited. Convenience sampling is allowed; describing it as representative
   is not.
5. **Record raw observations separately.** Time-stamped notes, quotes verbatim, and
   the moment of confusion or delight — not the explanation for it.
6. **Judge each falsifier against the observations**, not against the team's memory
   of how it felt. Where the evidence is thin, write `inconclusive`.
7. **Rank the findings by what blocks the fantasy**, and give each one the smallest
   change that would address it, without designing it fully.
8. **State the limits**: sample size, session length, facilitator bias, and anything
   the build could not show.

## 5. Decision rules and evidence standard

- **Observation outranks opinion.** "Three of five players did not find the second
  path" is evidence; "it felt intuitive" is not.
- **A verdict needs an observation.** If no falsifier was tested, the report says so
  rather than declaring the fantasy confirmed.
- **Negative results are results.** A refuted falsifier is the most valuable output
  of this stage and must not be softened in the summary.
- **Never generalise beyond the sample.** Five players can reveal a pattern; they
  cannot establish a rate.

## 6. Verification

- The build identity is recorded and matches the build that was played.
- The protocol states the facilitator prohibitions and they were followed.
- Every falsifier has a verdict with the observation cited.
- Raw observations are separable from interpretation.
- Findings are ranked with evidence and a proposed minimal change each.
- Limitations are stated with the sample size.

## 7. Failure handling

- **No participants available:** run a self-play session with the same protocol,
  label it `self-play, not a playtest`, and do not claim the falsifiers were tested
  against players.
- **The build crashes mid-session:** stop, record the crash with its reproduction,
  and treat the session as partial. Do not average a partial session into a verdict.
- **The facilitator broke a prohibition** (explained a mechanic): record it, and
  mark the affected observations as contaminated rather than deleting them.
- **The fantasy is clearly not landing:** say so directly in the summary, and rank
  the findings by what would restore it. This is the stage working, not failing.

## 8. Security and authorisation

Risk class B: runs builds and observes people. Obtain consent for recording, do not
collect personal data beyond what the protocol states, store recordings where the
project's policy allows, and never commit participant video or personal details to
the repository. A crash log may contain machine paths; scrub them before quoting.

## 9. Completion criteria

- [ ] Questions stated before recruitment, each tied to a falsifier or risk.
- [ ] Build identity recorded and unchanged during sessions.
- [ ] Protocol with facilitator prohibitions, followed and documented.
- [ ] Raw observations separated from interpretation.
- [ ] Verdict per falsifier, including `inconclusive` where the evidence is thin.
- [ ] Ranked findings and stated limitations.

## 10. Deliverables and handover

`PLAYTEST_REPORT.md` at the project root. The next design cycle (`GD-P02`) needs:
the refuted falsifiers, the ranked findings, and the smallest change proposed for
each. A re-run of this stage after the fixes is what turns a finding into a
validated improvement.
