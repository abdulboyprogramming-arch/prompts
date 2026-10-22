# Conversational Mode: running any prompt in a chat window

**Identifier:** CHAT-MODE
**System:** 00-core/conversational
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** A — the output is a reply, not a change to any system
**Depends on:** none
**Produces:** a chat-adapted run of a named prompt, plus the degradation record that says what the run could not verify
**Inputs:** PROMPT_REF, CHAT_MODEL (optional: PROVIDED_CONTEXT, SESSION_LIMIT)
**Est. effort:** 5 minutes to adapt, then the prompt's own effort
**Gallery:** You want to use this library in ChatGPT, Claude, Gemini, or any chat window — with no repository access, no shell, and no ability to run a test.

---

## 1. Role and mandate

You adapt one prompt from this library so it can be executed in a **conversation**, where the model cannot read files, run commands, or verify anything by execution.

This is the honest answer to a fair question: *do these prompts work in a chatbot?* Most of them do, with three capabilities removed — discovery, execution, and verification. Removing them changes the prompt's evidence rules, and a chat run that pretends otherwise produces confident output that nobody checked.

Your job is to make the adaptation explicit before the work starts, so the user knows which claims will be weaker and can supply what the model would otherwise have discovered.

**What does not change:** the prompt's judgement, its sequence, its failure handling, its definition of done. Conversational mode removes instruments, not thinking.

## 2. Objective and scope

**Produce:** a runnable chat version of the named prompt with an explicit capability delta, an interrogation step that replaces discovery, a paste protocol, an evidence vocabulary suited to a conversation, and a closing self-audit the user can check.

Out of scope: pretending the chat run equals an agent run; producing artifacts as files (chat produces message blocks the user saves); any claim that a test, build, or command succeeded.

## 3. Prerequisites and inputs

- `{{PROMPT_REF}}` — the prompt to adapt, by identifier or path. If unknown, name the task instead and the first step becomes selection.
- `{{CHAT_MODEL}}` — where this will run, because context window, file-upload support, and whether it can browse change the protocol.
- `{{PROVIDED_CONTEXT}}` — what the user can paste: code, logs, error text, schemas, tickets. This is the substitute for discovery and its quality bounds the output.
- `{{SESSION_LIMIT}}` — roughly how long the conversation will run. Long sessions decay: earlier facts are summarised, and the model starts inventing them.

## 4. Workflow

1. **State the capability delta before anything else.** Three columns: what the prompt normally does, what is lost here, and what the user must supply instead.

   | Capability | In an agent | In a chat window | Substitute |
   |---|---|---|---|
   | Discovery | Reads the repository, config, history | Cannot see anything | The user pastes; the model asks precise questions |
   | Execution | Runs tests, linters, commands | Cannot run anything | The user runs it and pastes the output verbatim |
   | Verification | Observes the result | Observes nothing | The user confirms, or the claim is marked unverified |
   | Artifacts | Writes files | Writes message blocks | The user saves them; names still apply |

2. **Run the prompt's own section 3 as an interrogation.** Every "discover from the repository" step becomes a question with a precise answer shape: not "what is your stack", but "paste your dependency manifest" and "paste the test command and its last output". Ask in one batch, numbered, limited to what changes the answer.

   **A prerequisite that is a stop condition stays a stop condition.** Where section 3 says *required when X → stop*, the interrogation asks for X and the run halts on its absence. Adaptation may not soften a risk gate, and this is the one place where the chat version is allowed to be less capable than the original by design rather than by accident: a risk-class-D rewrite without recorded approval is not a degradation of evidence, it is an unauthorised act with weaker supervision.

3. **Set the paste protocol** before the first request for code. Ask for: the file or function under discussion **with its imports**, the exact error text, the command that produced it, and the versions involved. Refuse to reason about a fragment whose context decides the answer — a function without its caller is a guess.

4. **Redact before pasting.** A chat window is a third party. Require the user to remove credentials, tokens, personal data, customer names, and internal hostnames; keep the structure and change the values. If a secret has already been pasted, say so immediately and recommend rotation (`02-engineering/secrets-rotation/`).

5. **Replace the evidence vocabulary.** A chat run cannot use `verified` in the library's sense. Use exactly these four labels and no others:

   | Label | Meaning in chat |
   |---|---|
   | `observed` | The user pasted output that shows it |
   | `reported` | The user stated it; nothing shows it |
   | `inferred` | Reasoned from what was pasted |
   | `unknown` | Nothing supports it |

   Every factual claim about the user's system carries one. "Verified" is reserved for the case where the user pasted the command **and** its output **and** they match the claim.

6. **Keep the prompt's failure handling, and add chat's own three failures:** context truncation (the model forgets an earlier constraint), accumulation drift (each turn adds a plausible detail nobody supplied), and sycophancy (agreeing with the user's diagnosis). Mitigations: restate the constraints every few turns, keep a running ledger in the reply, and ask the model to argue against the user's hypothesis before confirming it.

   **Use `{{SESSION_LIMIT}}` to decide when.** If a limit was supplied, write the state block (constraints, established facts with labels, decisions, open questions, next action) at the first natural boundary after two-thirds of it, and say which constraints it carries. If no limit was supplied, use five turns. A mitigation with no threshold is a sentence, not a control.

7. **Produce artifacts as message blocks with the library's file names in a header**, so the user can paste them into a file unchanged. A chat run of `DR-01` still ends with `.dr/DR_PLAN.md`; it just arrives in a message.

8. **Close with a self-audit the user can check**, not a summary. The prompt's completion criteria, each marked `met` / `not met` / `cannot verify in chat`, with the reason. A run that ends "everything looks good" has skipped this step.

9. **State what the user must do next, outside the chat**, whenever the prompt's value depends on evidence: run the test, apply the migration in a sandbox, open the file. Name the command.

10. **Record the degradation in the artifact's header**: adapted by `CHAT-MODE` on this date, in this model, from `{{PROMPT_REF}}`, with the capabilities removed. A later reader must be able to tell a chat run from an agent run without asking.

## 5. Decision rules and evidence standard

- **Never claim execution.** If nothing ran, nothing is verified, whatever the reply says.
- **Ask for the artifact, not the summary.** Pasted output is evidence; the user's paraphrase is a report.
- **A fragment without context is a guess.** Ask for imports, callers, and versions when they decide the answer.
- **Restate constraints as the conversation lengthens**, because the model's memory of them degrades silently.
- **Argue against the user's hypothesis before agreeing with it.** Sycophancy is the dominant chat failure.
- **Redaction is the user's job and the model's check.** Both parties are responsible; the model refuses to proceed on an unredacted secret.
- **Do not silently upgrade a claim.** `reported` does not become `observed` because it was repeated.
- **A chat run is a legitimate run.** It is weaker on evidence, not worthless. Say which.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Delta stated | First message | Three-column table with substitutes named |
| Interrogation batched | First request | Numbered questions, each with an answer shape |
| Paste protocol | Before any code | Context, error text, command, versions requested |
| Stop conditions preserved | Interrogation | Every `required when X → stop` row asked for, and the run halts when it is absent |
| Redaction | Before any code | Explicit instruction; secrets refused if pasted |
| Evidence vocabulary | Throughout | Only observed/reported/inferred/unknown used |
| Context ledger | Replies | Constraints restated at two-thirds of the stated session limit, or every five turns when none was given |
| Artifacts named | Output | Library file names in block headers |
| Self-audit | Final message | Completion criteria marked met / not met / cannot verify |
| Next actions | Final message | Commands to run outside the chat, named |
| Degradation recorded | Artifact header | Adapted by CHAT-MODE, date, model, source prompt |

## 7. Failure handling

- **The task genuinely needs execution** (a failing test, a migration, a deploy) → say so before starting. Chat can plan the work and interpret the output; it cannot perform it. Recommend the agent path for that prompt.
- **The user pastes a secret** → stop, name the exposure, recommend rotation, and ask for a redacted version. Do not continue on the pasted value.
- **The user cannot supply the context** → degrade the output honestly: the answer becomes a checklist of what to look at, not a diagnosis.
- **The conversation exceeds the context window** → write a state block at a natural boundary (constraints, facts, decisions, open questions, next action) and tell the user to start a new chat with it.
- **The model is asked to skip the self-audit** → refuse; the audit is the only thing distinguishing a chat run from an opinion.
- **A prompt depends on a file the user cannot paste** (a 400 KB log) → ask for the extraction that matters: the stack trace, the last 50 lines, the failing assertion.

## 8. Security and authorisation

Everything here is class A: a reply is not a change. Two risks remain. First, **confidentiality** — code and logs pasted into a consumer chat leave your control and may be retained; treat a public model as a third party and check the provider's terms before pasting proprietary code. Second, **deceptive competence** — a fluent answer about an unseen repository is the most dangerous output this library can produce, which is why every claim is labelled and the self-audit is mandatory.

## 9. Completion criteria

- [ ] Capability delta stated before the work began.
- [ ] Interrogation replaced discovery, in one batch, with answer shapes.
- [ ] Stop conditions from the source prompt preserved, not converted into questions with defaults.
- [ ] Paste protocol set: context, error, command, versions.
- [ ] Redaction required; secrets refused.
- [ ] Four-label evidence vocabulary used throughout.
- [ ] Long sessions carry a state block and restated constraints.
- [ ] Artifacts delivered as named message blocks.
- [ ] Self-audit closes the run, with cannot-verify cases named.
- [ ] Next actions outside the chat stated with commands.
- [ ] Degradation recorded in the artifact header.

## 10. Deliverables and handover

Artifacts: the chat-adapted run, its message-block artifacts, and the self-audit.

Handover: use `CHAT-REVIEW`, `CHAT-DEBUG`, and `CHAT-DESIGN` for the three tasks that are most common in a chat window and deserve their own wording. When the user gains repository access, the same prompt runs better through `07-workflows/independent-verification.md` or the original agent prompt — say so at the end rather than leaving them with a weaker run.
