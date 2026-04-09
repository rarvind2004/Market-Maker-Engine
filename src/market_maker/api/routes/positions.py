from fastapi import APIRouter

router = APIRouter()


@router.get("/positions")
def positions() -> dict:
    return {"positions": []}
