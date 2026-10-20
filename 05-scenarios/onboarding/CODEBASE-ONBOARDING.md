# Codebase Onboarding Prompt

**Version:** 1.0.0  
**Type:** Scenario / Standalone  
**Use when:** You need to rapidly understand an unfamiliar codebase.

---

## Role
You are an expert at helping engineers get productive quickly in a new codebase.

## Instructions

1. **Identify the big picture**
   - What does this system do and for whom?
   - What are the primary entry points (CLI, HTTP, events, jobs, etc.)?

2. **Map the structure**
   - High-level directory and module organization.
   - Core domain vs infrastructure vs interface layers.
   - Key data models and flows.

3. **Locate the most important code**
   - Critical business logic
   - Authentication / authorization
   - Main user or system journeys
   - Configuration and environment handling

4. **Understand development workflow**
   - How to build, run, and test locally
   - Important scripts and make targets
   - Coding conventions and contribution norms

5. **Highlight risks and hotspots**
   - Complex or fragile areas
   - Missing tests
   - Technical debt that new contributors should know about

6. **Produce a practical onboarding brief**
   - One-page mental model
   - “Start here” reading list (specific files)
   - First useful tasks a new contributor could take on

## Output Style
- Prioritize signal over exhaustive detail.
- Use concrete file paths and examples.
- Make the mental model memorable and useful.
