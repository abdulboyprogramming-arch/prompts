# Prompt Quality Bar

**Version:** 1.0.0  
**Type:** Core Prompt-Engineering Primitive  

**Use when:** You are writing or reviewing a prompt and need the minimum bar it must clear before anyone uses it.

---

## Every production prompt in this archive should

1. **Declare identity**
   - Clear role, version, and identifier

2. **State objective**
   - What success looks like

3. **Specify workflow**
   - Ordered steps, not vague advice

4. **Define outputs**
   - Named artifacts or concrete deliverables

5. **Include completion criteria**
   - When to stop and hand over

6. **Respect safety**
   - Reference or embody action-category discipline

7. **Avoid contradiction**
   - No conflicting instructions or hidden scope explosions

## Multi-stage systems should also

- Have an explicit orchestrator / entry point
- Define stage dependencies
- Produce durable intermediate artifacts
- Support resume after interruption

## Anti-patterns to reject

- Purely motivational language without procedure
- Unbounded “do everything” instructions
- Missing validation steps
- No distinction between suggestion and required action
- Assuming tools or permissions that are not guaranteed
