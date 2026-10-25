dev:
	uv run uvicorn endpoint_observatory.main:app --reload

test:
	uv run pytest

.PHONY: dev test
