from market_maker.storage.redis_streams import RedisStreamStore


class EventPublisher:
    def __init__(self) -> None:
        self.store = RedisStreamStore()

    def publish(self, stream: str, payload: dict) -> None:
        self.store.publish_event(stream, payload)
