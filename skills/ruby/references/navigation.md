# Ruby Navigation and Impact Analysis

Use semantic navigation when an actual Ruby LSP or equivalent tool is available
and helpful. Do not mandate a particular external service or initialize one for
simple text work.

## Preferred Operations

For declarations, signatures, definitions, references, inheritance, mixins,
diagnostics, or call hierarchy, prefer the available semantic operation. Read
only the method or class bodies needed for the task.

For configuration, strings, templates, metaprogramming, and DSL declarations,
text search may be more complete than an LSP.

## Fallback Workflow

1. Locate files with `rg --files` and a narrow Ruby or template glob.
2. Get structure with a semantic overview, an exact declaration search, or the
   bundled `scripts/ruby_outline.rb` helper resolved relative to this skill.
3. Read a targeted line window around the relevant definition.
4. Search callers before changing names, arity, visibility, or return behavior.
5. Verify with focused tests, diagnostics, and lint.

Useful fallback searches include exact class/module declarations, method
definitions, and word-bounded call names. Inspect ambiguous results rather than
assuming text matches are semantic references.

## Trace a User Flow

For a feature or user action, start at every route, command, event, or scheduled
entry point. Follow success and failure paths through authorization,
controllers, models or services, callbacks, jobs, mailers, broadcasts, storage,
and external systems. Record the decisions that change the path and side
effects that outlive the request. Consult local Git history when the code alone
cannot explain a surprising constraint; do not fetch remotes just to narrate a
flow.

## Dynamic Ruby and Rails

Account for references hidden in:

- callbacks, associations, validations, scopes, and route helpers;
- concerns, inheritance, refinements, delegation, and generated methods;
- `send`, `public_send`, `define_method`, `method_missing`, and constantization;
- serializers, policies, jobs, mailers, views, and i18n keys; and
- autoload paths, inflections, engines, and framework conventions.

When fallback search cannot establish semantic certainty, state the residual
risk instead of pretending the result is complete.
