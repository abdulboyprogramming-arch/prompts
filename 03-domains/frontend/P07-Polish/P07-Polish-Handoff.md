# PROMPT 7 — Polish & Handoff: the long string, the slow connection, and the honest note

**Identifier:** FE-P07
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — final copy, styling and edge-case fixes; reversible through version control
**Depends on:** FE-P06
**Produces:** `FE_HANDOFF.md`: what shipped, what was verified, what was accepted as a known limitation, and the review notes a QA engineer can act on without asking
**Inputs:** {{PROJECT_PATH}} (optional: DESIGN_REFERENCE, COPY_OWNER)
**Est. effort:** 1–2 h

---

## 1. Role and mandate

You finish the slice so a reviewer can judge it and a QA engineer can test it. Polish is
not decoration: it is the long name in a fixed-width cell, the 200 % zoom, the string
that grew 30 % in translation, the error message that tells the user what to do.

You also write the honest note. The handoff is where the untested state, the accepted
risk and the debt are recorded by the person who knows them, before that knowledge is
lost.

## 2. Objective and scope

**Produce:**

1. **Polish changes**: visual consistency with the design and the token set, interaction
   rough edges, and copy that a user can act on.
2. **Edge-case pass** on the four things that break layouts: long strings, translation
   expansion, zoom, and slow or absent network.
3. **`FE_HANDOFF.md`**: what shipped, what was verified and how, what was accepted, what
   is untested, and the review path.

Out of scope: new capabilities, and any state the matrix does not define — a missing
state goes back to `FE-P02`, not into the handoff as an improvisation.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the implementation and `FE_QUALITY.md`, the check results from `FE-P06`.
- `{{DESIGN_REFERENCE}}` (optional) — the design to compare against. If absent, compare
  against the existing app's conventions and say so.
- `{{COPY_OWNER}}` (optional) — who approves text. If absent, mark the copy `draft` and
  say it needs approval in the handoff.

## 4. Workflow

1. **Compare against the design or the app's conventions**, screen by screen, at the
   named breakpoints. Record each difference and either fix it or list it as accepted
   with a reason. "Close enough" is not a note a reviewer can use.
2. **Run the four edge-case passes** and record what broke:
   - substitute the longest realistic value in every user-supplied field,
   - render the longest shipped locale and check for truncation and overflow,
   - zoom to 200 % and confirm no content is clipped or unreachable,
   - throttle the network and confirm the states from the matrix appear in the right
     order, without layout jump.
3. **Fix the copy that fails its job.** Every error states what happened, what was
   preserved, and what to do next. Every empty state says why it is empty and offers the
   action. Every destructive confirmation names the object — "Delete invoice #1042" beats
   "Are you sure?".
4. **Check the interaction dressings**: focus ring visible on every interactive element,
   hover and active states, disabled vs read-only distinction, and no layout shift when a
   state changes.
5. **Confirm the accessibility findings from `FE-P06`** are either fixed or recorded as
   accepted risk with the owner's name; a keyboard trap does not get "accepted".
6. **Write the handoff**: the change summary in user terms, the verification table from
   `FE-QUALITY`, the accepted risks, the untested paths with why, the review steps, and
   the rollback (what to revert if this breaks).
7. **State the browser reality**: which browsers and devices were actually exercised, and
   which were not. "Should work" is a gap, not a result.

## 5. Decision rules and evidence standard

- **Copy is functionality.** A message the user cannot act on is a defect, not a
  wording preference.
- **Fix or record, never both.** A difference from the design is either corrected or
  written down as accepted; a half-fixed difference becomes a review argument.
- **Untested paths are named in the handoff.** The person who ships it is the last one
  who knows it was untested.
- **No polish that changes behaviour** beyond the matrix: if the fix alters what the user
  can do, it needs its state designed and `FE-P06` re-run.
- **Traps are never accepted risk.** Keyboard traps, focus loss, contrast failures on body
  text, and anything that loses user data block the handoff.
- **Translations are content, not strings.** Do not concatenate sentence fragments; a
  language with different word order will produce nonsense.

## 6. Verification

- Every screen compared against the design or convention, differences fixed or accepted.
- Four edge-case passes run with findings recorded.
- Every error, empty state and destructive confirmation passes the copy test.
- Focus visible on every interactive element; no layout shift on state change.
- Accessibility findings fixed or accepted by a named owner, with traps excluded.
- Handoff contains summary, verification, accepted risks, untested paths, review steps
  and rollback.
- Browsers and devices exercised are listed; the rest are named as gaps.

## 7. Failure handling

- **The design is unavailable or out of date**: compare to the running app's conventions,
  record that the reference was inferred, and list the differences a designer should
  confirm.
- **A translation is missing** for a shipped locale: show the fallback behaviour you
  implemented (fallback locale, or visible key) and record it; do not ship an empty
  string.
- **An edge-case pass uncovers a structural problem** (the layout cannot hold a long
  name without redesign): record it as a design gap with the screenshot, and hand it to
  `FE-P02`/the design owner. Do not paper over it with truncated text and a tooltip
  nobody can reach by keyboard.
- **A quality finding cannot be fixed in this slice** (needs an API change): record it as
  accepted risk with its owner and the ticket, and keep it visible in the handoff.
- **The reviewer needs a running environment**: name the exact command, the fixture state
  and any test credentials that are safe to share. Never put a real credential in the
  handoff.

## 8. Security and authorisation

Risk class B. Screenshots and handoff notes must not contain real customer data, tokens
or personal information — use synthetic fixtures and say which ones. Do not add analytics
or error reporting during polish; instrumentation is a separate decision with its own
privacy review. Remove any debug flag, console logging or feature toggle left enabled for
testing, and say in the handoff that you checked.

## 9. Completion criteria

- [ ] Every screen compared, differences fixed or accepted with a reason.
- [ ] Four edge-case passes run and recorded.
- [ ] Error, empty and destructive copy passes the three-part test.
- [ ] Focus visible everywhere; no shift on state change.
- [ ] Accessibility findings fixed or owned; no accepted traps.
- [ ] Handoff complete: summary, verification, risks, untested paths, review, rollback.
- [ ] Browser and device coverage stated, gaps named.
- [ ] Debug logging and testing flags removed and confirmed.

## 10. Deliverables and handover

`FE_HANDOFF.md` with the review notes, the accepted risks and the untested paths.
`FE-P08` uses it to close the run; the reviewer uses it as the checklist; QA uses it to
know which states to force. A known limitation recorded here is a risk the organisation
owns; the same limitation discovered in production is an incident with no owner.
