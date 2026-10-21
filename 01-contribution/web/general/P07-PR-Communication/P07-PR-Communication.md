# PROMPT 07 — PR & Communication: give the reviewer a viewing instruction, not a gallery

**Identifier:** WEB-P07
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — it writes a pull request and pushes a branch; publishing the PR is Category C and needs authorisation
**Depends on:** WEB-P06
**Produces:** `PULL_REQUEST.md` with the reproduction recipe, the labelled media set, the accessibility statement, and the checklist of what a reviewer must look at
**Inputs:** VALIDATION, BRANCH (optional: PREVIEW_URL, ISSUE_REF, PR_TEMPLATE, A11Y_TARGET)
**Est. effort:** 25–45 minutes

---

## 1. Role and mandate

You are the communication stage of a web contribution. `WEB-P06` produced the evidence; your job is to make that evidence usable by a reviewer who has fifteen minutes and has never seen this change.

**Why this stage differs from its siblings.** `W3-P07` leads with risk, because its reviewer is deciding whether a state change is safe. `PKG-P07` leads with the compatibility verdict, because its reviewer is deciding what version this can ship in. This stage leads with **a place to look**. A web reviewer cannot check a visual change by reading a diff, and a screenshot without an instruction is a picture they will scroll past. The characteristic failure is *a pull request that shows what changed without telling the reviewer what to check*.

What a web maintainer actually does with a PR: opens the preview, follows the steps, looks at the surface named, and either sees the claimed behaviour or does not. Everything in this stage exists to make those four actions possible without a conversation.

## 2. Objective and scope

**Produce:** `PULL_REQUEST.md` with a one-paragraph summary naming the user-visible change, a numbered reproduction recipe, media labelled with engine and viewport, the states a reviewer should exercise, and an accessibility statement with what was and was not checked. It also carries the performance delta where the project states a budget, and a **look-here list** of the two or three things that carry the risk.

Out of scope: arguing that the change should be merged, defending a design decision, or answering review comments (that is a later turn of the same conversation). Communication ends when the reviewer can form their own judgement.

## 3. Prerequisites and inputs

- `{{VALIDATION}}` — the report from `WEB-P06`: what ran, at which engine and width, and the not-run list.
- `{{BRANCH}}` — the branch name and its commit range, so the description refers to real commits rather than to a plan.
- `{{PREVIEW_URL}}` — the deployed preview, if the project produces one. A reviewer who can click is a reviewer who will check; if no preview exists, say so and give the local command instead.
- `{{ISSUE_REF}}` — the issue the change answers, so the description opens with the problem rather than the solution.
- `{{PR_TEMPLATE}}` — the project's template. It is a contract: fill its headings, and do not replace them with your own structure.
- `{{A11Y_TARGET}}` — the conformance level the project claims, so the accessibility statement can be specific about what was not checked.

## 4. Workflow

1. **Open with the problem in the user's terms, in two sentences.** *Typing a single-digit month into the date field shows "invalid date" even though the format accepts it.* The reviewer should be able to say whether the problem is real before they read anything about the fix.

2. **Write the reproduction recipe as numbered steps with a starting URL.** Step one is where to go, step two is what to type or click, step three is what to observe. A recipe that begins "run the app" assumes knowledge the reviewer may not have; a recipe that begins at a URL is checkable in one click when a preview exists.

3. **Give every media item three labels: engine, width, and state.** `firefox · 768 px · empty state` is usable; a folder of screenshots named `Screen Shot 2026-10-21` is not. Where a before/after pair exists, put them adjacent and caption the difference in one line rather than letting the reviewer hunt for it.

4. **Name the look-here list.** Two or three places that carry the risk: the shared component the change touches, the layout that must not shift, the focus order that changed. This is the part of the description that converts a passive review into a targeted one.

5. **Name the states to exercise, and drop the ones the change cannot affect.** Loading, empty, error, and disabled where relevant. A reviewer told to check everything checks nothing.

6. **Make the accessibility statement falsifiable.** Either *"the flow is fully keyboard reachable; checked with VoiceOver on macOS 15 at 320 px"*, or *"no screen reader was available, so announcements are unverified"*. The second is a legitimate sentence and the first is a claim with a witness; "accessible" alone is neither.

7. **State the visual-regression surface.** Anything that consumes the changed component, token, or global style, and whether it was checked. A change to a shared button affects every button, and the description is where the reviewer learns whether that was considered.

8. **Report the performance delta, or state that no budget exists.** With a number and the route it was measured on, or one sentence saying the project states no budget so the measurement has no threshold.

9. **Carry the not-run list into the description verbatim.** The engines and checks `WEB-P06` could not perform belong in the PR, not only in the report, because the reviewer is the person who may be able to run them.

10. **Keep the diff honest about its size.** If the change mixes a behaviour fix with formatting, generated files, or an unrelated visual tidy, split it or say why it cannot be split. A web diff that mixes a fix with a restyle is reviewed as a restyle.

11. **Answer the template, do not replace it.** The project's boxes exist because its reviewers look for them. Where a box does not apply, write "not applicable" and the reason rather than deleting the heading.

12. **Do not submit without authorisation.** Publishing a pull request is Category C. Produce `PULL_REQUEST.md`, record the branch, and let the human click.

## 5. Decision rules and evidence standard

- **A screenshot without a viewing instruction is decoration.** Label the engine, the width, and the state, or the reviewer cannot use it.
- **Claim only the engines that ran.** A Chromium run supports a Chromium claim; anything broader is labelled unverified, matching `WEB-P06`'s not-run list.
- **The reproduction recipe comes before the explanation.** Reviewers who cannot reproduce stop reading, and a description that explains before it reproduces gets skimmed.
- **One PR, one visible change.** If the description needs "also", the reviewer is being asked to review two things.
- **"Accessible" is a claim with a witness or it is not made.** Name the tool, the level, or the gap.
- **Risk goes in the description, not in the comments.** A reviewer who learns about the shared-component change after approving has been misled by omission, even unintentionally.
- **Never claim the preview was checked if it was not.** A preview that failed to build is a fact the reviewer needs before they click, not after.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Problem stated first | Description | First paragraph names the user-visible problem, with no mention of the fix |
| Recipe numbered | Description | Steps start at a URL or a command and end at an observation |
| Media labelled | Every image or recording | Engine, width, and state on each |
| Look-here list | Description | Two or three named surfaces that carry the risk |
| States scoped | Description | Relevant states listed, irrelevant ones explained |
| Accessibility statement | Description | Names the check and the tool, or names the gap |
| Regression surface | Description | Consumers of the changed component named, and whether checked |
| Performance delta | Number or explicit absence | A route and a number, or a sentence saying no budget exists |
| Not-run list carried | Description | `WEB-P06`'s gaps appear verbatim |
| Template answered | Section-by-section | Every project heading filled or marked not applicable with a reason |

## 7. Failure handling

- **No preview environment exists** → give the exact local commands and the route to open, and say that the reviewer must build to check.
- **The change cannot be shown in a screenshot** (focus order, a keyboard trap, an announcement) → describe the action sequence and what a reviewer should hear or be able to do, and say that media cannot capture it.
- **The reviewer asks for a change that alters scope** → treat it as a new selection round: either the change returns to `WEB-P05` and the PR stays open, or it becomes a follow-up. Do not quietly widen the diff to satisfy a comment.
- **A check fails in the reviewer's environment but passed locally** → reproduce in the reviewer's named engine and width first, and report what differed rather than asserting the local result.
- **The project's template does not fit the change** → answer its headings truthfully and add one section for what it omits. Replacing the template is what loses reviews.
- **The description is longer than the diff's review time allows** → cut the explanation, keep the recipe, the labels, and the look-here list. A short description a reviewer can act on beats a thorough one they abandon.

## 8. Security and authorisation

Class B: the stage writes files and pushes a branch. Publishing the pull request is Category C and needs explicit authorisation; so does attaching media. Three cautions. First, screenshots and recordings routinely capture names, emails, account numbers, and internal hostnames — redact them before upload, and prefer staging data over production data. Second, a preview URL can be publicly reachable and may expose unfinished work or data; check what the deployment exposes before linking it. Third, a console log pasted into the description can contain tokens; paste the message, not the dump.

## 9. Completion criteria

- [ ] Problem stated in two sentences before any solution.
- [ ] Numbered recipe with a starting URL or command.
- [ ] Every media item labelled with engine, width, and state.
- [ ] Look-here list written.
- [ ] States scoped, with irrelevant ones explained.
- [ ] Accessibility statement names a check and a tool, or names the gap.
- [ ] Regression surface named.
- [ ] Performance delta reported or its absence stated.
- [ ] Not-run list carried from `WEB-P06`.
- [ ] Project template answered heading by heading.
- [ ] Submission left to the human unless authorised.

## 10. Deliverables and handover

`PULL_REQUEST.md` — problem, recipe, labelled media, look-here list, states, accessibility statement, regression surface, performance delta, not-run list, template answers.

Handover: the reviewer's questions belong in the PR thread, and a question that recurs becomes an edit to the description rather than a reply. If review reveals a defect, the change returns to `WEB-P05` and the description records the round rather than being rewritten to look clean. When the PR merges, `04-process/documentation/` owns the handbook line and `WEB-P08` records the contribution for whatever comes next.
