---
name: fish-shell
description: >
  Fish shell scripting reference and enforcement. Activate whenever executing shell commands,
  writing shell scripts, using run_command, or any shell interaction in the user's environment.
  The user's shell is fish — never use bash/zsh/POSIX syntax in interactive commands.
  Trigger on: any shell command, heredoc, string manipulation, variable assignment, loop,
  conditional, arithmetic, pipe, or script writing.
---

# Fish Shell Reference

The user's shell is **fish** (<https://fishshell.com>). All interactive commands via `run_command`
and all shell scripts MUST use fish syntax unless the script has an explicit `#!/usr/bin/env bash`
shebang (standalone scripts only).

## Critical Rules

1. **No heredocs** — fish has no `<< EOF`. Use multiline quoted strings instead (quotes span newlines natively)
2. **No `$((…))`** — use `math` builtin: `math $i + 1`
3. **No `export`** — use `set -gx VAR value`
4. **No `VAR=value`** — use `set VAR value` (except single-command override: `VAR=value command`)
5. **No `[[ ]]`** — use `test` or `[ ]` (no `==`, use `=`)
6. **No `${var}`** — use `$var` or `{$var}` for concatenation
7. **No `${var%…}` `${var#…}` `${var/…/…}`** — use `string replace`, `string match`, `string trim`
8. **No `$#`** — use `count $argv`
9. **No `$?`** — use `$status`
10. **No `$$`** — use `$fish_pid`
11. **No `$0`** — use `status filename`
12. **No `$(( ))` or `(( ))`** — use `math`
13. **No `local`** — use `set -l`
14. **No `function name() {}`** — use `function name; ...; end`
15. **No `; do` / `; done` / `; then` / `; fi`** — use `; ...; end`
16. **No `source <(cmd)`** — use `cmd | source`
17. **No `<(cmd)`** — use `(cmd | psub)`
18. **No `set -e` / `set -euo pipefail`** — fish has no equivalent; check `$status` explicitly
19. **No multiline strings with `\` continuation** — fish quotes span newlines naturally

## Gotchas / Common Pitfalls

### Reserved / Read-Only Variable Names

Fish has built-in variables that **cannot be used as loop variables or overwritten with `set`**.
Using them in `for` loops causes: `for: <name>: cannot overwrite read-only variable`.

Known read-only names to avoid:

- `version` — use `ver` or `v` instead
- `status` — use `exit_code` or `rc` instead
- `hostname` — use `host` instead
- `fish_pid`, `fish_trace`, `pipestatus`
- `FISH_VERSION`, `SHLVL`

### `set -l` Scoping Across Blocks

`set -l` inside an `if` block is technically scoped to the enclosing function, but in practice
variables set inside one `if` block may not be reliably visible in a sibling `if` block.

**Fix**: Declare shared variables at the top of the function, then assign inside blocks:

```fish
function my_func
    # Declare at function top
    set -l list_a
    set -l list_b

    if test -f file_a
        set list_a (cat file_a)    # assign (no -l)
    end

    if test -f file_b
        set list_b (cat file_b)
        # list_a is reliably available here
        for item in $list_b
            contains -- $item $list_a
        end
    end
end
```

## Variables

```fish
# Set local variable
set -l name value

# Set global variable
set -g name value

# Set exported (environment) variable
set -gx NAME value

# Set list (array)
set -l mylist one two three

# Append to list
set -a mylist four

# Prepend to list
set -p mylist zero

# Erase variable
set -e name

# Check if variable exists
set -q name

# Check if variable has N+ elements
set -q name[2]
```

### Variable Expansion

```fish
echo $var           # expands to all elements (one arg each)
echo "$var"         # joins elements with space into one arg
echo {$var}suffix   # concatenation: {$var}suffix
echo $var[1]        # first element (1-indexed!)
echo $var[-1]       # last element
echo $var[2..4]     # slice
```

**No word splitting** — fish never splits variables on whitespace. A variable with spaces stays
as one element unless explicitly set as a list.

## String Manipulation

The `string` builtin replaces `sed`, `grep`, `awk`, `tr`, `cut`, `${var%…}`, etc.

```fish
# Replace (literal)
string replace old new $var
string replace -a old new $var          # all occurrences

# Replace (regex)
string replace -r 'pattern' 'replacement' $var
string replace -ra '^\s+' '' $var       # strip leading whitespace

# Match (returns matches, sets $status)
string match -q '*.txt' $filename       # glob match, quiet
string match -r '(\d+)\.(\d+)' $ver     # regex with capture groups
string match -rq 'pattern' $str        # quiet regex test

# Split
string split ',' 'a,b,c'               # → a b c (as list)
string split -m1 '/' $path             # split on first / only
string split0 (find . -print0)         # split on NUL

# Join
string join ', ' $mylist               # → "one, two, three"
string join \n $mylist                  # one per line
string join0 $mylist                   # NUL-separated

# Trim
string trim $var                        # trim whitespace both sides
string trim -l $var                     # left only
string trim -r $var                     # right only
string trim -c '/' $var                 # trim specific chars

# Length
string length $var                      # length of each element

# Substring
string sub -s 2 -l 3 $var              # from pos 2, length 3
string sub -s 2 $var                    # from pos 2 to end

# Case
string lower $var
string upper $var

# Pad
string pad -w 20 $var                   # left-pad to width 20
string pad -c 0 -w 5 $num              # zero-pad

# Collect (prevent splitting in command substitution)
set -l content (cat file | string collect)

# Filter with --filter
echo $lines | string match --filter '*.fish'
string replace --filter old new $lines  # only print lines where replacement happened

# Repeat
string repeat -n 3 'ab'                # → ababab

# Escape/unescape
string escape $var                      # shell-escape
string escape --style=url $var          # URL-encode
```

## Counting and Lists

```fish
# Count elements
count $mylist                           # prints count, exits 0 if >0

# Count lines from command
cmd | count

# Check membership
contains element $mylist                # exits 0 if found
contains -i element $mylist             # prints index if found
contains -- -q $argv                    # use -- before items starting with -

# Iterate
for item in $mylist
    echo $item
end

# Sequence
for i in (seq 1 10)
    echo $i
end
```

## Arithmetic

```fish
math 1 + 1                    # → 2
math $x + 1                   # variable in expression
math -s0 10 / 3               # integer division → 3
math -s2 10 / 3               # 2 decimal places → 3.33
math "floor($x / 10)"         # functions need quotes for parens
math "ceil(3.2)"              # → 4
math "max($a, $b)"            # max of two values
math "$x >= 10"               # comparison: returns 0 (true) or 1 (false) exit status
```

**Gotcha**: `*` must be quoted or escaped (`\*` or `"$x * 2"`) because it's a glob character.
Use `x` for multiplication when unquoted: `math 5 x 2`.

## Control Flow

```fish
# If/else
if test -f $file
    echo exists
else if test -d $file
    echo directory
else
    echo nope
end

# Negation
if not test -f $file
    echo missing
end

# Switch
switch $var
    case 'pattern1'
        echo matched
    case 'pattern2' 'pattern3'
        echo one of these
    case '*'
        echo default
end

# Combiners
cmd1; and cmd2              # cmd2 runs only if cmd1 succeeds
cmd1; or cmd2               # cmd2 runs only if cmd1 fails
cmd1 && cmd2                # same as and
cmd1 || cmd2                # same as or

# For loop
for file in *.txt
    echo $file
end

# While loop
while read -l line
    echo "line: $line"
end < $file

# Break / Continue
for i in (seq 100)
    test $i -gt 10; and break
end
```

## Functions

```fish
function greet -a name
    echo "Hello, $name"
end

function mycommand -d "Description for completions"
    # $argv contains all arguments
    # Use argparse for option parsing:
    argparse 'v/verbose' 'o/output=' -- $argv
    or return

    if set -q _flag_verbose
        echo "Verbose mode"
    end
    echo "Output: $_flag_output"
end
```

- **`$argv`** — all arguments (like bash `$@`)
- **`$argv[1]`** — first argument (1-indexed)
- **`-a name`** — named argument (syntactic sugar for `set -l name $argv[1]`)
- **`return N`** — return with exit status N

## Interactive Commands (run_command Best Practices)

When using `run_command` (which requires user approval), **avoid multiline file-creation commands**.
They are hard to review in the approval prompt.

- **Prefer IDE tools** (`write_to_file`, `edit`, `multi_edit`) to create/modify files — no approval needed
- **If shell is unavoidable**, use a single multiline quoted `echo` over `printf` with many args:

  ```fish
  # Readable in approval prompt
  echo 'line one
  line two
  line three' > outfile
  ```

- **Never** use `printf '%s\n' "arg1" "arg2" "arg3" ...` in interactive commands — it's unreadable

## Multiline Strings (Heredoc Alternative)

Fish has no `<< EOF` heredocs, but **quotes span newlines natively** — both `'single'` and
`"double"` quotes. This is the idiomatic way to handle multiline strings:

```fish
# Multiline string in a variable (single quotes — no interpolation)
set -l msg '---
hello world
goodbye world
---'
echo $msg

# Multiline string with variable interpolation (double quotes)
set -l name "fish"
set -l greeting "Hello from $name
This is line two
And line three"

# Multiline string piped to a command (replaces heredoc)
echo 'first line
second line
third line' | mycommand

# Write multiline to file
echo 'line one
line two
line three' > outfile

# Alternative: printf for explicit per-line control
printf '%s\n' "line one" "line two" "line three" > outfile

# Read multiline into variable from command
set -l content (cat file | string collect)
```

## Redirections and Pipes

```fish
cmd > file              # stdout to file
cmd 2> file             # stderr to file
cmd &> file             # both stdout+stderr to file
cmd >> file             # append stdout
cmd 2>&1                # stderr to stdout
cmd > /dev/null 2>&1    # silence everything
```

## Status and Error Handling

```fish
# Fish has no set -e. Check status explicitly:
command arg
if test $status -ne 0
    echo "command failed" >&2
    return 1
end

# Or use and/or:
command arg; or begin; echo "failed" >&2; return 1; end

# Or simply:
command arg
or return $status
```

## Process Substitution

```fish
# Bash: diff <(cmd1) <(cmd2)
diff (cmd1 | psub) (cmd2 | psub)

# Bash: source <(cmd)
cmd | source
```

## Common Patterns

```fish
# Bash: local var=$(cmd)
set -l var (cmd)

# Bash: var=${var:-default}
set -q var; or set -l var default

# Bash: [[ -z "$var" ]]
test -z "$var"

# Bash: [[ -n "$var" ]]
test -n "$var"

# Bash: for f in $(cmd); do ...; done
for f in (cmd)
    ...
end

# Bash: while IFS= read -r line; do ...; done < file
while read -l line
    ...
end < file

# Bash: arr+=("element")
set -a arr element

# Bash: ${#arr[@]}
count $arr

# Bash: echo "${arr[@]}" | tr '\n' ','
string join ',' $arr

# Bash: if echo "$var" | grep -q pattern
if string match -q 'pattern' $var

# Bash: var=$(echo "$var" | sed 's/old/new/g')
set var (string replace -a old new $var)

# Bash: tmpdir=$(mktemp -d); trap 'rm -rf $tmpdir' EXIT
set -l tmpdir (mktemp -d)
# No trap in fish — clean up manually or use a function with --on-process-exit
```

## Writing Fish Scripts

```fish
#!/usr/bin/env fish

# Scripts use the same syntax as interactive commands.
# No need for set -euo pipefail — check $status where needed.
# Functions defined in a script are available throughout that script.

function main
    # your code
end

main $argv
```

## Debugging

```fish
# Trace execution (like bash set -x)
set fish_trace 1

# Profile a script
fish --profile /tmp/profile.log myscript.fish
```
