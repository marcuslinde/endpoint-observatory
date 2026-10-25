"""Stand-in for the outside world.

The monitor is meant to watch somebody else's APIs. This module plays that part: one local
service that answers instead of the internet, so its behaviour can be chosen and repeated.
It is the thing being measured, never the thing doing the measuring.
"""

import asyncio
import random

from fastapi import APIRouter, HTTPException

# Fixed seed so the behaviour is reproducible across runs.
rng = random.Random(69)

# Relative weights. random.choices normalises them, so the total does not matter.
FAST = "fast"
SLOW = "slow"
ERROR = "error"
OUTCOMES = [FAST, SLOW, ERROR]
WEIGHTS = [90, 8, 2]

router = APIRouter()


def pick_outcome(rng: random.Random) -> str:
    return rng.choices(OUTCOMES, weights=WEIGHTS)[0]


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/endpoints/{endpoint_id}")
async def endpoint(endpoint_id: str):
    outcome = pick_outcome(rng)
    if outcome == FAST:
        await asyncio.sleep(rng.uniform(0.8, 1.2))
        return {"type": "SUCCESS", "output": endpoint_id}
    elif outcome == SLOW:
        await asyncio.sleep(rng.uniform(2, 4))
        return {"type": "SUCCESS", "output": endpoint_id}
    else:
        raise HTTPException(
            status_code=500, detail={"type": "ERROR", "reason": "Server-side error"}
        )
