import asyncio
import time
import socketio
import numpy as np
import cv2
import base64
import threading

cap0 = cv2.VideoCapture(0)
cap0.set(3,320)
cap0.set(4,240)
loop = asyncio.get_event_loop()
#sio = socketio.AsyncClient()
sio = socketio.Client()
start_timer = None

def setInterval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
    # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
  		     function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap

@setInterval(0.07)
def gg():
    retval, image = cap0.read()
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    # print (jpg_as_text)
    sio.emit('kawang boot', jpg_as_text)

@sio.on('connect')
def on_connect():
    print('connected to server')
    gg()

def start_server():
    sio.connect('http://172.16.1.5:4000')
    sio.wait()

#if __name__ == '__main__':
loop.run_until_complete(start_server())
