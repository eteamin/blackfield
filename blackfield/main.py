import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from rfid.main import Driver

from blackfield.data_access.select import select
from blackfield.model import Person
from blackfield.variables import DB_TEST_FILE, BACKGROUND, SERIAL_PATH, TEST_ENCRYPTION_KEY


screen_manager = ScreenManager()
CART_INSERT_TIMEOUT = 1
QUEUE_TIMEOUT = 0.1
carts = Queue()
cursor = sqlite3.connect(DB_TEST_FILE).cursor()
person_to_view = None
driver = Driver(SERIAL_PATH, encrypion_key=TEST_ENCRYPTION_KEY, timeout=1)


def read_cart():
    while True:
        code = driver.loop()
        carts.put(code)
        time.sleep(2)

rfid_thread = Thread(name='RFID', target=read_cart, daemon=True)
rfid_thread.start()


class MainScreen(Screen):

    def __init__(self):
        super(MainScreen, self).__init__()
        background = Image(source=BACKGROUND)
        self.add_widget(background)
        # Checking for cart input 30 times per second
        self.event = Clock.schedule_interval(self.listen_for_cart_input, 1/30.)

    def listen_for_cart_input(self, dt):
        try:
            code = carts.get(timeout=QUEUE_TIMEOUT)
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
    def __init__(self):
        super(ImageScreen, self).__init__()
        trigger_back_to_main = Clock.create_trigger(self.back_to_main, timeout=2)
        self.add_widget(Button(text='Hi'))
        trigger_back_to_main()

    def back_to_main(self, dt):
        screen_manager.switch_to(MainScreen())


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
