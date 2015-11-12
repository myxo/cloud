import threading
from BaseHTTPServer import HTTPServer

from taskpool import TaskPool
from client_listener import ClientListener
from engine_listener import EngineListener
from clientHTTPlistener import ClientHTTPListener



tp = TaskPool()
clientListener = ClientListener(tp)
engineListener = EngineListener(tp)

threading.Thread(target=tp.loop, args=()).start()
threading.Thread(target=engineListener.loop, args=()).start()
threading.Thread(target=clientListener.loop, args=()).start()


serv = HTTPServer(("localhost", 8889), ClientHTTPListener)
serv.serve_forever()

