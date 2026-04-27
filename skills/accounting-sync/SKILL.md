---
name: accounting-sync
description: Synchronizes bank transactions from FreeAgent with invoices found in Gmail, uploads them to Paperless-ngx, and attaches them back to FreeAgent. Use this skill for weekly accounting maintenance or when the user asks to "sync invoices" or "connect FreeAgent and Paperless".
---

# Accounting Sync: FreeAgent <-> Gmail <-> Paperless-ngx

This skill automates the workflow of matching bank transactions with their corresponding invoices and ensuring they are archived in Paperless-ngx and linked in FreeAgent.

## Core Workflow

### 1. Verify Authentication
- Confirm Gmail auth is valid before searching for invoices.
- `gws auth status`
- Confirm FreeAgent auth is valid before querying bank data.
- `freeagent-cli auth status`
- Confirm Paperless is reachable before attempting uploads.
- `paperless stats`
- In this environment, Gmail reads via `gws` may fail inside the sandbox even when auth looks valid. Run `gws` outside the sandbox when keychain or trust-store errors appear.

### 2. Identify Target Transactions
- Query FreeAgent for unexplained or recently explained transactions in the past 7 days.
- Start by listing available bank accounts and identifying the primary account to inspect.
- `freeagent-cli bank-accounts list`
- Reference `references/vendors.json` to filter transactions from known sources (Anthropic, Windsurf, OpenAI, Maslins, etc.).
- Use the bank transaction commands to review and work with transactions instead of relying on raw API calls where possible.
- `freeagent-cli bank explain --help`
- `freeagent-cli bank approve --help`
- In practice, FreeAgent review workflows still require `freeagent-cli --json raw --path ...` for efficient discovery of `marked_for_review`, existing explanations, and attachment state.

### 3. Search Gmail for Invoices
- For each target transaction, use the vendor's `gmail_query` from `references/vendors.json`.
- Match emails by date (within +/- 3 days) and amount (considering currency conversion if applicable).
- `gws gmail +triage --query "from:vendor@example.com subject:invoice"`
- Windsurf receipts currently arrive from Stripe as `Your receipt from Exafunction, Inc. #...` with PDF attachments. Match on `Exafunction` receipt subjects, not just `codeium.com`.
- Cloudflare may require USD-to-GBP conversion before a receipt amount can be matched to the bank transaction amount.

### 4. Extract and Process PDFs
- If a matching email has a PDF attachment:
  - Download the PDF into the Paperless staging area inside the workspace, not `/tmp`.
  - `mkdir -p ./paperless`
  - `gws gmail users messages attachments get --params '{"userId": "me", "messageId": "MSG_ID", "id": "ATTACH_ID"}' | jq -r .data | tr '_-' '/+' | base64 -D -o ./paperless/receipt.pdf`
  - Upload to Paperless-ngx with the vendor's tags.
  - `paperless documents upload "./paperless/receipt.pdf" --tag vendor_tag --tag AI`
- Treat Paperless as the durable staging location for matched receipts before any FreeAgent mutation.

### 5. Link back to FreeAgent
- If the transaction is already explained but lacks an attachment:
  - First try updating the explanation in place with a receipt.
  - `freeagent-cli bank explain update EXPLANATION_ID --receipt ./paperless/receipt.pdf`
  - If `freeagent-cli` refuses receipt-only updates, fall back to the "Delete and Re-create" pattern.
  - `freeagent-cli raw --method "DELETE" --path "/v2/bank_transaction_explanations/EXPLANATION_ID"`
  - `freeagent-cli bank explain create --bank-transaction TX_ID --dated-on ... --description ... --gross-value ... --category ... --receipt ./paperless/receipt.pdf`
- After receipts are attached or explanations are confirmed correct, clear review flags with `freeagent-cli bank approve`.
- Payroll, dividend, and pension transactions may be valid non-receipt review items. If their explanation type/category is already correct, approve them without forcing a Gmail receipt lookup.

## Vendor Configuration
See [references/vendors.json](references/vendors.json) for the list of known vendors and their matching rules.

## Security & Reliability
- Always verify the amount matches before attaching a document.
- Handle "database is locked" errors in Paperless by retrying with a short delay.
- Use `--dry-run` with `gws` or `freeagent-cli` if unsure about a mutation.
- Prefer automation in two stages:
  - Gmail/Paperless sync: search, fetch, decode, and upload receipts.
  - FreeAgent review cleanup: identify review-flagged transactions, attach receipts where available, and approve correctly explained items.
