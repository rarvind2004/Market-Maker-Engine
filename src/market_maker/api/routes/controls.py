from fastapi import APIRouter
from market_maker.api.schemas import ControlResponse

router = APIRouter()


@router.post("/controls/start", response_model=ControlResponse)
def start() -> ControlResponse:
    return ControlResponse(status="ok", detail="engine start requested")


@router.post("/controls/stop", response_model=ControlResponse)
def stop() -> ControlResponse:
    return ControlResponse(status="ok", detail="engine stop requested")
