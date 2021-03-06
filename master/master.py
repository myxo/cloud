import threading
import os
import sys
import json
from BaseHTTPServer import HTTPServer

from taskpool import TaskPool
from HTTPlistener import httpServerFactory

f = open('taskpool_config', 'r')
master_config = json.load(f)
f.close


tp = TaskPool(master_config)
taskpool_thread = threading.Thread(target=tp.loop, args=()).start()

ip = master_config['master address']
port = master_config['master port']
HTTPListener = httpServerFactory({'taskpool': tp})
serv = HTTPServer((ip, port), HTTPListener)
print 'Starting master http server at port %d ....'%master_config['master port']


try:
    serv.serve_forever()
except KeyboardInterrupt:
    tp.close_connection()
    print 'KeyboardInterrupt 8P'
    os._exit(0)
