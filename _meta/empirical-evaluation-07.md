# Empirical evaluation 07 — `CHAT-HANDOFF` on the 2.22.0 engagement

**Prompt:** `00-core/conversational/CHAT-HANDOFF.md` (v1.0.0, operational)
**Date:** 2026-10-22 · **Method:** agent execution, one pass, agent-evaluated. The packet is the artifact; the test of the packet is a reconstruction with the packet as the only input.
**Evaluator:** the prompt's author. Conflict of interest recorded, and it matters most here: an author who wrote the packet can reconstruct from memory and call it a successful cold read.

---

## 1. Inputs

```
ENGAGEMENT     = ship v2.22.0 of the prompt library: honest gates, honest counts, evidence of execution
PACKET_VERSION = 1 (first handoff of this engagement)
OPEN_QUESTIONS = whether PR #12 should merge before or after the first independent run
REDACTED_ITEMS = none; no credentials or customer data entered this engagement
```

## 2. The packet produced

```
# HANDOFF — prompt library v2.22.0 — packet 1 of 2.22.0 — 2026-10-22

GOAL  Ship v2.22.0 as an open-source release whose claims are all machine-checked or
      labelled. DONE = PR #12 merged to main after a release-readiness review that names
      what is still unproven, plus a tagged release.

CONSTRAINTS
 1. Never merge PR #12 without the owner's explicit instruction (standing order).
 2. Every count in prose must be generated or gate-checked; no hand-maintained total.
 3. No claim of execution without a record in _meta/evidence.json and a write-up file.
 4. Work only on branch arena/cdb05e8f-prompts. No force-push, no history rewrite.
 5. Prose lint hard-fails at baseline 0; new long sentences break the gate.

FACTS
 - 462 Markdown files, 364 prompts: 228 operational, 5 draft, 131 skeleton.  [observed: validator]
 - 52 multi-stage systems, 239 dependency links; 92 (38%) do not cite the upstream
   filename, 82 name no artifact.  [observed: check_prompt_contract.py]
 - 4 prompts have recorded runs: DBG-01, CHAT-DEBUG, CHAT-SELECT, CHAT-REVIEW.  [observed: evidence.json]
 - All 14 gates pass locally; CI cannot run (Actions billing).  [observed locally; CI blocked = reported by GitHub API]
 - _.github/workflows holds TWO workflows_ (validate.yml runs check_all.py; validate-library.yml
   re-lists 12 commands and skips the composition gate).  [observed; contradicts the docs]
 - The owner has not said when PR #12 may merge.  [unknown]

DECISIONS
 - Dual licence: MIT for code, CC BY 4.0 for content.  (rejected: single MIT — content reuse
   without attribution was the risk.)
 - Sponsorship: not enabled.  (rejected: enable now — sponsors pay for updates, and execution
   is the bottleneck at 4 of 228.)
 - The composition metric now requires the filename, not the stem.  (rejected: keep the stem
   match — 30 links were false positives and the published number was inflated.)
 - Batches: B0 conversational first, B2 process work next.  (rejected: alphabetical folder
   order — it puts the 92-prompt process batch before the 8-prompt one.)

ELIMINATED (do not revisit)
 - "Lower the duplicate threshold to catch the drift" — died 2026-10-22: the metric was
   matching a stem, not a filename; a threshold cannot fix a wrong predicate.
 - "Close the readiness gap with more documentation" — died 2026-10-22: the gap is 224
   unexecuted prompts, which documentation cannot reduce.
 - "CI will catch regressions on the PR" — died 2026-10-21: Actions billing blocks the run;
   the local check_all.py is the only gate.
 - "CHAT-ASK exists" — died 2026-10-22: 00-core/conversational has 6 prompts, not 8; the
   plan document was wrong.

OPEN QUESTIONS
 1. (BLOCKING) May PR #12 merge before an independent run exists? Owner decision.
 2. Should validate-library.yml be deleted or converted to call check_all.py?
 3. Who is the second evaluator for batch C, and what do they run first?

NEXT ACTION  python3 scripts/check_all.py   (must pass before any commit; then commit the
              B0 records and push to arena/cdb05e8f-prompts)

RESTATEMENT REQUIRED before work resumes: the completion condition, the three constraints you
will obey, the eliminated hypotheses you will not revisit, and one fact you think is wrong.
```

Length: 48 lines, inside the limit.

## 3. The reconstruction test

Five questions were answered from the packet alone, without re-reading the repository or the earlier conversation:

| Question | Answered by the packet? | Where |
|---|---|---|
| What does done mean? | yes | GOAL, first two sentences |
| What must not happen? | yes — merge without instruction, hand-maintained counts, unrecorded claims | CONSTRAINTS 1–3 |
| Which hypothesis about CI is already dead? | yes | ELIMINATED, line 3 |
| What do I run next? | yes — one command, with its consequence | NEXT ACTION |
| Which fact must I not assume? | yes — merge permission; also the two-workflow fact is flagged as contradicting the docs | FACTS, `[unknown]` and the italicised line |

**Score: 5 of 5 answerable, 0 requiring the transcript.** That is the prompt's own bar.

## 4. Findings

| # | Severity | Finding |
|---|---|---|
| 1 | **Medium** | The four labels (`observed`/`reported`/`inferred`/`unknown`) have no way to express **"true when written, and generated"**. The counts in this packet are correct as of this run and will be wrong after the next prompt edit; label them `observed` and the next conversation treats a snapshot as a property. The packet needed a fifth form — *observed, generated, as of date* — which the prompt does not offer. |
| 2 | **Low** | Step 10 requires a restatement but gives no template, so the receiving conversation invents its own order. The four items are listed in prose, and this packet had to restate them in its own words. |
| 3 | **Low** | The prompt covers conflicting packets ("keep both, mark the conflict") but not **superseded facts inside one packet** — the two-workflow line both states the fact and marks it as contradicting the documentation, and the ad-hoc italics show the format is missing. |
| 4 | **Low** | "Under about sixty lines" is the only size control; there is no rule for what to cut when the frame and the constraints alone exceed it. Here the packet fits, so the rule was not tested — recorded as untested rather than passed. |

## 5. Changes made

`CHAT-HANDOFF` v1.1.0:

- Step 3 gains a fifth label, `generated`, defined as *true when the command ran, produced by the tooling, and expected to change* — with the date required and the command named. Generated counts are the most common fact in a repository handoff and the most dangerous to freeze.
- Step 3 also requires that a fact contradicting the project's own documentation is marked `conflict`, with both claims and where each came from, rather than being written in italics.
- Step 10 supplies a four-line restatement template so the receiving conversation's reply has a shape.
- Step 9 gains a cut order for oversized packets: drop narrative, then restated context, then interesting-but-not-blocking questions; never drop constraints, the completion condition, or an eliminated hypothesis.

## 6. Retest

The packet above was rebuilt from the revised text with the fifth label applied to the four generated counts (`generated, 2026-10-22, validate_library.py`) and the two-workflow fact marked `conflict`. It re-passed the five-question reconstruction, 5 of 5, and the receiving restatement now has a template to fill. The cut order was not exercised: the packet is inside the limit.

## 7. Limitations

- **The cold read was not cold.** The same agent wrote the packet, wrote the five questions, and answered them. The questions are the ones the author expected the packet to answer; a real reader would ask others. This is the single largest weakness of the run, and it is the weakness `CHAT-HANDOFF` exists to prevent.
- The packet was never pasted into a different model or a ticket, so the portability claims are untested.
- No secret appeared in the engagement, so the redaction line is present but vacuous — the prompt's most emphatic requirement was not exercised.
