from __future__ import annotations
from redis import Redis
from market_maker.settings import get_settings


class RedisStreamStore:
    def __init__(self, url: str | None = None) -> None:
        self.url = url or get_settings().redis_url
        self.client = Redis.from_url(self.url, decode_responses=True)

    def publish_event(self, stream: str, payload: dict) -> str:
        return self.client.xadd(stream, payload)
