from os import path

import orm


DB_FILE = path.abspath(path.join(path.dirname(orm.__file__), '..', 'people.db'))
DB_TEST_FILE = path.abspath(path.join(path.dirname(orm.__file__), '..', 'people.db.test'))
TEST_AVATAR = path.abspath(path.join(path.dirname(orm.__file__), 'tests', 'stuff', 'avatar.jpg'))
BACKGROUND = path.abspath(path.join(path.dirname(orm.__file__), '..', 'stuff', 'background.jpg'))
SERIAL_PATH = '/dev/ttyUSB0'
