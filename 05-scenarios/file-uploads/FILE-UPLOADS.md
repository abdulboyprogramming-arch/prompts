# PROMPT 01 — File Uploads and Object Storage

**Identifier:** UPLOAD-01
**System:** 05-scenarios/file-uploads
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B (writes upload paths and storage config; public bucket changes are C)
**Depends on:** none
**Produces:** `.uploads/UPLOAD_DESIGN.md`, validation tests, a lifecycle policy
**Inputs:** STORAGE_BACKEND, USE_CASES (optional: MAX_SIZE, FILE_TYPES, TARGET_ENV, RETENTION)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You make file uploads safe, resumable, and bounded — and you stop the storage bucket from becoming an unindexed copy of the customer database.

Uploads are a security surface (malware, path traversal, content-type spoofing, SSRF through image processing), a cost surface (unbounded storage, egress, orphaned objects), and a privacy surface (documents and photos containing personal data that no deletion process knows about). Most implementations handle the happy path and none of the three.

## 2. Objective and scope

**Produce:** a validated upload path with signed direct-to-storage transfers for files over the size limit of the application server, content verification, size and type limits, lifecycle rules for orphans and retention, and tests for the attacks.

Out of scope: media transcoding pipelines (a product concern), and CDN performance tuning.

## 3. Prerequisites and inputs

- `{{STORAGE_BACKEND}}` — S3/GCS/Azure Blob/local disk; whether the bucket is public, private, or signed-URL only.
- `{{USE_CASES}}` — avatars, documents, CSV imports, media, attachments. Each has different risks and limits.
- `{{MAX_SIZE}}`, `{{FILE_TYPES}}` — the declared policy; `{{RETENTION}}` — how long objects live and whether deletion is user-triggered.
- `{{TARGET_ENV}}` — test in a non-production bucket.

## 4. Workflow

1. **Decide the transfer path deliberately**: direct-to-storage with a short-lived signed URL (scales, avoids proxying bytes through your app) versus through the application (allows inspection before storage, costs bandwidth). State which and why. If direct, the validation must still happen **after** upload and before the object is marked usable.

2. **Enforce limits in three places**, because any one of them can be bypassed: the client (UX only), the signed-URL policy or reverse proxy (size, content type), and the server (authoritative). A size limit only in the browser is not a limit.

3. **Validate content by inspection, not by declaration.** Trust the magic bytes over the `Content-Type` header and the extension. Reject mismatches. For images, re-encode rather than trusting the file: re-encoding strips embedded scripts, EXIF metadata (including GPS), and malformed payloads.

4. **Design naming and access**: never use the user-supplied filename as the storage key (path traversal, collisions, unicode tricks); generate a key and store the original name as metadata. Make the bucket private; serve via signed URLs with a short TTL, or through an authorising proxy. Check that an object can only be fetched by someone who is entitled to it.

5. **Handle the malware case**: scan uploads before they are downloadable by anyone else, quarantine rather than delete, and define what the user sees while a scan is pending. For document use cases this is a requirement, not an enhancement.

6. **Stop SSRF in processing**: never fetch a URL supplied by a user to produce a thumbnail or preview (`?url=`), and never let an image library follow remote references. Allowlist outbound hosts if the feature is unavoidable.

7. **Make uploads resumable and idempotent** for large files: multipart with part checksums, a client-generated idempotency key so a retry does not create a second object, and an explicit abort path that cleans up incomplete parts (they are billed).

8. **Design lifecycle**: orphaned uploads (object created, form never submitted) expire after N days; soft-deleted files purge after retention; versions are limited; incomplete multipart uploads abort. Without rules, storage grows monotonically and nobody notices until the invoice.

9. **Connect deletion to privacy**: a user deletion request must delete their objects too (`04-process/privacy-requests/`). Objects referenced only by a URL in a database row are the ones that survive a "delete account" button. Record object keys against the owning entity so deletion is queryable.

10. **Write `.uploads/UPLOAD_DESIGN.md`**: transfer path, limit enforcement points, content validation, naming and access, scanning, lifecycle rules, retention, and the tests that prove each control.

## 5. Decision rules and evidence standard

- **The bucket is private**; access is granted per request, not by obscurity.
- **Inspect content; do not trust declarations.**
- **Re-encode images** — it removes more attacks than any filter.
- **Server-side limits are the only limits.**
- **Every object has an owner row**, so deletion and retention are possible.
- **Incomplete multipart uploads are a cost bug** and a cleanup job.
- **Quarantine, never silently delete**, when scanning is in play.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Limit enforcement | Oversized upload at proxy and server | Rejected at both |
| Type validation | Renamed `.exe` as `.jpg` | Rejected on magic-byte check |
| Image re-encode | Upload with EXIF GPS and embedded payload | Metadata stripped, payload gone |
| Key generation | Upload named `../../etc/passwd` | Stored under a generated key |
| Access control | Fetch another user's object | Denied |
| Signed URL expiry | Use an expired URL | Rejected |
| Malware scan | EICAR-style test file | Quarantined, not downloadable |
| SSRF | Submit a URL for processing | Refused or allowlisted |
| Resumable upload | Interrupt and resume | Single object, no duplicate |
| Idempotency | Repeat the finalise call | One object |
| Orphan cleanup | Abandon an upload | Expired per lifecycle rule |
| Deletion | Delete the owning entity | Objects and parts removed |

## 7. Failure handling

- **The bucket is already public** → treat as a data exposure: enumerate objects, assess sensitivity, switch to private, and issue signed URLs; if the URLs were indexed, that is an incident (`05-scenarios/security-incident/`).
- **A file type cannot be validated reliably** (proprietary formats) → accept only from trusted sources, scan, and store isolated; do not pretend validation happened.
- **Virus scanning is not available** → restrict the use case (no public sharing of uploaded documents) and record the risk.
- **Storage cost is growing faster than usage** → check orphans, versions, and incomplete parts before adding lifecycle rules; the leak is usually one of the three.
- **Deletion requests leave objects behind** → add the object key to the deletion query, and verify by attempting to fetch after deletion.
- **An image pipeline is exploited through a crafted file** → pin and patch the processing library, run it in a sandbox with no network, and re-encode on ingest.

## 8. Security and authorisation

Risk class B; making a bucket public or changing CORS is C and needs review. Uploads are untrusted input: never execute, include, or serve them from your application's origin (serve from a separate domain to avoid stored XSS). Store malware scans' results, and never log file contents. EXIF and document metadata are personal data; strip or handle them deliberately.

## 9. Completion criteria

- [ ] Transfer path chosen and justified.
- [ ] Size and type limits enforced at proxy and server, not only in the client.
- [ ] Content validated by magic bytes; mismatches rejected.
- [ ] Images re-encoded; metadata stripped.
- [ ] Storage keys generated; user filenames kept as metadata only.
- [ ] Bucket private; access via short-lived signed URLs or an authorising proxy.
- [ ] Malware scanning or an explicitly recorded risk.
- [ ] SSRF paths refused or allowlisted.
- [ ] Multipart uploads resumable and idempotent; incomplete parts aborted.
- [ ] Lifecycle rules for orphans, versions, and retention.
- [ ] Object keys tied to owning entities; deletion verified.
- [ ] Tests written for the attacks above.

## 10. Deliverables and handover

Artifacts: `.uploads/UPLOAD_DESIGN.md`, validation tests, lifecycle configuration.

Handover: `04-process/privacy-requests/` P02 includes object keys in deletion scope; `03-domains/cost-engineering/` watches storage and egress growth; `05-scenarios/deployment-target/` notes that local disk is ephemeral — uploads must never be written to the container filesystem; `02-engineering/security-hardening/` owns the malware and SSRF findings as security work.
