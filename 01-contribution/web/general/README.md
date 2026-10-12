# General Web Contribution System

**Status:** Operational (v1.0)  
**Entry Point:** [`P08-Orchestrator/P08-Web-Contribution-Orchestrator.md`](P08-Orchestrator/P08-Web-Contribution-Orchestrator.md)

A practical multi-stage system for making high-quality contributions to web projects (frontend, backend, or fullstack). Designed to work across common web stacks while remaining adaptable.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| WEB-P01 | Context & Project Understanding | Understand the web project, stack, and contribution norms |
| WEB-P02 | Discovery & Opportunity Identification | Find valuable, suitable contribution opportunities |
| WEB-P03 | Opportunity Selection & Framing | Choose and clearly frame the work |
| WEB-P04 | Planning & Design | Plan the change with web-specific considerations |
| WEB-P05 | Implementation | Execute the change following project conventions |
| WEB-P06 | Validation & Quality | Test, lint, accessibility, performance, and visual checks |
| WEB-P07 | PR & Communication | Prepare and submit a professional pull request |
| WEB-P08 | Master Orchestrator | Coordinates the full contribution flow |

## Web-Specific Considerations Built In

- Component structure and design-system alignment (frontend)
- API contracts, data fetching, and error handling
- Accessibility (a11y) and responsive behavior
- Performance implications (bundle size, rendering, network)
- Security basics (XSS, CSRF, auth handling, secrets)
- Testing patterns common in web projects (unit, component, e2e)
- CI, preview deployments, and visual regression signals
