from os import path
import sqlite3

import blackfield
from blackfield.model import Person


DB_FILE = path.abspath(path.join(path.dirname(blackfield.__file__), 'people.db'))
DB_TEST_FILE = path.abspath(path.join(path.dirname(blackfield.__file__), 'people.db.test'))
BACKGROUND = path.abspath(path.join(path.dirname(blackfield.__file__), 'stuff', 'background.png'))
NAME_FRAME = path.abspath(path.join(path.dirname(blackfield.__file__), 'stuff', 'name_frame.png'))
PERSON_IMAGE = path.abspath(path.join(path.dirname(blackfield.__file__), 'stuff', 'person_image.png'))
TEST_AVATAR = path.abspath(path.join(path.dirname(blackfield.__file__), 'tests', 'stuff', 'avatar.png'))
SERIAL_PATH = '/dev/ttyUSB0'
with open(TEST_AVATAR, 'rb') as avatar:
    TEST_PERSON = Person(name='test', code=0, image=sqlite3.Binary(avatar.read()))
TEST_ENCRYPTION_KEY = 281474976710655
