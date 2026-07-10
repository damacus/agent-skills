# Ruby and Rails Security

Security review is evidence-driven and version-aware. Load current Rails and
gem advisories for the versions locked by the project when vulnerability status
matters.

## Tooling

Use repository wrappers for configured tools such as Brakeman,
`bundler-audit`, dependency scanners, secret scanners, and custom checks. Do
not install scanners, update dependencies, or accept automated rewrites without
authorization. Confirm a finding against the actual dependency version and code
path before reporting it.

## Review Areas

Inspect relevant boundaries for:

- SQL, shell, template, and code injection;
- unsafe HTML, JavaScript contexts, and content sanitization;
- strong-parameter and mass-assignment mistakes;
- missing authentication, authorization, tenancy, or ownership checks;
- CSRF, CORS, session, cookie, redirect, and host validation;
- SSRF, unsafe URL fetching, and open redirects;
- path traversal, archive extraction, uploads, and content-type trust;
- unsafe deserialization, YAML loading, constantization, and dynamic dispatch;
- secrets in source, logs, errors, jobs, or serialized arguments;
- weak token generation, comparison, expiry, and replay handling; and
- background-job or webhook authenticity, idempotency, and retry behavior.

## Rails Context

Rails provides safe defaults in many paths, but helpers can be bypassed. Trace
data from input through normalization, authorization, persistence, rendering,
logging, and external effects. Check whether APIs, Action Cable, Active Storage,
GraphQL, engines, or admin surfaces use different controls.

## Reporting

For each issue, state the attacker-controlled input, required conditions,
impact, affected code path, and remediation. Distinguish a confirmed exploit
path from a defense-in-depth improvement or scanner hypothesis.
