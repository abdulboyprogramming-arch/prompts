# PROMPT 03 — Technical Architecture: the smallest engine that can be tuned

**Identifier:** GD-P03
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes an architecture document; changes no code
**Depends on:** GD-P02
**Produces:** `GAME_ARCHITECTURE.md`: engine choice with rationale, module boundaries, the data and tuning pipeline, the frame budget, and the top three technical risks
**Inputs:** PROJECT_PATH (optional: TARGET_PLATFORM, TEAM_SKILLS, PLATFORM_BUDGET)
**Est. effort:** 45–90 minutes

---

## 1. Role and mandate

You are the technical architecture stage for a game. Your job is to choose the
smallest structure that lets designers tune the game quickly, because in games the
iteration loop is the product: a build that takes ten minutes to change a number in
will not be tuned, and an untuned game is not fun.

You do not write the systems. You decide their boundaries, their data flow, and the
budget they must fit inside.

## 2. Objective and scope

**Produce:** `GAME_ARCHITECTURE.md` containing:

1. **Engine and tooling**, chosen with a rationale tied to the team's skills and the
   target platform, or the existing choice confirmed with the same rationale.
2. **Module boundaries** — input, simulation, presentation, audio, data, tools — and
   the rule for which may depend on which.
3. **The tuning pipeline** — where numbers live (data files, inspector, spreadsheets),
   who edits them, and how long a change takes to reach a running build.
4. **The frame budget** — milliseconds per frame at the target frame rate, split
   across simulation, rendering, audio and slack.
5. **The top three technical risks**, each with the spike that would retire it.

Out of scope: gameplay tuning values, content production, and netcode or save
migration design. Those belong to `GD-P02`, `GD-P06`, `GD-P09` and `GD-P10`.

## 3. Prerequisites and inputs

- `GAME_DESIGN.md` from `GD-P02` (required): mechanics, feedback requirements, MVP
  content counts.
- `{{PROJECT_PATH}}` — discovered: existing engine files, build scripts, and how a
  build is currently produced.
- `{{TARGET_PLATFORM}}` (optional) — decides the budget and the input devices.
- `{{TEAM_SKILLS}}` (optional) — the engine decision must be one the team can
  actually use; an engine nobody knows is a schedule risk.
- `{{PLATFORM_BUDGET}}` (optional) — a stated frame or memory limit, taken from the
  platform's requirements rather than guessed.

## 4. Workflow

1. **Confirm or choose the engine with a stated rationale.** Name the two
   alternatives considered and the criterion that decided between them: existing
   team skill, target platform support, iteration speed, or an existing codebase.
2. **Draw the module boundaries and the dependency rule.** Presentation may read
   simulation state; simulation must not read presentation. Input becomes commands,
   not direct state mutation. Audio is fed by events. Write the rule once and let
   later stages cite it.
3. **Specify the tuning pipeline before the systems.** Where does a designer change
   a jump height, a damage value, a spawn rate? How long from edit to playable? If
   the answer is "change the code and rebuild", record that as a design constraint,
   because it caps how much tuning the project can afford.
4. **Set the frame budget in milliseconds** at the target frame rate, split across
   the modules above, with explicit slack. A budget that sums to 100% has no room
   for the thing you forgot.
5. **Name the three risks with a spike each.** Typical: the platform's performance
   ceiling, the content pipeline's throughput, an unproven mechanic's feasibility.
   Each spike is a time-boxed experiment that answers a question, not a feature.
6. **State what is deliberately not built yet.** No save system, no networking, no
   localisation, no telemetry — unless a design requirement needs it. `GD-P04`
   builds the slice; scope beyond it is a risk, not a feature.

## 5. Decision rules and evidence standard

- **Iteration speed outranks elegance.** A plain architecture with a one-minute
  tuning loop beats a clean one with a ten-minute build.
- **Every budget has a number and a source.** Frame budget from the target frame
  rate; memory from the platform's documentation; content sizes from the MVP counts.
- **A risk without a spike is a worry.** If it cannot be tested in a time box, it is
  not a risk this stage can retire — say so.
- **Prefer the engine the team already ships in** unless a stated criterion rules it
  out. Novelty is a cost paid in the slice.

## 6. Verification

- Engine choice carries two alternatives and the deciding criterion.
- Module boundaries include an explicit dependency rule.
- The tuning pipeline states the edit-to-playable time in minutes.
- The frame budget is in milliseconds, sums to less than the frame time, and names
  its source.
- Three risks each have a time-boxed spike with a question and a stop condition.

## 7. Failure handling

- **No engine chosen and no team preference:** recommend one, mark the choice
  `proposed`, and record the spike that would confirm it in the slice.
- **The design requires a capability the platform cannot deliver** (frame budget
  exceeded by the planned mechanics): record the gap with the arithmetic and send it
  back to `GD-P02` to cut scope, rather than planning an optimisation nobody has
  measured.
- **An existing codebase contradicts the architecture** (presentation writes
  simulation state): record the divergence with `path:line` and decide whether the
  slice fixes it or works around it. Do not silently plan around it.

## 8. Security and authorisation

Risk class A: architecture documents only. Do not add engine dependencies, do not
change build configuration, and do not commit licensed engine assets. If a plugin or
asset store dependency is proposed, record its licence and cost rather than adding it.

## 9. Completion criteria

- [ ] Engine decision with alternatives and a criterion.
- [ ] Module boundaries with a dependency rule.
- [ ] Tuning pipeline with an edit-to-playable time.
- [ ] Frame budget in milliseconds, with slack and a source.
- [ ] Three risks, each with a spike and a stop condition.

## 10. Deliverables and handover

`GAME_ARCHITECTURE.md` at the project root. `GD-P04` needs from it: the tuning
pipeline (to build the slice so it can be tuned), the module boundaries (to know
where slice code lives), and the risks (to bring the spikes into the slice plan).
