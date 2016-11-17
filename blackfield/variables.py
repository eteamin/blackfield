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
INVALID_CART_AVATAR = path.abspath(
    path.join(
        path.dirname(blackfield.__file__), 'stuff', 'invalid_cart_avatar.png'
    )
)
LAYOUT = path.abspath(path.join(path.dirname(blackfield.__file__), 'view', 'view.kv'))
SERIAL_PATH = '/dev/ttyUSB0'

with open(TEST_AVATAR, 'rb') as avatar:
    TEST_PERSON = Person(name='test', code=0, image=sqlite3.Binary(avatar.read()))

with open(INVALID_CART_AVATAR, 'rb') as invalid_avatar:
    INVALID_CART = Person(name='invalid', code=500, image=sqlite3.Binary(invalid_avatar.read()))

TEST_ENCRYPTION_KEY = 281474976710655
