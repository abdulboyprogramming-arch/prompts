# PROMPT 07 — Agent Permissions and Tool Supply Chain

**Identifier:** AI-P07
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** B (reads configuration and reduces permissions; any widening is C or D and separately approved)
**Depends on:** AI-P04 (injection defence), `04-process/agent-context/` P01
**Produces:** `TOOL_PERMISSIONS.md`, a permission diff, an approval matrix
**Inputs:** REPO_PATH, AGENT_CONFIG (optional: ENVIRONMENT, TOOL_INVENTORY)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You audit what an AI agent can actually do — not what its documentation says it does.

An agent's permission surface is the union of: the shell it can run, the filesystem it can read and write, the network it can reach, the credentials in its environment, and every third-party tool or MCP server it is configured with. That union is almost never reviewed as a whole, because it is assembled incrementally by people trying to unblock a task.

The failure mode is quiet: a tool server installed to read Jira also has a shell; a "read-only" filesystem mount includes `.ssh`; a rules file fetched from a repository carries instructions and a package install.

## 2. Objective and scope

**Produce:** a complete inventory of tools, servers, and capabilities; an effective-permission table; a least-privilege diff with each reduction applied where safe; an approval matrix for anything irreversible; and a supply-chain review of every third-party component.

Out of scope: reviewing the model's alignment, choosing an agent product, and granting new permissions (that is a separate authorised decision).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` and the agent configuration: `.mcp.json`, `mcp.json`, `claude_desktop_config.json`, `.cursor/mcp.json`, `.vscode/settings.json`, `settings.json` / `settings.local.json` for permission rules, `AGENTS.md`/`CLAUDE.md`/rules files, and any `devcontainer.json`.
- `{{AGENT_CONFIG}}` — the configuration under audit; `{{ENVIRONMENT}}` — developer laptop, CI runner, or production-adjacent host (the same config is a different risk in each).
- `{{TOOL_INVENTORY}}` — any existing list, which you will verify rather than trust.
- Credentials in the environment: list *names* only, never values.

## 4. Workflow

1. **Enumerate every executable capability**, not every tool name. For each configured server or tool, answer: what process does it run, what does it read, what does it write, what network egress does it have, what credentials does it receive, and can it execute arbitrary commands. A tool's description is marketing; its invocation is the truth.

2. **Build the effective-permission table** across six axes: **filesystem read**, **filesystem write**, **shell execution**, **network egress**, **credential access**, **irreversible actions** (send, pay, deploy, delete, merge, publish). Mark each as none / scoped / broad, and record the evidence (config line) for each.

3. **Find the accidental escalations**, which are the common ones:
   - a filesystem mount that includes the home directory, `.ssh`, `.aws`, `.env`, or the browser profile;
   - a shell tool that is "just for tests" but has no command allowlist;
   - a network-allowed tool with unrestricted egress, which makes exfiltration of anything it can read possible;
   - a Docker socket mounted into the dev container, which is host root;
   - `--dangerously-skip-permissions` or its equivalent enabled "temporarily";
   - credentials exported in the shell profile that the agent inherits.

4. **Review the third-party supply chain for each MCP server or plugin**: publisher identity, repository, whether the version is pinned, whether it executes `npx`/`uvx` at run time (which fetches latest on every start — an unaudited update channel), install scripts, and what its dependencies can do. An unpinned `npx` server is remote code execution with a version-pinning illusion.

5. **Treat agent-readable text as an input channel, not as configuration.** Rules files, fetched documentation, issue descriptions, and tool descriptions can all carry instructions. Check: is any rule file fetched from a remote source at run time? Can a repository's `AGENTS.md` change the agent's behaviour when the agent opens a PR from a fork? A malicious `CLAUDE.md` in a dependency's repository is a live attack path.

6. **Derive the least-privilege configuration**: explicit allowlists over broad grants; scoped paths over home directories; per-server credential scoping; network allowlists where the tool supports them; approval prompts for irreversible actions; and a separate profile for "trusted task" versus "untrusted content", switched deliberately.

7. **Add the controls that survive a mistake**: an approval gate on the irreversible set, a spend or call cap for paid tools, an audit log of tool invocations that a human can read, a kill switch (how to stop a running agent), and a rule that secrets are injected per-command, not inherited.

8. **Verify the reductions did not break the workflow.** Run the three or four most common developer tasks with the tightened configuration; a security posture that blocks the daily workflow will be reverted by Friday, with the audit forgotten.

9. **Record the residual risk by name**: which broad permission remains, why it is needed, who accepted it, and when it will be reviewed. A residual risk without an owner is an unowned vulnerability.

10. **Write `TOOL_PERMISSIONS.md`**: inventory with evidence, effective-permission table, supply-chain findings, applied reductions, approval matrix, residual risks with owners, and the procedure for adding a new tool (the gate that prevents this audit from being needed again).

## 5. Decision rules and evidence standard

- **Capability, not intent.** Judge what the tool can do, not what it is for.
- **Broad egress plus broad read equals exfiltration.** Evaluate the pair, not each axis alone.
- **Unpinned remote execution is a supply-chain gap**, regardless of the publisher's reputation.
- **Untrusted text is an instruction channel**; fetched config is code execution with extra steps.
- **Least privilege must still be usable**, or it will be reverted.
- **Every irreversible action has an approval gate** and a logged actor.
- **Residual risk is recorded with a name and a review date.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every server enumerated | Config diff | Inventory matches configuration files |
| Capabilities evidenced | Config lines cited | Six axes filled per tool |
| Escalation patterns checked | Checklist | Each of the six patterns addressed |
| Supply chain reviewed | Package metadata | Publisher, pin, install scripts recorded |
| Unpinned `npx`/`uvx` found | Config search | Zero, or each justified |
| Remote-fetched rules checked | Config and network | None, or trust boundary stated |
| Least-privilege diff applied | New config | Broad grants replaced with scoped ones |
| Workflow still works | Task run | Daily tasks pass with the tightened config |
| Approval gates on irreversible actions | Config | Enforced, not advisory |
| Audit log available | Tooling | Invocations visible to a human |
| Residual risks owned | Document | Name and review date per item |

## 7. Failure handling

- **The agent cannot function without broad filesystem access** (a monorepo with generated code) → scope to the repository root, exclude `.git` internals where possible, and add write approval for paths outside it.
- **A required server is unpinned** → pin to a digest, vendor it, or accept it with a written residual risk and network restriction.
- **The team disables approvals for speed** → make the irreversible set smaller so the gate is tolerable; never remove the gate on actions that move money, data, or code to production.
- **A tool description changes after an update** → re-review on version change; descriptions are an injection surface, so a "minor" update is still a review trigger.
- **Secrets are already in the environment** → rotate (`04-process/git-operations/` P03), then re-scope; do not merely remove the environment variable.
- **A malicious instruction is found in a fetched file** → treat as a security incident: identify every machine and session that fetched it, revoke credentials used in those sessions, and add provenance to the fetch path.
- **The audit reveals production credentials in a developer agent** → stop, rotate, and move to short-lived, per-command injection before continuing the audit.

## 8. Security and authorisation

Risk class B: you may read configuration and *reduce* permissions. Widening any permission, or granting a new tool, is C/D and requires an explicit approver. Never print a credential value, token, or key; enumerate names only. Never run an untrusted server to "see what it does" on a host with real credentials — use a disposable environment. If an exfiltration path is plausible, assume it may already have been used and escalate to incident response rather than silently tightening the config.

## 9. Completion criteria

- [ ] Inventory matches the actual configuration files.
- [ ] Six-axis capability table with cited evidence per tool.
- [ ] All six accidental-escalation patterns checked.
- [ ] Supply chain recorded per server: publisher, source, pin, install scripts.
- [ ] Remote-fetched rule/document channels identified with their trust boundary.
- [ ] Least-privilege changes applied and recorded as a diff.
- [ ] Daily workflow still passes with the tightened configuration.
- [ ] Approval gates enforced on the irreversible set.
- [ ] Audit log and kill switch available.
- [ ] Residual risks recorded with owners and review dates.
- [ ] A procedure exists for approving new tools.

## 10. Deliverables and handover

Artifacts: `TOOL_PERMISSIONS.md`, permission diff, approval matrix, new-tool procedure.

Handover: `04-process/agent-context/` P02 documents the approved tool set in the canonical context file so the configuration has one stated source; AI-P04 uses the approval matrix when designing guardrails; `02-engineering/security-hardening/` owns the credential and egress findings that are not agent-specific.
