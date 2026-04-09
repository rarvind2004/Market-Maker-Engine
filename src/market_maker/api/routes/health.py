from fastapi import APIRouter
from market_maker.monitoring.health import get_health_snapshot

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return get_health_snapshot()
