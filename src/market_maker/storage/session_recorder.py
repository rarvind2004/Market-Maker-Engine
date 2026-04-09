from market_maker.storage.parquet_store import ParquetStore


class SessionRecorder:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.store = ParquetStore()

    def append(self, payload: dict) -> None:
        self.records.append(payload)

    def flush(self, path: str) -> None:
        self.store.write_records(path, self.records)
