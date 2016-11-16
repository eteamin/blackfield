import sqlite3

from blackfield.model.person import Person
from blackfield.variables import DB_FILE, DB_TEST_FILE, TEST_AVATAR


if __name__ == '__main__':
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    connection_to_test_db = sqlite3.connect(DB_TEST_FILE)
    cursor_to_test_db = connection_to_test_db.cursor()

    try:
        # Create the db
        cursor.execute(
            """
            CREATE TABLE people (id int primary_key, name char, person_code unique, image BLOB)
            """
        )
    except sqlite3.OperationalError:
        pass

    try:
        # Create test db
        cursor_to_test_db.execute(
            """
            CREATE TABLE people (id int primary_key, name char, person_code unique, image BLOB)
            """
        )
    except sqlite3.OperationalError:
        pass

    try:
        # Insert test data
        with open(TEST_AVATAR, 'rb') as avatar:
            test_person = Person(name='test', code='1', image=[memoryview(avatar.read())])
            values = (test_person.name, test_person.code, test_person.image)
            cursor_to_test_db.execute(
                """
                INSERT INTO people VALUES (?, ?, ?)
                """,
                values
            )
    except sqlite3.OperationalError:
        pass
