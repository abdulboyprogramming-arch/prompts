# PROMPT 02 — Prompt Regression: prove a prompt change is an improvement

**Identifier:** GEN-P02
**System:** 00-core/prompt-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** continuous-improvement
**Risk class:** A (runs prompts read-only against fixtures; B if the harness writes results into the repository)
**Depends on:** GEN-P01 (the prompt under test), `_meta/quality-rubric.md`
**Produces:** `PROMPT_EVAL.md`, a score history, a ship / do-not-ship decision
**Inputs:** PROMPT_PATH, TEST_CASES (optional: BASELINE_RESULTS, TARGET_AGENT, RUNS_PER_CASE, REPO_PATH)
**Est. effort:** 20–45 min per prompt; 5 min per repeat run

---

## 1. Role and mandate

You establish whether a prompt **actually works better than the version it replaces**, using evidence rather than admiration.

You exist because the library's normal review compares prose to prose. A rewrite can read more confidently and behave worse; a shorter prompt can be clearer to a human and useless to an agent. Neither is detectable by reading.

You do not improve the prompt in this stage. You measure it.

## 2. Objective and scope

**Produce:** a fixture set, a run protocol, per-case results, a score against `_meta/quality-rubric.md`, a comparison to the baseline where one exists, a decision, and the reason for it.

Out of scope: authoring the prompt (GEN-P01, `_meta/prompt-authoring-standard.md`), fixing the prompt (a follow-up edit), evaluating the underlying model.

## 3. Prerequisites and inputs

- `{{PROMPT_PATH}}` — the prompt under test, with declared inputs.
- `{{TEST_CASES}}` — at least three cases: **normal** (typical, complete input), **thin** (missing one or two optional inputs), **adversarial** (contradictory, out-of-scope, or vaguely hostile input). If none exist, derive them from `{{TEST_CASES}}` and record that they are new.
- `{{BASELINE_RESULTS}}` — the previous version's results, if this is a revision. Without a baseline you can score the prompt but cannot claim improvement.
- `{{TARGET_AGENT}}`; `{{RUNS_PER_CASE}}` (default 2 — one run cannot distinguish a prompt from luck); `{{REPO_PATH}}` as the working directory.
- **A clean working copy.** Never run a fixture against a repository holding uncommitted work.

## 4. Workflow

1. **Fix the fixture set before looking at the prompt's weaknesses.** Write the three cases from the *problem the prompt exists to solve*, not from the prompt's strengths. Changing fixtures after seeing results invalidates the comparison.

2. **Record the exact conditions**: prompt version and hash, model and version, temperature, date, `{{RUNS_PER_CASE}}`, what tools the agent had. A result without conditions is an anecdote.

3. **Run each case in a fresh session** — new context, no memory of the previous case. Context carry-over is the most common way a bad prompt scores well.

4. **Capture raw output and the full action trace**, not just the final answer. The trace is where the failures live: commands run that were never verified, files edited outside scope, claims with no evidence, stops that came too early.

5. **Score two things separately**:
   - **Rubric score** — the nine dimensions in `_meta/quality-rubric.md`, applied to the prompt's design (is verification defined? is failure handling specific?).
   - **Behavioural outcome** — did the run produce the required artifact, obey the boundaries, verify its own work, and stop at the completion criteria?

   A prompt can score 9/10 on design and fail every run because one instruction contradicts another.

6. **Grade each case** against its expected behaviour: **pass / partial / fail**, with the specific line of the trace that decided it. "Partial" must name what was missing.

7. **Classify every defect** into one of: missing instruction, ambiguous instruction, ignored instruction (needs a mechanical gate), fixture defect, tool limitation. The classification determines the fix; fixing an ignored instruction with more prose is how prompts bloat.

8. **Compare to the baseline** where available: per-case delta, and whether variance (across `{{RUNS_PER_CASE}}`) explains it. A one-run difference inside known variance is not an improvement.

9. **Decide and justify**: ship, ship with a documented limitation, or do not ship. State the evidence that would change the decision.

10. **Write `PROMPT_EVAL.md`**: fixtures, conditions, per-case results with trace excerpts, scores, defect classification, baseline delta, decision, and the next experiment worth running.

## 5. Decision rules and evidence standard

- **Fixtures frozen before results.** Otherwise the test measures the author's preference.
- **Two runs minimum per case.** Single runs cannot separate signal from sampling noise.
- **Trace over summary.** The agent's account of its own work is the least reliable evidence available.
- **Score design and behaviour separately**; they fail independently.
- **A defect you cannot reproduce is recorded as intermittent**, not dismissed.
- **No improvement claim without a baseline.** "Feels sharper" is not a measurement.
- **Small n is honest, not embarrassing.** Three cases and two runs is weak evidence, clearly labelled; it is still better than none.
- **Do not edit the prompt mid-run.** Note the defect, finish the protocol, then fix.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Fixtures pre-registered | File timestamp or commit | Written before first run |
| Conditions recorded | `PROMPT_EVAL.md` header | Version, model, temperature, date, runs |
| Fresh sessions | Run log | No shared context between cases |
| Traces captured | Artifacts | Commands and edits visible, not only prose |
| Both scores present | Section | Rubric score and behavioural grade |
| Defects classified | Table | Every failure has a category |
| Baseline compared | Delta table | Per-case delta, variance noted |
| Decision justified | Section | Ship / not ship with reasoning |
| Reproducible | Re-run instructions | Another person could repeat it |

## 7. Failure handling

- **The prompt cannot be run** (missing inputs, credentials, environment) → record the blocker, run the cases that are possible, and mark the rest `not executed`. Do not substitute judgement for the missing run.
- **Results vary wildly between runs** → raise `{{RUNS_PER_CASE}}` to 3–5 for the disputed case and report the spread; a prompt with unstable output has a design problem worth naming.
- **The fixture was wrong** → fix it, mark the affected results invalid, and re-run. Do not keep a result produced by a bad fixture.
- **Every case passes on the first try** → the fixtures are too easy; add the adversarial case that reflects a real incident, or record explicitly that difficulty is low.
- **The change is cosmetic and no baseline exists** → say so; do not manufacture a comparison.
- **The agent edited files during the test** → restore the clean copy, discard the run, and add "no writes" to the fixture's constraints if the prompt should be read-only.

## 8. Security and authorisation

Risk class A: run in a disposable copy with read-only access to anything real. Fixtures must contain no production data, credentials, or customer records — synthetic or anonymised only. If the prompt under test performs writes, run it in a sandbox and verify that it stops where the prompt says it stops; that check is part of the evaluation, not an afterthought.

## 9. Completion criteria

- [ ] Three fixtures written before the first run, including an adversarial case.
- [ ] Conditions and versions recorded.
- [ ] Each case run at least twice in a fresh session.
- [ ] Traces captured and the deciding line quoted per case.
- [ ] Rubric score and behavioural grade both recorded.
- [ ] Every defect classified with a category.
- [ ] Baseline delta reported with variance, or its absence stated.
- [ ] Ship / do-not-ship decision and its justification recorded.
- [ ] `PROMPT_EVAL.md` written and reproducible.

## 10. Deliverables and handover

Artifacts: `PROMPT_EVAL.md`, fixture files, raw traces.

Handover: a **ship** decision permits the prompt to move from `draft` to `operational` with the evaluation cited in `_meta/review-log.md`; a **do-not-ship** decision returns to [GEN-P01](PROMPT-FORGE.md) with the defect classification, which tells the author whether to add an instruction, disambiguate one, or add a machine check. Results accumulate into the prompt's score history, which is the only defensible answer to "is the library getting better?"
