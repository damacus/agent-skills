---
name: go-optimizer
description: Optimize Go code for security, speed, memory use, and operational reliability. Use when working on Go performance tuning, benchmark-driven optimization, pprof analysis, allocation reduction, concurrency safety, request signing, crypto, input validation, dependency risk, or when the user asks to make Go code faster or safer.
license: MIT
allowed-tools: Read, Grep, Glob, Bash
metadata:
  author: damacus
  version: "1.0.0"
  domain: go
  triggers: go performance, golang optimization, pprof, benchmark, gosec, govulncheck, allocations, concurrency safety, crypto review, request signing, speed up go
  role: specialist
  scope: implementation
  output-format: evidence-first patch summary
---

# Go Optimizer

Use this skill for Go code where security and speed both matter. Treat performance work as a measurement problem and security work as a correctness boundary problem.

## Core Principles

- Measure before changing code. Keep baseline numbers and compare after each patch.
- Prefer small, local improvements with clear evidence over broad rewrites.
- Security constraints outrank speed. Never optimize by weakening validation, auth, crypto, permissions, or error handling.
- Keep Go idiomatic. Favor standard library primitives and simple data flow unless profiling proves otherwise.
- Stop when the next candidate has no defensible evidence or the risk outweighs the gain.

## Workflow

1. **Scope**
   - Identify the hot path, security boundary, and user-visible operation.
   - Check current git state and preserve unrelated user changes.
   - Find existing benchmarks, tests, and integration paths before adding new ones.

2. **Security Pass**
   - Review input parsing, path handling, auth, crypto, request signing, permissions, unsafe use, goroutine lifetimes, and resource limits.
   - Run focused tools when available:
     - `go test ./...`
     - `go vet ./...`
     - `govulncheck ./...`
     - `gosec ./...`
   - Treat tool output as a starting point. Manually inspect code that crosses trust boundaries.

3. **Performance Baseline**
   - Add or reuse a benchmark that represents the real workflow.
   - Run with repeat counts and allocation metrics:
     - `go test ./pkg -run=^$ -bench BenchmarkName -benchmem -count 10`
   - For unclear hotspots, capture profiles:
     - `go test ./pkg -run=^$ -bench BenchmarkName -benchmem -cpuprofile /tmp/name.cpu -memprofile /tmp/name.mem -count 1`
     - `go tool pprof -top /tmp/name.cpu`
     - `go tool pprof -top /tmp/name.mem`

4. **Optimize Loop**
   - Make one targeted change at a time.
   - Re-run the exact benchmark command.
   - Keep the change only if wall time, allocations, memory, syscalls, or tail latency improve by a meaningful amount.
   - Revert candidates that are noise-level, riskier, or slower.
   - Repeat up to the requested loop count, or stop early when no clear next target remains.

5. **Validation**
   - Run focused tests for touched packages.
   - Run `go test ./...` and `go vet ./...` before finalizing unless the user narrows scope.
   - Run security tools if the change touches trust boundaries, crypto, auth, file paths, network calls, or dependency handling.

## Go Security Checklist

- **Paths and archives:** prevent traversal, symlink surprises, hidden metadata leaks, and unintended recursive walks.
- **Crypto and signing:** match protocol semantics exactly; use constant-time comparisons for secrets; avoid inventing formats.
- **HTTP clients:** set timeouts, bound response bodies, check status codes, preserve context cancellation, and avoid leaking credentials in errors.
- **Parsing:** reject unsupported syntax clearly; bound input sizes where practical; prefer structured parsers over regex for complex formats.
- **Concurrency:** close channels, avoid goroutine leaks, use contexts, avoid shared mutable state without synchronization.
- **Dependencies:** prefer maintained modules; check known vulnerabilities; avoid unnecessary transitive dependencies.
- **Secrets:** never log private keys, tokens, request signatures, or credential file contents unless explicitly redacted.

## Go Performance Checklist

- Benchmark real workflows, not only micro-helpers.
- Use `pprof` to distinguish CPU, allocation, syscall, and IO costs.
- Avoid repeated filesystem traversal, repeated parsing, unnecessary `stat` calls, and avoid walking ignored directories such as `.git` when packaging.
- Preallocate slices and maps only when sizes are known and evidence shows benefit.
- Stream large payloads when memory use matters, but keep deterministic output where required.
- Reuse buffers only when it measurably reduces allocations and does not increase retained memory or complexity.
- Prefer algorithmic wins over allocation shaving.

## Evidence Format

When reporting results, include:

```text
Before: 12.306 ms/op, 4.24 MB/op, 14435 allocs/op
After:   1.794 ms/op, 2.56 MB/op,   931 allocs/op
Delta:   6.86x faster, 85.4% less time, 39.7% less memory, 93.6% fewer allocations
```

Also include the benchmark command, test commands, and any candidates rejected because they failed to improve results.

## Output Style

Lead with concrete findings and measured deltas. Keep summaries short. Include file paths and the exact validation commands. If no improvement is found, say so and leave the code unchanged.
