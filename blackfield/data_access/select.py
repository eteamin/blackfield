import sqlite3

from blackfield.model import Person


def select(cursor: sqlite3.Cursor, code: bytes) -> Person:
    query_result = cursor.execute(
        """
        SELECT * FROM people WHERE code = (?)
        """,
        (int(code), )
    ).fetchone()
    if not query_result:
        return None
    return personify(query_result)


def personify(query_result):
    return Person(
        name=query_result[1],
        code=query_result[2],
        image=query_result[3]
    )
