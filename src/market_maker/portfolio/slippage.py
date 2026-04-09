def slippage_cost(expected_px: float, actual_px: float, qty: float) -> float:
    return abs(actual_px - expected_px) * qty
