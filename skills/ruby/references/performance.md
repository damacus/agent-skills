# Ruby Performance

Measure the reported workload before optimizing. Generic advice about symbols,
memoization, Enumerable chains, freezing, or object allocation is not evidence
that a particular change is faster or safer.

## Establish the Bottleneck

Classify the dominant cost using representative inputs:

- CPU time and method hot spots;
- allocations, retained memory, and garbage collection;
- database query count and duration;
- network, filesystem, subprocess, or lock waits;
- boot, autoload, serialization, or template cost; and
- thread, fiber, process, Ractor, or queue contention.

Use existing benchmark or profiling tasks first. Detect configured tools such
as `Benchmark`, benchmark-ips, StackProf, ruby-prof, memory_profiler, rbspy,
rack-mini-profiler, Vernier, or application telemetry. Do not install a
profiler or enable invasive production tracing without authorization.

## Compare Changes Fairly

Keep Ruby version, runtime flags, YJIT configuration, data size, warmup,
environment, and external services consistent. Run enough iterations to
separate signal from noise and report both latency and allocation or throughput
changes relevant to the task.

Optimize the measured path, then re-run correctness tests and the same
measurement. Consider readability, memory, startup, cache invalidation, and
concurrency trade-offs rather than reporting one number in isolation.

Runtime, JIT, GC, fiber, and Ractor behavior is version-sensitive. Consult
current primary documentation for the locked Ruby version before changing
runtime flags or concurrency architecture.

Load [database.md](database.md) when SQL or Active Record dominates the result.
