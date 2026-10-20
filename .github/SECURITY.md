# Security Policy

This repository is a library of Markdown prompts and four small Python scripts. It has no runtime, no network service, and no user data. The security surface is therefore narrow, but it is not zero.

## What is in scope

| Area | Example report |
|------|----------------|
| **Prompts that instruct harmful behaviour** | A prompt that tells an agent to delete data, exfiltrate secrets, bypass a review gate, or disable logging without an approval step |
| **Tooling vulnerabilities** | Code execution or path traversal in `scripts/*.py`; a crafted prompt file that makes the validator or gallery generator behave unexpectedly |
| **Secret or personal-data exposure in the repository** | A committed credential, token, customer record, or internal hostname |
| **Supply-chain risk in CI** | A workflow step that can be tricked into running untrusted code from a pull request |

## What is not in scope

- The behaviour of third-party AI models or agents that use these prompts. The prompts define constraints; whether a specific product honours them is that product's responsibility.
- Vulnerabilities in software you audit **using** the prompts. That is your engagement, and it is covered by `02-engineering/security-hardening/`.
- Prompt-injection attempts against a model (interesting, but a vulnerability in the model, not in a Markdown file). If a prompt in this library is itself a *carrier* for injection — for example it tells an agent to execute instructions found in repository content — that **is** in scope.

## Reporting

Use GitHub's private reporting: **Security → Advisories → Report a vulnerability** on this repository. Please do not open a public issue for a security report.

Include what you need to make the report actionable:

- the file and line, or the workflow run;
- what an agent or user would do because of it, and the harm that follows;
- a minimal reproduction if one exists — for prompts, the smallest instruction sequence that produces the unwanted behaviour;
- whether you believe a fix is already implied elsewhere in the library.

## What to expect

- Acknowledgement within **7 days**; an assessment within **14 days**.
- If the report is valid, a fix on the default branch, a `CHANGELOG.md` entry describing the class of defect, and credit in the advisory unless you prefer otherwise.
- If it is not in scope, an explanation of why and — where useful — the prompt or system that does cover it.

## Guidance for users of this library

- Prompts that change production are marked **Risk class C** or **D** in their metadata. Read that line before running one.
- The library's own rule applies to your use of it: an agent's claim of completion is not evidence. `07-workflows/independent-verification.md` exists for that reason.
- Never paste credentials into a prompt. Inputs are declared as names (`SECRET_*`) precisely so the value stays in your credential store — see `_meta/prompt-inputs.md`.
