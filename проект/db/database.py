import sqlite3
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    db = "database.sqlite"

    def __init__(self):
        self._connection = sqlite3.connect(Database.db)

    def execute(self, query, params=tuple()):
        cursor = self._connection.cursor()
        return cursor.execute(query, params)

    def executemany(self, query, params=tuple(tuple())):
        cursor = self._connection.cursor()
        return cursor.executemany(query, params)

    def commit(self):
        self._connection.commit()

    def __del__(self):
        self._connection.close()
