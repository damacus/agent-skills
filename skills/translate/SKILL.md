---
name: translate
description: Update, add, or delete i18n translation nodes while keeping every accompanying language file structurally in sync. Use /translate for translation files of any format, locale drift, missing keys, or user-facing copy changes.
license: MIT
metadata:
  author: damacus
---

# Translate

Use `/translate` whenever a task updates, adds, renames, or deletes a node in a
translation file. This applies to translation files of any format, including
YAML, JSON, TOML, properties, gettext, and framework-specific locale formats.

## Non-Negotiable Rule

A translation-tree change is incomplete until the equivalent node change has
been made in every accompanying language.

This remains true when the request names only one locale file: treat that file
as the starting point, then inspect and update the repository's other locales.

For example, if `en.yml` changes and the repository also contains Spanish,
Polish, and Welsh locale files, update all four files in the same change. Do not
update only the source or default locale.

## Workflow

1. Read repository instructions and determine the locale layout and default or
   source language.
2. Find every accompanying language file. Check sibling locale files, split
   locale directories, and framework configuration; do not assume the languages
   from the files already changed.
3. Identify each node being added, updated, renamed, moved, or deleted.
4. Apply the same structural operation to every language:
   - add the same node path and translate its value;
   - update the corresponding meaning in each language;
   - rename or move the same node path everywhere;
   - delete the obsolete node everywhere.
5. Preserve interpolation variables exactly, including `%{name}`, `{{name}}`,
   printf-style placeholders, and format-specific escaping.
6. Preserve plural, gender, select, and HTML-safe branches. Do not collapse
   branches such as `zero`, `one`, `few`, `many`, and `other`.
7. Preserve each file's ordering, comments, quoting, encoding, and established
   formatting where its format permits this.
8. Run the repository's format-native parser or tests, then run the bundled
   locale-tree checker when the files use a format supported by `yq`.

Do not silently copy source-language text into other locales unless the project
explicitly uses source text as its fallback policy. If a translation is
ambiguous or domain-specific, call that out rather than inventing terminology.

## Locale Tree Checker

The bundled checker compares node paths and node kinds. It ignores translated
values and normalizes a single top-level locale key, so `en.greeting` and
`es.greeting` are treated as the same logical path.

From the directory containing this `SKILL.md`, run the checker with only a
reference file to discover locale-named sibling files having the same extension:

```bash
./scripts/check_locale_sync.sh /path/to/project/config/locales/en.yml
```

Pass files explicitly for split directories, mixed extensions, or locale
layouts the discovery rule cannot infer safely:

```bash
./scripts/check_locale_sync.sh \
  /path/to/project/locales/en/messages.yml \
  /path/to/project/locales/es/messages.yml \
  /path/to/project/locales/pl/messages.yml \
  /path/to/project/locales/cy/messages.yml
```

The checker requires mikefarah `yq` v4 and accepts formats it can parse, such as
YAML, JSON, TOML, XML, properties, and INI. For formats `yq` cannot parse, such
as gettext PO, use the format's native validation tooling and manually verify
the same node set across all languages.

## Completion Checks

- Every supported language was identified and updated.
- Added, renamed, moved, and deleted paths are structurally identical across
  locale files.
- Interpolation variables and plural/select branches match across languages.
- Every translation file parses successfully.
- The bundled sync checker passes where applicable.
- The patch contains no unrelated translation churn.
