# Stage Prompt Template

**Version:** 1.0.0  
**Type:** Core Template  

---

```markdown
# PROMPT NN — <Stage Name>
**Version:** 1.0.0  
**Identifier:** <SYS>-P<NN>  
**Depends on:** <prior stage ids, if any>

---

## Role
You are the <specific> agent.

## Objective
<one paragraph>

## Workflow
1. ...
2. ...
3. Write `<ARTIFACT>.md` containing:
   - ...

## Completion Criteria
- <measurable done state>
```

## Notes
- Keep workflow concrete.
- Name artifacts explicitly.
- Prefer short, enforceable completion criteria.
