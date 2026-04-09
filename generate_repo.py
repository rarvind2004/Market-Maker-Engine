from pathlib import Path
import textwrap, os, json

root = Path('/mnt/data/market-maker-py')
files = {}

def add(path, content):
    files[path] = textwrap.dedent(content).lstrip('\n')

add('README.md', '''
# Market Maker Py

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
''')

add('pyproject.toml', '''
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "market-maker-py"
version = "0.1.0"
description = "Event driven market making engine in Python"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "pydantic>=2.8.0",
    "pydantic-settings>=2.4.0",
    "numpy>=2.0.0",
    "pandas>=2.2.0",
    "pyarrow>=17.0.0",
    "pyyaml>=6.0.2",
    "prometheus-client>=0.20.0",
    "redis>=5.0.8",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.6.0",
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
''')

add('.env.example', '''
APP_ENV=dev
REDIS_URL=redis://localhost:6379/0
SYMBOLS=BTCUSD,ETHUSD
LOG_LEVEL=INFO
''')

add('.gitignore', '''
__pycache__/
.pytest_cache/
.ruff_cache/
.venv/
.env
*.pyc
*.pyo
*.parquet
*.db
*.sqlite
coverage.xml
htmlcov/
''')

add('docker-compose.yml', '''
version: "3.9"
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    volumes:
      - ./infra/redis/redis.conf:/usr/local/etc/redis/redis.conf

  api:
    build:
      context: .
      dockerfile: infra/docker/app.Dockerfile
    ports:
      - "8000:8000"
    environment:
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - redis

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
''')

add('Makefile', '''
install:
	pip install -e .[dev]

backtest:
	python scripts/run_backtest.py

api:
	uvicorn market_maker.api.app:app --reload

test:
	pytest
''')

add('configs/app.yaml', '''
app_name: market-maker-py
symbols:
  - BTCUSD
  - ETHUSD
loop_sleep_ms: 25
metrics_port: 9100
''')
add('configs/strategy.yaml', '''
weights:
  imbalance: 0.45
  momentum: 0.25
  mean_reversion: 0.15
  volatility: -0.15
base_spread_bps: 4.0
inventory_skew_bps: 7.0
max_quote_size: 0.02
''')
add('configs/risk.yaml', '''
max_position_abs: 1.0
max_daily_loss: 500.0
max_order_size: 0.10
stale_after_ms: 1500
reject_limit: 20
''')
add('configs/execution.yaml', '''
latency_ms: 20
maker_fee_bps: 1.0
taker_fee_bps: 3.0
partial_fill_probability: 0.35
''')
add('configs/feeds.yaml', '''
feed: simulated
symbols:
  BTCUSD:
    mid: 65000.0
    spread: 2.5
  ETHUSD:
    mid: 3200.0
    spread: 0.5
''')
add('configs/logging.yaml', '''
version: 1
formatters:
  simple:
    format: '%(asctime)s %(levelname)s %(name)s %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
root:
  handlers: [console]
  level: INFO
''')

add('scripts/run_backtest.py', '''
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest
from market_maker.backtest.reports import build_summary


def main() -> None:
    events = generate_synthetic_events(symbol="BTCUSD", steps=1000)
    result = run_backtest(events)
    print(build_summary(result))


if __name__ == "__main__":
    main()
''')

add('scripts/run_live.py', '''
import asyncio
from market_maker.main import run_live_stack


if __name__ == "__main__":
    asyncio.run(run_live_stack())
''')

add('scripts/replay_session.py', '''
from pathlib import Path
from market_maker.backtest.replay_engine import load_events_from_parquet
from market_maker.backtest.simulator import run_backtest


if __name__ == "__main__":
    path = Path("data/replays/session.parquet")
    events = load_events_from_parquet(path)
    result = run_backtest(events)
    print(result.metrics)
''')

add('scripts/seed_redis_streams.py', '''
from market_maker.storage.redis_streams import RedisStreamStore
from market_maker.backtest.replay_engine import generate_synthetic_events


if __name__ == "__main__":
    store = RedisStreamStore()
    for event in generate_synthetic_events("BTCUSD", 100):
        store.publish_event("market:events", event.model_dump())
    print("seeded")
''')

add('scripts/profile_latency.py', '''
import cProfile
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_backtest(generate_synthetic_events("BTCUSD", 5000))
    profiler.disable()
    profiler.print_stats(sort="cumtime")
''')

add('scripts/healthcheck.py', '''
from market_maker.monitoring.health import get_health_snapshot


if __name__ == "__main__":
    print(get_health_snapshot())
''')

# package files
base_init = '''
__all__ = []
'''
add('src/market_maker/__init__.py', '__version__ = "0.1.0"\n')
add('src/market_maker/constants.py', '''
DEFAULT_SYMBOLS = ["BTCUSD", "ETHUSD"]
BPS = 1e-4
''')
add('src/market_maker/settings.py', '''
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    redis_url: str = "redis://localhost:6379/0"
    symbols: str = Field(default="BTCUSD,ETHUSD")
    log_level: str = "INFO"

    @property
    def symbol_list(self) -> list[str]:
        return [s.strip() for s in self.symbols.split(",") if s.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
''')
add('src/market_maker/logger.py', '''
import logging


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    return logging.getLogger(name)
''')
add('src/market_maker/main.py', '''
import asyncio
from market_maker.logger import get_logger
from market_maker.market_data.feed_manager import SimulatedFeedManager
from market_maker.execution.execution_engine import LiveCoordinator
from market_maker.monitoring.metrics import metrics_registry

logger = get_logger(__name__)


async def run_live_stack() -> None:
    manager = SimulatedFeedManager(["BTCUSD"])
    coordinator = LiveCoordinator()
    async for event in manager.stream_events():
        await coordinator.on_market_event(event)
        metrics_registry.market_events.inc()


if __name__ == "__main__":
    asyncio.run(run_live_stack())
''')

# common
for path, content in {
'src/market_maker/common/__init__.py': base_init,
'src/market_maker/common/enums.py': '''
from enum import Enum


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    OPEN = "open"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    PARTIAL = "partial"
''',
'src/market_maker/common/types.py': '''
from __future__ import annotations
from pydantic import BaseModel, Field
from market_maker.common.enums import Side, OrderStatus


class BookLevel(BaseModel):
    price: float
    size: float


class MarketEvent(BaseModel):
    ts_ns: int
    symbol: str
    bid: float
    ask: float
    bid_size: float
    ask_size: float
    trade_price: float | None = None
    trade_size: float | None = None


class SignalVector(BaseModel):
    imbalance: float = 0.0
    momentum: float = 0.0
    mean_reversion: float = 0.0
    volatility: float = 0.0
    alpha: float = 0.0


class Quote(BaseModel):
    symbol: str
    bid_px: float
    ask_px: float
    bid_sz: float
    ask_sz: float
    fair_value: float
    alpha: float


class Order(BaseModel):
    order_id: str
    symbol: str
    side: Side
    price: float
    size: float
    ts_ns: int
    status: OrderStatus = OrderStatus.OPEN
    filled_size: float = 0.0


class Fill(BaseModel):
    order_id: str
    symbol: str
    side: Side
    fill_px: float
    fill_size: float
    ts_ns: int
    fee: float = 0.0


class PositionSnapshot(BaseModel):
    symbol: str
    quantity: float = 0.0
    avg_price: float = 0.0
    realized_pnl: float = 0.0
    mark_price: float = 0.0

    @property
    def unrealized_pnl(self) -> float:
        if self.quantity == 0:
            return 0.0
        sign = 1 if self.quantity > 0 else -1
        return sign * abs(self.quantity) * (self.mark_price - self.avg_price)


class RiskDecision(BaseModel):
    allowed: bool
    reason: str = "ok"
''',
'src/market_maker/common/utils.py': '''
from __future__ import annotations
import time
import uuid


def now_ns() -> int:
    return time.time_ns()


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def order_id(prefix: str = "ord") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"
''',
'src/market_maker/common/time.py': '''
from market_maker.common.utils import now_ns


def age_ms(ts_ns: int) -> float:
    return (now_ns() - ts_ns) / 1_000_000
''',
'src/market_maker/common/ids.py': '''
from market_maker.common.utils import order_id

__all__ = ["order_id"]
'''} .items(): add(path, content)

# market data
for path, content in {
'src/market_maker/market_data/__init__.py': base_init,
'src/market_maker/market_data/adapters/__init__.py': base_init,
'src/market_maker/market_data/adapters/base.py': '''
from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent


class MarketDataAdapter(ABC):
    @abstractmethod
    async def stream(self) -> AsyncIterator[MarketEvent]:
        raise NotImplementedError
''',
'src/market_maker/market_data/adapters/simulated_adapter.py': '''
from __future__ import annotations
import asyncio
import random
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent
from market_maker.common.utils import now_ns
from market_maker.market_data.adapters.base import MarketDataAdapter


class SimulatedAdapter(MarketDataAdapter):
    def __init__(self, symbol: str, mid: float = 65000.0, spread: float = 2.5) -> None:
        self.symbol = symbol
        self.mid = mid
        self.spread = spread

    async def stream(self) -> AsyncIterator[MarketEvent]:
        while True:
            drift = random.uniform(-3.0, 3.0)
            self.mid += drift
            bid = self.mid - self.spread / 2
            ask = self.mid + self.spread / 2
            yield MarketEvent(
                ts_ns=now_ns(),
                symbol=self.symbol,
                bid=round(bid, 2),
                ask=round(ask, 2),
                bid_size=round(random.uniform(0.1, 3.0), 4),
                ask_size=round(random.uniform(0.1, 3.0), 4),
                trade_price=round(random.choice([bid, ask, self.mid]), 2),
                trade_size=round(random.uniform(0.01, 0.5), 4),
            )
            await asyncio.sleep(0.025)
''',
'src/market_maker/market_data/adapters/polygon_adapter.py': 'from market_maker.market_data.adapters.base import MarketDataAdapter\n\nclass PolygonAdapter(MarketDataAdapter):\n    async def stream(self):\n        raise NotImplementedError("Polygon integration not implemented in scaffold")\n',
'src/market_maker/market_data/adapters/binance_adapter.py': 'from market_maker.market_data.adapters.base import MarketDataAdapter\n\nclass BinanceAdapter(MarketDataAdapter):\n    async def stream(self):\n        raise NotImplementedError("Binance integration not implemented in scaffold")\n',
'src/market_maker/market_data/parsers/l2_parser.py': 'def parse_l2(payload: dict) -> dict:\n    return payload\n',
'src/market_maker/market_data/parsers/trade_parser.py': 'def parse_trade(payload: dict) -> dict:\n    return payload\n',
'src/market_maker/market_data/parsers/snapshot_parser.py': 'def parse_snapshot(payload: dict) -> dict:\n    return payload\n',
'src/market_maker/market_data/normalizer.py': '''
from market_maker.common.types import MarketEvent


def normalize_event(payload: dict) -> MarketEvent:
    return MarketEvent(**payload)
''',
'src/market_maker/market_data/publisher.py': '''
from market_maker.storage.redis_streams import RedisStreamStore


class EventPublisher:
    def __init__(self) -> None:
        self.store = RedisStreamStore()

    def publish(self, stream: str, payload: dict) -> None:
        self.store.publish_event(stream, payload)
''',
'src/market_maker/market_data/feed_manager.py': '''
from __future__ import annotations
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent
from market_maker.market_data.adapters.simulated_adapter import SimulatedAdapter


class SimulatedFeedManager:
    def __init__(self, symbols: list[str]) -> None:
        self.adapters = [SimulatedAdapter(symbol=s) for s in symbols]

    async def stream_events(self) -> AsyncIterator[MarketEvent]:
        # simple single symbol streaming for scaffold
        async for event in self.adapters[0].stream():
            yield event
'''} .items(): add(path, content)

# order book
for path, content in {
'src/market_maker/order_book/__init__.py': base_init,
'src/market_maker/order_book/levels.py': '''
from market_maker.common.types import BookLevel


def best_level(side_levels: list[BookLevel]) -> BookLevel | None:
    return side_levels[0] if side_levels else None
''',
'src/market_maker/order_book/book.py': '''
from __future__ import annotations
from collections import deque
from market_maker.common.types import BookLevel, MarketEvent


class OrderBook:
    def __init__(self, symbol: str, max_history: int = 128) -> None:
        self.symbol = symbol
        self.bids: list[BookLevel] = []
        self.asks: list[BookLevel] = []
        self.last_event: MarketEvent | None = None
        self.mid_history: deque[float] = deque(maxlen=max_history)

    def apply_event(self, event: MarketEvent) -> None:
        self.last_event = event
        self.bids = [BookLevel(price=event.bid, size=event.bid_size)]
        self.asks = [BookLevel(price=event.ask, size=event.ask_size)]
        self.mid_history.append(self.mid_price())

    def best_bid(self) -> float:
        return self.bids[0].price if self.bids else 0.0

    def best_ask(self) -> float:
        return self.asks[0].price if self.asks else 0.0

    def spread(self) -> float:
        return max(0.0, self.best_ask() - self.best_bid())

    def mid_price(self) -> float:
        if not self.bids or not self.asks:
            return 0.0
        return (self.best_bid() + self.best_ask()) / 2.0
''',
'src/market_maker/order_book/imbalance.py': '''
from market_maker.order_book.book import OrderBook


def imbalance(book: OrderBook) -> float:
    if not book.bids or not book.asks:
        return 0.0
    bid_size = book.bids[0].size
    ask_size = book.asks[0].size
    total = bid_size + ask_size
    if total == 0:
        return 0.0
    return (bid_size - ask_size) / total
''',
'src/market_maker/order_book/microprice.py': '''
from market_maker.order_book.book import OrderBook


def microprice(book: OrderBook) -> float:
    if not book.bids or not book.asks:
        return 0.0
    bid = book.bids[0]
    ask = book.asks[0]
    total = bid.size + ask.size
    if total == 0:
        return book.mid_price()
    return (ask.price * bid.size + bid.price * ask.size) / total
''',
'src/market_maker/order_book/book_builder.py': '''
from market_maker.order_book.book import OrderBook
from market_maker.common.types import MarketEvent


class BookBuilder:
    def __init__(self, symbol: str) -> None:
        self.book = OrderBook(symbol)

    def on_event(self, event: MarketEvent) -> OrderBook:
        self.book.apply_event(event)
        return self.book
'''} .items(): add(path, content)

# signals
for path, content in {
'src/market_maker/signals/__init__.py': base_init,
'src/market_maker/signals/base.py': '''
from abc import ABC, abstractmethod
from market_maker.common.types import SignalVector
from market_maker.order_book.book import OrderBook


class Signal(ABC):
    @abstractmethod
    def compute(self, book: OrderBook) -> float:
        raise NotImplementedError
''',
'src/market_maker/signals/order_flow.py': '''
from market_maker.order_book.book import OrderBook
from market_maker.order_book.imbalance import imbalance


class OrderFlowSignal:
    def compute(self, book: OrderBook) -> float:
        return imbalance(book)
''',
'src/market_maker/signals/momentum.py': '''
from market_maker.order_book.book import OrderBook


class MomentumSignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 5:
            return 0.0
        return (hist[-1] - hist[-5]) / max(hist[-5], 1e-9)
''',
'src/market_maker/signals/mean_reversion.py': '''
from market_maker.order_book.book import OrderBook


class MeanReversionSignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 10:
            return 0.0
        mean = sum(hist) / len(hist)
        return (mean - hist[-1]) / max(mean, 1e-9)
''',
'src/market_maker/signals/volatility.py': '''
from market_maker.order_book.book import OrderBook


class VolatilitySignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 10:
            return 0.0
        mean = sum(hist) / len(hist)
        variance = sum((x - mean) ** 2 for x in hist) / len(hist)
        return variance ** 0.5 / max(mean, 1e-9)
''',
'src/market_maker/signals/alpha_model.py': '''
from market_maker.common.types import SignalVector


class WeightedAlphaModel:
    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self.weights = weights or {
            "imbalance": 0.45,
            "momentum": 0.25,
            "mean_reversion": 0.15,
            "volatility": -0.15,
        }

    def score(self, vector: SignalVector) -> SignalVector:
        alpha = (
            vector.imbalance * self.weights["imbalance"]
            + vector.momentum * self.weights["momentum"]
            + vector.mean_reversion * self.weights["mean_reversion"]
            + vector.volatility * self.weights["volatility"]
        )
        vector.alpha = alpha
        return vector
''',
'src/market_maker/signals/signal_engine.py': '''
from market_maker.common.types import SignalVector
from market_maker.order_book.book import OrderBook
from market_maker.signals.alpha_model import WeightedAlphaModel
from market_maker.signals.order_flow import OrderFlowSignal
from market_maker.signals.momentum import MomentumSignal
from market_maker.signals.mean_reversion import MeanReversionSignal
from market_maker.signals.volatility import VolatilitySignal


class SignalEngine:
    def __init__(self) -> None:
        self.order_flow = OrderFlowSignal()
        self.momentum = MomentumSignal()
        self.mean_reversion = MeanReversionSignal()
        self.volatility = VolatilitySignal()
        self.alpha_model = WeightedAlphaModel()

    def compute(self, book: OrderBook) -> SignalVector:
        vector = SignalVector(
            imbalance=self.order_flow.compute(book),
            momentum=self.momentum.compute(book),
            mean_reversion=self.mean_reversion.compute(book),
            volatility=self.volatility.compute(book),
        )
        return self.alpha_model.score(vector)
'''} .items(): add(path, content)

# strategy
for path, content in {
'src/market_maker/strategy/__init__.py': base_init,
'src/market_maker/strategy/state.py': '''
from pydantic import BaseModel


class StrategyState(BaseModel):
    last_alpha: float = 0.0
    last_fair_value: float = 0.0
''',
'src/market_maker/strategy/fair_value.py': '''
from market_maker.order_book.book import OrderBook
from market_maker.order_book.microprice import microprice
from market_maker.common.types import SignalVector


def fair_value(book: OrderBook, signals: SignalVector) -> float:
    base = microprice(book) or book.mid_price()
    return base * (1 + 0.001 * signals.alpha)
''',
'src/market_maker/strategy/skew.py': '''
from market_maker.constants import BPS


def inventory_skew(position_qty: float, max_position_abs: float, inventory_skew_bps: float = 7.0) -> float:
    if max_position_abs <= 0:
        return 0.0
    ratio = max(-1.0, min(1.0, position_qty / max_position_abs))
    return ratio * inventory_skew_bps * BPS
''',
'src/market_maker/strategy/spread_model.py': '''
from market_maker.constants import BPS
from market_maker.common.types import SignalVector


def spread_fraction(base_spread_bps: float, signals: SignalVector) -> float:
    widen = max(0.0, signals.volatility) * 3
    tighten = min(0.0, signals.alpha) * -1
    return (base_spread_bps + widen - tighten) * BPS
''',
'src/market_maker/strategy/inventory_model.py': '''
from market_maker.common.types import PositionSnapshot


def target_size(position: PositionSnapshot, max_quote_size: float = 0.02) -> tuple[float, float]:
    penalty = min(0.8, abs(position.quantity) * 0.2)
    size = max_quote_size * (1 - penalty)
    return size, size
''',
'src/market_maker/strategy/quote_policy.py': '''
from market_maker.common.types import PositionSnapshot, Quote, SignalVector
from market_maker.order_book.book import OrderBook
from market_maker.strategy.fair_value import fair_value
from market_maker.strategy.inventory_model import target_size
from market_maker.strategy.skew import inventory_skew
from market_maker.strategy.spread_model import spread_fraction


class QuotePolicy:
    def __init__(self, base_spread_bps: float = 4.0, inventory_skew_bps: float = 7.0, max_position_abs: float = 1.0) -> None:
        self.base_spread_bps = base_spread_bps
        self.inventory_skew_bps = inventory_skew_bps
        self.max_position_abs = max_position_abs

    def make_quote(self, book: OrderBook, signals: SignalVector, position: PositionSnapshot) -> Quote:
        fv = fair_value(book, signals)
        spread = spread_fraction(self.base_spread_bps, signals)
        skew = inventory_skew(position.quantity, self.max_position_abs, self.inventory_skew_bps)
        bid_sz, ask_sz = target_size(position)
        bid_px = fv * (1 - spread / 2 - skew)
        ask_px = fv * (1 + spread / 2 - skew)
        return Quote(
            symbol=book.symbol,
            bid_px=round(bid_px, 2),
            ask_px=round(ask_px, 2),
            bid_sz=round(bid_sz, 4),
            ask_sz=round(ask_sz, 4),
            fair_value=round(fv, 4),
            alpha=round(signals.alpha, 6),
        )
''',
'src/market_maker/strategy/strategy_engine.py': '''
from market_maker.common.types import PositionSnapshot, Quote
from market_maker.order_book.book import OrderBook
from market_maker.signals.signal_engine import SignalEngine
from market_maker.strategy.quote_policy import QuotePolicy


class StrategyEngine:
    def __init__(self) -> None:
        self.signals = SignalEngine()
        self.quote_policy = QuotePolicy()

    def on_book(self, book: OrderBook, position: PositionSnapshot) -> Quote:
        vector = self.signals.compute(book)
        return self.quote_policy.make_quote(book, vector, position)
'''} .items(): add(path, content)

# risk
for path, content in {
'src/market_maker/risk/__init__.py': base_init,
'src/market_maker/risk/limits.py': '''
from pydantic import BaseModel


class RiskLimits(BaseModel):
    max_position_abs: float = 1.0
    max_daily_loss: float = 500.0
    max_order_size: float = 0.1
    stale_after_ms: int = 1500
    reject_limit: int = 20
''',
'src/market_maker/risk/checks.py': '''
from market_maker.common.time import age_ms
from market_maker.common.types import PositionSnapshot, Quote, RiskDecision
from market_maker.order_book.book import OrderBook
from market_maker.risk.limits import RiskLimits


def check_quote(book: OrderBook, quote: Quote, position: PositionSnapshot, limits: RiskLimits) -> RiskDecision:
    if book.last_event and age_ms(book.last_event.ts_ns) > limits.stale_after_ms:
        return RiskDecision(allowed=False, reason="stale_market_data")
    if max(quote.bid_sz, quote.ask_sz) > limits.max_order_size:
        return RiskDecision(allowed=False, reason="order_size_limit")
    if abs(position.quantity) > limits.max_position_abs:
        return RiskDecision(allowed=False, reason="position_limit")
    if position.realized_pnl + position.unrealized_pnl < -limits.max_daily_loss:
        return RiskDecision(allowed=False, reason="daily_loss_limit")
    return RiskDecision(allowed=True)
''',
'src/market_maker/risk/position_manager.py': '''
from market_maker.common.enums import Side
from market_maker.common.types import Fill, PositionSnapshot


class PositionManager:
    def __init__(self, symbol: str) -> None:
        self.snapshot = PositionSnapshot(symbol=symbol)

    def apply_fill(self, fill: Fill) -> PositionSnapshot:
        qty_change = fill.fill_size if fill.side == Side.BUY else -fill.fill_size
        old_qty = self.snapshot.quantity
        new_qty = old_qty + qty_change

        if old_qty == 0 or (old_qty > 0 and qty_change > 0) or (old_qty < 0 and qty_change < 0):
            total_notional = self.snapshot.avg_price * abs(old_qty) + fill.fill_px * abs(qty_change)
            self.snapshot.quantity = new_qty
            self.snapshot.avg_price = total_notional / max(abs(new_qty), 1e-9)
        else:
            closing = min(abs(old_qty), abs(qty_change))
            if old_qty > 0:
                pnl = (fill.fill_px - self.snapshot.avg_price) * closing
            else:
                pnl = (self.snapshot.avg_price - fill.fill_px) * closing
            self.snapshot.realized_pnl += pnl - fill.fee
            self.snapshot.quantity = new_qty
            if new_qty == 0:
                self.snapshot.avg_price = 0.0
            elif abs(qty_change) > abs(old_qty):
                self.snapshot.avg_price = fill.fill_px
        return self.snapshot

    def mark(self, price: float) -> PositionSnapshot:
        self.snapshot.mark_price = price
        return self.snapshot
''',
'src/market_maker/risk/exposure.py': 'def gross_exposure(price: float, qty: float) -> float:\n    return abs(price * qty)\n',
'src/market_maker/risk/kill_switch.py': '''
class KillSwitch:
    def __init__(self) -> None:
        self.active = False
        self.reason = ""

    def trigger(self, reason: str) -> None:
        self.active = True
        self.reason = reason

    def reset(self) -> None:
        self.active = False
        self.reason = ""
''',
'src/market_maker/risk/risk_engine.py': '''
from market_maker.common.types import PositionSnapshot, Quote, RiskDecision
from market_maker.order_book.book import OrderBook
from market_maker.risk.checks import check_quote
from market_maker.risk.kill_switch import KillSwitch
from market_maker.risk.limits import RiskLimits


class RiskEngine:
    def __init__(self) -> None:
        self.limits = RiskLimits()
        self.kill_switch = KillSwitch()
        self.reject_count = 0

    def evaluate(self, book: OrderBook, quote: Quote, position: PositionSnapshot) -> RiskDecision:
        if self.kill_switch.active:
            return RiskDecision(allowed=False, reason=f"kill_switch:{self.kill_switch.reason}")
        decision = check_quote(book, quote, position, self.limits)
        if not decision.allowed:
            self.reject_count += 1
            if self.reject_count >= self.limits.reject_limit:
                self.kill_switch.trigger("reject_limit")
        return decision
'''} .items(): add(path, content)

# execution
for path, content in {
'src/market_maker/execution/__init__.py': base_init,
'src/market_maker/execution/broker/__init__.py': base_init,
'src/market_maker/execution/broker/base.py': '''
from abc import ABC, abstractmethod
from market_maker.common.types import Fill, Order


class Broker(ABC):
    @abstractmethod
    def place(self, order: Order) -> Fill | None:
        raise NotImplementedError
''',
'src/market_maker/execution/broker/simulated_broker.py': '''
from __future__ import annotations
import random
from market_maker.common.enums import OrderStatus
from market_maker.common.types import Fill, MarketEvent, Order


class SimulatedBroker:
    def __init__(self, maker_fee_bps: float = 1.0, partial_fill_probability: float = 0.35) -> None:
        self.maker_fee_bps = maker_fee_bps
        self.partial_fill_probability = partial_fill_probability

    def place(self, order: Order, event: MarketEvent) -> Fill | None:
        crossed = (
            order.side.value == "buy" and order.price >= event.ask
        ) or (
            order.side.value == "sell" and order.price <= event.bid
        )
        if not crossed:
            return None
        fill_size = order.size
        if random.random() < self.partial_fill_probability:
            fill_size = max(order.size * 0.5, 1e-6)
            order.status = OrderStatus.PARTIAL
        else:
            order.status = OrderStatus.FILLED
        fee = abs(order.price * fill_size) * self.maker_fee_bps * 1e-4
        order.filled_size += fill_size
        return Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            fill_px=order.price,
            fill_size=fill_size,
            ts_ns=event.ts_ns,
            fee=fee,
        )
''',
'src/market_maker/execution/broker/alpaca_broker.py': 'from market_maker.execution.broker.base import Broker\n\nclass AlpacaBroker(Broker):\n    def place(self, order):\n        raise NotImplementedError("Live broker adapter not implemented in scaffold")\n',
'src/market_maker/execution/broker/ibkr_broker.py': 'from market_maker.execution.broker.base import Broker\n\nclass IbkrBroker(Broker):\n    def place(self, order):\n        raise NotImplementedError("Live broker adapter not implemented in scaffold")\n',
'src/market_maker/execution/order_manager.py': '''
from market_maker.common.enums import Side
from market_maker.common.types import Order, Quote
from market_maker.common.utils import order_id


class OrderManager:
    def quote_to_orders(self, quote: Quote, ts_ns: int) -> list[Order]:
        return [
            Order(order_id=order_id(), symbol=quote.symbol, side=Side.BUY, price=quote.bid_px, size=quote.bid_sz, ts_ns=ts_ns),
            Order(order_id=order_id(), symbol=quote.symbol, side=Side.SELL, price=quote.ask_px, size=quote.ask_sz, ts_ns=ts_ns),
        ]
''',
'src/market_maker/execution/order_router.py': 'class OrderRouter:\n    def route(self, orders: list):\n        return orders\n',
'src/market_maker/execution/fill_handler.py': 'from market_maker.common.types import Fill\n\n\ndef handle_fill(fill: Fill) -> Fill:\n    return fill\n',
'src/market_maker/execution/cancel_replace.py': 'def cancel_replace_needed(old_quote, new_quote) -> bool:\n    return old_quote != new_quote\n',
'src/market_maker/execution/execution_engine.py': '''
from __future__ import annotations
from market_maker.common.types import Fill, MarketEvent, Quote
from market_maker.execution.broker.simulated_broker import SimulatedBroker
from market_maker.execution.order_manager import OrderManager
from market_maker.monitoring.metrics import metrics_registry
from market_maker.order_book.book_builder import BookBuilder
from market_maker.risk.position_manager import PositionManager
from market_maker.risk.risk_engine import RiskEngine
from market_maker.strategy.strategy_engine import StrategyEngine


class ExecutionEngine:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.book_builder = BookBuilder(symbol)
        self.position_manager = PositionManager(symbol)
        self.strategy_engine = StrategyEngine()
        self.risk_engine = RiskEngine()
        self.order_manager = OrderManager()
        self.broker = SimulatedBroker()
        self.last_quote: Quote | None = None
        self.last_fill: Fill | None = None

    def on_market_event(self, event: MarketEvent) -> tuple[Quote | None, list[Fill]]:
        book = self.book_builder.on_event(event)
        self.position_manager.mark(book.mid_price())
        quote = self.strategy_engine.on_book(book, self.position_manager.snapshot)
        decision = self.risk_engine.evaluate(book, quote, self.position_manager.snapshot)
        if not decision.allowed:
            metrics_registry.risk_rejects.inc()
            return None, []
        fills: list[Fill] = []
        for order in self.order_manager.quote_to_orders(quote, event.ts_ns):
            fill = self.broker.place(order, event)
            if fill:
                self.position_manager.apply_fill(fill)
                fills.append(fill)
                metrics_registry.fills.inc()
        self.last_quote = quote
        metrics_registry.quotes.inc()
        return quote, fills


class LiveCoordinator:
    def __init__(self, symbol: str = "BTCUSD") -> None:
        self.engine = ExecutionEngine(symbol)

    async def on_market_event(self, event: MarketEvent) -> None:
        self.engine.on_market_event(event)
'''} .items(): add(path, content)

# portfolio
for path, content in {
'src/market_maker/portfolio/__init__.py': base_init,
'src/market_maker/portfolio/positions.py': 'from market_maker.risk.position_manager import PositionManager\n',
'src/market_maker/portfolio/pnl.py': '''
from market_maker.common.types import PositionSnapshot


def total_pnl(position: PositionSnapshot) -> float:
    return position.realized_pnl + position.unrealized_pnl
''',
'src/market_maker/portfolio/fees.py': 'def fee_bps_to_cost(price: float, qty: float, fee_bps: float) -> float:\n    return abs(price * qty) * fee_bps * 1e-4\n',
'src/market_maker/portfolio/slippage.py': 'def slippage_cost(expected_px: float, actual_px: float, qty: float) -> float:\n    return abs(actual_px - expected_px) * qty\n',
'src/market_maker/portfolio/inventory.py': 'def inventory_ratio(qty: float, limit: float) -> float:\n    return 0.0 if limit == 0 else qty / limit\n'} .items(): add(path, content)

# backtest
for path, content in {
'src/market_maker/backtest/__init__.py': base_init,
'src/market_maker/backtest/replay_engine.py': '''
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
''',
'src/market_maker/backtest/event_loop.py': '''
from collections.abc import Iterable
from market_maker.common.types import MarketEvent


def iter_events(events: Iterable[MarketEvent]):
    for event in events:
        yield event
''',
'src/market_maker/backtest/fills.py': 'from market_maker.common.types import Fill\n\n\ndef fill_notional(fill: Fill) -> float:\n    return fill.fill_px * fill.fill_size\n',
'src/market_maker/backtest/metrics.py': '''
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class BacktestMetrics:
    trades: int
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    final_position: float
    max_abs_position: float
''',
'src/market_maker/backtest/reports.py': '''
from market_maker.backtest.metrics import BacktestMetrics


def build_summary(result) -> str:
    m = result.metrics
    return (
        f"trades={m.trades} total_pnl={m.total_pnl:.2f} "
        f"realized_pnl={m.realized_pnl:.2f} unrealized_pnl={m.unrealized_pnl:.2f} "
        f"final_position={m.final_position:.4f} max_abs_position={m.max_abs_position:.4f}"
    )
''',
'src/market_maker/backtest/parameter_sweep.py': '''
from market_maker.backtest.simulator import run_backtest


def sweep(events, spreads=(2.0, 4.0, 6.0)) -> list[dict]:
    results = []
    for spread in spreads:
        result = run_backtest(events, base_spread_bps=spread)
        results.append({"spread": spread, "total_pnl": result.metrics.total_pnl})
    return results
''',
'src/market_maker/backtest/simulator.py': '''
from __future__ import annotations
from dataclasses import dataclass
from market_maker.backtest.metrics import BacktestMetrics
from market_maker.execution.execution_engine import ExecutionEngine
from market_maker.strategy.quote_policy import QuotePolicy


@dataclass
class BacktestResult:
    metrics: BacktestMetrics
    fills: list
    last_quote: object | None


def run_backtest(events, base_spread_bps: float = 4.0) -> BacktestResult:
    engine = ExecutionEngine("BTCUSD")
    engine.strategy_engine.quote_policy = QuotePolicy(base_spread_bps=base_spread_bps)
    fills = []
    max_abs_position = 0.0
    for event in events:
        quote, new_fills = engine.on_market_event(event)
        fills.extend(new_fills)
        max_abs_position = max(max_abs_position, abs(engine.position_manager.snapshot.quantity))
    snap = engine.position_manager.snapshot
    metrics = BacktestMetrics(
        trades=len(fills),
        realized_pnl=snap.realized_pnl,
        unrealized_pnl=snap.unrealized_pnl,
        total_pnl=snap.realized_pnl + snap.unrealized_pnl,
        final_position=snap.quantity,
        max_abs_position=max_abs_position,
    )
    return BacktestResult(metrics=metrics, fills=fills, last_quote=engine.last_quote)
'''} .items(): add(path, content)

# storage
for path, content in {
'src/market_maker/storage/__init__.py': base_init,
'src/market_maker/storage/parquet_store.py': '''
from pathlib import Path
import pandas as pd


class ParquetStore:
    def write_records(self, path: str | Path, records: list[dict]) -> None:
        pd.DataFrame(records).to_parquet(path, index=False)
''',
'src/market_maker/storage/redis_streams.py': '''
from __future__ import annotations
from redis import Redis
from market_maker.settings import get_settings


class RedisStreamStore:
    def __init__(self, url: str | None = None) -> None:
        self.url = url or get_settings().redis_url
        self.client = Redis.from_url(self.url, decode_responses=True)

    def publish_event(self, stream: str, payload: dict) -> str:
        return self.client.xadd(stream, payload)
''',
'src/market_maker/storage/sqlite_store.py': '''
import sqlite3
from pathlib import Path


class SQLiteStore:
    def __init__(self, path: str | Path = "data/results/session.db") -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("create table if not exists runs (id integer primary key, note text)")

    def insert_run(self, note: str) -> None:
        self.conn.execute("insert into runs(note) values (?)", (note,))
        self.conn.commit()
''',
'src/market_maker/storage/session_recorder.py': '''
from market_maker.storage.parquet_store import ParquetStore


class SessionRecorder:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.store = ParquetStore()

    def append(self, payload: dict) -> None:
        self.records.append(payload)

    def flush(self, path: str) -> None:
        self.store.write_records(path, self.records)
'''} .items(): add(path, content)

# monitoring
for path, content in {
'src/market_maker/monitoring/__init__.py': base_init,
'src/market_maker/monitoring/metrics.py': '''
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
''',
'src/market_maker/monitoring/tracing.py': 'def trace_event(name: str, payload: dict) -> dict:\n    return {"event": name, **payload}\n',
'src/market_maker/monitoring/health.py': '''
from market_maker.common.utils import now_ns


def get_health_snapshot() -> dict:
    return {"status": "ok", "ts_ns": now_ns()}
''',
'src/market_maker/monitoring/alerts.py': 'def should_alert(total_pnl: float, threshold: float = -250.0) -> bool:\n    return total_pnl <= threshold\n',
'src/market_maker/monitoring/dashboards.py': 'DASHBOARDS = ["latency", "pnl", "risk"]\n'} .items(): add(path, content)

# api
for path, content in {
'src/market_maker/api/__init__.py': base_init,
'src/market_maker/api/schemas.py': '''
from pydantic import BaseModel


class ControlResponse(BaseModel):
    status: str
    detail: str
''',
'src/market_maker/api/services/session_service.py': 'def get_session_state() -> dict:\n    return {"status": "idle"}\n',
'src/market_maker/api/services/replay_service.py': 'def replay() -> dict:\n    return {"status": "replayed"}\n',
'src/market_maker/api/services/metrics_service.py': 'def metrics_snapshot() -> dict:\n    return {"quotes": 0, "fills": 0}\n',
'src/market_maker/api/routes/health.py': '''
from fastapi import APIRouter
from market_maker.monitoring.health import get_health_snapshot

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return get_health_snapshot()
''',
'src/market_maker/api/routes/positions.py': '''
from fastapi import APIRouter

router = APIRouter()


@router.get("/positions")
def positions() -> dict:
    return {"positions": []}
''',
'src/market_maker/api/routes/pnl.py': '''
from fastapi import APIRouter

router = APIRouter()


@router.get("/pnl")
def pnl() -> dict:
    return {"realized_pnl": 0.0, "unrealized_pnl": 0.0, "total_pnl": 0.0}
''',
'src/market_maker/api/routes/quotes.py': '''
from fastapi import APIRouter

router = APIRouter()


@router.get("/quotes")
def quotes() -> dict:
    return {"quotes": []}
''',
'src/market_maker/api/routes/controls.py': '''
from fastapi import APIRouter
from market_maker.api.schemas import ControlResponse

router = APIRouter()


@router.post("/controls/start", response_model=ControlResponse)
def start() -> ControlResponse:
    return ControlResponse(status="ok", detail="engine start requested")


@router.post("/controls/stop", response_model=ControlResponse)
def stop() -> ControlResponse:
    return ControlResponse(status="ok", detail="engine stop requested")
''',
'src/market_maker/api/app.py': '''
from fastapi import FastAPI
from market_maker.api.routes.health import router as health_router
from market_maker.api.routes.positions import router as positions_router
from market_maker.api.routes.pnl import router as pnl_router
from market_maker.api.routes.quotes import router as quotes_router
from market_maker.api.routes.controls import router as controls_router

app = FastAPI(title="market-maker-py")
app.include_router(health_router)
app.include_router(positions_router)
app.include_router(pnl_router)
app.include_router(quotes_router)
app.include_router(controls_router)
'''} .items(): add(path, content)

# infra / deployment
for path, content in {
'infra/docker/app.Dockerfile': '''
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .
CMD ["uvicorn", "market_maker.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
''',
'infra/docker/worker.Dockerfile': 'FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install --no-cache-dir -e .\nCMD ["python", "scripts/run_live.py"]\n',
'infra/docker/backtest.Dockerfile': 'FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install --no-cache-dir -e .\nCMD ["python", "scripts/run_backtest.py"]\n',
'infra/redis/redis.conf': 'appendonly yes\n',
'infra/prometheus/prometheus.yml': '''
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
''',
'infra/grafana/dashboards/latency_dashboard.json': '{"title": "Latency"}\n',
'infra/grafana/dashboards/pnl_dashboard.json': '{"title": "PnL"}\n',
'infra/grafana/dashboards/risk_dashboard.json': '{"title": "Risk"}\n',
'deployment/systemd/market_data.service': '[Unit]\nDescription=market data service\n',
'deployment/systemd/strategy.service': '[Unit]\nDescription=strategy service\n',
'deployment/systemd/execution.service': '[Unit]\nDescription=execution service\n',
'deployment/systemd/risk.service': '[Unit]\nDescription=risk service\n',
'deployment/k8s/api-deployment.yaml': 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: mm-api\n',
'deployment/k8s/worker-deployment.yaml': 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: mm-worker\n',
'deployment/k8s/redis-deployment.yaml': 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: mm-redis\n',
'deployment/k8s/monitoring.yaml': 'apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: mm-monitoring\n'} .items(): add(path, content)

# tests
for path, content in {
'tests/unit/test_order_book.py': '''
from market_maker.common.types import MarketEvent
from market_maker.order_book.book import OrderBook


def test_order_book_mid_and_spread():
    book = OrderBook("BTCUSD")
    book.apply_event(MarketEvent(ts_ns=1, symbol="BTCUSD", bid=100, ask=102, bid_size=2, ask_size=3))
    assert book.mid_price() == 101
    assert book.spread() == 2
''',
'tests/unit/test_signals.py': '''
from market_maker.common.types import MarketEvent
from market_maker.order_book.book import OrderBook
from market_maker.signals.signal_engine import SignalEngine


def test_signal_engine_returns_alpha():
    book = OrderBook("BTCUSD")
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    vector = SignalEngine().compute(book)
    assert isinstance(vector.alpha, float)
''',
'tests/unit/test_quote_engine.py': '''
from market_maker.common.types import MarketEvent, PositionSnapshot
from market_maker.order_book.book import OrderBook
from market_maker.strategy.strategy_engine import StrategyEngine


def test_quote_engine_bid_below_ask():
    book = OrderBook("BTCUSD")
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    quote = StrategyEngine().on_book(book, PositionSnapshot(symbol="BTCUSD"))
    assert quote.bid_px < quote.ask_px
''',
'tests/unit/test_risk_engine.py': '''
from market_maker.common.types import MarketEvent, PositionSnapshot
from market_maker.order_book.book import OrderBook
from market_maker.strategy.strategy_engine import StrategyEngine
from market_maker.risk.risk_engine import RiskEngine


def test_risk_engine_allows_basic_quote():
    book = OrderBook("BTCUSD")
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=10_000_000_000 + i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    position = PositionSnapshot(symbol="BTCUSD")
    quote = StrategyEngine().on_book(book, position)
    decision = RiskEngine().evaluate(book, quote, position)
    assert decision.allowed
''',
'tests/unit/test_pnl.py': '''
from market_maker.common.enums import Side
from market_maker.common.types import Fill
from market_maker.risk.position_manager import PositionManager


def test_position_manager_realizes_pnl():
    pm = PositionManager("BTCUSD")
    pm.apply_fill(Fill(order_id="1", symbol="BTCUSD", side=Side.BUY, fill_px=100, fill_size=1, ts_ns=1))
    snap = pm.apply_fill(Fill(order_id="2", symbol="BTCUSD", side=Side.SELL, fill_px=105, fill_size=1, ts_ns=2))
    assert snap.realized_pnl > 0
''',
'tests/integration/test_feed_to_signal_flow.py': '''
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.execution.execution_engine import ExecutionEngine


def test_feed_to_signal_flow_runs():
    events = generate_synthetic_events("BTCUSD", 10)
    engine = ExecutionEngine("BTCUSD")
    for event in events:
        engine.on_market_event(event)
    assert engine.last_quote is not None
''',
'tests/integration/test_quote_to_execution_flow.py': '''
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.execution.execution_engine import ExecutionEngine


def test_quote_to_execution_flow_runs():
    engine = ExecutionEngine("BTCUSD")
    fills = []
    for event in generate_synthetic_events("BTCUSD", 20):
        _, new_fills = engine.on_market_event(event)
        fills.extend(new_fills)
    assert isinstance(fills, list)
''',
'tests/integration/test_backtest_pipeline.py': '''
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest


def test_backtest_pipeline_runs():
    result = run_backtest(generate_synthetic_events("BTCUSD", 50))
    assert result.metrics.trades >= 0
''',
'tests/fixtures/sample_l2.json': '{"symbol": "BTCUSD"}\n',
'tests/fixtures/sample_trades.json': '{"symbol": "BTCUSD"}\n'} .items(): add(path, content)

for path, content in files.items():
    full = root / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content)

print(f"wrote {len(files)} files")
