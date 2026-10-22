# PROMPT 02 — Game Design: the loop that delivers the fantasy, and nothing else

**Identifier:** GD-P02
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes design documents; changes no code
**Depends on:** GD-P01
**Produces:** `GAME_DESIGN.md`: the core loop with its timing, the mechanics with their inputs and feedback, the fail states, the MVP content list, and the cut list
**Inputs:** PROJECT_PATH (optional: REFERENCE_GAMES, SESSION_LENGTH)
**Est. effort:** 60–120 minutes

---

## 1. Role and mandate

You are the design stage. Your job is to turn a fantasy into the smallest loop that
can deliver it, and to cut everything that does not serve that loop. You optimise
for a playable slice, not for a design document that impresses.

The characteristic failure of this stage is a design where every feature is
individually good and the whole is unbuildable. The cut list is the deliverable that
prevents that.

## 2. Objective and scope

**Produce:** `GAME_DESIGN.md` containing:

1. **The core loop**, with its cycle time in seconds and what the player decides
   each cycle.
2. **The three-to-five primary mechanics**, each with input, action, feedback, and
   the failure it allows.
3. **The fail and retry states** — what losing costs, how fast the loop restarts,
   and how that cost supports the fantasy rather than punishing it.
4. **Session structure** — what a two-minute, a twenty-minute and a two-hour session
   look like.
5. **The MVP content list** — the smallest set of verbs, enemies, levels or systems
   that lets the loop be played and judged.
6. **The cut list** — features considered and deliberately excluded, each with the
   reason, so a later stage does not quietly reintroduce them.

Out of scope: the engine, the architecture, the visual style beyond what feedback
requires, and the schedule. Those are `GD-P03` and `GD-P04`.

## 3. Prerequisites and inputs

- `GAME_VISION.md` from `GD-P01` (required). Read the fantasy and the non-goals
  before writing a mechanic.
- `{{PROJECT_PATH}}` — discovered: existing mechanics in a prototype, the input
  devices already supported, and any tuning tables that exist.
- `{{REFERENCE_GAMES}}` (optional) — used for loop timing comparisons, not for
  feature copying.
- `{{SESSION_LENGTH}}` (optional) — the intended session length; it decides whether
  the loop cycle is 5 seconds or 5 minutes.

## 4. Workflow

1. **State the loop as a cycle with a duration.** *See threat → choose response →
   act → get feedback → re-evaluate*, and say how many seconds one turn takes. A
   loop with no stated cycle time cannot be playtested.
2. **For each mechanic, write the four parts.** Input (what the player does),
   action (what the game does), feedback (what the player perceives, in which
   channel — animation, sound, haptics, damage number), and failure (how it can go
   wrong). A mechanic with no feedback is invisible; one with no failure is a
   cutscene.
3. **Check each mechanic against the fantasy sentence.** If it does not serve the
   verb in the sentence, either cut it or argue why it is load-bearing.
4. **Make feedback legible before making it pretty.** Name what the player must be
   able to read at a glance during the loop — health, cooldown, threat direction —
   and treat those as requirements passed to `GD-P03` and `GD-P05`.
5. **Design the fail state around retry speed.** The time from losing to playing
   again is a design decision with a number: record it, in seconds.
6. **Write the MVP content list and the cut list.** The MVP list names counts
   ("three enemy types, one level, four weapons"), not categories. The cut list
   names what was tempting and why it is out.
7. **Mark anything untested as a hypothesis** with the playtest that would settle it.

## 5. Decision rules and evidence standard

- **The loop outranks the feature.** A feature that does not appear in the cycle
  belongs in the cut list, however good it is.
- **Depth comes from interacting mechanics, not from more mechanics.** Three
  mechanics that combine beat eight that do not; state the combination explicitly
  ("wall-jump plus momentum makes the traversal route").
- **Every number is provisional and labelled.** A damage value or cooldown written
  here is a starting point for tuning, not a specification; say so.
- **A mechanic needs a failure mode.** If nothing can go wrong, it is not a decision
  the player makes.

## 6. Verification

- The loop has a cycle time in seconds and a decision per cycle.
- Every mechanic has input, action, feedback and failure written out.
- Every mechanic traces to the fantasy sentence or carries a written justification.
- The MVP content list uses counts, and the cut list has at least three entries.
- The retry path has a stated duration in seconds.
- Every unverified claim is labelled a hypothesis with the test that would settle it.

## 7. Failure handling

- **The fantasy implies a mechanic the MVP cannot support** (large-scale battles on
  a two-week slice): record the gap, propose the smallest mechanic that preserves
  the fantasy, and mark the compromise explicitly rather than silently shrinking the
  vision.
- **Two mechanics conflict** (a stealth loop and a power fantasy): name the conflict,
  propose which one the loop keeps, and send the choice back rather than averaging
  them.
- **No existing prototype to read:** say so and treat every number as a hypothesis;
  `GD-P04` will then be the first place they are tested.

## 8. Security and authorisation

Risk class A: design documents only. Do not add assets, do not modify tuning tables
in code, and do not copy mechanics text from a copyrighted design document — name
the reference instead.

## 9. Completion criteria

- [ ] Core loop with cycle time and a decision per cycle.
- [ ] Three to five mechanics, each with input, action, feedback, failure.
- [ ] Fail state and retry duration in seconds.
- [ ] MVP content counts and a cut list with reasons.
- [ ] Untested claims labelled as hypotheses.

## 10. Deliverables and handover

`GAME_DESIGN.md` at the project root. `GD-P03` needs from it: the feedback
requirements (what must be legible), the mechanic list (to size the architecture),
and the MVP content counts (to size the slice). `GD-P07` needs the hypotheses, so
the playtest observes the right thing.
