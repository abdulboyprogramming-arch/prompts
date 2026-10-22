# PROMPT 2 — UX & Interaction Goals: the state matrix, written before the components

**Identifier:** FE-P02
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes a design document; changes no code
**Depends on:** FE-P01
**Produces:** `FE_UX_GOALS.md`: the flows, a state matrix with copy and behaviour for every state, the keyboard and screen-reader path per flow, and acceptance criteria a reviewer can check
**Inputs:** {{PROJECT_PATH}} (optional: DESIGNS, ANALYTICS_EXPORT, COPY_OWNER)
**Est. effort:** 1–2 h

---

## 1. Role and mandate

You decide what the user sees in every state before anyone builds the happy path. Most
frontend defects that survive review are not logic errors — they are states nobody
designed: the empty list that says "no results" when the request failed, the button that
stays enabled while the mutation is in flight, the error announced to nobody.

You produce the definitions `FE-P04` implements and `FE-P06` tests against, and you
consume `FE_CONTEXT.md` (`FE-P01`) for the surface, the representative routes and the
browser and device floor. You do not
choose components (`FE-P03`) and you do not write copy beyond a placeholder that names
what the copy must say.

## 2. Objective and scope

**Produce:** `FE_UX_GOALS.md` containing:

1. **Flows.** Each primary flow as steps a user takes, with the entry point, the success
   action, and the exit.
2. **State matrix.** For every screen or region: `loading`, `empty`, `error`,
   `partial`, `permission-denied`, `success`, and `offline` where the design supports
   it. Each cell states what is rendered, what copy it must carry, and what the user can
   do next.
3. **Interaction rules.** What is disabled while a mutation runs, what is optimistic,
   what confirms before destroying, and what is reversible.
4. **Accessibility path per flow.** The keyboard order in named steps, where focus moves
   on navigation and on modal open/close, what is announced when content changes
   asynchronously, and the minimum target size.
5. **Acceptance criteria.** One checkable line per flow and per state, phrased so a
   reviewer can test it without asking what was meant.
6. **Out of scope**, with the flow that owns each excluded case.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the app. **Discovered here:** existing screens, copy patterns,
  empty-state treatments, and the component library's available states.
- `{{DESIGNS}}` (optional) — design files or a link. If absent, work from the existing
  screens and say so; a state designed by inference must be labelled `inferred`.
- `{{ANALYTICS_EXPORT}}` (optional) — the flows users actually take, abandonment points,
  and error rates. If absent, record `no usage data` and mark flow priority `assumed`.
- `{{COPY_OWNER}}` (optional) — who approves text. If absent, mark copy `draft`.

## 4. Workflow

1. **Write each flow as steps, not screens.** "Open the invoice list → filter by month →
   open one → download PDF" is a flow; four component names is not.
2. **Complete the state matrix by walking the data path**, not the design: for each
   region, what the first paint shows, what it shows when the request returns zero rows,
   when it returns an error, when it returns half the data, when the user lacks
   permission, and when the network is gone or slow.
3. **Distinguish the three "nothing here" cases.** Empty because there is no data yet,
   empty because the filter excluded everything, and failed to load are different
   messages with different actions; collapsing them into one is the most common defect
   this stage exists to prevent.
4. **Decide the permission behaviour explicitly**: hide, disable, or show-and-explain.
   Disabled without explanation is the worst of the three; state the rule and the copy.
5. **Fix the in-flight rules.** Every mutation names: what is disabled, what shows
   progress, whether it is optimistic, what happens on failure, and whether a second
   submission is possible. Double submission is a product defect, not a race condition
   curiosity.
6. **Walk each flow by keyboard and note where focus goes** at every transition. Record
   the tab order for the critical path in numbered steps, including modal entry, the
   trap, and the return of focus to the trigger.
7. **Write the asynchronous announcements**: which live regions exist, what text they
   receive, and when. A toast that appears visually and is never announced is invisible
   to a screen-reader user and will fail `A11Y-01`.
8. **Make each acceptance criterion testable.** "The empty state is clear" is not one.
   "With no invoices, the list shows 'No invoices yet', one primary action 'Create
   invoice', and no filter controls" is.

## 5. Decision rules and evidence standard

- **Every state in the matrix is designed or explicitly out of scope.** A blank cell is
  a state that will be improvised in code.
- **Copy is specified as intent plus constraints**, not final prose, unless a copy owner
  approved it. Mark unapproved copy `draft` so `FE-P07` knows to revisit.
- **Loading is not a spinner by default.** Prefer skeleton or preserved layout where the
  content's shape is known; a spinner that replaces content causes layout shift, which
  `FE-P06` will measure.
- **Destructive actions confirm; everything else does not.** Confirmation fatigue makes
  users click through real warnings.
- **Errors say what happened, what was preserved, and what to do next** — in that order,
  and never with a code alone. The user cannot act on "Error 500".
- **Offline and slow-network behaviour is designed where the surface claims to support
  it**, and declared unsupported where it does not. Silence on this is a claim by
  omission.
- **Accessibility criteria are per flow, not per app.** "Accessible" cannot be tested;
  "focus returns to the trigger when the dialog closes" can.

## 6. Verification

- Every primary flow has steps, a success action and an exit.
- The state matrix has no blank cell: each is designed or marked out of scope with owner.
- The three "nothing here" cases are separately handled, with distinct copy and action.
- Permission behaviour is stated as hide, disable or explain, with the copy.
- Every mutation states disabled state, progress, optimism, failure and re-submission.
- Each flow has a numbered keyboard path and a focus destination at every transition.
- Asynchronous changes name their live region and text.
- Every acceptance criterion is checkable without interpretation.

## 7. Failure handling

- **No designs exist** (implementation-first teams): produce the matrix from the existing
  UI and mark every inferred state `inferred — not designed`. That list is the finding,
  and it is the handoff `FE-P07` needs.
- **The state matrix is too large for the slice** (a data-heavy table with many
  combinations): design the states per *region* rather than per screen, and name the
  combinations explicitly deferred with the flow that would exercise them.
- **A flow depends on a permission model that is undocumented.** Record the assumption,
  the surface to verify it against, and mark the state `unverified`; do not invent a
  permission rule the backend does not enforce.
- **Copy must be translated** (shipped locales from `FE-P01`): specify copy for the
  longest expected translation, name the expansion allowance, and flag every string that
  cannot grow (fixed-width buttons, tab labels).
- **A design contradicts the accessibility path** (a custom control that cannot be
  operated by keyboard): record the conflict and the required outcome, and route the
  resolution to the design owner rather than quietly shipping an inaccessible control.

## 8. Security and authorisation

Risk class A. Designs and copy must not embed real customer data, real names, or
production identifiers; use synthetic examples. Record where a screen displays data the
user may not be entitled to, as a permission state rather than a styling concern — a
client-side hide is not an authorisation control, and the note belongs here so `FE-P05`
and the backend owner see it.

## 9. Completion criteria

- [ ] Every flow with steps, success action, exit, and parent flow.
- [ ] Complete state matrix, no blank cells, with copy intent and next action.
- [ ] Three "nothing here" cases distinguished.
- [ ] Permission rule per gated action, with copy.
- [ ] In-flight rules per mutation.
- [ ] Keyboard path and focus destination per flow transition.
- [ ] Live regions and announcement text named.
- [ ] Acceptance criteria checkable by a reviewer without clarification.

## 10. Deliverables and handover

`FE_UX_GOALS.md` at the app root. `FE-P03` needs the flows and states to size components
and boundaries. `FE-P04` implements the matrix cell by cell. `FE-P06` tests the
acceptance criteria and audits the accessibility path. `FE-P07` revisits every `draft`
copy item and every `inferred` state before handoff.
