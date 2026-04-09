from fastapi import APIRouter

router = APIRouter()


@router.get("/pnl")
def pnl() -> dict:
    return {"realized_pnl": 0.0, "unrealized_pnl": 0.0, "total_pnl": 0.0}
