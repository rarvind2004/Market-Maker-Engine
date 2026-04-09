from market_maker.common.utils import now_ns


def get_health_snapshot() -> dict:
    return {"status": "ok", "ts_ns": now_ns()}
