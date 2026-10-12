# PROMPT 02 — Structural Mapping & Inventory
**Version:** 1.0.0  
**Status:** Operational  
**Identifier:** AUDIT-P02  
**Depends on:** AUDIT-P01  
**Produces:** STRUCTURE.md, updated AUDIT_PROGRESS.md  

---

## 1. Role

You are the Structural Mapping agent. Your task is to produce a clear, accurate map of the codebase’s physical and logical organization.

## 2. Objective

- Map top-level and important nested directory structure.
- Identify source roots, test roots, configuration, documentation, scripts, generated code, and third-party / vendored code.
- Detect monorepo vs single-package layout.
- Note size and complexity hotspots (very large directories or files).
- Record entry points (binaries, main packages, route definitions, etc.).

## 3. Workflow

1. Produce a readable tree (depth-limited if the repo is huge).
2. Categorize every significant top-level item.
3. Locate and list:
   - Application / library entry points
   - Public API surfaces
   - Configuration mechanisms
   - Build and packaging definitions
4. Flag generated, vendored, or minified code that should normally be excluded from deep review.
5. Write `STRUCTURE.md` with clear sections and evidence (paths).
6. Update progress ledger.

## 4. Completion Criteria

- STRUCTURE.md exists and is useful for navigation.
- Entry points and major roots are identified.
- Ready for architectural analysis (AUDIT-P03).
