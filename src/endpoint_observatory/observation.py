from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class Observation:
    endpoint_id: str
    duration_ms: float
    status_code: int | None
    error: str | None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
