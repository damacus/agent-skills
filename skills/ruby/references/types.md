# Ruby Type Tooling

Detect the repository's type system and ownership model before editing
signatures. RBS, Steep, Sorbet, TypeProf, generated RBI/RBS files, and framework
plugins have different workflows.

## Detection

Inspect:

- `sig/`, `rbs_collection.yaml`, and RBS tasks;
- `Steepfile` and Steep configuration;
- `sorbet/`, `sorbet/config`, RBI generators, and Tapioca or Parlour;
- inline `sig` blocks or RBS comments;
- TypeProf tasks and generated output; and
- CI checks and project wrappers.

## Working Rules

- Match the locked tool version and local strictness level.
- Update hand-written signatures with the implementation when the public
  contract changes.
- Regenerate generated signatures through the repository task; do not hand-edit
  generated output unless the project explicitly does so.
- Preserve runtime behavior. A type-driven refactor still needs tests.
- Treat dynamic Rails APIs according to the project's chosen plugin or shim
  strategy rather than inventing declarations.
- Avoid widening to untyped or suppressing errors without explaining the
  boundary that cannot be represented.

Run the narrowest supported type check, then the broader configured check when
the changed signature is shared widely.
