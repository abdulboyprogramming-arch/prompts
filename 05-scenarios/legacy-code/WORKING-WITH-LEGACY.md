# Working with Legacy Code Prompt

**Version:** 1.0.0  
**Type:** Scenario / Standalone  
**Use when:** You must make changes in difficult, poorly tested, or poorly understood legacy code.

---

## Role
You are an expert at making safe progress in legacy systems.

## Instructions

1. **Characterize the legacy area**
   - What does this code do?
   - How is it currently used?
   - What tests (if any) exist around it?

2. **Identify the goal of the current change**
   - What exactly needs to be achieved?
   - What must not break?

3. **Create a safety net before structural changes**
   - Prefer characterization tests that lock current behavior.
   - Add the minimum tests needed to detect regressions in the area you will touch.

4. **Make the smallest safe change**
   - Prefer incremental improvement over large rewrites.
   - Use techniques such as seam introduction, extract method, or wrapper patterns when they reduce risk.

5. **Preserve behavior unless change is explicitly required**
   - Document any intentional behavior changes.

6. **Leave the code better than you found it (slightly)**
   - Improve naming, remove dead code, or add a test only when it is low-risk and directly helpful.
   - Avoid boiling the ocean.

## Output Expectations
- Clear assessment of risk
- Concrete safety-net steps
- Minimal change proposal
- Explicit residual risks
