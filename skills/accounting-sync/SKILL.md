---
name: accounting-sync
description: Use when reviewing or synchronising FreeAgent bank evidence with an account-specific mailbox and Paperless, including VAT checks, carry-over review items, dry runs, and approved item-level mutations.
---

# Accounting Sync

Reconcile accounting evidence across a configured mailbox, Paperless-ngx, and FreeAgent. Keep account identities, vendor matching, tax treatment, and standing approvals outside this reusable skill.

## Policy Configuration

Resolve the NDJSON policy file in this order:

1. A path explicitly supplied by the user or automation.
2. `ACCOUNTING_SYNC_RULES`.
3. `accounting/accounting-sync.ndjson` below the current working directory.

If no policy file exists, reads and evidence classification may continue, but do not mutate anything. Report the missing policy as a blocker.

Parse the entire file before contacting any service. Require:

- one `settings` record with `schema_version: 1`;
- unique non-empty IDs for every `approval_rule` and `exception_rule`;
- only the record types `settings`, `approval_rule`, and `exception_rule`;
- decimal money values encoded as strings;
- each approval rule to define `match`, `expected`, `evidence`, and `auto_approve`;
- each exception rule to use `action: "manual_review"`.

Reject an invalid or ambiguous policy before any mutation. Never create or amend policy rules based only on a transaction observed during the current run.

The settings record supplies mailbox roles and Paperless metadata. It must not contain passwords, tokens, or other secrets. An approval rule is standing approval only when every configured matcher succeeds. An exception rule wins over an approval rule.

## Safety Contract

- Default to dry-run unless the user explicitly requests real mode or the automation explicitly declares real mode.
- Dry-run performs reads only. Do not download, create, upload, update tax, attach receipts, or approve review items.
- Before an ad-hoc real run, name the exact items and proposed mutations. Approval is item-specific and does not cover newly found items.
- In an explicitly real automation, an exact `auto_approve: true` policy match is standing item-specific approval. A rule never overrides dry-run mode.
- In real mode, mutate one item, read it back, then reload the complete review list before continuing.
- Never create missing Paperless metadata during a routine upload. Report it as a setup blocker.

## Preflight

Use keychain and network-capable execution when required.

1. Resolve and validate the policy.
2. Require `paperless >= 2.1.3` and `freeagent-cli >= 0.5.5`.
3. Run `spark accounts`. Require the configured accounting mailbox. Use other configured mailboxes only for their declared roles.
4. Run `freeagent-cli --json auth ensure --min-validity 15m`.
5. Run compact `paperless --output json status`.
6. In real mode, stop if any required system is unavailable. In dry-run, report a Paperless-only blocker but continue read-only FreeAgent and mailbox classification when those systems are healthy.

## Scope

Use the requested window or the last 7 days. Always list every outstanding FreeAgent item marked for review, including carry-over outside the window.

Start with:

```text
freeagent-cli --json bank-accounts list
freeagent-cli --json bank review list --bank-account BANK_ACCOUNT_URL --per-page 100
```

If the account summary reports outstanding review items but `bank review list` returns fewer, use `bank list --view marked_for_review` as a diagnostic fallback and report a CLI defect. Do not silently omit carry-over items.

For every touched or remaining review item collect the transaction and explanation IDs, date, amount, vendor, category, `sales_tax_status`, `sales_tax_rate`, `sales_tax_value`, attachment state, and review state.

## Rule Matching

Evaluate exception rules first. For approval rules, require every populated matcher to agree, including direction, description or reference pattern, amount constraint, category, tax treatment, and evidence policy.

- `amount_gbp.exact` must match exactly after decimal normalisation.
- `amount_gbp.min` and `amount_gbp.max` are inclusive.
- Regular expressions are applied only to their named fields.
- `required_attachment` requires an exact document match before approval.
- `required_text_regex` must match the exact supporting evidence, not a prior transaction.
- `archive_if_available` allows approval without a document but keeps missing evidence in the backlog.
- `invoice_match` requires an existing FreeAgent invoice match.
- A category or tax mismatch is a proposed correction only when the rule explicitly specifies the expected value.

If more than one approval rule matches, or an amount, category, tax field, or evidence requirement differs, stop and report the item for manual review.

## Evidence Search

Search each configured mailbox only for its declared role. Match vendor, amount, and plausible date. Search Paperless by invoice or receipt number, vendor, and amount before proposing an upload. Never attach a different charge's document, terms, or marketing material.

Classify every candidate into exactly one bucket:

1. **PDF-backed syncs**: exact PDF can be archived and attached.
2. **Existing Paperless evidence**: exact document already exists.
3. **Exact email-evidence approvals**: email body exactly supports approval but has no PDF.
4. **Standalone archives**: valid business document has no matching bank item yet.
5. **Review-only items**: operational or tax item can be reviewed without external evidence.
6. **Portal evidence needed**: evidence exists only behind a vendor portal.
7. **No-evidence items**: no reliable evidence found.

## Paperless Metadata

Use the correspondent, required tags, document type, and rule-specific vendor/domain tags from policy. Resolve names exactly and case-insensitively. Missing or ambiguous names block the item.

```text
paperless --output json document upload FILE --wait --timeout 60s --title TITLE --correspondent CORRESPONDENT --type TYPE --tag REQUIRED_TAG --tag VENDOR_TAG
```

Require the upload token, `SUCCESS` task status, and final document ID. If a successful upload omits the document ID, do not upload again. Find the document by its exact title and original filename, require exactly one match, and report the CLI defect. Read the document back and verify correspondent, type, title, and every tag. If Paperless processing overrides explicit metadata or adds an unwanted tag, correct the document to the exact policy metadata and read it back again before attaching it to FreeAgent.

## Approved Mutations

Combine only policy-approved receipt, tax, and review changes:

```text
freeagent-cli --json bank review update --explanation EXPLANATION_URL --file FILE --sales-tax-status STATUS --sales-tax-rate RATE --approve
```

Omit unapproved flags. Preserve all existing explanation fields. Never infer approval from a dry-run request.

## Post-Sync Review

After dry-run classification and after every real mutation, list category, tax status, tax rate, VAT value, evidence bucket, and tax confidence (`high`, `medium`, or `low`) for touched and remaining review items.

Flag tax inconsistencies against exact evidence and equivalent prior entries. Do not certify a vendor's VAT from identity alone when the invoice is missing.

Read back every update. Require requested tax fields and attachment filename to match, clear `marked_for_review` only when approved, and preserve category, date, gross value, description, project, and rebill fields.

After every approval, reload the complete review list and compare it with the expected remaining IDs. If unrelated items disappear, stop further approvals, compare their update timestamps, and restore policy exceptions to review before continuing.

## Report

State the mode, window, policy path, preflight health, all seven evidence buckets, matched rule IDs, proposed or completed mutations, blockers, and post-sync review. Include transaction ID, explanation ID, Paperless document ID, and filename for completed syncs.
