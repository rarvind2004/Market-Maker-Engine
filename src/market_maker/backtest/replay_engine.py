from __future__ import annotations
from pathlib import Path
import pandas as pd
from market_maker.common.types import MarketEvent


def generate_synthetic_events(symbol: str, steps: int) -> list[MarketEvent]:
    from market_maker.market_data.adapters.simulated_adapter import SimulatedAdapter
    import asyncio

    async def collect() -> list[MarketEvent]:
        adapter = SimulatedAdapter(symbol)
        result: list[MarketEvent] = []
        async for event in adapter.stream():
            result.append(event)
            if len(result) >= steps:
                break
        return result

    return asyncio.run(collect())


def load_events_from_parquet(path: Path) -> list[MarketEvent]:
    df = pd.read_parquet(path)
    return [MarketEvent(**row) for row in df.to_dict(orient="records")]
