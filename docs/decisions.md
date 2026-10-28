# Decisions

Lasting choices, recorded so they stop being discussed. Two people in this
file: the agent proposes, the project owner approves. An entry stays
`Proposed` until the owner accepts it.

Every entry answers three questions: what we chose, why, and **what measurement
would make us change our mind**. That last one is the point of the project —
the record should show which bottleneck drove which decision.

If a real alternative was genuinely weighed, name it in **Reason**. There is no
separate field for it: writing one for choices that never had a serious
contender invites invented alternatives.

---

## One record per monitoring attempt

**Decision:** Each attempt produces exactly one observation: endpoint ID, UTC timestamp, elapsed duration, HTTP status if any, error details if any.
**Status:** Proposed
**Reason:** Failed attempts must be recorded rather than dropped — history cannot be reconstructed later. An HTTP error response and a timeout or connection failure are different events and stay distinguishable.
**Revisit when:** per-attempt volume makes retention or report queries slow, or when a run needs to be described by something other than its individual attempts.

## Timing

**Decision:** `time.perf_counter()` for elapsed duration.
**Status:** Proposed
**Reason:** Monotonic, so it is unaffected by wall-clock adjustments. The wall-clock UTC timestamp of the attempt is stored alongside it.
**Revisit when:** durations have to be compared across process restarts or machines, where monotonic clocks are not comparable.

## One simulator, many endpoints

**Decision:** One simulator service simulates many endpoints, selected by ID or configuration.
**Status:** Proposed
**Reason:** Keeps the topology single-process while still giving 1,000 distinct targets to monitor.
**Revisit when:** the simulator stops behaving like a real fleet — for example if it becomes CPU-bound and stops being a stand-in for I/O-bound endpoints.

## Simulator behaviour: per-call draws, seeded

**Decision:** The simulator picks each call's behaviour (ok / slow / fail) at random from fixed weights, using a seeded random generator. Endpoints have no persistent bad state yet.
**Status:** Proposed
**Reason:** Small enough to build now, varied enough to produce something worth measuring. The seed makes two runs face the same endpoints, so a later before/after comparison measures my code rather than my luck. Persistent outages are deferred until there is persistence to record gaps in.
**Revisit when:** the report must represent a multi-day outage, or an endpoint needs to stay broken across many calls.

## Stack

**Decision:** Python on the existing `uv` setup, FastAPI for HTTP, HTTPX2 for the monitor client, pytest for tests, SQLite once persistence is needed.
**Status:** Proposed
**Reason:** Already scaffolded, and each is the smallest thing that does the job. Nothing here is permanent. HTTPX2 replaced HTTPX because starlette deprecated `httpx` in its test client; the swap was a rename, not a redesign, and it removed the deprecation warning from the test suite.
**Revisit when:** monitoring shows a component is the bottleneck — SQLite write contention or slow report queries, HTTPX2 client behaviour, FastAPI throughput. Replacing a component because measurement implicated it is a success, not a rewrite.

## Manual runs before scheduling

**Decision:** Run monitoring by hand first. Measure a sequential baseline, then introduce bounded async concurrency.
**Status:** Proposed
**Reason:** A baseline is what makes the effect of concurrency visible; without it there is no way to tell improvement from noise.
**Revisit when:** the sequential baseline is measured and the next comparison is available.

## Explicit timeouts, no retries yet

**Decision:** Every request has an explicit timeout and failures are recorded. Retries are added only when their behaviour is understood.
**Status:** Proposed
**Reason:** Silent retries hide the failure rate and distort latency.
**Revisit when:** retry limits, retryable failures and duplicate records have been reasoned through and a measured failure rate justifies retrying.
