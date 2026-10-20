# Web3 Contribution Systems

Prompt systems for contributing to Web3 / blockchain projects (smart contracts, dApps, frontend, backend/indexing, and infrastructure).

> **Scope boundary.** This folder answers *"how do I contribute to someone else's protocol"*. If you own the contracts and need to review, upgrade, hold keys for, or respond to an exploit on them, use [`03-domains/web3/`](../../03-domains/web3/README.md) (`CHAIN-P01..P04`). The identifiers here (`W3-*`) belong to contribution stages; the domain uses `CHAIN-*`, so the two cannot be confused in a run log.

## Structure

| Path | Purpose |
|------|---------|
| `general/` | Core multi-stage Web3 contribution system |
| `smart-contracts/` | Solidity / contract-focused extensions |
| `frontend/` | dApp frontend specific patterns |
| `backend/` | Indexers, APIs, services |
| `infra/` | Node infrastructure, deployment, monitoring |

## Currently Available

- **general/** — Skeleton multi-stage Web3 contribution system: 8 stage outlines with sound sequencing but no evidence rules, verification, or failure handling yet. Useful for structuring a human-led session; not safe for unsupervised agent execution
