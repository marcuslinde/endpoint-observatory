import asyncio
import time

import httpx2

from endpoint_observatory.observation import Observation


async def one_call(url: str, endpoint_id: str) -> Observation:
    async with httpx2.AsyncClient(timeout=5.0) as client:
        #we start counter after opening a client
        start = time.perf_counter()

        try:
            res = await client.get(url)
            status = res.status_code
            error = None
        except httpx2.HTTPError as exc:
            status = None
            error = str(exc)
        finally:
            elapsed_ms = 1000 * (time.perf_counter() - start)

        return Observation(
            endpoint_id=endpoint_id,
            duration_ms=elapsed_ms,
            status_code=status,
            error=error,
        )

if __name__ == "__main__":
    result = asyncio.run(one_call("http://127.0.0.1:8000/endpoints/1", "1"))

    print(
        f"endpoint  {result.endpoint_id}",
        f"duration  {(result.duration_ms / 1000):.3f} s",
        f"status    {result.status_code}",
        f"error     {result.error}",
        sep="\n",
    )