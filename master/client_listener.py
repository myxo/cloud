import socket
import threading
import sys

from task import Task
from utils import *

class ClientListener:
    def __init__(self, taskpool, port=9090):
        self.port = port

        self.socket = socket.socket()
        self.socket.bind(('', port))
        self.socket.listen(5)

        self.taskpool = taskpool

    def loop(self):
        while 1:
            try:
                connection, address = self.socket.accept()
            except KeyboardInterrupt:
                sys.exit(0)
            print_message('  o  client connection from ' +  str(address))
            threading.Thread(target=handle, args=(connection, self.taskpool)).start()


def handle(client, taskpool):
    lock = threading.Lock()

    header = client.recv(9)
    if header != 'i am rock':
        print 'ERROR in recieve socket message: header does not match'
        print header
        client.close()
        return
    task_name = client.recv(1024)
    task = Task(task_name)

    lock.acquire()
    taskpool.add_new_task(task)
    lock.release()
    

    client.close()