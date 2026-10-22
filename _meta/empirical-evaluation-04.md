# Empirical evaluation 04 — `CHAT-REVIEW` against a real file, with a defect the reviewer had written

**Prompt:** `00-core/conversational/CHAT-REVIEW.md` (v1.0.0, operational)
**Date:** 2026-10-22
**Evaluator:** the prompt's author. The code under review was also written by the author in the same session, which makes this the weakest kind of self-test: a review by the person who wrote both the prompt and the target. It is recorded because the alternative — no execution at all — is weaker still.
**Method:** the prompt ran as written against one file, kept in full, not summarised. The target was `scripts/check_prompt_contract.py` (roughly 300 lines, itself written earlier the same day), asked for in the *"is this safe to merge"* intent the prompt's `{{REVIEW_INTENT}}` input names.

---

## 1. What the prompt produced

The workflow's ten steps were followed in order. The steps that did actual work:

**Window stated first (step 1).** *"I can see the whole file, 300 lines including imports, with no callers, no tests, and no sample of the data it parses."* Two items were requested and one offered to proceed without: the fixture file, and one real `Depends on:` line that names a missing prompt. The review proceeded without both, which is what step 1 asks for.

**Consequence ordering (step 2).** Correctness first — the dependency check, then the collision check, then the flow measurement. Style was not reviewed at all, since no project standard for it was supplied, which is what the prompt demands rather than what it merely permits.

**Findings, classified (steps 3–5).** Each finding named a triggering input, as required:

| # | Bucket | Finding | Trigger |
|---|--------|---------|---------|
| 1 | **defect** | The flow check counted a link as satisfied if the artifact's **stem** appeared anywhere in the downstream text, ignoring the extension. | `PKG-P04` declares `{{SELECTED_WORK}}` as an *input*; the string `SELECTED_WORK` therefore appears, and the link to `SELECTED_WORK.md` was scored as named. |
| 2 | **defect** | The same check matched substrings of unrelated words. | The word `planning` in any prompt satisfied `PLAN.md`. |
| 3 | **risk** | The check required *any* upstream artifact to be named, not *all* of them, so a three-artifact handoff is satisfied by naming one. | 20 of the 157 links then scored as named were pairs where the upstream produces several artifacts and only some appear. |
| 4 | **risk** | `--check-report` compares the whole rendered file to the generated text, so any prose edit to the report fails the gate even when nothing it describes has changed. | Editing one sentence of `_meta/conformance-report.md` by hand. |
| 5 | **preference** | The per-system `Artifacts` column counts only non-orchestrator artifacts, which undercounts in systems where the orchestrator produces a manifest. | Any system with a P07 orchestrator. |
| 6 | question | Whether a stem-only mention should count as a failure rather than a separate measure. The prompt says a finding that depends on a decision the author must make is a question. | — |

**Findings 1 and 2 were confirmed by measurement rather than argument:** 30 of 157 links scored as "named" were stem-only, and one of the review's own fixtures — a prompt with no reference to `PLAN.md` at all — passed only because its template header says *Execution mode: planning*.

**Not assessed (step 7):** whether the metric produces the right *decisions*; whether any of the 82 unnamed links is actually a modelling error rather than a documentation gap; performance on 10,000 prompts; and everything the callers do with `check()`, since no caller was supplied.

**Verdict, scoped to the excerpt (step 8):** *"Two real defects in the measurement, one of which overstates the library's own integration claim by twelve percentage points. No defect found in dependency parsing, cycle detection, or the collision rule, given the tests supplied."* No merge recommendation was made, which the prompt forbids from an excerpt.

**What would raise confidence (step 10):** the fixture file, and one downstream prompt that names its upstream file, to confirm the strict path passes for the right reason.

## 2. What the run found

### The prompt's defects

1. **It has no rule for a *measuring* artefact.** The defects it found were all in a check, not in the code the check describes. A review of a script that produces a number should ask what would make that number wrong — the prompt's consequence ordering (correctness against stated intent) gets there eventually, but only because the stated intent happened to be measurement. Adding a step for it is the change below.

2. **The not-assessed list needed a category for the review itself.** The prompt requires tests, migrations, configuration, dependencies, callers and data to be listed. It has no slot for *"the standard this code implements was not supplied"*, which was exactly the largest gap here: whether a stem match is acceptable is a decision about the metric, and no rule in the prompt says to say so instead of asserting an answer.

3. **"Ask before assuming the framework" (step 6) did not generalise to "ask before assuming the standard".** The same discipline applies to a measurement definition, a schema, an error taxonomy — anything where the author's intent is not visible in the text.

### The repository's defects

The review's two defects were real and were fixed the same session: the check now strips `{{…}}` placeholders and requires the filename with its extension, and the three-way result (cited / stem-only / absent) is reported separately with four new fixtures. Twenty-one operational prompts were given explicit filenames, and the honest figure moved from **34% unnamed to 38% do not cite a filename, 34% absent entirely** — a worse number that is true.

## 3. Verdict on the prompt

**Operational, and it earned its label.** The window-first rule and the defect/risk/preference split did the work: without the classification, finding 1 would have been filed as a preference about metrics rather than as a defect that inflates a published claim, and without the scoped verdict the run would have ended in a vague endorsement.

**Three changes made to the prompt** (v1.1.0):

- Step 2 now includes *"if the code computes a number the project publishes, the number is the correctness question"* ahead of the usual ordering.
- A new decision rule: *"Ask about the standard, not only the framework. A metric, a schema, and an error taxonomy are all definitions the author holds and the excerpt does not."*
- The not-assessed list gained a required line for *"definitions and standards this review had to assume"*.

## 4. Limitations

- **Author-evaluated, and twice over:** the reviewer wrote the prompt, the target, and the standard the target implements.
- **One file in one stack**, Python, small enough to hold in a window — the review's central claim (the window defines the verdict) was not tested at all, because the window happened to be complete.
- **The defects found were found by measurement**, which this prompt is unusually good at prompting for. A prompt that reviews prose would not have surfaced them by the same route.
- **No second reader.** A real test needs someone who did not write either artefact to run it and report what the prompt made them do.
