from pydantic import BaseModel


class RiskLimits(BaseModel):
    max_position_abs: float = 1.0
    max_daily_loss: float = 500.0
    max_order_size: float = 0.1
    stale_after_ms: int = 1500
    reject_limit: int = 20
