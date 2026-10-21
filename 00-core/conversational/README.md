# Conversational Mode — using this library in a chat window

**Maturity: operational (v1.0.0).** Four prompts that make the library usable when the only tool available is a conversation: ChatGPT, Claude, Gemini, or any chat interface with no file access, no shell, and no ability to run a test.

## The question this answers

> *Do these prompts work in a chatbot?*

**Most of them, with three capabilities removed.** The library was written for agents that can read a repository, run commands, and observe results. A chat window has none of those. What survives is the part that matters most: the judgement, the sequence, the failure handling, and the definition of done.

| Capability | Agent | Chat window | Consequence for the run |
|---|---|---|---|
| Discovery | Reads files, config, history | Nothing | The model must **ask**, and the user must paste |
| Execution | Runs tests and commands | Nothing | The user runs; the model interprets |
| Verification | Observes the outcome | Nothing | Claims are labelled, never verified |

A chat run is a legitimate run. It is weaker on evidence, not on thinking — and the difference is recorded in the artifact so a later reader can tell which kind of run produced it.

## Contents

| Prompt | Use when | Produces |
|---|---|---|
| [`CHAT-MODE.md`](CHAT-MODE.md) | You want to run **any** prompt from this library in a conversation | An adapted run with an explicit capability delta and a self-audit |
| [`CHAT-REVIEW.md`](CHAT-REVIEW.md) | You are pasting code or a diff for review | A bounded review with severities, the missing-context list, and what was not assessed |
| [`CHAT-DEBUG.md`](CHAT-DEBUG.md) | Something is broken and you can only paste the error | A ranked hypothesis set, one discriminating test at a time, and an evidence ledger |
| [`CHAT-DESIGN.md`](CHAT-DESIGN.md) | You are choosing between approaches | An ADR with rejected options, reversibility, and what would reopen the decision |

## The three rules that make chat runs honest

1. **`verified` means someone ran it and pasted the output.** Everything else is `observed`, `reported`, `inferred`, or `unknown`. A fluent answer about an unseen repository is the most dangerous output this library can produce.
2. **Redact before pasting.** Code, logs, and errors pasted into a consumer model leave your control. Remove credentials, personal data, customer names, and internal hostnames — keep the structure, change the values. If a secret is already pasted, rotate it.
3. **The self-audit closes every run**, with each completion criterion marked `met`, `not met`, or `cannot verify in chat`. A run that ends "everything looks good" has skipped the only step that distinguishes a chat run from an opinion.

## When to leave the chat window

Move to the agent version — or to a human with repository access — when any of these is true:

- the task needs execution to be meaningful (a failing test, a migration, a deploy);
- the diagnosis depends on code the user cannot paste;
- the decision depends on facts about the system that nobody has written down;
- the output will be acted on without review.

The chat prompts say when they have hit one of these; that is the escalation, and taking it early is a finding, not a failure.

## How the two versions relate

The chat prompts are not shorter versions of the agent prompts. They replace a capability the agent has and the chat does not, and they keep the reasoning the agent version uses:

| Agent version | Chat version | Shared | Replaced |
|---|---|---|---|
| `05-scenarios/debugging/` | `CHAT-DEBUG` | hypothesis discipline, one variable at a time, cause versus symptom | reproduction and minimisation become experiments the user runs |
| `04-process/code-review/` | `CHAT-REVIEW` | consequence ordering, evidence per finding, scoped verdict | repository context becomes a missing-context list |
| `02-engineering/architecture-review/` | `CHAT-DESIGN` | constraint analysis, options with costs, ADR | inspection becomes interrogation |

Where both exist, the chat version names the agent version and says when to switch. A run that needs the switch says so in its self-audit.
