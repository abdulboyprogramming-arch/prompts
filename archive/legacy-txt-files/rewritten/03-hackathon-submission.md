<!-- not-a-prompt -->

# Rewrite 03 — "it's a hackathon, I don't know what's next"

**Source:** [`../process4(chat1).txt`](../process4%28chat1%29.txt) — 1 paragraph, 315 bytes
**Status:** archive rewrite.
**Closest library prompt:** `05-scenarios/hackathon-sprint/HACKATHON-SPRINT.md` (`HACK-01`).

---

## 1. The original, verbatim

> Please, i need you to help me. Actually it's an hackathon, i don't know what's next for the demo and
> submission process. how am i to do it now...what's next? Is it deployment how... what are the stuff or
> data needed. please, see me like a nerd who you have to be instructing with the step by step
> procedures in order

## 2. What it was trying to say

*"I am in a hackathon and I have lost track of the process. I do not know what has to be submitted,
in what form, by when, or what I have to prepare before the demo. I also do not know whether deploying
is part of it. Treat me as someone who has never done this: give me the ordered steps, and tell me what
I need to have ready — accounts, links, a video, a repository, a slide — before each deadline."*

The emotional register is part of the meaning: *"please, see me like a nerd who you have to be
instructing"* is asking for a tone, not for more analysis. A rewrite that produces a beautiful
strategic framework and no ordered steps has failed the actual request.

## 3. Why the original fails as a prompt

| Defect | Consequence |
|---|---|
| **five questions in one paragraph** | the model answers whichever it notices first, usually the interesting one (architecture) and not the urgent one (what gets submitted) |
| **no date, no deadline, no timezone** | every recommendation about "what's next" depends on how long is left; without it the answer is generic |
| **no judging criteria** | a demo optimised for a technical judge and one optimised for a business judge are different demos |
| **the ask is for a process, but the process is the event's, not the model's** | a model does not know this hackathon's rules; it must be told to ask for them rather than invent them. The original never says who knows the rules |
| **"what are the stuff or data needed"** is a list request with no list | the most useful output — accounts, links, artifacts — is the one easiest to skip |
| **no state** | nothing says what already exists: a repo, a demo, a pitch, a deployed URL |

## 4. The rewritten prompt

> **Role.** You are the person who has run hackathon submissions before. You are not going to write the
> product plan; you are going to make sure this team submits something that can be opened, judged, and
> seen working, by the deadline. Assume the user has never done this.
>
> **Inputs.** `{{DEADLINE}}` — date, time, and timezone; `{{RULES_SOURCE}}` — the event's rules page,
> submission form, or the exact text the organisers gave; `{{JUDGING_CRITERIA}}` if published;
> `{{WHAT_EXISTS}}` — repository, running demo, pitch deck, video, team members; `{{TEAM_SIZE}}`.
>
> **Step 1 — get the rules before the advice.** Read `{{RULES_SOURCE}}`. If it is missing, say exactly
> what you need from it (submission platform, artifact list, deadline, demo length, judging criteria)
> and stop on those points rather than guessing. **Never invent a hackathon's rules**: the cost of being
> wrong is disqualification, and it is the one failure a model cannot detect.
>
> **Step 2 — work backwards from the deadline.** Produce a timeline in absolute times, not durations:
> *"T−24h: submission form complete with placeholder video. T−6h: demo path frozen. T−2h: video
> recorded. T−30min: link re-checked from a phone."* Every entry names who does it and what "done" looks
> like.
>
> **Step 3 — the submission inventory.** A table of every artifact the rules require: the form fields,
> the repository link, a public URL, the video, the slide deck, the team roster, the licence, any
> account that must be created *before* the deadline. For each: does it exist, who owns it, what is
> missing. **This table is the answer to "what's next"** — everything else is commentary.
>
> **Step 4 — the demo path.** The exact sequence of screens or commands the judges will see, in order,
> with the data already loaded and the failure-prone step named. A four-minute demo cannot include a
> live sign-up, a payment, a network call to a service that may be rate-limited, or anything that takes
> more than two seconds to respond.
>
> **Step 5 — what is real and what is faked.** A short list: what genuinely works, what is hard-coded,
> what is mocked, what was skipped. This protects the team in the Q&A, where a judge asks "does it
> actually do that?" and a confident answer matters more than the answer itself.
>
> **Step 6 — deploy only what the rules require.** If the submission needs a public URL, that is a
> deployment, and it must be done **before** the final hour — a deploy that fails at T−20min is the
> most common way a finished hackathon project is never seen. If the rules accept a video, record the
> video from a working local build and treat the URL as a bonus.
>
> **Failure handling.** Rules unreadable → ask for the four facts in step 1 and say what you will assume
> otherwise. No deployable path → record the demo as a local run-through on video, and say so in the
> submission text rather than implying a live system. Time already short → cut scope in this order:
> features the demo does not touch, then screens after the judged flow, then polish. **Never cut the
> video, the form, or the link check.**
>
> **Done when:** every required artifact exists and can be opened by someone who is not on the team; the
> timeline has no step scheduled in the last thirty minutes except re-checking links; and the
> real-versus-faked list is written.

### What changed, phrase by phrase

| Original | Rewritten as | Why |
|---|---|---|
| "i don't know what's next" | a submission inventory table + a backwards timeline in absolute times | "what's next" is answered by a list of artifacts and owners, not by advice |
| "how am i to do it now...what's next?" | `{{RULES_SOURCE}}` as a required input, with an instruction never to invent rules | the rules belong to the event; a model that improvises them is dangerous |
| "Is it deployment how" | "deploy only what the rules require", with the T−1h constraint | deployment is a means to a judged artifact, not a goal |
| "what are the stuff or data needed" | the inventory: accounts created *before* the deadline, video, deck, roster, licence | the phrase was asking for exactly this list and had nowhere to put it |
| "see me like a nerd who you have to be instructing" | "assume the user has never done this", and steps that each end in an observable result | the tone request is real; the rewrite keeps it as an operating instruction |
| *(absent)* | the real-versus-faked list | the Q&A is judged, and honesty under pressure is a deliverable |

## 5. Does the library cover this now?

**Yes — `HACK-01`**, which is stricter than the rewrite: it fixes the priority order (demo path works →
submission opens → what is real is recorded), forces the scope cuts in writing at the start rather than
at 3 a.m., and treats a rushed credential as a risk-class escalation.

The rewrite keeps one thing `HACK-01` assumes: that the rules are knowable. For a first-time
participant, the rules are the part they do not know to look for — which is why step 1 exists here and
not there.
