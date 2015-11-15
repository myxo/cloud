import threading
import os
from BaseHTTPServer import HTTPServer

from taskpool import TaskPool
from client_listener import ClientListener
from engine_listener import EngineListener
# from clientHTTPlistener import ClientHTTPListener
from clientHTTPlistener import httpServerFactory



tp = TaskPool()
clientListener = ClientListener(tp)
engineListener = EngineListener(tp)

taskpool_thread = threading.Thread(target=tp.loop, args=()).start()
# threading.Thread(target=engineListener.loop, args=()).start()
# threading.Thread(target=clientListener.loop, args=()).start()

ClientHTTPListener = httpServerFactory({'taskpool': tp})
serv = HTTPServer(("192.168.0.108", 8889), ClientHTTPListener)
# serv = HTTPServer(("localhost", 8889), ClientHTTPListener)
try:
    serv.serve_forever()
except KeyboardInterrupt:
    print 'KeyboardInterrupt 8P'
    os._exit(0)
# taskpool_thread.join()