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
                self.add_widget(PersonContainer())
            except (Empty, Person):
                time.sleep(0.1)
                continue


class PersonContainer(Widget):
    def __init__(self):
        super(PersonContainer, self).__init__()
        container = RelativeLayout()
        image = Image(source=person_to_view.image)
        title = Label(text='Sign Up', pos_hint={'center_x': 0.5, 'center_y': 0.9})
        container.add_widget(title)

        # password_input = TextInput(
        #     hint_text='Password',
        #     size_hint=(None, None),
        #     size=(Window.width / 2, Window.height / 20),
        #     pos_hint={'center_x': 0.5, 'center_y': 0.6},
        #     password=True
        # )
        # container.add_widget(password_input)


class BlackField(App):
    def build(self):
        screen_manager.add_widget(MainScreen())
        return screen_manager


if __name__ == '__main__':
    BlackField().run()
