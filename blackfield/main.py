import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from rfid.main import Driver

from blackfield.data_access.select import select
from blackfield.model import Person
from blackfield.variables import DB_TEST_FILE, BACKGROUND, SERIAL_PATH, TEST_ENCRYPTION_KEY, NAME_FRAME, PERSON_IMAGE


screen_manager = ScreenManager(transition=FadeTransition())
CART_INSERT_TIMEOUT = 1
TRANSITION_TIMEOUT = 2
EVENT_INTERVAL_RATE = 1/30.
QUEUE_TIMEOUT = 0.1
READ_CARD_SLEEP_TIMEOUT = 2
DRIVER_TIMEOUT = 1
carts = Queue()
cursor = sqlite3.connect(DB_TEST_FILE).cursor()
person_to_view = None
driver = Driver(SERIAL_PATH, encrypion_key=TEST_ENCRYPTION_KEY, timeout=DRIVER_TIMEOUT)


def read_cart():
    while True:
        code = driver.loop()
        carts.put(code)
        time.sleep(READ_CARD_SLEEP_TIMEOUT)

rfid_thread = Thread(name='RFID', target=read_cart, daemon=True)
rfid_thread.start()


def store_file(file):
    with open(PERSON_IMAGE, 'wb') as image:
        image.write(file)


class MainScreen(Screen):

    def __init__(self):
        super(MainScreen, self).__init__()
        # Checking for cart input 30 times per second
        self.event = Clock.schedule_interval(self.listen_for_cart_input, EVENT_INTERVAL_RATE)

    # noinspection PyUnusedLocal
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
        trigger_back_to_main = Clock.create_trigger(self.back_to_main, timeout=TRANSITION_TIMEOUT)
        self.add_widget(PersonInfoContainer())
        trigger_back_to_main()

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def back_to_main(self, dt):
        screen_manager.switch_to(MainScreen())


class PersonInfoContainer(RelativeLayout):
    def __init__(self):
        super(PersonInfoContainer, self).__init__()


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
