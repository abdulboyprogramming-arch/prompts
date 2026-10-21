# General Web Contribution System

**Maturity: four skeletons, four operational.** `WEB-P02` (discovery) walks the running app instead of reading code, recording an observation at a named engine and width for every candidate. `WEB-P03` (selection) refuses any visual change with no named owner of the design decision. `WEB-P06` (validation) carries the browser matrix, the accessibility pass, the visual diff, and the not-run list. `WEB-P07` (communication) gives the reviewer a reproduction recipe and a look-here list rather than a gallery. The other four are outlines, and the system as a whole is not operational.

**Intended use today:** as a human-supervised checklist for contributing to a web project.
**Not yet ready for:** unattended autonomous contribution.

## Stages

| ID | Stage | Purpose | Maturity |
|----|-------|---------|----------|
| WEB-P01 | [Context & Project Understanding](P01-Context/P01-Context-Project-Understanding.md) | Stack, build, data flow, conventions | skeleton |
| WEB-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) | A surface walk at three widths, a keyboard pass, and an observation per candidate | **operational** |
| WEB-P03 | [Opportunity Selection & Framing](P03-Opportunity/P03-Opportunity-Selection-Framing.md) | Claim register, a proof artifact per claim, the design owner of anything visible | **operational** |
| WEB-P04 | [Planning & Design](P04-Planning/P04-Planning-Design.md) | Design the change against existing patterns | skeleton |
| WEB-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | Build it within the project's conventions | skeleton |
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
5. `P04`, `P05` and `P08` are still the same file as their `web3` and `packages` counterparts with different nouns (backlog #107). `P02`, `P03`, `P06` and `P07` have been through a differentiation pass, and each now asks for evidence neither sibling asks for: an observation in a browser, a design owner, a browser matrix, a viewing instruction.

Tracked in `_meta/ROADMAP-AND-BACKLOG.md`.

## Related

- Deep frontend engineering: `03-domains/frontend/`
- Full autonomous contribution (the developed system): `01-contribution/open-source/general-agent/`
