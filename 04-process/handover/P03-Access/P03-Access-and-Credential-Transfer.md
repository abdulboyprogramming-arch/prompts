# PROMPT 03 — Access, Credentials, and Revocation

**Identifier:** HAND-P03
**System:** 04-process/handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D — ownership moves and standing access changes; a mistake leaves access with the wrong party or removes it from the right one
**Depends on:** HAND-P02
**Produces:** `ACCESS_TRANSFER.md`
**Inputs:** TARGET_SERVICE, HANDOVER_RECEIVER (optional: APPROVER, CHANGE_WINDOW)
**Est. effort:** 1–3 h, often gated by account owners

---

## 1. Role and mandate

You move control of the system's identities from the sender to the receiver, and you remove the sender's standing access. Both halves are required. Handovers that add the receiver but never revoke the sender are how ex-contractors keep production access for a year.

This is the highest-consequence stage in the system: a wrong revocation takes the system's only owner account offline; a missed revocation leaves an outsider with production rights.

## 2. Objective and scope

**Produce:** `ACCESS_TRANSFER.md` — every identity, role, and secret relevant to the system, its before/after holder, the transfer mechanism, the revocation performed, the rotation performed, and the evidence for each.

Out of scope: deciding what transfers (P01), capability testing (P04). Credential rotation for a *leaked* secret is `04-process/git-operations/` P03, not this stage.

## 3. Prerequisites and inputs

- `HANDOVER_STATE.md` (where the identities and secret stores are for `{{TARGET_SERVICE}}`), `HANDOVER_SCOPE.md` (who is authorised to hold what).
- `{{HANDOVER_RECEIVER}}` identity — a named principal in each system, not a shared account.
- `{{APPROVER}}` for owner-level grants and for revocations that affect production; `{{CHANGE_WINDOW}}` where access changes require one.

## 4. Workflow

1. **Build the identity inventory before changing anything.** For each system: cloud account and organisation, source control and its owners, CI/CD and its secrets, registries, databases and their superusers, DNS and domains, certificates, monitoring, flag providers, vendor consoles, billing, and the break-glass credential. Record current holders, roles, and whether the account is personal or organisational.

2. **Identify the accounts that cannot be removed** — the ones whose loss locks everyone out: the domain registrar contact, the cloud root/owner, the billing owner, the sole admin of a vendor console. For each, plan a **dual-control** end state: a named receiver plus a documented recovery path (a second owner, a sealed break-glass, a support escalation). Never leave exactly one holder.

3. **Prefer adding the receiver before removing the sender.** Order matters: grant scoped access to the receiver, verify they can use it, then revoke. The reverse order creates a window where nobody can fix a problem.

4. **Transfer ownership, not just permissions.** Organisation ownership, billing responsibility, domain registrant, repository ownership, app installations, and the "owner" role in each SaaS console. A receiver with member access but no owner cannot accept the handover.

5. **Rotate every shared secret the sender could read.** Shared passwords, service-account keys, CI tokens, webhook signing secrets, API keys in the vendor consoles. Rotation is the only way a departed holder loses the capability. Record each rotation and confirm the system still works afterwards.

6. **Verify least privilege for the receiver.** Their access should match their role, not mirror the sender's accumulated permissions. Remove the extras; note each removal.

7. **Revoke the sender explicitly, and prove it.** After revocation, attempt the access you removed (a login attempt, a token use, a console check) and record the result. "I removed them from the group" is a claim; a failed authentication is evidence.

8. **Handle the retained-access exceptions deliberately.** Where the sender must stay reachable (a support window), grant time-boxed, narrow, logged access — not their old standing role — and record the expiry and the person who will revoke it.

9. **Record the recovery path** so the receiver is not one accident from lockout: who else holds owner, where break-glass is stored and how it is used, how a lost MFA device is recovered, and which vendor support route exists.

10. **Write `ACCESS_TRANSFER.md`:** the inventory with before/after, mechanisms, rotations, revocations with proof, exceptions with expiry, the recovery path, and an explicit list of anything left unresolved with its owner and date.

## 5. Decision rules and evidence standard

- **Two halves or it did not happen.** Grant without revoke, or revoke without proof, is an incomplete transfer.
- **No shared accounts as the end state.** Where a shared identity exists, replace with named principals and a documented recovery path.
- **Rotate everything the sender could read**, including secrets that "only" grant read access.
- **Dual control for the irreversible** — ownership of domains, cloud root, and billing always has a second holder.
- **Evidence over assertion**: a failed login attempt, a console screenshot reference, a command output.
- **Exceptions expire.** Any retained access has a date and a named revoker.
- **Order: add, verify, remove.** Never create an ownership vacuum to save a step.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Inventory complete | cross-check with P02 | every identity listed |
| Lockout-risk accounts identified | review | each has a dual-control plan |
| Receiver access verified | receiver performs a scoped action | succeeds |
| Ownership transferred, not just membership | console check | owner/admin role confirmed |
| Secrets rotated | rotation log + system check | works after rotation |
| Sender revocation proven | access attempt | denied |
| Least privilege applied | role diff | no inherited excess |
| Exceptions time-boxed | table | expiry and revoker named |
| Recovery path documented | inspect | second holder + break-glass |

## 7. Failure handling

- **The sender is the sole owner of a system** (domain, cloud root, vendor console) → transfer ownership before anything else; if the mechanism requires the sender to act and they are unavailable, escalate to vendor support and record the delay as a blocking dependency.
- **Revocation would break the system** (a CI service still authenticates as the sender) → replace the credential with a service identity first, then revoke; record the interim exposure.
- **MFA or hardware token is the only second factor** → establish a second enrolled device held by the receiving organisation before revoking the sender's.
- **A secret appears in history or a document** → rotate now and treat any use as a potential compromise; route evidence to `02-engineering/security-hardening/`.
- **Revocation cannot be proven** (no audit log, no test identity) → record it as unverified, name the owner who must confirm, and do not close the stage as complete.

## 8. Security and authorisation

Risk class D: this stage changes production access and ownership. Every grant and revocation requires the authority named in P01 and, for owner-level changes, `{{APPROVER}}`. Never paste credentials, tokens, or recovery codes into the artifact — record the store and the holder. Do not create a shared account "temporarily" (it will survive the handover). Do not disable audit logging to simplify the transfer. If a revocation affects a production control, perform it inside `{{CHANGE_WINDOW}}` with the receiver present.

## 9. Completion criteria

- [ ] Identity inventory complete, including vendor and billing consoles.
- [ ] Lockout-risk accounts identified with a dual-control plan.
- [ ] Receiver access granted, scoped, and verified in use.
- [ ] Ownership roles transferred in every system.
- [ ] All shared secrets the sender could read rotated, system verified after.
- [ ] Sender access revoked with proof of denial.
- [ ] Retained-access exceptions time-boxed with a named revoker.
- [ ] Recovery path documented (second holder, break-glass, MFA recovery).
- [ ] Unresolved items listed with owner and date.

## 10. Deliverables and handover

Artifact: `ACCESS_TRANSFER.md`.

P04 receives: the receiver's confirmed access, so the capability tests exercise real permissions rather than the sender's. P05 receives: any unresolved revocation or rotation as a condition of acceptance — a handover cannot be signed while an outsider still holds access.
