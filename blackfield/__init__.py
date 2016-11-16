import threading
import time

_time = 0


def wait():
    global _time
    _time = 30
    time.sleep(_time)
    _time = 0

my_thread = threading.Thread(target=wait)
my_thread.start()
while _time:
    time.sleep(.01)
