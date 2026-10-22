<!-- not-a-prompt -->

# Routing fixture — fourteen requests with a ground truth the repository defines

**Purpose:** test `WIZ-P01` (System Selector) against a fixed set of requests whose correct
destination is **already written down in this repository**, so the score does not depend on the
selector's author agreeing with the selector's author.

**Ground truth source:** [`TASKS.md`](../../../TASKS.md) — the generated index of 21 situations. Each
request below names the `TASKS.md` section it belongs to and the destination that section's
**Start here** line names. Where a section gives two destinations for two conditions (slow now vs
invoice is the symptom), the request is written so exactly one condition holds.

**Grading:** for each request the selector must produce

1. a **destination path that exists in the repository** (checked with `ls`), and
2. the destination the ground-truth column names — or the other branch of the same section's
   "Start here" line, which is also correct.

A plausible-sounding path that does not exist is a **fail**, not a partial: every downstream prompt
in this library is addressed by path.

| # | The user's words (as a requester would type them) | TASKS.md section | Ground-truth destination |
|---|---|---|---|
| 1 | "The checkout service started 500ing about twenty minutes ago and it's still going." | Something is broken right now | `05-scenarios/incident-response/` (repo access, live failure) |
| 2 | "I just joined a team and inherited a 200k-line Go repo. I have no idea where anything is." | I have to work in a codebase I have never seen | `ONBOARD-01` — `05-scenarios/onboarding/` — the orientation document the section's Start here line names |
| 3 | "I need to rename a config key across twelve services without breaking anything." | I need to change existing code without breaking it | `02-engineering/refactoring/` (not a small change) |
| 4 | "We want to build a notification service from scratch, team of three, six months." | I am starting something from nothing | `02-engineering/from-scratch/` |
| 5 | "Before we raise the next round I need an honest picture of whether this codebase is healthy." | I need to know whether this codebase is healthy | `02-engineering/codebase-audit/` |
| 6 | "Cutting a release on Friday and I want a checklist that isn't vibes." | I am shipping a release | `04-process/release-engineering/` |
| 7 | "We have 400 tests, they pass, and I still don't believe them. Where do I start?" | I need confidence that the tests mean something | `04-process/testing-qa/` |
| 8 | "Someone pasted a 300-line diff into Slack and asked me to review it." | I have to review a change, or get mine reviewed | `CHAT-REVIEW` (the diff arrives as a paste) |
| 9 | "I'm taking over on-call for a system next week and I've never run it." | I am handing over a system, or taking one over | `05-scenarios/on-call-handover/` (rota change at speed) |
| 10 | "The AWS bill doubled and nobody knows why." | Something costs too much or runs too slowly | `03-domains/cost-engineering/` (invoice is the symptom) |
| 11 | "Legal says we must delete every record for a customer who exercised their rights, and prove it." | I need to move or delete data | `04-process/privacy-requests/` (legal obligation) |
| 12 | "We're adding an agent that can open PRs on our own repo and I want guardrails before it does." | I am building with AI or agents | `03-domains/ai-agentic/` |
| 13 | "I need to ship something to app stores in six weeks and I'm not sure the auth flow is right." | I am building a specific kind of application | `03-domains/mobile/` |
| 14 | "I only have ChatGPT, no repo access, and I need to know whether this AI-written function is safe." | I only have a chat window | `00-core/conversational/CHAT-MODE.md` — the section names no other destination |

## Why these fourteen

They are not random. They span:

- **six sections whose destination systems did not exist when `WIZ-P01` was written** —
  `release-engineering`, `testing-qa`, `cost-engineering`, `ai-agentic`, `on-call-handover`,
  `privacy-requests` — which is the documented gap at `06-interactive/README.md` §3;

**A correction to this fixture's first draft, kept visible:** it named `project-recovery` for request 2
and `ai-output-verification` for request 14. Both were checked against `TASKS.md` and both were wrong —
that section's *Start here* line names `ONBOARD-01`, and the chat section names only the `CHAT-*`
prompts. The ground truth is what the index says, not what an author remembers, which is the same
finding the selector itself was rewritten for.
- **three sections where two destinations are both legitimate and the condition decides** (2, 10, 14) —
  this is where a selector that names one system without checking the condition is wrong half the time;
- **one chat-only request** (8, 14) where the correct answer is a different prompt *and* a different
  capability assumption;
- **one request whose wording points at a folder that is not the right one** (13: "auth flow" suggests a
  security prompt; the section and the ground truth are the mobile system).

## What the score means

A selector that scores 14/14 has routed correctly on a fixture whose answers it did not write. A
selector that scores well by naming folders that do not exist has learned nothing: the second
grading condition exists so that confidence cannot substitute for a path.
