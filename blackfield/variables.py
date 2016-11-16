from os import path

import blackfield


DB_FILE = path.abspath(path.join(path.dirname(blackfield.__file__), 'people.db'))
DB_TEST_FILE = path.abspath(path.join(path.dirname(blackfield.__file__), 'people.db.test'))
BACKGROUND = path.abspath(path.join(path.dirname(blackfield.__file__), 'stuff', 'background.jpg'))
TEST_AVATAR = path.abspath(path.join(path.dirname(blackfield.__file__), 'tests', 'stuff', 'avatar.jpg'))
SERIAL_PATH = '/dev/ttyUSB0'
