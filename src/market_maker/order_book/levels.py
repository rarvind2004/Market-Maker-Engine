from market_maker.common.types import BookLevel


def best_level(side_levels: list[BookLevel]) -> BookLevel | None:
    return side_levels[0] if side_levels else None
