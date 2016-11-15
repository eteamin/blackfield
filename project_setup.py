import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect('people.db')
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE people (id int primary_key, name char, person_code unique, image BLOB)
        """
    )
