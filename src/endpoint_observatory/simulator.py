from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/endpoints/{endpoint_id}")
async def endpoint(endpoint_id: str):
    return {"endpoint_id": endpoint_id}