# Secrets & Sensitive Data Handling

**Version:** 1.0.0  
**Type:** Core Safety Primitive  

---

## Rules

1. **Never commit secrets**
   - API keys, tokens, private keys, passwords, session cookies, connection strings with credentials.

2. **Never print secrets in full**
   - If a secret appears in logs or files, redact it in summaries and outputs.

3. **Do not request secrets casually**
   - Prefer environment variables, secret managers, or user-side injection.
   - If a secret is required, ask the user to place it in a secure location rather than pasting it into chat when avoidable.

4. **Treat production data carefully**
   - Minimize copies of personal data.
   - Do not export production datasets into prompts or public artifacts.

5. **Responsible disclosure**
   - Security findings should be documented with enough detail to fix, not enough to weaponize casually.
   - Prefer private reporting channels when the project specifies them.

6. **Credential rotation awareness**
   - If a secret may have been exposed during work, flag it for rotation.
