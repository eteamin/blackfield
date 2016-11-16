import sqlite3

from blackfield.model import Person


def select(cursor: sqlite3.Cursor, code: int) -> Person:
    return personify(cursor.execute(
        """
        SELECT * FROM people WHERE person_num = ?
        """,
        code
    ).fetchone())


def personify(query_result):
    return Person(
        name=query_result[1],
        code=query_result[2],
        image=query_result[3]
    )
