# Market Maker Engine

A Python based event driven market making research and systems repo.

This repository includes:
- live and simulated market data adapters
- local order book reconstruction
- multi factor signal engine
- inventory aware quoting
- risk checks and kill switch
- simulated execution and backtesting
- Redis Streams integration hooks
- FastAPI control plane
- Prometheus metrics hooks
- Docker based local development

## Important note

This project is a strong research and systems foundation, but it is **not safe for live trading without additional exchange specific validation, extensive testing, and operational review**.

## Repo highlights

- `src/market_maker/order_book`: local L2 book and market microstructure utilities
- `src/market_maker/signals`: alpha factors and weighted signal aggregation
- `src/market_maker/strategy`: fair value, spread, skew, and quote policy
- `src/market_maker/risk`: position, loss, stale feed, and kill switch controls
- `src/market_maker/execution`: broker abstraction, simulated execution engine, cancel replace loop
- `src/market_maker/backtest`: event loop, replay engine, fill simulator, metrics and reports
- `src/market_maker/api`: FastAPI endpoints for health, positions, PnL, quotes, and controls
- `src/market_maker/storage`: Redis, Parquet, and session persistence helpers
- `src/market_maker/monitoring`: Prometheus metrics and health surfaces

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
python scripts/run_backtest.py
uvicorn market_maker.api.app:app --reload
```

## Tests

```bash
pytest
```

## Example architecture

```text
feed adapter -> normalizer -> event bus / redis -> order book -> signals -> strategy -> risk -> execution -> fills -> pnl / metrics
```

## Future work

- exchange specific websocket adapters with sequence reconciliation
- authenticated broker execution adapters
- persistent experiment tracking
- richer fill model calibrated to venue microstructure
- portfolio optimizer across symbols
