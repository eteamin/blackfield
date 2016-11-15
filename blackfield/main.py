import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from rfid.main import Driver

from blackfield.data_access import select
from blackfield.variables import DB_FILE, BACKGROUND


screen_manager = ScreenManager()
CART_INSERT_TIMEOUT = 1
carts = Queue()
db_connection = sqlite3.connect(DB_FILE)
cursor = db_connection.cursor()
person_to_view = None


class MainScreen(Screen):

    def __init__(self):
        super(MainScreen, self).__init__()
        rfid_thread = Thread(name='RFID', target=self.read_cart, daemon=True)
        rfid_thread.start()

        background = Image(source=BACKGROUND)
        self.add_widget(background)

        try:
            cart_num = carts.get(timeout=0.1)
            person = select(cursor, cart_num)
            global person_to_view
            person_to_view = person
            screen_manager.switch_to(ImageScreen())
        except Empty:
            time.sleep(0.1)

    def read_cart(self):
        cart_num = read()
        carts.put(cart_num)


class ImageScreen(Screen):
    def __init__(self):
        super(ImageScreen, self).__init__()


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
