import sqlite3
import unittest

from rfid.main import Driver

from blackfield.variables import TEST_PERSON, DB_TEST_FILE, SERIAL_PATH, TEST_ENCRYPTION_KEY
from blackfield.data_access.select import select


class TestCase(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(DB_TEST_FILE)
        self.cursor = self.connection.cursor()
        self.driver = Driver(serial_path=SERIAL_PATH, encrypion_key=TEST_ENCRYPTION_KEY, timeout=1)

    def test_read_cart(self):
        rfid_resp = int(self.driver.loop()[:12])
        person = select(self.cursor, rfid_resp)
        self.assertEqual(person.__dict__, TEST_PERSON.__dict__)


if __name__ == '__main__':
    unittest.main()



