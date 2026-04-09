from market_maker.common.utils import now_ns


def age_ms(ts_ns: int) -> float:
    return (now_ns() - ts_ns) / 1_000_000
