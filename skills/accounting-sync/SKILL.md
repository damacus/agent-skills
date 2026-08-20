---
name: accounting-sync
description: Synchronizes bank transactions from FreeAgent with invoices found through Spark, uploads them to Paperless-ngx, and attaches them back to FreeAgent. Use this skill for weekly accounting maintenance or when the user asks to "sync invoices" or "connect FreeAgent and Paperless".
---

# Accounting Sync: FreeAgent <-> Spark <-> Paperless-ngx

This skill automates the workflow of matching bank transactions with their corresponding invoices and ensuring they are archived in Paperless-ngx and linked in FreeAgent.

## Core Workflow

### 0. Mandatory Auth Preflight
Run this before any dry-run or real-mode work. If either Spark or FreeAgent is unavailable, stop and report the blocker. Do not continue to mailbox searches, FreeAgent reads, Paperless checks, or local file staging.

- `spark accounts`
  - Required: Spark Desktop is running, CLI access is enabled, and the accounting-evidence account `dan.webb@damacus.io` (damacus.io) is listed.
  - Optional: `dan.m.webb@gmail.com` (personal Gmail) and `daniel.webb@equalexperts.com` (EE) may be listed when their scoped workflows are needed; do not block routine accounting sync if either is absent.
  - Run through keychain/network-capable execution when the sandbox cannot reach the Spark Desktop bridge.
- `freeagent-cli auth status`
  - Required: exit code 0 and `expired=false`.
  - If the CLI reports `no tokens stored`, stop and ask the user to reauthenticate FreeAgent.
- `paperless status`
  - Required for real mode.
  - In dry-run mode, a Paperless failure may be reported as a Paperless-only blocker, but do not upload or attach anything.

The auth preflight is step zero because partial runs create noise: mailbox-only or FreeAgent-only scans cannot prove whether an item is ready to sync.

### 1. Establish Run Mode and Date Window
- Confirm whether the run is dry-run or real mode.
- Use the requested window. If the user does not specify one, default to the past 7 days.
- Record the exact window in the final report, for example `2026-04-16 through 2026-04-30`.

### 2. Identify Target Transactions
- Query FreeAgent for unexplained or recently explained transactions in the date window.
- Prefer the primary active business bank account unless the user specifies another account.
- Reference `references/vendors.json` to filter transactions from known sources.
- Include recently explained transactions with `has_attachment=false`; those are often the main sync targets.
- Example:
  - `freeagent-cli --json bank-accounts list`
  - `freeagent-cli --json bank list --bank-account BANK_ACCOUNT_URL --from YYYY-MM-DD --to YYYY-MM-DD --per-page 100`
  - `freeagent-cli --json bank review get BANK_TRANSACTION_URL`

### 3. Search Spark for Invoices
- Use account-scoped Spark searches. The normal accounting-evidence account is `dan.webb@damacus.io`; do not search the personal Gmail account by default.
- `dan.m.webb@gmail.com` (Gmail) is for personal mail and EE-Timesheet OTPs, not routine accounting evidence.
- `daniel.webb@equalexperts.com` (EE) is for consultancy correspondence. Search it only when a transaction is clearly EE-related or the user asks for consultancy evidence.
- For each target transaction, use the vendor's `gmail_query` from `references/vendors.json` as Spark's Gmail-style `--filter` value.
- Match emails by date (within +/- 3 days) and amount (considering currency conversion if applicable).
- Use a broad attachment search for the same window to catch vendors not yet in the config:
  - `spark search --in dan.webb@damacus.io --filter '(receipt OR invoice) has:attachment after:YYYY/MM/DD before:YYYY/MM/DD' --page-size 50`
- Use vendor-specific searches for known vendors:
  - `spark search --in dan.webb@damacus.io --filter 'from:vendor@example.com subject:invoice after:YYYY/MM/DD' --page-size 10`

### 4. Extract and Validate PDFs
- If a matching email has a PDF attachment:
  - Read the full thread to identify the attachment IDs: `spark thread MESSAGE_ID`.
  - Download only the business invoice or receipt PDF, not terms and conditions or marketing attachments.
  - `spark attachment ATTACHMENT_ID --stream > /Users/damacus/receipts/paperless/FILENAME.pdf`
- Store staged PDFs under `/Users/damacus/receipts/paperless/` using the original invoice or receipt filename when possible.
- Verify before upload or attachment:
  - `file /Users/damacus/receipts/paperless/FILENAME.pdf`
  - Required: `PDF document`, expected file size, and the expected vendor amount visible in the email body or extracted text.

### 5. Search Paperless Before Uploading
- Search by invoice number, receipt number, vendor, and amount before uploading.
- If Paperless already has the document, do not upload a duplicate; use the existing document as the archive evidence and continue to FreeAgent attachment if needed.
- Examples:
  - `paperless --output json search query 'AKD-736127147787'`
  - `paperless --output json search query '2171 4358'`

### 6. Upload to Paperless
- In real mode, upload the verified PDF with IDs resolved from the user's local Paperless instance.
- Treat `references/vendors.json` as semantic configuration, not an ID registry:
  - Use `default_paperless_profile` and `paperless_profiles` for shared user/work tags, such as `Work`.
  - Use the vendor's `paperless_profile` to select those shared tags.
  - Use `paperless_correspondent` for the document sender/vendor, falling back to `name` if it is absent.
  - Use `paperless_tags` for vendor or domain tags, such as `anthropic`, `AI`, `DNS`, or `accounting`.
  - Resolve every tag, correspondent, and document type name to the user's local Paperless IDs before upload.
  - Do not assume numeric Paperless IDs are portable between users or instances.
- Example:
  - `paperless --output json document upload PDF_PATH --title 'TITLE' --type-id TYPE_ID --correspondent-id VENDOR_CORRESPONDENT_ID --tag-id YEAR_TAG_ID --tag-id PROFILE_TAG_ID --tag-id VENDOR_TAG_ID`
- If Paperless returns `database is locked`, wait briefly and retry once. If the retry also fails, stop and report the Paperless blocker without re-attaching the same receipt again.

### 7. Link Back to FreeAgent
- For an already explained transaction with no attachment, attach the verified PDF to the existing explanation.
- Prefer the review helper over delete/re-create when available:
  - `freeagent-cli --json bank review attach-receipt --explanation EXPLANATION_URL --file PDF_PATH --approve`
- Only use delete/re-create when the helper is unavailable or the existing explanation cannot accept an attachment.
- Never attach if amount, date, and vendor do not all match.
- Never attach terms and conditions PDFs.

### 8. Post-Mutation Verification
After each real-mode sync, verify both sides before reporting success:

- FreeAgent:
  - `freeagent-cli --json bank review get BANK_TRANSACTION_URL`
  - Required: `has_attachment=true`, expected filename, and `marked_for_review=false` if `--approve` was used.
- Paperless:
  - Search by invoice or receipt number.
  - Required: one matching document and the expected title/content.
- Final report:
  - List synced items with transaction ID, explanation ID, Paperless document ID, and attachment filename.
  - List skipped items and why they were skipped.
  - List blockers separately from skipped non-target transactions.

## Vendor Configuration
See [references/vendors.json](references/vendors.json) for the list of known vendors and their matching rules.

## Security & Reliability
- Auth preflight is mandatory in dry-run and real mode.
- Always verify the amount, date, and vendor before attaching a document.
- Always verify the staged file is a PDF before uploading or attaching.
- Search Paperless before uploading to avoid duplicates.
- Handle `database is locked` errors in Paperless by retrying once with a short delay.
- Use dry-run mode to enumerate candidates only; do not stage partial evidence as a substitute for authentication.
- In real mode, mutate one matched item at a time and verify it before moving to the next.
