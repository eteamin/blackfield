import sqlite3
import unittest

from blackfield.variables import TEST_AVATAR
from blackfield.model import Person


class TestCase(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('people.test.db')
        self.cursor = self.connection.cursor()

    def test_read_cart(self):
        pass


