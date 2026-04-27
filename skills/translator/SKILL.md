---
name: translator
description: Maintain translation files and keep locale trees in sync when UI copy changes, locale YAML files change, or new typography or design-system components introduce user-facing text. Use this skill for Rails i18n work, locale drift fixes, missing translation keys, and translation updates across config/locales.
license: Complete terms in LICENSE.txt
---

Use this skill when a repository needs translation maintenance rather than general copywriting.

The usual inputs are changed locale files, changed UI components, or new typography/design-system primitives that introduce user-facing strings.

## Goal

Keep locale files complete, structurally aligned, and safe to use in production.

## Workflow

1. Inspect the changed files and identify any new, renamed, or removed user-facing strings.
2. Find the canonical locale file, which is usually the default language file such as `config/locales/en.yml`.
3. Add or update keys in the canonical locale first, then propagate the same key structure to every supported locale file.
4. Preserve interpolation placeholders exactly, including `%{name}` style variables.
5. Preserve pluralization branches and do not collapse keys such as `zero`, `one`, `other`.
6. Preserve HTML-safe conventions and any existing YAML structure unless a change is required for correctness.
7. If a translation is missing and the task expects completion, provide a direct translation instead of leaving the English text duplicated, unless repository instructions say otherwise.
8. Avoid unrelated edits. Translation maintenance should usually touch locale files and only the minimum supporting code.

## Checks

- Every locale file should contain the same key path for newly added strings.
- Interpolation variables must match across locales.
- YAML should remain valid.
- Existing translations should not be replaced casually if the source text did not meaningfully change.

## Typography And Design System Changes

When typography or design-system components add visible copy:

- Treat those strings as product copy that should move behind i18n keys.
- Add the new keys to the canonical locale file.
- Add corresponding translations to the remaining locale files.
- If the component already uses i18n and only the copy changed, update all locale files to match the new source meaning.

## Output Discipline

- Prefer editing existing locale files over creating new translation infrastructure.
- Keep the patch narrow and reviewable.
- Call out uncertainty if a phrase is ambiguous or domain-specific.
