---
name: accounting-sync
description: Synchronizes bank transactions from FreeAgent with invoices found in Gmail, uploads them to Paperless-ngx, and attaches them back to FreeAgent. Use this skill for weekly accounting maintenance or when the user asks to "sync invoices" or "connect FreeAgent and Paperless".
---

# Accounting Sync: FreeAgent <-> Gmail <-> Paperless-ngx

This skill automates the workflow of matching bank transactions with their corresponding invoices and ensuring they are archived in Paperless-ngx and linked in FreeAgent.

## Core Workflow

### 1. Identify Target Transactions
- Query FreeAgent for unexplained or recently explained transactions in the past 7 days.
- Reference `references/vendors.json` to filter transactions from known sources (Anthropic, Windsurf, OpenAI, Maslins, etc.).
- `freeagent-cli --json raw --path "/v2/bank_transactions?bank_account=YOUR_PRIMARY_ACCOUNT_URL&from_date=YYYY-MM-DD"`

### 2. Search Gmail for Invoices
- For each target transaction, use the vendor's `gmail_query` from `references/vendors.json`.
- Match emails by date (within +/- 3 days) and amount (considering currency conversion if applicable).
- `gws gmail +triage --query "from:vendor@example.com subject:invoice"`

### 3. Extract and Process PDFs
- If a matching email has a PDF attachment:
  - Download the PDF to a temporary location.
  - `gws gmail users messages attachments get --params '{"userId": "me", "messageId": "MSG_ID", "id": "ATTACH_ID"}'`
  - Upload to Paperless-ngx with the vendor's tags.
  - `PAPERLESS_URL="..." paperless documents upload "/tmp/invoice.pdf" --tag vendor_tag --tag AI`

### 4. Link back to FreeAgent
- If the transaction is already explained but lacks an attachment:
  - Use the "Delete and Re-create" pattern to attach the receipt.
  - `freeagent-cli raw --method "DELETE" --path "/v2/bank_transaction_explanations/EXPLANATION_ID"`
  - `freeagent-cli bank explain create --bank-transaction TX_ID --dated-on ... --description ... --gross-value ... --category ... --receipt /tmp/invoice.pdf`

## Vendor Configuration
See [references/vendors.json](references/vendors.json) for the list of known vendors and their matching rules.

## Security & Reliability
- Always verify the amount matches before attaching a document.
- Handle "database is locked" errors in Paperless by retrying with a short delay.
- Use `--dry-run` with `gws` or `freeagent-cli` if unsure about a mutation.
