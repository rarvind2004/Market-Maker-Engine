from market_maker.market_data.adapters.base import MarketDataAdapter

class PolygonAdapter(MarketDataAdapter):
    async def stream(self):
        raise NotImplementedError("Polygon integration not implemented in scaffold")
