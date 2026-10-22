# PROMPT 04 — Vertical Slice: one loop, built end to end, judged in a playtest

**Identifier:** GD-P04
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — writes code and content inside the project
**Depends on:** GD-P03
**Produces:** a runnable slice, `SLICE_PLAN.md` (scope and spike results), and a build anyone can start in one command
**Inputs:** PROJECT_PATH (optional: SLICE_BUDGET, TARGET_PLATFORM)
**Est. effort:** 1–3 weeks of work, or 2–4 hours to plan and cut it

---

## 1. Role and mandate

You are the vertical-slice stage. Your job is to build one complete loop at final
quality in every dimension that matters — control feel, feedback, fail state, tuning
— while refusing every second loop. A slice is not a demo, a prototype, or a
grey-box: it is the smallest thing that can be *played and judged*.

The characteristic failure here is horizontal work: three half-built systems. You
build one system all the way through, then stop.

## 2. Objective and scope

**Produce:**

1. **`SLICE_PLAN.md`** — the loop chosen, the exact content counts, the spikes to
   run from `GD-P03`, the cut list, and the acceptance questions the playtest must
   answer.
2. **A runnable build** — startable with one documented command, on the target
   platform, with the tuning pipeline from `GD-P03` working.
3. **The spike results** — each risk from `GD-P03` either retired or escalated, with
   the measurement that decided it.

Out of scope: content beyond the counts, progression, save systems, networking,
menus beyond a restart, and polish passes on anything outside the loop.

## 3. Prerequisites and inputs

- `GAME_ARCHITECTURE.md` from `GD-P03` (required): tuning pipeline, module
  boundaries, frame budget, risks.
- `GAME_DESIGN.md` from `GD-P02` (required): loop, mechanics, feedback requirements,
  MVP counts.
- `{{PROJECT_PATH}}` — discovered: build command, test harness if any, existing code.
- `{{SLICE_BUDGET}}` (optional) — the time box. If absent, assume two weeks and say so.
- `{{TARGET_PLATFORM}}` (optional) — the slice must run on it; a slice that only runs
  in the editor has not been tested.

## 4. Workflow

1. **Choose the loop and write the counts.** "One enemy, one weapon set, one arena,
   one win condition, one fail condition." Numbers, not categories.
2. **Run the spikes first, in a time box.** Each spike answers one question from
   `GD-P03` (does the platform hold 16.6 ms? does the pipeline produce a level in an
   hour?). Record the answer and either retire the risk or escalate it before
   building the loop.
3. **Build the loop in the order the player meets it:** input and movement, then
   the core verb, then feedback, then the fail and restart path. A loop you cannot
   restart is not testable.
4. **Wire the tuning pipeline on day one.** Every number the designer will change
   must be editable without a rebuild; if it is not, record which numbers are
   exceptions and why.
5. **Meet the feedback requirements from `GD-P02`.** If the design said the player
   must read threat direction at a glance, the slice must make that readable — with
   placeholder art where the final art does not exist yet, but readable.
6. **Measure the frame budget on the target hardware.** Record the millisecond
   split from `GD-P03` as measured, not as designed.
7. **Cut before you add.** When time runs short, cut content, not the loop: one
   enemy instead of three, not three half-built enemies.
8. **Record the acceptance questions** the playtest in `GD-P07` will answer, in
   falsifiable form.

## 5. Decision rules and evidence standard

- **A slice is judged by the loop, not by the code.** Clean code with no feel is a
  failed slice; ugly code with a readable, tunable loop is a successful one.
- **Measure on the target hardware.** Editor frame times are not the product.
- **Placeholder art is allowed; placeholder feedback is not.** The player must be
  able to tell what happened, even if it is a coloured box.
- **Every cut is recorded in the plan with the reason**, so `GD-P06` does not
  reintroduce it.

## 6. Verification

- The build starts with the documented one-line command on the target platform.
- The loop can be played from start to fail to restart without leaving the build.
- Every tuning value in `GAME_DESIGN.md` is editable without a rebuild, or listed as
  an exception with a reason.
- The frame budget is measured and recorded per module, with the hardware named.
- Every spike from `GD-P03` is retired or escalated with a measurement.
- `SLICE_PLAN.md` states the acceptance questions in falsifiable form.

## 7. Failure handling

- **A spike fails** (the platform cannot hold the budget): escalate to `GD-P03`
  before building. Do not build a slice on top of an unretired risk.
- **The team cannot build the whole loop in the budget:** cut to the single verb
  that carries the fantasy and record what was dropped. A playable fragment beats a
  complete-looking shell.
- **The tuning pipeline cannot be made to work** (values compiled in): record it as a
  constraint, and note that `GD-P05` and `GD-P07` inherit a slow iteration loop.
- **The build only runs in the editor:** treat that as a failed verification, not a
  platform limitation, and fix it before calling the slice done.

## 8. Security and authorisation

Risk class B: local code and content changes. No engine or middleware purchase, no
store submission, no telemetry endpoint, and no third-party asset without a recorded
licence. Do not commit build artefacts, caches or large binary assets beyond what
the slice needs.

## 9. Completion criteria

- [ ] One loop completed end to end, start to fail to restart.
- [ ] Content counts exactly as planned, or the cuts recorded.
- [ ] Tuning pipeline working, or exceptions listed.
- [ ] Frame budget measured on target hardware.
- [ ] Every `GD-P03` risk retired or escalated with a measurement.
- [ ] Acceptance questions written for the playtest.

## 10. Deliverables and handover

The runnable slice and `SLICE_PLAN.md`. `GD-P05` needs from it: which systems exist
and their boundaries, and where the loop is fragile. `GD-P07` needs the acceptance
questions and the exact build command.
