def should_alert(total_pnl: float, threshold: float = -250.0) -> bool:
    return total_pnl <= threshold
