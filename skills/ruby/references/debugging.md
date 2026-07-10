# Debugging Ruby

Start from a reproducible symptom in the repository's normal environment. Keep
the same Mise, Task, Rake, or container boundary used by the failing command.

## Narrow the Failure

1. Capture the exact command, exception class, message, backtrace, exit status,
   and relevant logs.
2. Re-run the smallest failing test, scenario, request, job, or script.
3. Identify the first application frame and trace inputs across the failing
   boundary.
4. Compare with nearby working behavior and recent changes.
5. Add or preserve a focused regression test before fixing the cause when
   practical.

Do not suppress the exception, broaden a rescue, or add retries until the
failure mode and ownership boundary are understood.

## Tools

Use syntax checks, focused tests, logs, and the configured debugger. Ruby's
`debug` gem, Byebug, Pry, Rails console, tracing, and profilers are optional
project tools; do not install or require one merely because it is familiar.

A Rails console can mutate real data or enqueue work. Confirm the environment
and prefer read-only inspection or an isolated sandbox where supported.
Avoid leaving breakpoints, temporary output, disabled callbacks, or debug-only
configuration in the final change.

## Intermittent Failures

For order-dependent or flaky behavior, capture seeds, time zones, process and
thread boundaries, job timing, database cleanup, shared files/ports, network
stubs, and global state. Reproduce under the same parallelization and container
settings before changing synchronization or retry behavior.

State what was reproduced and what remains inferred.
