# endpoint-observatory

[![CI](https://github.com/marcuslinde/endpoint-observatory/actions/workflows/ci.yml/badge.svg)](https://github.com/marcuslinde/endpoint-observatory/actions/workflows/ci.yml)
[![last commit](https://img.shields.io/github/last-commit/marcuslinde/endpoint-observatory)](https://github.com/marcuslinde/endpoint-observatory/commits/master)
[![commit activity](https://img.shields.io/github/commit-activity/m/marcuslinde/endpoint-observatory)](https://github.com/marcuslinde/endpoint-observatory/graphs/commit-activity)
[![python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)

Monitor many logical API endpoints: record latency, status and failures, and report on how
they behaved over a time window.

Inspired by an interview case (1,000 endpoints at ~1 s, report over the last 10 hours) but not
a replica of it. The point is the learning: concurrency, measurement, workers and persistence,
one observed bottleneck at a time.

Raw measurement, aggregation, scoring and payout are kept separate, and missing observations
never count as healthy.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Commands

| Command | What it does |
| --- | --- |
| `uv run poe` | list available tasks |
| `uv run poe dev` | run the simulator with auto-reload |
| `uv run poe test` | run the test suite |
| `uv run poe check` | ruff + ty + pytest (the whole gate) |

## Phases

| # | Phase | Goal | Status |
| --- | --- | --- | --- |
| 1 | Simulator | A fake endpoint that answers fast, slow or fails, reproducibly | ✅ |
| 2 | One observation | Time a single call and store what happened | ⬜ |
| 3 | Sequential baseline | Monitor N endpoints one after another and measure it | ⬜ |
| 4 | Bounded concurrency | Same work, overlapping waits, with a cap and a timeout | ⬜ |
| 5 | Persistence and report | Store observations, aggregate per endpoint over a window | ⬜ |
| 6 | Windows and gaps | Reports over arbitrary windows where gaps are visible | ⬜ |
| 7 | Scheduling | Repeated runs, without overlapping when a run is slow | ⬜ |
| 8 | Scale | Push to 1,000 endpoints until something breaks, then fix that | ⬜ |

Lasting choices are recorded in [docs/decisions.md](docs/decisions.md).
