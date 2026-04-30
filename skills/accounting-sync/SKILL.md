---
name: accounting-sync
description: Synchronizes bank transactions from FreeAgent with invoices found in Gmail, uploads them to Paperless-ngx, and attaches them back to FreeAgent. Use this skill for weekly accounting maintenance or when the user asks to "sync invoices" or "connect FreeAgent and Paperless".
---

# Accounting Sync: FreeAgent <-> Gmail <-> Paperless-ngx

This skill automates the workflow of matching bank transactions with their corresponding invoices and ensuring they are archived in Paperless-ngx and linked in FreeAgent.

## Core Workflow

### 0. Mandatory Auth Preflight
Run this before any dry-run or real-mode work. If either Gmail or FreeAgent is not authenticated, stop and report the blocker. Do not continue to Gmail searches, FreeAgent reads, Paperless checks, or local file staging.

- `gws auth status`
  - Required: exit code 0, `token_valid: true`, and usable credential encryption.
  - If the sandbox cannot read keychain credentials but an escalated/keychain-capable check succeeds, note that future commands must use the same keychain-capable execution path.
- `freeagent-cli auth status`
  - Required: exit code 0 and `expired=false`.
  - If the CLI reports `no tokens stored`, stop and ask the user to reauthenticate FreeAgent.
- `paperless status`
  - Required for real mode.
  - In dry-run mode, a Paperless failure may be reported as a Paperless-only blocker, but do not upload or attach anything.

The auth preflight is step zero because partial runs create noise: Gmail-only or FreeAgent-only scans cannot prove whether an item is ready to sync.

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

### 3. Search Gmail for Invoices
- For each target transaction, use the vendor's `gmail_query` from `references/vendors.json`.
- Match emails by date (within +/- 3 days) and amount (considering currency conversion if applicable).
- Use a broad attachment search for the same window to catch vendors not yet in the config:
  - `gws gmail +triage --format json --max 50 --query '(receipt OR invoice) has:attachment after:YYYY/MM/DD before:YYYY/MM/DD'`
- Use vendor-specific searches for known vendors:
  - `gws gmail +triage --format json --max 10 --query "from:vendor@example.com subject:invoice after:YYYY/MM/DD"`

### 4. Extract and Validate PDFs
- If a matching email has a PDF attachment:
  - Read full message metadata to identify attachment IDs.
  - Download only the business invoice or receipt PDF, not terms and conditions or marketing attachments.
  - `gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' --format json`
  - `gws gmail users messages attachments get --params '{"userId":"me","messageId":"MSG_ID","id":"ATTACH_ID"}' --format json`
- If `gws` returns base64url JSON instead of writing a file, decode `.data` into a local PDF.
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
- In real mode, upload the verified PDF with vendor/year/company tags and the best document type.
- Prefer existing Paperless IDs:
  - `2026`: tag id 57
  - `AI`: tag id 59
  - `exafunction`: tag id 61
  - `Webb Agile Solutions Ltd`: tag id 2
  - `Invoice`: document type id 8
  - `Receipt`: document type id 2
  - `Webb Agile Solutions Ltd`: correspondent id 7
- Example:
  - `paperless --output json document upload PDF_PATH --title 'TITLE' --type-id TYPE_ID --correspondent-id 7 --tag-id 57 --tag-id 59 --tag-id VENDOR_TAG --tag-id 2`
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
