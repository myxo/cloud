import socket
import threading
import sys

from utils import *

class EngineListener:  # FIXME code for listener pretty much the same =\
    def __init__(self, taskpool, port=9000):
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
            print_message(' <-- engine connection from ' +  str(address))
            threading.Thread(target=handle, args=(connection, address, self.taskpool)).start()


def handle(client, address, taskpool):
    lock = threading.Lock()

    header = client.recv(9)
    if header != 'i am rock':
        print 'ERROR in recieve socket message: header does not match'
        print header
        client.close()
        return
    task_status = client.recv(4)
    engine_id = int(client.recv(1))
    task_id = client.recv(1024)
    print '---' + task_status
    print '---' + task_id

    lock.acquire()
    taskpool.task_done(task_id, task_status, engine_id, address)
    lock.release()
    if task_status == 'done':
        print_message(' - task done ' + str(task_id))
    elif task_status == 'time':
        print_message(' -!! task timeout ' + str(task_id))

    client.close()