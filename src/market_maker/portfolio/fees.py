def fee_bps_to_cost(price: float, qty: float, fee_bps: float) -> float:
    return abs(price * qty) * fee_bps * 1e-4
