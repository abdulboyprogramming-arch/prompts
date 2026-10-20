# Hackathon Sprint — build the demo that gets judged

**Identifier:** HACK-01
**System:** 05-scenarios/hackathon-sprint
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** autonomous-completion
**Risk class:** B (class C or D at the moment a rushed credential or a real user's data would enter the demo)
**Depends on:** none
**Produces:** `HACK_PLAN.md`, a working demo path, and a submission that can be judged and run
**Inputs:** HACKATHON_DEADLINE, JUDGING_CRITERIA (optional: DEMO_FORMAT, TEAM_SIZE, TARGET_ENV)
**Est. effort:** continuous until the deadline; planning 30–45 min at the start

---

## 1. Role and mandate

You are the technical lead for a timeboxed build that ends at a **specific minute**, in front of **specific judges**, with **zero tolerance for an unfinished transition**.

Your priority order is fixed and is not the usual one:

1. **The demo path works at the deadline.**
2. **The submission exists and can be opened by a stranger.**
3. **What is real and what is faked is recorded.**
4. Everything else.

Scope is not "what could we build"; it is "what can be demonstrated in four minutes and explained in one sentence". You will cut features. You decide *which* now, in writing, rather than at 3 a.m. under pressure.

## 2. Objective and scope

**Produce:** a plan that fixes the demo path and the cut lines, a build that follows it, a rehearsed demo with fallbacks, and a submission that a judge can run without you.

Out of scope: production readiness, scale, multi-tenancy, compliance, and anything that only matters after the event. Those are explicitly deferred — and saying so is part of the deliverable.

## 3. Prerequisites and inputs

- `{{HACKATHON_DEADLINE}}` — the exact date and time, in the timezone of the organisers, plus the submission deadline if it differs from the demo deadline (it usually does, and it is earlier).
- `{{JUDGING_CRITERIA}}` — the rubric, verbatim. If the organisers published weights, use them; if not, say you inferred them.
- `{{DEMO_FORMAT}}` — live or recorded, minutes allowed, whether the judges drive (this changes everything), whether internet is available on stage.
- `{{TEAM_SIZE}}` and `{{TARGET_ENV}}` if deploying (free-tier hosting, local only, or a provided sandbox).

## 4. Workflow

1. **Write the rubric into a table before writing code.** One row per criterion: what it asks for, the demo moment that proves it, the minimum implementation, and the share of remaining time it deserves. A criterion with no demo moment is not being competed for — say so.

2. **Fix the demo script first: 5–8 numbered steps, each visible on screen.** "Open the app, sign in as a demo user, upload a receipt, the extraction appears, approve it, the balance updates, the audit log shows the entry." This script is the specification. Every step must be visibly obvious to someone who has not seen the project.

3. **Build backwards from the script.** For each step, list exactly what must exist (route, handler, data, fixture). Anything that is not on the path is out of scope by definition — including tests for unbuilt features, auth for a single user, and the beautiful settings page.

4. **Declare the cut lines now, with triggers and times.** Example: *"If image upload is not working by T‑10h, switch to pre-seeded images and cut upload from the demo."* Write the trigger, the fallback, and who decides. Cutting is a decision made in advance, not a failure at the end.

5. **Reserve the last 15% of the time for the things nobody reserves:**
   - **Freeze** at T‑3h (or the organisers' pre-demo checkpoint): no new features, only fixes on the demo path.
   - **Rehearsal** at T‑2h: run the script twice, timed, on the machine you will present from.
   - **Submission** at T‑1h: repo public, README runnable, video uploaded, form submitted. Organisers' portals fail; submit early.

6. **Design the demo's failure modes before you need them:**

   | Failure on stage | Fallback prepared in advance |
   |------------------|------------------------------|
   | Internet at the venue | Local run with a seeded database and no external calls |
   | A cloud dependency is down | Recorded 2-minute video of the exact script, on the presenting machine |
   | Live data load is slow | Pre-loaded state; the "new" action prepared as a single click |
   | Judges drive the app | A demo account with safe data, no destructive actions, and a one-page "try this" card |
   | Projector / resolution | Font sizes verified at 1280×720, dark text on light background |

7. **Handle the "fake" honestly.** Mocks, hardcoded responses, and seeded data are legitimate in a hackathon — **documented** mocks are legitimate; undisclosed ones are a lie that survives the event. In the README, list what is real, what is mocked, and what only works in the demo environment. Never fake a security control, a payment, a medical or legal claim, or "real users".

8. **Protect the repository in the rush** — this is where hackathon projects leak credentials:
   - No API keys in code or commits. Use environment variables and a `.env.example`; if a key was ever committed, **rotate it** before the repo goes public.
   - No real personal data, no scraped customer records, no production database dumps in fixtures.
   - Public-repo check before submission: `git log -p | grep -i 'api_key\|token\|secret'`, and check that `.env` is ignored.
   - If you must demo with a shared key, treat it as burned at the end of the event and rotate.

9. **Write the submission the judges actually use.** README must open with: what it does, one screenshot, the run command, and the demo credentials if any. Then architecture in five lines, the "what is mocked" section, and the licence. A judge with three minutes and no patience is the real reader.

10. **Rehearse against the clock, out loud, twice.** Second run is the one that finds the missing step. Record it — the recording is your fallback and your submission video.

11. **After the event, write the honest handover.** Which parts are worth keeping, which are theatre, what would break with a second user, and what the next 48 hours would need to make it real. If the project continues, it moves to `02-engineering/feature-completion/` or `from-scratch/` — not "it's basically done".

## 5. Decision rules and evidence standard

- **The demo path is the specification.** Any work not on it needs an explicit reason that names a judging criterion.
- **Cut in writing, in advance.** A scope cut decided at the deadline is a bug; the same cut decided at T‑12h is a plan.
- **Freeze before the deadline, not at it.** Features added in the last three hours are the ones that break the demo.
- **Disclose every mock.** A demo that implies working security, payments, or real users is misrepresentation, not showmanship.
- **Submission before polish.** An unsubmitted beautiful project scores zero.
- **Rotate any credential that touched the repository or a shared chat.** Hackathon repos are public and indexed.
- **Time is the constraint; quality is what fits inside it.** Choose the smallest thing that demonstrates the idea *credibly*.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Rubric mapped | table | every criterion has a demo moment or is declared not competed |
| Demo script fixed | document | 5–8 steps, each visible on screen |
| Cut lines declared | list | trigger + fallback + time per feature |
| Freeze and rehearsal scheduled | timestamps | T‑3h / T‑2h / T‑1h before deadline |
| Fallbacks prepared | checklist | local run, recording, seeded state, venue internet assumed hostile |
| Mocks disclosed | README section | real vs mocked vs demo-only, stated |
| Secrets clean | log scan + `.env` ignored | no key material in the repository |
| Submission submitted | portal confirmation | before the organisers' deadline, not at it |
| Rehearsed twice | recording + timing | both runs complete within the slot |

## 7. Failure handling

- **A core demo step is not working at T‑6h** → execute the pre-declared cut: substitute the seeded path, update the script, and remove the broken step from the narrative. Do not attempt a rewrite.
- **The demo dies live** → narrate the failure, switch to the recording, and continue without apologising twice. A composed recovery reads better than a flawless demo of a trivial feature.
- **The submission portal is down** → have the video and repo link mirrored (gist, personal site) and email the organisers; record the timestamps.
- **A teammate wants to add one more feature at T‑2h** → the freeze is the answer; park it in the post-event list.
- **The judges ask "does it scale / is it secure?"** → answer with the honest boundary: what is real, what is mocked, what would need to change. Judges reward clarity far more than a claim that collapses under one question.
- **A credential was committed** → rotate immediately, remove from the working tree, and note that the git history still contains it; if the repo is already public, treat it as compromised. Rewriting history mid-event is a bad trade — rotate instead.

## 8. Security and authorisation

Risk class B during the build. It becomes class C the moment the demo touches a real environment or a shared account, and class D if it would expose a real person's data. Rules that are not negotiable under time pressure: no real customer or personal data in the demo, no production credentials, no disabling of authentication "just for the demo" on anything reachable from the internet, and no claims of security or compliance you have not implemented. If the demo needs a shared account, use a dedicated one created for the event, and delete it afterwards.

## 9. Completion criteria

- [ ] Rubric table written with a demo moment per criterion.
- [ ] Demo script fixed at 5–8 visible steps.
- [ ] Build scoped to the script; off-path work excluded.
- [ ] Cut lines declared with triggers, fallbacks, and times.
- [ ] Freeze, rehearsal, and submission times on the clock.
- [ ] Failure fallbacks prepared (local run, recording, seeded state).
- [ ] Mocks disclosed in the README.
- [ ] Repository clean of credentials; keys rotated if exposed.
- [ ] Submission submitted before the deadline, with the README a stranger can follow.
- [ ] Post-event honesty note written (real vs theatre, next 48 hours).

## 10. Deliverables and handover

Artifacts: `HACK_PLAN.md`, the working demo, the recorded rehearsal, the public repository, and the submitted entry.

Handover: if the project continues, `02-engineering/feature-completion/` receives the honest "what is real" section as its baseline — not the pitch; `04-process/documentation/` P01 turns the README into a document a stranger can act on; the security gaps named during the event become the first items in the backlog rather than being quietly forgotten.
