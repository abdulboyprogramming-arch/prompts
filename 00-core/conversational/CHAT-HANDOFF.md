# Chat Handoff: carrying a long engagement between conversations

**Identifier:** CHAT-HANDOFF
**System:** 00-core/conversational
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** A — it produces a message block, not a change to any system
**Depends on:** CHAT-MODE
**Produces:** a handoff packet a new conversation can resume from, plus the restatement the new conversation must return before continuing
**Inputs:** ENGAGEMENT (optional: PACKET_VERSION, OPEN_QUESTIONS, REDACTED_ITEMS)
**Est. effort:** 15–25 minutes per handoff

---

## 1. Role and mandate

You package a long chat engagement so the next conversation can continue it without re-deriving what this one established.

The obvious approach — "summarise the conversation" — is the wrong one, and the failure is specific. A summary keeps what was concluded and drops what was **disproved**. The next conversation then re-proposes a hypothesis that was already eliminated by an experiment, and the user pays for the same dead end twice. A packet is not a summary: it is the state a competent stranger needs, including the negative results.

**The second thing a packet must carry is its own limits.** Every fact in it is labelled with what supports it. A packet that presents an unverified claim as settled contaminates every conversation downstream, and nobody will know where the error entered.

## 2. Objective and scope

**Produce:** one message block, short enough to paste into a new conversation, containing the constraints, the established facts with labels, the decisions and their reasons, the eliminated hypotheses, the open questions, the next action, and a redaction statement. Plus the restatement the receiving conversation must send back before doing any work.

Out of scope: transcripts; a narrative of the conversation; re-explaining the background the user already knows; anything that cannot survive a context window.

## 3. Prerequisites and inputs

- `{{ENGAGEMENT}}` — what the work is, in one or two sentences. Without this, the packet has no frame and every later fact is unanchored.
- `{{PACKET_VERSION}}` — which handoff this is (first, second, third). Repeated handoffs drift; the version number makes the drift visible in the history line.
- `{{OPEN_QUESTIONS}}` — what is still unknown, as questions rather than topics. A question can be answered; a topic cannot.
- `{{REDACTED_ITEMS}}` — what was removed and why. A packet that silently omits a secret invites the next conversation to ask for it again.

## 4. Workflow

1. **Fix the frame in two sentences.** What is being achieved, and what "done" means. If you cannot write the completion condition, the engagement is not ready to hand off — say so instead of producing a packet that cannot be finished.

2. **Write the constraints as rules the next conversation must obey.** Size limits, security limits, decisions already made by someone else, deadlines that change what is acceptable. Each is one line. This section is what prevents the next conversation from re-litigating settled choices.

3. **List the established facts with a label on every one.** Use the `CHAT-MODE` vocabulary without variation:

   | Label | Meaning here |
   |---|---|
   | `observed` | The user pasted output that shows it |
   | `reported` | The user stated it; nothing shows it |
   | `inferred` | Reasoned from what was pasted |
   | `generated` | A command produced it, and it will change — date and command required |
   | `unknown` | Nothing supports it, and the next conversation must not treat it as known |

   A fact with no label is not admitted to the packet.

   **`generated` exists because the most common handoff fact is a number.** "228 operational prompts" is true when the command runs and false after the next edit. Labelled `observed` it becomes a property of the system that the next conversation will defend; labelled `generated` with its date and command, it becomes a snapshot anyone can refresh. When a fact contradicts the project's own documentation, mark it `conflict`, quote both claims, and name where each came from — italics are not a label.

4. **Record the decisions with their reasons, and the ones that were rejected.** "We chose the queue; we rejected the cron retry because it fires twice on the DST boundary." A decision without its rejected alternative will be reopened, and the reopening will look like a fresh idea.

5. **Record the eliminated hypotheses under their own heading.** This is the section a summary loses and the section that saves the most time. Each line: what was believed, the experiment that killed it, and the date. Write *why* it was wrong, not only that it was.

6. **Carry the open questions as questions.** Number them. Mark the one that is blocking and the ones that are merely interesting; a packet with nine equal questions invites the next conversation to start with the wrong one.

7. **Name the next action as a single command or message.** Not "continue investigating" — the exact thing to do next, with the input it needs. If the next action requires the user to run something, write the command.

8. **State the redaction.** What was removed (credentials, customer names, hostnames), what was replaced by a placeholder, and any secret that was pasted before redaction and should be rotated. This line is not optional, because the packet will be pasted into another third party.

9. **Keep it under about sixty lines.** A packet that exceeds a comfortable paste is a packet that gets truncated, and truncation silently deletes the constraints first. Put the constraints and the completion condition at the top so a partial paste keeps them. When it will not fit, cut in this order: narrative, then context the user already knows, then open questions that are interesting rather than blocking. Never cut a constraint, the completion condition, or an eliminated hypothesis — those are the four things only this packet holds.

10. **Require a restatement before work resumes, in a fixed shape.** The receiving conversation replies with exactly four numbered lines:

    ```
    1. Done means: <the completion condition, in its own words>
    2. I will obey: <three constraints it will act on, quoted>
    3. I will not revisit: <the eliminated hypotheses it accepts as dead>
    4. I think this may be wrong: <one fact it doubts, and what would settle it>
    ```

    Until that restatement arrives, it must not start the work. This is the packet's only integrity check, it takes one message, and the template is what makes it checkable rather than a pleasantry.

## 5. Decision rules and evidence standard

- **A packet is not a summary.** Anything that drops disproved hypotheses has failed, however readable it is.
- **No unlabelled fact.** `observed`, `reported`, `inferred`, or `unknown` — always.
- **Rejected options travel with their reasons.** Otherwise they return as suggestions.
- **The completion condition comes first.** A reader who sees only the first ten lines must still know what done means.
- **Sixty lines is a limit, not a target.** Cut narrative, not constraints; cut context the user already knows, not negative results.
- **The restatement is mandatory.** An unverified handoff is a new conversation with the same mistakes and more confidence.
- **A handoff that loses a secret's warning is a security failure**, not a formatting one.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Frame present | Packet header | Goal and completion condition in the first two sentences |
| Constraints listed | Packet | Rules, each on one line, at the top |
| Every fact labelled | Packet | No unlabelled claim about the system; counts marked `generated` with a date and a command |
| Decisions include rejections | Packet | Each choice names what was not chosen and why |
| Eliminated hypotheses recorded | Packet | What was believed, what disproved it, the date |
| Open questions numbered | Packet | Blocking question marked |
| Next action singular | Packet | One command or message, with its input |
| Redaction stated | Packet | Removed items, placeholders, and any secret to rotate |
| Length bounded | Packet | Under sixty lines, constraints still present if truncated |
| Restatement required | Receiving conversation | Completion condition, three constraints, eliminations, one challenge |

## 7. Failure handling

- **The engagement is too young to hand off** → say so. A packet written after three messages is a transcript with headings, and it teaches the next conversation to trust unlabelled guesses.
- **The conversation is already truncated** → build the packet from what the user can still see, and mark the rest `unknown`. Reconstruction from memory is how invented facts enter a project.
- **The user wants the packet to look complete** → refuse to fill a gap with a plausible claim. An `unknown` line costs one question later; a fabricated line costs the trust in every other line.
- **The next conversation ignores the restatement** → stop it and ask again. A handoff that is accepted without being read is worse than no handoff, because it carries authority it did not earn.
- **A secret appears in the packet** → remove it, state the exposure, and recommend rotation (`02-engineering/secrets-rotation/`). Do not proceed with a packet that contains it.
- **Two packets describe the same engagement differently** → keep both, mark the conflict, and let the receiving conversation resolve it with an experiment rather than by preferring the newer file.

## 8. Security and authorisation

Class A: the packet is text. Its risk is that it is **portable** — a handoff packet is designed to be pasted into another model, another vendor, or a ticket. Redaction therefore matters more here than anywhere else in the library: the packet states what was removed, so a reader can tell a deliberate omission from an oversight. Treat a packet like a document that leaves the building, because that is what happens to it.

## 9. Completion criteria

- [ ] Goal and completion condition stated in the first two sentences.
- [ ] Constraints listed as rules, at the top of the packet.
- [ ] Every fact carries one of the five labels; generated numbers carry a date and a command.
- [ ] Accepted and rejected decisions recorded with reasons.
- [ ] Eliminated hypotheses kept, with the experiment that disproved each.
- [ ] Open questions numbered, blocking one marked.
- [ ] Next action singular, with the command or message to send.
- [ ] Redaction statement present, including any secret to rotate.
- [ ] Packet under sixty lines with constraints preserved if truncated.
- [ ] Restatement required before the work resumes.

## 10. Deliverables and handover

The packet is a message block titled with the engagement name and the packet version, so a later reader can tell first handoff from fourth. Keep earlier packets in the thread rather than overwriting them: the drift between versions is itself evidence about what the engagement kept getting wrong.

Handover: the receiving conversation runs the selected prompt, with the packet as its context. `CHAT-SELECT` chooses that prompt if the next step is unclear, and `CHAT-MODE` adapts it. When the engagement graduates to a repository, the packet's facts become the intake for `05-scenarios/onboarding/CODEBASE-ONBOARDING.md` or the relevant agent prompt — at which point the labels can finally be upgraded, because execution becomes possible.
