# Quickstart — start being useful in ten minutes

364 prompts is an archive, not a starting point. This page is the starting point: six situations, the exact prompts to run, in order, with what you should be holding at the end of each.

**Read this instead of the README if you have a job to do today.**

---

## Before anything: what this library can and cannot do

| It can | It cannot |
|---|---|
| Give a capable agent or an engineer a procedure with evidence rules and a definition of done | Make an agent honest; the prompts that check another agent's work exist because of this |
| Tell you when a prompt is an outline rather than a procedure | Guarantee quality — `operational` means *structurally reviewed*, not *proven* (see [`_meta/evidence-levels.md`](_meta/evidence-levels.md): 33 of 281 executed (11.7%)) |
| Prevent a long list of specific, named failures | Replace your judgement about your system |

Use the prompts as an experienced colleague's checklist, not as an authority.

---

## Path 0 — You only have a chat window (no repo access)

If you are in ChatGPT, Claude, Gemini, or any chat interface with no file access, you do not need a different library — you need the capability delta stated up front.

| Step | Prompt | You end with |
|---|---|---|
| 1 | [`00-core/conversational/CHAT-MODE.md`](00-core/conversational/CHAT-MODE.md) | Any prompt in this library adapted for a conversation, with what it cannot verify written down |
| 2 | [`00-core/conversational/CHAT-DEBUG.md`](00-core/conversational/CHAT-DEBUG.md) | One discriminating test at a time instead of five guesses |
| 3 | [`00-core/conversational/CHAT-REVIEW.md`](00-core/conversational/CHAT-REVIEW.md) | A bounded review with the not-assessed list |
| 4 | [`00-core/conversational/CHAT-DESIGN.md`](00-core/conversational/CHAT-DESIGN.md) | An ADR you can file, with what would reopen it |
| 5 | [`00-core/conversational/CHAT-SELECT.md`](00-core/conversational/CHAT-SELECT.md) | One prompt chosen for your situation, with the fact that would change the choice |
| 6 | [`00-core/conversational/CHAT-HANDOFF.md`](00-core/conversational/CHAT-HANDOFF.md) | A packet that lets a fresh chat continue without repeating a disproved hypothesis |

Three rules apply to every chat run: **`verified` means someone ran it and pasted the output**, **redact before pasting** — a consumer chat window is a third party — and **a route without the index is `inferred`, never `verified`**.

---

## Path 1 — Something is broken (30–90 minutes)

You have a failing system and you need it working, not explained.

| Step | Prompt | You end with |
|---|---|---|
| 1 | [`05-scenarios/incident-response/`](05-scenarios/incident-response/PRODUCTION-INCIDENT.md) — if production is down right now | Service restored, timeline started |
| 2 | [`05-scenarios/debugging/`](05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md) | A reproduced defect and a **proven** cause, not a guess |
| 3 | [`05-scenarios/failed-fix/`](05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md) — only if two fix attempts failed | A decision to revert, re-scope, or escalate, with the attempt ledger |
| 4 | [`05-scenarios/incident-communications/`](05-scenarios/incident-communications/INCIDENT-COMMUNICATIONS.md) — in parallel, from step 1 | Customer updates on a cadence, with no speculation |

Do not skip step 2 when the fix looks obvious. The most expensive incidents in most teams are the second and third fixes applied to an unproven cause.

---

## Path 2 — You are taking over something you did not write (half a day)

Inherited repo, abandoned project, a contractor's code, or an agent's half-finished work.

| Step | Prompt | You end with |
|---|---|---|
| 1 | [`02-engineering/project-recovery/`](02-engineering/project-recovery/README.md) — whole system, 7 stages | Containment, a working build, and a written state |
| 2 | [`05-scenarios/onboarding/`](05-scenarios/onboarding/CODEBASE-ONBOARDING.md) — for a codebase that runs but is unknown | A mental model backed by evidence |
| 3 | [`02-engineering/tenancy-audit/`](02-engineering/tenancy-audit/TENANCY-AUDIT.md) or [`05-scenarios/client-secrets/`](05-scenarios/client-secrets/CLIENT-SIDE-SECRETS.md) — if it handles customer data or ships to browsers | The two leaks that hurt most, checked |
| 4 | [`04-process/handover/`](04-process/handover/README.md) — if you are inheriting formally | Capability-tested access, not just credentials |

Workflow version: [`07-workflows/recover-abandoned-project.md`](07-workflows/recover-abandoned-project.md).

---

## Path 3 — You are about to ship (2–4 hours)

A release, a launch, a migration, a big dependency upgrade.

| Step | Prompt | You end with |
|---|---|---|
| 1 | [`04-process/release-engineering/`](04-process/release-engineering/README.md) P01 | A readiness verdict with named conditions |
| 2 | [`05-scenarios/operational-readiness/`](05-scenarios/operational-readiness/OPERATIONAL-READINESS.md) | Proof that on-call can survive this at 03:00 |
| 3 | [`05-scenarios/capacity-planning/`](05-scenarios/capacity-planning/CAPACITY-PLANNING.md) | What runs out first and when |
| 4 | [`05-scenarios/disaster-recovery/`](05-scenarios/disaster-recovery/DISASTER-RECOVERY.md) — at least the backup-chain audit, ideally the drill | A restore that has been performed |
| 5 | [`07-workflows/independent-verification.md`](07-workflows/independent-verification.md) — when an agent or teammate says it is done | Claims checked, not trusted |

If you only have an hour: **step 2 and the six silent backup failures in step 4** catch the releases that become incidents.

---

## Path 4 — Someone is asking for proof (1–3 days)

A security questionnaire, an audit, a customer contract with a standard in it, an enterprise deal.

| Step | Prompt | You end with |
|---|---|---|
| 1 | [`04-process/standards-conformance/`](04-process/standards-conformance/STANDARDS-CONFORMANCE.md) | Requirement → practice → **dated evidence**, per row |
| 2 | [`04-process/governance-compliance/`](04-process/governance-compliance/README.md) | Organisation-level controls mapped and tested |
| 3 | [`02-engineering/access-review/`](02-engineering/access-review/ACCESS-REVIEW.md) | Entitlements from the providers, removals verified |
| 4 | [`04-process/licence-compliance/`](04-process/licence-compliance/LICENCE-COMPLIANCE.md) + [`05-scenarios/supply-chain/`](05-scenarios/supply-chain/SUPPLY-CHAIN.md) | Software obligations and build integrity |
| 5 | [`05-scenarios/data-residency/`](05-scenarios/data-residency/DATA-RESIDENCY.md) | Where the data actually is |

Workflow version: [`07-workflows/compliance-readiness.md`](07-workflows/compliance-readiness.md) — it sequences these with gates and an evidence pack.

**The one rule that saves the most time:** capture evidence for practices you already have before engineering new controls. Days instead of weeks, and it buys the time the real gaps need.

---

## Path 5 — You are building something new (onboarding to a project)

| Step | Prompt | Note |
|---|---|---|
| 1 | [`02-engineering/from-scratch/`](02-engineering/from-scratch/README.md) | **Skeleton.** Use it as a human checklist, not unsupervised |
| 2 | [`04-process/testing-qa/`](04-process/testing-qa/README.md) | Set the safety net before the code volume |
| 3 | [`05-scenarios/dev-environment/`](05-scenarios/dev-environment/DEV-ENVIRONMENT.md) | One command, every machine |
| 4 | [`04-process/agent-context/`](04-process/agent-context/README.md) | If agents will work in the repo, give them one canonical instruction file |

---

## How to run a prompt so it works

1. **Fill the run sheet once.** Copy [`00-core/inputs/RUN-SHEET.md`](00-core/inputs/RUN-SHEET.md); a worked multi-stage example is in [`RUN-SHEET-EXAMPLE.md`](00-core/inputs/RUN-SHEET-EXAMPLE.md).
2. **Paste the prompt plus the sheet**, not the prompt alone. Stages that declare `Inputs` need the values.
3. **Ask for the artifact, not a summary.** Every prompt names what it produces; the artifact is what the next stage reads.
4. **Check the completion criteria yourself.** They are written to be evaluated by a reviewer who trusts nothing — that reviewer is you.
5. **When an agent claims success, run [`07-workflows/independent-verification.md`](07-workflows/independent-verification.md).** Verifying is cheaper than being wrong.

## If you only remember three things

- **`operational` means structurally reviewed.** Read [`_meta/evidence-levels.md`](_meta/evidence-levels.md) before treating any prompt as proven.
- **Skeletons are checklists.** Anything labelled `skeleton` names a sensible sequence and nothing more; supervise it or don't use it.
- **The evidence rules are the value.** `verified` / `inferred` / `unknown` is the discipline that separates this from a list of suggestions.

---

**Next:** [`README.md`](README.md) for routing by symptom, [`TASKS.md`](TASKS.md) for the library indexed by problem, [`GALLERY.md`](GALLERY.md) for all 364 prompts, [`_meta/ROADMAP-AND-BACKLOG.md`](_meta/ROADMAP-AND-BACKLOG.md) for what is deliberately unfinished.
