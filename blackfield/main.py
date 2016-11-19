import sqlite3
import time
from queue import Queue, Empty
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from rfid.main import Driver

from blackfield.data_access.select import select
from blackfield.variables import DB_TEST_FILE, BACKGROUND, SERIAL_PATH, TEST_ENCRYPTION_KEY, LAYOUT, NAME_FRAME, \
    INVALID_CART


screen_manager = ScreenManager(transition=FadeTransition())
TRANSITION_TIMEOUT = 1.5
EVENT_INTERVAL_RATE = 1/30.
QUEUE_TIMEOUT = 0.01
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


class MainScreen(Screen):
    background = BACKGROUND

    def __init__(self):
        super(MainScreen, self).__init__()
        # Checking for cart input 30 times per second
        self.event = Clock.schedule_interval(self.listen_for_cart_input, EVENT_INTERVAL_RATE)

    # noinspection PyUnusedLocal
    def listen_for_cart_input(self, dt):
        try:
            code = carts.get(timeout=QUEUE_TIMEOUT)
            print(code)
            person = select(cursor, code)
            Clock.unschedule(self.event)
            global person_to_view
            if person:
                person_to_view = person
            else:
                person_to_view = select(cursor, INVALID_CART.code)
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
    name = StringProperty()
    image = StringProperty()
    frame = NAME_FRAME

    def __init__(self):
        super(PersonInfoContainer, self).__init__()
        self.name = person_to_view.name
        self.image = person_to_view.image_path
        print(self.name)
        print(self.image)


class BlackField(App):
    def build(self):
        Builder.load_file(LAYOUT)
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
