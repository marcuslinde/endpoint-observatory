import random
from collections import Counter

from fastapi.testclient import TestClient

from endpoint_observatory.main import app
from endpoint_observatory.simulator import pick_outcome

client = TestClient(app)

DRAWS = 100_000
TOLERANCE = 0.005  # 0.5 percentage points, about 5x the random noise


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_endpoint_distribution():
    rng = random.Random(33)
    counts = Counter(pick_outcome(rng) for _ in range(DRAWS))

    assert abs(counts["fast"] / DRAWS - 0.90) < TOLERANCE
    assert abs(counts["slow"] / DRAWS - 0.08) < TOLERANCE
    assert abs(counts["error"] / DRAWS - 0.02) < TOLERANCE
