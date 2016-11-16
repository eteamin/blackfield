import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.core.text import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from rfid.main import Driver

from blackfield.data_access.select import select
from blackfield.model import Person
from blackfield.variables import DB_FILE, BACKGROUND, SERIAL_PATH


def read_cart():
    # cart_num = read()
    # carts.put(cart_num)
    pass

screen_manager = ScreenManager()
CART_INSERT_TIMEOUT = 1
carts = Queue()
db_connection = sqlite3.connect(DB_FILE)
cursor = db_connection.cursor()
person_to_view = None
driver = Driver(SERIAL_PATH)
rfid_thread = Thread(name='RFID', target=read_cart, daemon=True)
rfid_thread.start()
image_view_timer = 0


def wait():
    global image_view_timer
    image_view_timer = 2
    time.sleep(image_view_timer)
    image_view_timer = 0

wait_thread = Thread(name='wait', daemon=True)


class MainScreen(Screen):

    def __init__(self):
        super(MainScreen, self).__init__()
        background = Image(source=BACKGROUND)
        self.add_widget(background)
        while True:
            try:
                cart_num = carts.get(timeout=0.5)
                person = select(cursor, cart_num)
                assert isinstance(person, Person)
                global person_to_view
                person_to_view = person
                screen_manager.switch_to(ImageScreen())
            except (Empty, AssertionError):
                time.sleep(0.1)
                continue


class ImageScreen(Screen):
    def __init__(self):
        super(ImageScreen, self).__init__()
        global image_view_timer
        wait_thread.start()
        while image_view_timer:
            time.sleep(0.1)
        screen_manager.switch_to(MainScreen())


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
