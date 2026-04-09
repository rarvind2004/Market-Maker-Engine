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
