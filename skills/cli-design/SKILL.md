---
name: cli-design
description: >-
  Design, build, review, or test command-line interfaces that work well for humans, scripts,
  agents, pipes, and CI. Use when defining command trees, arguments and flags, stdout/stderr
  contracts, human and structured output, exit codes, prompts, configuration precedence,
  destructive-action safeguards, TTY behavior, completion, or CLI compatibility. Also use when a
  TUI needs a stable non-interactive command surface. Language-agnostic core with optional
  TypeScript implementation references.
---

# CLI Design: Unix-Composable Command-Line Interfaces

This skill covers **language-agnostic** CLI design principles. Apply them proportionately to the tool's users, compatibility promises, platforms, and existing conventions.

Read repository instructions and inspect the existing command surface before changing it. Existing flags, output schemas, exit codes, shell completions, and automation consumers are public contracts even when they were not designed deliberately.

**TypeScript implementation patterns** are in the `resources/` directory. Load them on demand when building a CLI in TypeScript:

| Resource | Load when... |
| ---------- | ------------- |
| `output-architecture.md` | Implementing Result types, entry point wiring, formatters, logger, JSON envelope schemas |
| `testing-cli.md` | Writing Vitest tests for CLI behavior (streams, exit codes, pipes, contract tests) |
| `stream-contracts.md` | Understanding Node.js buffering, NDJSON, signal handling, crash-only design |
| `composability.md` | Designing or testing pipe behavior — worked shell examples (jq filtering, NDJSON streaming, stdin, chaining, `--fields`, parallel `xargs`) |

The TypeScript resources are implementation examples, not requirements. Preserve the project's language, framework, and test conventions.

---

## When to Use

- Building any command-line tool (any language)
- Designing command tree, flags, and I/O contracts
- Implementing the output layer (format detection, stream routing)
- Testing CLI behavior (stdout/stderr separation, exit codes)
- Reviewing a CLI for Unix composability
- Adding a scriptable CLI beside a TUI or other interactive interface

---

## Core Principle

**stdout is for DATA only — the product the user asked for.**
**stderr is for EVERYTHING ELSE — diagnostics, progress, spinners, warnings, errors.**

This separation is what makes `mycli --json | jq ...` work. One spinner character on stdout breaks every downstream pipe.

> "Whatever software you're building, you can be absolutely certain that people will use it in ways you didn't anticipate. Your software will become a part in a larger system — your only choice is over whether it will be a well-behaved part." — clig.dev

---

## The Unix Stream Contract

| Content | Stream | Why |
| --------- | -------- | ----- |
| Primary output (data, results, JSON) | stdout | Pipeable, buffered for throughput |
| Progress bars, spinners, status | stderr | Not data — must not corrupt pipes |
| Warnings, errors, diagnostics | stderr | Visible to user even when stdout is piped |
| Debug/verbose output | stderr | Diagnostic, never data |

**Buffering behavior:**

- **stdout**: line-buffered when connected to a TTY, block-buffered when piped (~2x faster than stderr)
- **stderr**: unbuffered — every write is a syscall (immediate but expensive)
- **Check each stream independently** — stdout being piped does not mean stderr is piped

When stdout is piped, the user doesn't want your status messages in their data. All non-data output must go to stderr.

For a deep dive on buffering behavior and performance implications, see `resources/stream-contracts.md`.

---

## Keep Handlers Pure

The practical rule: **functions that do the work should return data, not write to stdout.** The CLI entry point handles all I/O.

```text
Entry point (CLI main)              Your logic (handlers)
─────────────────────               ─────────────────────
parse args                          (input) → structured result
detect format (json/plain/human)    no printing to stdout
call handler                        no writing to stderr
format the result                   no calling exit
write to correct stream             just returns data
set exit code
```

This isn't an architecture mandate — it's just clean function design. The benefits are concrete:

- **Testable without subprocess spawning** — call the handler, assert on the returned value
- **Format flexibility for free** — same data renders as JSON, plain text, or coloured tables by swapping one function
- **Reusable** — the same handler works from a CLI, MCP server, HTTP API, or programmatic import

For simple CLIs where the "handler" is just calling a library, this separation already exists naturally — your library returns data, your CLI formats it. No extra layers needed.

If a project already uses hexagonal architecture, the CLI entry point commonly acts as a driving adapter and delegates to application behavior. Do not introduce that architecture merely to obtain testable handlers.

For TypeScript implementation patterns (Result types, entry point wiring, formatters, logger interfaces), see `resources/output-architecture.md`.

---

## Format Flag Contract

Choose the smallest output contract the CLI needs. A common hierarchy is:

### Default: Human-Readable

- Colors, tables, formatted text
- Progress bars and spinners on **stderr**
- Output tailored for terminal width
- May change between versions — this is **not** a contract

#### Literal Terminal Output Is Not Markdown

Before choosing formatting syntax, verify what actually renders the output.
Most CLIs print literal terminal text: Markdown markers such as `#`, `**`,
backticks, and pipe-table separators will be shown verbatim unless the output
is deliberately passed through a Markdown renderer.

For literal terminal output:

- use plain labels, spacing, ASCII rules, and explicitly padded columns
- use ASCII art sparingly when it provides useful identity or hierarchy
- calculate column widths from both headers and values; do not rely on Markdown
  table syntax to align columns
- replace embedded newlines, tabs, and delimiter characters before rendering a
  row so one value cannot break the table
- test table alignment structurally by asserting that every row's column
  boundaries occur at the same character positions
- render representative long errors in tests and inspect the actual terminal
  output, not only string fragments

Do not assume an output mode named `markdown` proves that users see rendered
Markdown. Check the final presentation path. If the CLI writes directly to a
terminal, design and test it as literal terminal text.

#### Status Output Should Summarize, Not Dump

A human-facing status command should present the smallest useful operational
summary:

- identity and version
- component status
- concise, actionable details for unhealthy components
- humanized capacity and timestamps where relevant

Avoid raw nested payloads, null error fields, internal service addresses, raw
byte counts, and implementation-only URLs in the default view. Keep the full
response available through structured output such as `--json`.

Keep aggregate language evidence-based. A component error does not
automatically mean the whole installation, authentication check, or command
failed. Prefer showing the failure on the affected component row over a broad
banner such as `Needs attention` unless the product has a documented rule for
that aggregate state.

### `--plain`: Grep/Awk-Friendly

- One record per line, no formatting, no colors
- Stable when documented for scripts; otherwise direct automation to structured output
- Flat table rows, no borders, no grouped sections
- Enables: `mycli list --plain | grep error | wc -l`

> "Encourage your users to use `--plain` or `--json` in scripts to keep output stable." — clig.dev

### `--json`: Structured Data

- stdout contains **ONLY** valid JSON — no spinners, no color, no progress
- stderr continues normally — human diagnostics still visible
- Define and test a machine-readable error contract as well as success output
- Treat documented fields and shapes as versioned public API
- `--json` implies non-interactive regardless of TTY

Choose one canonical flag, such as `--format json`; keep `--json` only as a documented alias when useful. A consistent envelope is one valid design:

```json
{ "ok": true, "data": { ... } }
{ "ok": false, "error": { "code": "CONFIG_MISSING", "message": "...", "fix": "..." } }
```

A direct resource or array can be a better JSON success shape when it composes more naturally. Whichever shape is chosen, specify where machine-readable failures are written. A practical default is one structured error object on stderr with a non-zero exit code; an established envelope-on-stdout contract is also valid if diagnostics remain separate.

### NDJSON for Streaming

For large datasets, use NDJSON (one JSON object per `\n`):

- Each line is independently parseable
- Include a `type` field per record for multiplexing events
- Final line can be a summary record
- Enables: `mycli run --format ndjson | while read -r line; do ...; done`

For NDJSON specification details, see `resources/stream-contracts.md`.

---

## Exit Codes

| Code | Meaning | When |
| ------ | --------- | ------ |
| 0 | Success | Operation completed as expected |
| 1 | Domain failure | Tool-specific failure (e.g. quality threshold not met) |
| 2 | Invalid usage | Bad flags, missing required args, validation error |
| 75 | Temporary failure (optional) | Network timeout, service unavailable — retry may help |
| 78 | Configuration error (optional) | Invalid config file, missing required config |
| 130 | SIGINT | User pressed Ctrl-C (128 + 2) |
| 143 | SIGTERM | Process terminated (128 + 15) |

**Rules:**

- Non-zero exit code **MUST** have a stderr explanation
- Document exit codes in `--help`
- Never use codes above 125 for application errors (reserved for signals: 128 + signal number)
- Start with portable `0`, `1`, and `2`; add codes such as `75` and `78` only when consumers benefit and the supported platforms interpret them consistently
- Map non-zero codes to the most important failure modes for your tool

---

## TTY Detection

Check priority order (first match wins):

| Priority | Condition | Effect |
| ---------- | ----------- | -------- |
| 1 | `--format json` or `--json` flag | Non-interactive, no color, no animation |
| 2 | `--no-color` flag | Disable color (output may still be interactive) |
| 3 | `NO_COLOR` env (non-empty) | Disable color |
| 4 | Project-supported force-color setting | Enable color even when not a TTY, without overriding an explicit no-color choice |
| 5 | `TERM=dumb` | Disable color and animations |
| 6 | `CI=true` | No interactive prompts |
| 7 | stdout is not a TTY (`!isatty(stdout)`) | Plain output, no animations on stdout |
| 8 | Default | Full interactive with colors |

**Check stdout and stderr independently.** When stdout is piped but stderr is a TTY, you can still show spinners on stderr while keeping stdout clean for the pipe consumer.

Optionally support `MYCLI_NO_COLOR` for app-specific color override.

---

## Input Design

### Flags Over Arguments

- **1 positional arg**: acceptable (the "main thing")
- **2 positional args**: reasonable when their order is conventional and memorable; otherwise consider flags
- **3+ positional args**: usually hard to discover unless they are a same-type variadic list
- Familiar idioms such as `cp source dest` and project-established command grammar are stronger evidence than a numeric rule

Flags are self-documenting, order-independent, and future-proof.

```bash
# Bad — which is source, which is destination?
mycli copy myapp backup

# Good — explicit
mycli copy --from myapp --to backup
```

### Standard Flags

Always provide long forms. Short flags only for the most common operations.

| Flag | Meaning |
| ------ | --------- |
| `-h`, `--help` | Show help (this should only mean help) |
| `--version` | Print version to stdout |
| `-q`, `--quiet` | Suppress non-essential output |
| `-v`, `--verbose` | More detail in human output |
| `-d`, `--debug` | Diagnostic output to stderr |
| `-f`, `--force` | Skip confirmation prompts |
| `-n`, `--dry-run` | Show what would happen without doing it |
| `--json` | Structured JSON output |
| `--plain` | Stable, grep-friendly plain text |
| `--no-color` | Disable color output |
| `--no-input` | Disable all prompts/interactivity |
| `-o`, `--output` | Output file |
| `--fields` | Select output columns |

### Prompts and Interactivity

- **All prompts MUST be bypassable** via flags for scriptability
- Confirmation → `--yes` or `--force`
- Selection → `--type=value`
- Text input → `--name=value`
- Passwords → `--password-file=path` or stdin pipe
- If stdin is not a TTY, never prompt — fail with a clear error or use defaults
- **Secrets: never via flag values** (leak to `ps` output and shell history). Prefer, in order: OS keychain or a `0600` credential file (`~/.config/mycli/credentials`), then stdin (`mycli login --with-token < token.txt`), then env vars **only where the platform injects them** (CI secret stores) — env leaks to child processes and crash reports, so never make it the primary documented path
- **Scale confirmation to severity**: mild → `y/N` prompt with `--yes` bypass; moderate → prompt plus suggest `--dry-run` first; severe/irreversible (delete a database, overwrite production) → require typing the resource name to confirm

### Conventions

- Support `--` to stop flag parsing: `mycli run -- --flag-for-child-process`
- Support `-` for stdin/stdout file arguments: `curl ... | mycli process -`
- Accept both `--flag=value` and `--flag value`
- If stdin is expected but is an interactive terminal, display help immediately (don't hang like `cat`)

---

## Config Precedence

Highest to lowest priority:

1. **Flags** — per-invocation overrides
2. **Environment variables** — `MYCLI_*` prefix, per-session
3. **Project config** — `.myclirc`, `mycli.config.ts`, or in `package.json`
4. **User config** — `~/.config/mycli/` (follow XDG spec)
5. **Defaults** — sensible built-in values

**Rules:**

- Follow the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) for config file locations
- Env var naming: `MYCLI_*` prefix, uppercase letters + digits + underscores; keep values single-line; don't commandeer POSIX names
- Respect the general-purpose env vars where relevant: `NO_COLOR`, `FORCE_COLOR`, `DEBUG`, `EDITOR`, `PAGER`, `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY`, `TMPDIR`, `TERM`, `LINES`/`COLUMNS`
- Never accept secrets via flags; prefer keychain/credential files or stdin, env vars only when platform-injected (CI) — see "Prompts and Interactivity"
- Read `.env` where appropriate, but don't use it as a substitute for proper config
- If you modify configuration that belongs to another program, ask consent first

---

## Error Design

Every error needs:

1. **Machine-readable code** — `UPPER_SNAKE_CASE` (e.g. `CONFIG_MISSING`, `AUTH_EXPIRED`)
2. **What went wrong** — context: which resource, operation, input
3. **How to fix it** — exact command or action the user should take
4. **Reference** — docs URL or `mycli help <topic>` (optional)

### Human Mode

```text
Error: CONFIG_MISSING — Configuration file not found
No configuration file found at ./mycli.config.ts or ~/.config/mycli/config.ts

Fix: Run `mycli init` to create a default configuration file
Docs: https://mycli.dev/docs/configuration
```

- Put the most important information **last** (the eye is drawn to the end)
- Use red sparingly and intentionally
- Suggest corrections for typos ("Did you mean 'deploy'?")
- Group similar errors under one header — don't repeat 50 similar-looking lines
- Write debug logs to a file, not the terminal (unless `--debug`)

### Structured Mode

Errors are structured too — not just success responses:

```json
{
  "ok": false,
  "error": {
    "code": "CONFIG_MISSING",
    "message": "No configuration file found at ./mycli.config.ts",
    "fix": "Run `mycli init` to create a default configuration file",
    "transient": false
  }
}
```

The `transient` boolean tells retry logic whether the failure may be temporary. Emit the object on the documented machine-error stream; do not print a human error and JSON error into the same stream.

---

## State Changes and Transparency

- **Confirm state changes** — say what changed and show (or point to) the resulting state; traditionally-silent commands look broken to humans
- **Make current state easy to see** — a `status`-style command for anything with complex state (the `git status` pattern)
- **Make hidden actions explicit** — if you read/write files not passed as arguments or talk to remote servers, say so (stderr in human mode)
- **Page long output** through `$PAGER` (e.g. `less -FIRX`) — only when stdout is a TTY, never when piped

---

## Robustness

- **Validate input early** — fail before any side effects, with a clear message
- **Responsiveness beats silence** — benchmark startup and show progress on stderr for perceptibly long interactive work; do not emit progress for fast or piped operations
- **Timeouts on all network operations** — configurable, with a documented transient-failure signal when retrying is safe
- **Recoverable by re-run** — after a transient failure, re-running the command should resume or be safely idempotent
- **Crash-only design** — exit fast on failure, defer cleanup to the next run; add timeouts to cleanup so Ctrl-C never hangs (second Ctrl-C skips cleanup) — see `resources/stream-contracts.md`
- **Expect misuse** — script wrapping, bad connections, concurrent instances, environments you never tested

---

## Composability Patterns

Design for real-world pipes: filtering with `jq`, streaming NDJSON line-by-line, feeding stdin, chaining commands through emitted identifiers, selecting columns with `--fields`, and fanning out with `xargs -P`.

See `resources/composability.md` for the worked shell examples covering each of these patterns.

**Key patterns:**

- Create commands output identifiers so subsequent commands can chain
- List commands support `--fields` for column selection (reduces output size, critical for agent efficiency)
- `--quiet` for CI scripts that only care about the exit code
- NDJSON for streaming large datasets without buffering everything in memory
- `--dry-run` with `--json` outputs planned changes as structured data

---

## CLI and TUI Composition

When a product has both a CLI and a TUI:

- Keep domain operations behind one application layer; the CLI and TUI are separate presentation adapters.
- Make every important TUI mutation available through a documented non-interactive command unless the action is inherently visual or continuous.
- Do not make hidden `--json` behavior the only automation path. Expose stable commands and structured output directly.
- Let the TUI launch explicitly through a command such as `<tool> tui` when the default invocation must remain safe for scripts. Preserve an established bare-command TUI when compatibility requires it.
- Share authentication, configuration, validation, and error codes without sharing terminal rendering code.
- Verify parity for permissions, validation, dry runs, destructive confirmations, and result semantics across both interfaces.

Use the `tui-expert` skill alongside this one for state, layout, keyboard, rendering, resizing, and terminal accessibility concerns.

---

## Subcommand Design

- Choose a grammar that matches user intent. Resource-oriented CLIs often use `noun verb` (`mycli config set`); action-oriented tools often use `verb noun` (`git clone repo`). Do not mix grammars arbitrarily.
- Be consistent across all subcommands — same flag names for same things
- No ambiguous pairs (`update` vs `upgrade` is confusing)
- No catch-all subcommands (you can never add subcommands with conflicting names)
- No arbitrary abbreviations — aliases must be explicit and stable
- With no args: show help, status, a safe default, or an established TUI. Never block on a surprise prompt when stdin is not interactive.

### Help

- `mycli --help` — top-level help
- `mycli help <subcommand>` — subcommand help
- `mycli <subcommand> --help` — same as above
- If run with missing required args, show concise help + 1-2 examples + "use --help for more"
- **Examples are the most-read section** — lead with them
- Include flag types, defaults, and allowed values for finite sets
- Include a support/bug-report link in top-level help; pre-populate issue URLs with diagnostics where possible
- Suggest the likely command on obvious typos ("Did you mean 'deploy'?") — ask, never auto-execute

---

## Output Stability Contract

**Stdout is a public API.** Breaking changes to stdout format are breaking changes to the CLI.

| Change | Impact |
| -------- | -------- |
| Adding new optional JSON fields | Safe (additive) |
| Adding new subcommands | Safe |
| Adding new flags with preserving defaults | Safe |
| Removing or renaming flags | **Breaking** |
| Removing or renaming JSON fields | **Breaking** |
| Changing exit codes | **Breaking** |
| Changing default behavior | **Breaking** |
| Changing human-readable output | Usually OK (not a contract) |

When in doubt, add alongside — don't modify. Deprecate with stderr warnings before removing — and once you can detect that users have migrated, stop warning.

---

## Naming, Distribution, Telemetry

- **Name**: short, memorable, lowercase, easy to type; not so generic it collides with existing commands
- **Distribution**: prefer a single binary; language-ecosystem tools (npm, pip) may reasonably assume their interpreter. Make uninstalling easy and documented
- **Telemetry**: never collect usage/crash data without explicit consent — opt-in, stating what, why, and retention. Instrumented web docs or download counts are usually enough

---

## Anti-Patterns

| # | Anti-Pattern | Why It's Wrong |
| --- | ------------- | ---------------- |
| 1 | Mixing data and diagnostics on stdout | Breaks every pipe: `mycli list \| jq .` fails if warnings are on stdout |
| 2 | Colors/ANSI in piped output | ANSI sequences corrupt downstream parsing. Check `isatty(stdout)` + `NO_COLOR` |
| 3 | Interactive prompts with no flag bypass | Agents can't type 'y'. Every prompt needs `--yes`/`--force`. Non-TTY without bypass = hang |
| 4 | Ambiguous success behavior | Mutating human workflows often need confirmation; Unix-style checks and filters may intentionally succeed silently. Document the rule and offer quiet output where useful |
| 5 | Designing for humans OR machines, not both | Detect context (TTY vs pipe), adapt automatically |
| 6 | Output that doesn't guide the next action | Every output is a signpost: success = next command, failure = fix command |
| 7 | Breaking existing CLI contracts | Flag names, exit codes, output shape are contracts. Add alongside, never modify |
| 8 | `console.log` anywhere except the CLI adapter | Handlers must return data; only the presentation layer writes to streams |
| 9 | Handlers that exit the process directly | Let the entry point decide. Handlers return errors as data |
| 10 | Non-zero exit without stderr explanation | Scripts need both the code and the reason |
| 11 | Verbose default output | A single test run can generate 419KB. Support `--fields`, `--quiet`, `--json` |
| 12 | Printing Markdown syntax to a literal terminal | Users see raw `**`, backticks, and broken pipe tables. Use terminal-native formatting unless a renderer is confirmed |
| 13 | Inferring global failure from one component | Overstates the result and confuses users. Keep failures scoped unless aggregate semantics are explicitly defined |

---

## Verification Checklist

After designing or reviewing a CLI:

- [ ] stdout has ONLY data; stderr has everything else
- [ ] Commands that return data or plans expose an appropriate stable machine-readable format
- [ ] Exit codes are semantic and documented in `--help`
- [ ] Every prompt has a `--yes`/`--force`/`--flag` bypass
- [ ] Errors include: code, message, fix suggestion
- [ ] `--dry-run` available for mutating commands
- [ ] Progress/spinners go to stderr, never stdout
- [ ] `NO_COLOR`, `TERM=dumb`, and `--no-color` respected
- [ ] Piped output contains zero ANSI escape codes
- [ ] Literal terminal output contains no accidental Markdown syntax
- [ ] Text-table rows have identical tested column-boundary positions
- [ ] Status summaries keep component failures scoped and evidence-based
- [ ] Default status output omits internal addresses, null errors, and raw capacity values
- [ ] Success output includes next-action guidance
- [ ] Existing flags, exit codes, output fields never removed or renamed
- [ ] JSON schema is versioned (additions safe, removals breaking)
- [ ] Config follows flags > env > project > user > defaults
- [ ] Secrets never via flags; keychain/credential-file/stdin preferred, env only when platform-injected (CI)
- [ ] Severe destructive actions require typed confirmation (resource name), not just y/N
- [ ] Network operations have configurable timeouts and a documented transient-failure signal
- [ ] Startup and time-to-feedback have been measured against an explicit project budget
- [ ] Ctrl-C exits fast with bounded cleanup
- [ ] `--help` includes 2-3 realistic examples
- [ ] Documented plain output is grep-parseable when the CLI promises a plain-text automation contract
- [ ] CLI and TUI operations share semantics without coupling their rendering layers

---

## Quick Reference

Stream routing, exit codes, and standard flags are tabled in the body — see "The Unix Stream Contract", "Exit Codes", and "Standard Flags" above.

### Format Hierarchy

```text
Default (TTY)     → colors, tables, formatted text
--plain           → one record per line, stable, grep-friendly
--json            → structured JSON, versioned schema
--format ndjson   → streaming, one JSON object per line
```

### Configuration Order

```text
flags > env vars > project config > user config > defaults
```
