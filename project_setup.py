import sqlite3

from blackfield.variables import DB_FILE, DB_TEST_FILE, TEST_PERSON, INVALID_CART


if __name__ == '__main__':
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    connection_to_test_db = sqlite3.connect(DB_TEST_FILE)
    cursor_to_test_db = connection_to_test_db.cursor()

    try:
        # Create the db
        cursor.execute(
            """
            CREATE TABLE people (id int primary_key, name char, code int unique, image BLOB);
            """
        )
    except sqlite3.OperationalError as ex:
        print('Creating db failed due to %s' % str(ex))

    try:
        # Create test db
        cursor_to_test_db.execute(
            """
            CREATE TABLE people (id int primary_key, name char, code int unique, image BLOB);
            """
        )
    except sqlite3.OperationalError as ex:
        print('Creating test db failed due to %s' % str(ex))

    try:
        # Insert test data
        values = (TEST_PERSON.name, TEST_PERSON.code, TEST_PERSON.image)
        cursor_to_test_db.execute(
            """
            INSERT INTO people (name, code, image) VALUES (?, ?, ?);
            """,
            values
        )
    except sqlite3.OperationalError as ex:
        print('Inserting test data failed due to %s' % str(ex))

    try:
        # Insert row for invalid card
        values = (INVALID_CART.name, INVALID_CART.code, INVALID_CART.image)
        cursor_to_test_db.execute(
            """
            INSERT INTO people (name, code, image) VALUES (?, ?, ?);
            """,
            values
        )
    except sqlite3.OperationalError as ex:
        print('Inserting test data failed due to %s' % str(ex))

    connection.commit()
    connection_to_test_db.commit()
