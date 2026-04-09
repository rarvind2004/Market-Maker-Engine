from pydantic import BaseModel


class StrategyState(BaseModel):
    last_alpha: float = 0.0
    last_fair_value: float = 0.0
