# General Web Contribution System

**Maturity: two skeletons, six operational.** Stages `P02`–`P07` are developed, and each one asks for evidence the others do not: discovery is a walk of the running app at three widths, selection refuses a visual change with no owner of the decision, planning is a state-by-breakpoint matrix, implementation builds those states with native semantics, validation carries the browser matrix and the not-run list, and communication gives the reviewer a reproduction recipe. `P01` (context) and `P08` (orchestrator) remain outlines, so the system as a whole is **mixed**, not operational, and running it unattended is not supported.

**Intended use today:** as a human-supervised checklist for contributing to a web project.
**Not yet ready for:** unattended autonomous contribution.

## Stages

| ID | Stage | Purpose | Maturity |
|----|-------|---------|----------|
| WEB-P01 | [Context & Project Understanding](P01-Context/P01-Context-Project-Understanding.md) | Stack, build, data flow, conventions | skeleton |
| WEB-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) | A surface walk at three widths, a keyboard pass, and an observation per candidate | **operational** |
| WEB-P03 | [Opportunity Selection & Framing](P03-Opportunity/P03-Opportunity-Selection-Framing.md) | Claim register, a proof artifact per claim, the design owner of anything visible | **operational** |
| WEB-P04 | [Planning & Design](P04-Planning/P04-Planning-Design.md) | State × breakpoint matrix, one test layer per behaviour | **operational** |
| WEB-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | Every state built, native semantics, behaviour-only diff | **operational** |
| WEB-P06 | [Validation & Quality](P06-Validation/P06-Validation-Quality.md) | Tests, a11y, browser checks, regression | **operational** |
| WEB-P07 | [PR & Communication](P07-PR-Communication/P07-PR-Communication.md) | Reproduction recipe, labelled media, look-here list | **operational** |
| WEB-P08 | [Orchestrator](P08-Orchestrator/P08-Web-Contribution-Orchestrator.md) | Sequences the stages, tracks state | skeleton |

## Preconditions this system assumes

- You can run the project's build and test commands locally.
- You have read the repository's contribution guide and code of conduct.
- Network publication (push/PR) is authorised separately — see `00-core/safety-and-security/ACTION-CATEGORIES.md` Category C.

## Known gaps before promotion to `operational`

1. ~~No stage defines what counts as evidence that a UI change is correct~~ — closed in 2.22.0 by `WEB-P06`: browser matrix, before/after visual diff, DOM assertion, not-run list.
2. ~~Accessibility is mentioned but has no pass criteria~~ — closed in 2.22.0: keyboard pass first, screen-reader pass second, scanners third, with the criterion named per finding.
3. The orchestrator does not define behaviour when a stage is blocked.
4. No regression-protection or rollback section in the implementation stages.
5. `P01` and `P08` remain outlines, and `P01` is close enough to its siblings that differentiating it would produce adjectives rather than instruments. `P02`–`P07` have each been through a differentiation pass (backlog #107, complete) and now ask for evidence neither sibling asks for.
6. No stage in this system has been executed against a real repository. The six developed stages are `operational` in the library's sense — structurally reviewed with evidence rules — and the review log says plainly that no run exists.

Tracked in `_meta/ROADMAP-AND-BACKLOG.md`.

## Related

- Deep frontend engineering: `03-domains/frontend/`
- Full autonomous contribution (the developed system): `01-contribution/open-source/general-agent/`
