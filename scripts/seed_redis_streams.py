from market_maker.storage.redis_streams import RedisStreamStore
from market_maker.backtest.replay_engine import generate_synthetic_events


if __name__ == "__main__":
    store = RedisStreamStore()
    for event in generate_synthetic_events("BTCUSD", 100):
        store.publish_event("market:events", event.model_dump())
    print("seeded")
