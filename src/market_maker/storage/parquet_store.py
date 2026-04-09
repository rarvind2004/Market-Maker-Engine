from pathlib import Path
import pandas as pd


class ParquetStore:
    def write_records(self, path: str | Path, records: list[dict]) -> None:
        pd.DataFrame(records).to_parquet(path, index=False)
