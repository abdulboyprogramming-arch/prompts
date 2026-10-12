# Prompt Archive Taxonomy

This document defines the living classification system for the entire archive.

## Primary Axes

1. **Purpose / Activity** (what the user is trying to accomplish)
2. **Domain / Technology** (the technical context)
3. **Scope** (single file → whole system → multi-repo / organization)
4. **Maturity of Target** (greenfield, existing mature, legacy, experimental)
5. **Interaction Style** (one-shot, multi-stage autonomous, interactive context-gathering)

## Top-Level Categories (Stable)

| Code | Name | Description |
|------|------|-------------|
| 00-core | Core & Meta | System prompts, orchestration patterns, safety, prompt engineering itself |
| 01-contribution | Contribution | Adding value to existing projects (OSS or private) |
| 02-engineering | Engineering | Analysis, design, transformation, and construction of software |
| 03-domains | Domains | Deep, technology-specific prompt systems |
| 04-process | Process | Methodology, research, QA, documentation, project management |
| 05-scenarios | Scenarios | Short, high-utility prompts for common situations |
| 06-interactive | Interactive | Prompts designed to gather missing context from the user |
| 99-misc | Miscellaneous | Temporary or uncategorized |
| archive | Archive | Deprecated or historical content |

## Contribution Sub-taxonomy (01-contribution)

- open-source/general-agent
- open-source/language-specific
- language-design (inventing or extending languages)
- packages-libraries
- web/frontend, web/backend, web/fullstack, web/infra-devops
- web3/frontend, web3/backend, web3/smart-contracts, web3/infra
- mobile
- docs-and-content
- games (contribution to existing game projects)

## Engineering Sub-taxonomy (02-engineering)

- codebase-audit
- architecture-review
- refactoring
- rewriting-migration (language or paradigm)
- feature-design-suggestion
- from-scratch
- patterns-strategies-methods (inventing or improving)
- performance
- security-hardening

## Domain Sub-taxonomy (03-domains)

Mirror common technology areas. Prefer putting *deep* domain systems here and *contribution* or *engineering* systems that happen to be in a domain under 01 or 02.

## Naming Conventions

- Folders: kebab-case
- Prompt files: `PXX-Short-Descriptive-Name.md` or `NN-descriptive-name.md`
- Multi-stage systems live in their own subfolder with a local README and INDEX
- Every major system should have a clear entry-point file (usually an Orchestrator)

## Evolution Rules

- Prefer deepening an existing category over creating a new top-level category.
- When a new major activity appears repeatedly, promote it to its own subfolder under the appropriate top-level.
- Keep 99-misc small; migrate content quickly.
