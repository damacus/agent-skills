# Coverage and SimpleCov

Use coverage to identify unexercised behavior and regression risk. Do not treat
a percentage as a substitute for meaningful tests.

## Detect Existing Configuration

Inspect the locked SimpleCov version, `.simplecov`, test helpers, formatter
gems, CI configuration, parallel-test setup, and existing coverage tasks.
SimpleCov must start before application code is loaded, but the correct require
location and profile depend on the suite.

Do not install SimpleCov, add formatters, change filters, or impose thresholds
unless the user requests setup or the task explicitly includes configuration.

## Run Coverage Through the Project

Prefer the established Mise, Task, Rake, or CI-equivalent command. Projects
often gate coverage behind an environment variable or separate task; inspect
the implementation instead of guessing.

For fast feedback:

1. reproduce the relevant test without coverage when appropriate;
2. run the smallest coverage-enabled scope that produces valid results;
3. inspect uncovered lines and branches in the changed behavior; and
4. widen to the complete suite only when merged results or project thresholds
   require it.

A single-file coverage run can under-report application coverage or overwrite
merged results. Keep separate command names, merge timeouts, parallel worker
contracts, and subprocess handling intact.

## Interpret Results

Prioritize:

- changed branches with no behavioral test;
- error, retry, authorization, and boundary paths;
- complex or frequently changed code with weak protection; and
- files unexpectedly absent because SimpleCov started too late.

Do not add tests solely to execute harmless lines, test private methods
directly, or exclude inconvenient production code without explaining why.
Avoid opening the HTML report automatically; use existing terminal summaries
or inspect generated artifacts only when needed.

If parsing `.resultset.json`, first inspect the installed SimpleCov format. Do
not assume an old schema or hand-maintained percentage calculation is current.
