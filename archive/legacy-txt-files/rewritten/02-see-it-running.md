<!-- not-a-prompt -->

# Rewrite 02 — "how will I see it, give me the step by step"

**Source:** [`../process3(chat1).txt`](../process3%28chat1%29.txt) — 1 sentence, 67 bytes
**Status:** archive rewrite.
**Closest library prompt:** `05-scenarios/deployment-target/DEPLOY-TO-PLATFORM.md` (`DEPLOY-01`).

---

## 1. The original, verbatim

> Now, how will i see it, give the step by step process of what to do

## 2. The correction that matters most in this whole folder

**This is not a prompt. It is the third turn of a conversation.**

The word "it" refers to something named two files earlier, and "now" refers to the state the previous
answer left behind. Read alone — which is how an archive is read — it is unanswerable. Any model
receiving it has to invent what "it" is, and will invent confidently.

That distinction is worth stating plainly because `../README.md` describes this folder as *"the raw
prompts and requests that the current library was built from"*. Three files here
(`process3`, `process4`, `process7`) are fragments of a chat, not prompts. They are still worth keeping —
they show what people actually type — but calling them prompts flatters them.

## 3. What it was trying to say

*"I have something built. I want to look at it running — properly, at a URL, on the internet, not only
in my terminal. Give me the ordered steps from the state I am in now to a page I can open on my phone,
including the accounts, the commands, and the decisions I have to make along the way."*

The two things that were missing from the original are the two that decide the answer:

1. **Where does it run now?** A local `npm run dev`, a Docker container, or nothing at all — three
   different procedures.
2. **Who needs to see it?** Only the author, a teammate on the same network, or a stranger with a link.
   Only the third one needs a host, a domain, and a certificate.

## 4. The rewritten prompt

> **Role.** You are taking an application from "it runs on my machine" to "someone else can open it at a
> URL". You are a deployment guide, not an architect: you name the decisions, state the default for
> each, and give the ordered procedure for the path the user is actually on.
>
> **Inputs.** `{{REPO_PATH}}`, `{{CURRENT_STATE}}` (*not running* / *runs locally* / *runs in Docker* /
> *deployed but broken*), `{{AUDIENCE}}` (*only me* / *my team* / *anyone with the link*), and
> `{{SPEND_LIMIT}}` (a platform that costs money needs one).
>
> **Step 1 — establish the truth before the steps.** Inspect the repository: runtime and version,
> package manifest, build command, start command, the port and host it binds to, environment variables
> the code reads, any database or external service, and whether a container definition exists. Report
> what you found with the file that shows it. **If the app cannot start locally, say so and stop** —
> deployment cannot fix a build that does not build.
>
> **Step 2 — decide the target, and say why.** Name the target for this state and audience (a
> platform-as-a-service for a first URL, a container host when a database or a long-running worker is
> involved, a plain VM only if something needs a real filesystem). State the monthly cost at the tier
> you would choose, and the one thing that would make you choose differently.
>
> **Step 3 — list the accounts and secrets before the commands.** Every account, every environment
> variable, every credential, and where each one lives. **Names only, never values.** If a value must be
> created, say where the user creates it and what to do with it — do not ask for it in the conversation.
>
> **Step 4 — give the procedure as numbered steps that each end in a check.** Not "configure the
> build"; *"set `NODE_ENV=production` in the platform's environment settings, then re-deploy and confirm
> the build log shows the production build"*. Every step states what the user should see when it worked.
>
> **Step 5 — the end-to-end check, from outside.** The page loads in a browser that is not the user's
> development machine, on a network that is not theirs (a phone on mobile data is the cheapest test), a
> real request returns a real response from the real datastore, and the logs show that request. A URL
> that returns a holding page is not a deployment.
>
> **Step 6 — the way back.** The command or click that reverts to the previous version, and whether it
> was exercised. A deployment without a rollback is a one-way door.
>
> **Failure handling.** Build fails on the platform but not locally → the platform's clock, image, or
> environment differs; diff the two rather than changing code. The app starts but every request 500s →
> check environment variables in the platform's scope, then the entry point and port binding. A secret
> was pasted into a chat or a commit → stop, rotate it, and say so plainly.
>
> **Done when:** the URL is reachable by someone who is not the author, the end-to-end check in step 5
> passed, the environment map is written down with names but no values, and a rollback exists and was
> tried once.

### What changed, phrase by phrase

| Original | Rewritten as | Why |
|---|---|---|
| "how will i see it" | `{{CURRENT_STATE}}` + `{{AUDIENCE}}` as required inputs | "it" had no antecedent and "see" has three different meanings |
| "step by step process" | numbered steps that **each end in an observable check** | a step you cannot check is a paragraph, not a step |
| "what to do" | decisions first (target, accounts, cost), then commands | the decisions are where people get stuck, and they were invisible in the original |
| *(absent)* | "if the app cannot start locally, say so and stop" | deployment cannot repair a broken build, and a guide that pretends otherwise wastes an afternoon |
| *(absent)* | the step-5 end-to-end check, from another network | "it works" on the author's laptop is the specific failure this prompt exists to prevent |
| *(absent)* | names-only secret handling | the original request is exactly where a user pastes a token into a chat |

## 5. Does the library cover this now?

**Yes — `DEPLOY-01`.** It covers the platform decision, the target profile, the real end-to-end check,
and the exercised rollback, with provider-specific traps in `PLATFORM-PROFILES.md`. The rewrite above is
a plainer version of the same procedure for a user who just wants a URL; run `DEPLOY-01` when the work
matters.

The gap that remains is not deployment but **"is it running anywhere I can see"** for a person who has
never deployed anything — that is a teaching aid, not an engineering prompt, and it does not belong in
a library of procedures.
