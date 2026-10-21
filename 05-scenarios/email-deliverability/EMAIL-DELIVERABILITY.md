# PROMPT 01 — Email Deliverability: it is not in the spam folder, it never arrived

**Identifier:** EMAIL-01
**System:** 05-scenarios/email-deliverability
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B (reads DNS and provider config; changing DNS records is C and affects a whole domain)
**Depends on:** none
**Produces:** `.email/DELIVERABILITY.md`, a DNS/auth record table, a warm-up and reputation plan
**Inputs:** DOMAIN, SENDER_STACK (optional: STREAM, VOLUME, BOUNCE_DATA, TARGET_ENV)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You find out why transactional or notification email is not arriving, and you fix the identity and reputation problems rather than the copy.

Email is the one dependency where success is invisible: the API returns `202 Accepted` and the message disappears. Nothing throws. The customer says "I never got the reset link", support blames spam, and the actual cause is a missing DMARC alignment, a shared IP with a bad reputation, or a suppression list that swallowed the address three years ago.

## 2. Objective and scope

**Produce:** an authentication record audit (SPF, DKIM, DMARC, alignment), a stream separation review, a bounce and complaint analysis, a suppression-list check, and a warm-up plan if volume is new.

Out of scope: marketing copy, template design, and purchasing a deliverability service.

## 3. Prerequisites and inputs

- `{{DOMAIN}}` — the sending domain and, critically, the **From** domain; the visible From and the envelope From differ, and alignment is measured between them.
- `{{SENDER_STACK}}` — provider (SES, Postmark, SendGrid, Resend, Google Workspace, self-hosted MTA) and whether it is shared IP or dedicated.
- `{{STREAM}}` — transactional vs marketing vs notifications; mixing them is the most common self-inflicted wound.
- `{{VOLUME}}` — daily volume and whether it is new (a new domain sending 50,000 messages on day one is a spam signal).
- `{{BOUNCE_DATA}}` — provider metrics for bounces, complaints, and opens if available.
- `{{TARGET_ENV}}` — the environment the failing send came from (production, staging, or a test domain), so test sends go only to seed addresses you control.

## 4. Workflow

1. **Verify the basics with DNS queries, not with the provider's dashboard.** The dashboard says what it configured; DNS says what the world sees. Check: `TXT` for SPF (exactly one record — two SPF records break evaluation), DKIM selectors, DMARC (`_dmarc` with `p=` and `rua=`), and the MX/return-path setup.

2. **Check SPF arithmetic.** The record has a 10-DNS-lookup limit; providers that include other providers exhaust it silently. Count the lookups (including nested `include:` and `a`/`mx`/`ptr`), and confirm the sending IP is authorised by the *envelope* sender, not the header From.

3. **Check DKIM signing and the selector in use**, including key length (1024-bit keys are deprecated in practice; 2048 is the floor) and rotation. A message signed with a selector whose public key is missing fails DKIM with no visible error.

4. **Check DMARC alignment, which is the part people get wrong.** SPF or DKIM must align with the **From** domain — not merely pass. `p=none` gives you reports and no enforcement; `p=reject` is the goal once reports are clean. Subdomain policy and the `sp=` tag matter if you send from `mail.example.com` while the From is `example.com`.

5. **Separate the streams.** Transactional (password reset, receipt) must not share a domain or IP reputation with marketing or notifications. If they do, one bad campaign suppresses every reset email. Check subdomains and provider stream configuration.

6. **Read the bounce and complaint data by category**: hard bounces (invalid address) must be suppressed permanently; soft bounces should retry with a cap; complaints above ~0.1% indicate list quality or consent problems. A suppression list that is never pruned, or never *applied* to transactional sends, causes silent non-delivery to real users.

7. **Check the content-level causes that are actually deliverability causes**: URL shorteners in transactional mail, link domains with bad reputation, image-only emails, missing `List-Unsubscribe` for bulk, and a From display name that changes every send.

8. **Check the receiving side for the specific case**: is the address a role address (`noreply@`, `admin@`)? Is the recipient on a corporate filter that blocks new domains? Ask the recipient for the SMTP response code — `550`, `421`, `5.7.1` and their provider-specific meanings — before changing anything.

9. **If the domain or IP is new, plan warm-up**: start with the most engaged recipients, ramp volume gradually, keep the bounce rate low, and do not begin with your largest batch.

10. **Write `.email/DELIVERABILITY.md`** with the DNS record table (current value, expected value, pass/fail), stream separation, bounce/complaint analysis, suppression policy, warm-up schedule, and a monitoring plan for reputation.

## 5. Decision rules and evidence standard

- **DNS is the source of truth**, not the provider UI.
- **Alignment, not just passing**, is what DMARC enforces.
- **One SPF record**; multiple records fail permanently and silently.
- **Transactional and marketing never share reputation.**
- **Hard bounces are permanent**; retrying them damages reputation.
- **A `202` from the provider means accepted, not delivered**, and is not evidence of anything.
- **Ask for the SMTP response code** before changing configuration.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| SPF | DNS query | Exactly one record, under 10 lookups, sending IP included |
| DKIM | DNS selector lookup + test send | Signature verifies; 2048-bit key |
| DMARC | DNS query | Record present, `p=` stated, alignment mode understood |
| Alignment tested | Send to a seed address | SPF or DKIM aligns with the From domain |
| Streams separated | Provider config | Transactional and marketing on distinct subdomains/IPs |
| Bounce handling | Provider logs | Hard bounces suppressed permanently |
| Suppression applied | Test address | Suppressed address is not retried |
| Complaint rate | Metrics | Below threshold, or list source investigated |
| Content risks reviewed | Template inspection | No shorteners, no image-only, unsubscribe present for bulk |
| SMTP response captured | Recipient report | Code obtained for a failing case |
| Warm-up plan | Document | Ramp schedule if domain/IP is new |

## 7. Failure handling

- **Mail goes to spam for one recipient only** → their filter, not your configuration; get the headers and the spam score before changing DNS.
- **Everything goes to spam after a campaign** → reputation damage from the shared stream; separate the streams and pause the campaign volume.
- **SPF passes but DMARC fails** → alignment problem: the envelope domain differs from the From domain. Fix by aligning the return-path or signing with the From domain.
- **Two SPF records exist** (often after adding a second provider) → merge into one; until then, SPF is broken for everyone.
- **The provider's dedicated IP has poor reputation** → warm it, or move back to shared while it recovers; a dedicated IP with no warm-up is worse than shared.
- **A user reports non-delivery and the provider says delivered** → the receiving server accepted and discarded; get the recipient's headers, and check whether the domain is on a blocklist.
- **Password resets are being suppressed** because the address hard-bounced years ago → suppression lists must distinguish "invalid" from "transient", and users need a way to re-enable email.

## 8. Security and authorisation

Risk class B: reads DNS and provider configuration. DNS changes are class C — a wrong DMARC policy can reject all legitimate mail for the domain, and a wrong SPF record can break every sender including the company's own staff. Never send test messages to real customer addresses; use seed addresses you control. DMARC aggregate reports contain recipient IPs and should be handled as personal data.

## 9. Completion criteria

- [ ] SPF verified by DNS: one record, lookup count within limits, sending IPs included.
- [ ] DKIM verified with selector and key length, including rotation status.
- [ ] DMARC present; alignment tested with a real send.
- [ ] Streams separated (transactional vs marketing) with distinct reputation.
- [ ] Bounce and complaint rates reviewed against thresholds.
- [ ] Suppression list applied and pruned.
- [ ] Content-level risks reviewed.
- [ ] SMTP response code obtained for the failing case.
- [ ] Warm-up plan written if the domain or IP is new.
- [ ] Reputation monitoring in place.

## 10. Deliverables and handover

Artifacts: `.email/DELIVERABILITY.md`, DNS table, warm-up plan.

Handover: `02-engineering/security-hardening/` owns the DNS-change review for records that affect the whole domain; `04-process/observability-reliability/` P03 adds bounce-rate and complaint-rate alerts, because these degrade before customers complain; `03-domains/payments/` reviews receipt deliverability if invoices are emailed, since a missing receipt becomes a chargeback.
