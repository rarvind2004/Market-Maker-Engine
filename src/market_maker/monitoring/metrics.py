from prometheus_client import Counter, Gauge


class MetricsRegistry:
    def __init__(self) -> None:
        self.market_events = Counter("mm_market_events_total", "Market events processed")
        self.quotes = Counter("mm_quotes_total", "Quotes generated")
        self.fills = Counter("mm_fills_total", "Fills observed")
        self.risk_rejects = Counter("mm_risk_rejects_total", "Risk rejects")
        self.position = Gauge("mm_position", "Current position")
        self.total_pnl = Gauge("mm_total_pnl", "Current total pnl")


metrics_registry = MetricsRegistry()
