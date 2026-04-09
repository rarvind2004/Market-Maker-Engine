def inventory_ratio(qty: float, limit: float) -> float:
    return 0.0 if limit == 0 else qty / limit
