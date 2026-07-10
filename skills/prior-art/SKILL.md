---
name: prior-art
description: >
  Discover how a codebase already handles a concern before extending it. Use
  when asked how the repository does something, where a pattern lives, whether
  implementations are consistent, or what convention new work should follow.
---

# Find Prior Art

Research the concern broadly enough to distinguish the dominant pattern from a
single example. This is codebase archaeology, not an automatic endorsement of
everything already present.

## Search

Use several relevant strategies:

- domain and implementation keywords;
- common framework, configuration, base-class, middleware, and task locations;
- dependency and lock files;
- dedicated directories, shared modules, and generated interfaces;
- tests that demonstrate the public contract; and
- local Git history for key files or concepts when it explains evolution.

Do not stop at the first match. Bound the search once additional results stop
changing the pattern, exception list, or recommendation. Do not fetch remotes
unless the task explicitly requires current remote history.

## Report

Explain:

1. the primary approach in plain language;
2. where configuration, shared setup, implementation, and tests live;
3. naming and structural conventions;
4. meaningful exceptions and why they may differ;
5. whether the pattern appears stable, mixed, or in migration; and
6. the safest way to extend it.

Include precise file references. Follow a healthy established convention when
it fits, but do not reproduce a known inconsistency, security weakness, or
legacy workaround without stating the trade-off.

## Provenance

Adapted from Thoughtbot's [rails-consultant][source] `prior-art` skill at
revision `f2cb97d`. Distributed under the accompanying MIT license.

[source]: https://github.com/thoughtbot/rails-consultant
