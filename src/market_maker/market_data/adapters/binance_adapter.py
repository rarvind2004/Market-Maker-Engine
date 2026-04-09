from market_maker.market_data.adapters.base import MarketDataAdapter

class BinanceAdapter(MarketDataAdapter):
    async def stream(self):
        raise NotImplementedError("Binance integration not implemented in scaffold")
