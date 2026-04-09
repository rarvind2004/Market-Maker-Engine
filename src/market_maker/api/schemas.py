from pydantic import BaseModel


class ControlResponse(BaseModel):
    status: str
    detail: str
