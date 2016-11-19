import sqlite3

from blackfield.model import Person


def insert(cursor: sqlite3.Cursor, name: str, code: int, image_path: str) -> Person:
    values = (name, code, image_path)
    cursor.execute(
        """
        INSERT INTO people (name, code, image) VALUES (?, ?, ?);
        """,
        values
    )
