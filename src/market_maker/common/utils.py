from __future__ import annotations
import time
import uuid


def now_ns() -> int:
    return time.time_ns()


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def order_id(prefix: str = "ord") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"
