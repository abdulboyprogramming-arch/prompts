# Recovery & Failure Handling

**Version:** 1.0.0  
**Type:** Core Orchestration Primitive  

**Use when:** A stage fails, stalls, or produces something unverifiable, and the workflow must decide whether to retry, escalate, or stop.

---

## Purpose
Define how agents should behave when a stage fails, stalls, or produces low-confidence results.

## Failure Classes

1. **Missing context** — need user input or access
2. **Tool / environment failure** — commands, network, permissions
3. **Technical dead-end** — approach invalid
4. **Quality failure** — output does not meet the system’s bar
5. **Safety boundary** — action would require higher authorization

## Response Pattern

1. Stop escalating blindly.
2. Classify the failure.
3. Preserve partial artifacts.
4. Propose the smallest recovery action:
   - retry with adjustment
   - alternative approach
   - ask user for specific input
   - downgrade scope
5. Update the progress ledger with blocked status and reason.

## Anti-Patterns
- Endless retries without changing strategy
- Hiding uncertainty
- Partially applying irreversible external actions
- Discarding evidence of what was tried
