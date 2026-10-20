# General Web Contribution System

**Maturity: skeleton (v0.1.0).** The eight stage files here are structural outlines. They identify a defensible contribution sequence and name the artifacts, but they do not yet contain the evidence rules, verification steps, or failure handling required to run them unsupervised. Do not present this system as operational.

**Intended use today:** as a human-supervised checklist for contributing to a web project.
**Not yet ready for:** unattended autonomous contribution.

## Stages

| ID | Stage | Purpose | Maturity |
|----|-------|---------|----------|
| WEB-P01 | [Context & Project Understanding](P01-Context/P01-Context-Project-Understanding.md) | Stack, build, data flow, conventions | skeleton |
| WEB-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Find defects and improvements worth doing | skeleton |
| WEB-P03 | [Opportunity Selection & Framing](P03-Opportunity/P03-Opportunity-Selection-Framing.md) | Pick one, define the acceptance bar | skeleton |
| WEB-P04 | [Planning & Design](P04-Planning/P04-Planning-Design.md) | Design the change against existing patterns | skeleton |
| WEB-P05 | [Implementation](P05-Implementation/P05-Implementation.md) | Build it within the project's conventions | skeleton |
| WEB-P06 | [Validation & Quality](P06-Validation/P06-Validation-Quality.md) | Tests, a11y, browser checks, regression | skeleton |
| WEB-P07 | [PR & Communication](P07-PR-Communication/P07-PR-Communication.md) | Reviewer-friendly change description | skeleton |
| WEB-P08 | [Orchestrator](P08-Orchestrator/P08-Web-Contribution-Orchestrator.md) | Sequences the stages, tracks state | skeleton |

## Preconditions this system assumes

- You can run the project's build and test commands locally.
- You have read the repository's contribution guide and code of conduct.
- Network publication (push/PR) is authorised separately — see `00-core/safety-and-security/ACTION-CATEGORIES.md` Category C.

## Known gaps before promotion to `operational`

1. No stage defines what counts as evidence that a UI change is correct (visual diff, DOM assertion, manual steps).
2. Accessibility is mentioned but has no pass criteria.
3. The orchestrator does not define behaviour when a stage is blocked.
4. No regression-protection or rollback section in the implementation stages.

Tracked in `_meta/ROADMAP-AND-BACKLOG.md`.

## Related

- Deep frontend engineering: `03-domains/frontend/`
- Full autonomous contribution (the developed system): `01-contribution/open-source/general-agent/`
