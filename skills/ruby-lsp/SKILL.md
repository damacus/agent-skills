---
name: ruby-lsp
description: >
  Use when navigating, auditing, or refactoring Ruby/Rails code and semantic code
  intelligence would help: file outlines, method signatures, definitions,
  references, inheritance/mixins, or impact analysis. Prefer native Ruby LSP
  operations when available, but fall back to token-efficient rg/outline/read
  workflows when Codex has no LSP tool.
---

# Ruby LSP Code Intelligence

## Core Rule

Use semantic navigation when a Ruby LSP tool is available. In Codex sessions without an LSP tool, do not pretend one exists; use the fallback workflow below and state the limitation when it affects confidence.

## Availability Check

Before using LSP-specific instructions, check the active tools.

- If a tool exists for `documentSymbol`, `goToDefinition`, `findReferences`, `hover`, diagnostics, or call hierarchy: use it for semantic questions.
- If no LSP tool is exposed: use `rg`, targeted reads, tests, RuboCop, and the bundled outline script.
- Do not ask the user to install tools unless the task truly needs semantic precision that fallbacks cannot provide.

## Decision Matrix

| Need | With LSP | Without LSP |
| --- | --- | --- |
| File/class/method outline | `documentSymbol` | `ruby scripts/ruby_outline.rb FILE` or `rg -n '^\s*(class|module|def)\b' FILE` |
| Method signature | `documentSymbol`, then targeted read | outline script, then targeted read around the line |
| Definition from call site | `goToDefinition` | `rg` exact method/constant patterns, then inspect likely owners |
| All usages before refactor | `findReferences` | `rg` exact symbol, filter comments/strings manually, inspect dynamic sends |
| Quick docs/signature at call | `hover` | inspect definition and nearby call sites |
| String literals, comments, configs | `rg` | `rg` |
| Verification after edits | LSP diagnostics plus tests/lint | tests/lint/syntax checks |

## Token-Efficient Ruby Workflow

1. Locate files with `rg --files -g '*.rb'` or a narrow filename query.
2. Get structure before reading large files:
   `ruby /Users/damacus/.agents/skills/ruby-lsp/scripts/ruby_outline.rb path/to/file.rb`
3. Read only the relevant line window for signatures and implementation details.
4. Before refactoring public methods/classes, search usages with exact patterns and inspect ambiguous results.
5. After edits, run the narrowest useful verification: syntax check, relevant specs, RuboCop, or project test task.

## LSP Operation Guidance

Use these only when an actual LSP tool is available in the session.

- `documentSymbol`: first choice for Ruby file structure. It returns classes, modules, methods, and line numbers, not full method bodies.
- `goToDefinition`: use from a call site or constant reference. Prefer it over searching for `def name` when inheritance or mixins may matter.
- `findReferences`: use before renames and behavior-changing refactors. It is better than text search because it can ignore unrelated strings and same-named methods.
- `hover`: useful at call sites and constants. Ruby LSP commonly does not return useful hover data on `def` lines, so do not rely on it for method signatures.

## Fallback Search Patterns

Use exact, scoped searches before broad ones.

```fish
rg -n '^\s*def (self\.)?method_name\b' app lib test spec
rg -n '^\s*(class|module) ConstantName\b|ConstantName\b' app lib test spec
rg -n '\bmethod_name\b' app lib test spec
```

When results are noisy, separate likely semantic references from comments, strings, factories, tests, and dynamically dispatched calls such as `public_send`, `send`, callbacks, route helpers, serializers, and Rails metaprogramming.

## Refactor Safety

Before changing a Ruby public API:

- Identify the owner class/module and full method signature.
- Find callers and inheritance/mixin relationships.
- Check tests that exercise the symbol before editing when feasible.
- Re-run caller searches after edits if names, arity, or return behavior changed.

## Rails Notes

Rails code often hides references in conventions. Include these in fallback impact analysis when relevant:

- routes, controllers, views, helpers, mailers, jobs, serializers, policies
- callbacks, scopes, validations, associations, concerns
- i18n keys, ActiveSupport inflections, autoload paths
- `send`, `public_send`, `constantize`, `safe_constantize`, `delegate`, and DSL macros

## Reporting

When LSP is unavailable and the task asked for semantic certainty, say that fallback search was used and name the residual risk. Keep the explanation short and attach confidence to concrete evidence: files inspected, references found, tests run.
