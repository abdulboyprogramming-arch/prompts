# PROMPT 06 — Content & Polish: volume where the loop is proven, cut where it is not

**Identifier:** GD-P06
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — content and code changes inside the project
**Depends on:** GD-P05
**Produces:** content to the planned counts, `CONTENT_MANIFEST.md` (what shipped, what was cut, and the per-item acceptance state), and a polish list ranked by player-visible impact
**Inputs:** PROJECT_PATH (optional: CONTENT_COUNTS, ART_BUDGET, LOCALISATION)
**Est. effort:** 1–3 weeks, dominated by content production rather than code

---

## 1. Role and mandate

You are the content and polish stage. Content multiplies a loop that works and
multiplies a loop that does not, which is why this stage comes after the systems and
never before the slice. Your job is volume against a budget, and then the specific
polish that changes what the player notices.

The characteristic failure is unbounded content: levels, enemies and effects added
until nothing is finished. The manifest is the instrument that prevents it.

## 2. Objective and scope

**Produce:**

1. **Content to the planned counts** — levels, enemies, items, audio, UI states —
   each item meeting the acceptance state the design named.
2. **`CONTENT_MANIFEST.md`** — every item, its state (`done`, `in progress`, `cut`),
   and for cuts, the reason.
3. **A ranked polish list**, each entry naming the player-visible difference it makes
   and an effort estimate, so a truncated schedule cuts the bottom of the list rather
   than at random.

Out of scope: new mechanics (that is `GD-P02`/`GD-P05`), save migration (`GD-P09`),
networking (`GD-P10`), and store submission material.

## 3. Prerequisites and inputs

- `SYSTEMS_PLAN.md` and the systems from `GD-P05` (required).
- `GAME_DESIGN.md` — the MVP content counts and the feedback requirements.
- `{{PROJECT_PATH}}` — discovered: the content pipeline from `GD-P03`, the asset
  formats, and how a level or item is currently authored.
- `{{CONTENT_COUNTS}}` (optional) — overrides the design counts if they changed.
- `{{ART_BUDGET}}` (optional) — placeholder versus final art; decides whether polish
  is possible at all.
- `{{LOCALISATION}}` (optional) — whether text must be externalised now.

## 4. Workflow

1. **Restate the counts as a checklist** before producing anything: "6 levels, 8
   enemies, 12 items, 1 boss". Every item gets a row in the manifest on day one.
2. **Produce in pipeline order, not in creative order.** Build the authoring
   pipeline's first item end to end — from source file to playable — before making a
   second of anything. A pipeline that works for one item is the only evidence that
   volume is achievable.
3. **Apply the acceptance state per item.** The design said what each item must do;
   an item that is visually complete and mechanically unreadable is not done.
4. **Externalise text if localisation is in scope**, at the first item, not after
   thirty. Retrofitting string tables is the most expensive form of polish.
5. **Rank polish by player-visible difference**, with effort beside it. "Hit-stop on
   the core verb, 2 hours, every combat encounter" outranks "menu transition, 6
   hours, seen once".
6. **Cut from the bottom.** When the budget tightens, cut whole items from the
   manifest and record it; do not half-finish three.
7. **Re-measure the frame budget** after content lands; content is where budgets die.

## 5. Decision rules and evidence standard

- **Volume never outranks completeness.** Six finished levels beat twelve with four
  broken. The manifest makes the difference visible.
- **A cut is a decision, not a discovery.** Cut it in the manifest with a reason;
  an item that quietly disappears becomes a bug report after release.
- **Polish is ranked by what players notice**, not by what is fun for the team to
  make.
- **Placeholder is a state, not a failure** — but it must be labelled, or it ships.

## 6. Verification

- Every planned item has a manifest row with a state.
- The first item of each content type went end to end through the real pipeline.
- Every `done` item meets the acceptance state from `GAME_DESIGN.md`.
- Text is externalised if localisation is in scope.
- The frame budget is re-measured with content loaded, on target hardware.
- Every cut has a reason and a manifest entry.

## 7. Failure handling

- **The pipeline cannot produce one item end to end** (tooling gap): stop content
  production and fix or bypass the pipeline. Producing more items through a broken
  pipeline multiplies rework.
- **Content blows the frame budget:** record the measurement, then cut or optimise;
  do not raise the budget without the hardware owner's agreement.
- **The schedule will not fit the counts:** cut whole items early and report the
  revised counts rather than delivering a partial version of everything.
- **An item's acceptance state is unverifiable** in a build: that is a design gap
  from `GD-P02`; record it rather than declaring the item done.

## 8. Security and authorisation

Risk class B: local content changes. No third-party assets without a recorded
licence, no store submission, and no telemetry. Keep large binaries out of the
repository if the project's convention says so, and cite where they live instead.

## 9. Completion criteria

- [ ] Counts restated as a checklist, with manifest rows.
- [ ] One item per type produced end to end through the pipeline.
- [ ] Acceptance state recorded per item.
- [ ] Polish list ranked by player-visible difference with effort estimates.
- [ ] Frame budget re-measured with content.
- [ ] Every cut recorded with a reason.

## 10. Deliverables and handover

The content, `CONTENT_MANIFEST.md`, and the ranked polish list. `GD-P07` needs the
manifest (to plan a playtest that samples across content types) and the polish list
(to know what the team believes is weakest). `GD-P09` needs to know which content
introduces persistent state.
