import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from rfid.main import Driver

from blackfield.data_access.select import select
from blackfield.model import Person
from blackfield.variables import DB_FILE, BACKGROUND, SERIAL_PATH, TEST_ENCRYPTION_KEY


screen_manager = ScreenManager()
CART_INSERT_TIMEOUT = 1
QUEUE_TIMEOUT = 0.5
carts = Queue()
cursor = sqlite3.connect(DB_FILE).cursor()
person_to_view = None
driver = Driver(SERIAL_PATH, encrypion_key=TEST_ENCRYPTION_KEY, timeout=1)


def read_cart():
    while True:
        code = driver.loop()
        carts.put(code)

rfid_thread = Thread(name='RFID', target=read_cart, daemon=True)
rfid_thread.start()


class MainScreen(Screen):

    def __init__(self):
        super(MainScreen, self).__init__()
        background = Image(source=BACKGROUND)
        self.add_widget(background)
        self.event = Clock.schedule_interval(self.listen_for_cart_input, 1/30.)

    def listen_for_cart_input(self, dt):
        try:
            code = carts.get()
            person = select(cursor, code)
            if person:
                Clock.unschedule(self.event)
                assert isinstance(person, Person)
                global person_to_view
                person_to_view = person
                screen_manager.switch_to(ImageScreen())
        except (Empty, AssertionError):
            pass


class ImageScreen(Screen):

    image_view_timer = 2
    wait_thread = Thread(name='wait', daemon=True)

    def __init__(self):
        super(ImageScreen, self).__init__()
        global image_view_timer
        self.wait_thread.start()
        while image_view_timer:
            pass
        screen_manager.switch_to(MainScreen())

    def wait(self):
        self.image_view_timer = 2
        time.sleep(self.image_view_timer)
        self.image_view_timer = 0


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
