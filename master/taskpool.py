# from Queue import Queue
import paramiko
import time
import socket

from engineinfo import EngineInfo
from utils import *

class TaskPool:
    def __init__(self, config):
        self.config = config

        self.task_quere = Queue()
        self.engine_list = []
        # self.clients_list = []
        self.username = self.config['engine username']
        self.userpass = self.config['engine password']

        # self.listner_socket = socket.socket()
        # self.listner_socket.bind(('', 9095))
        # self.listner_socket.listen(5)

        self.init_engines()

    def init_engines(self):
        for i, engine_address in enumerate(self.config['engine address']):
            self.engine_list.append(EngineInfo(engine_address, i, cores_available=2))

        for engine in self.engine_list:
            engine.connect(self.username, self.userpass)

    def add_new_task(self, task):
        self.task_quere.put(task)
        print_message('  +  add new task ' + str(task.id))

    def task_done(self, task_id, task_status, engine_id, engine_address):
        self.engine_list[engine_id].status = 'available'
        self.engine_list[engine_id].task_done(task_id)


        if task_status == 'done':
            print_message('  -  task done ' + str(task_id), 'green')
        elif task_status == 'time':
            print_message(' !-! task timeout ' + str(task_id), 'red')


    def close_connection(self):
        for engine in self.engine_list:
            engine.disconnect()

    def loop(self):
        print 'taskpool: start loop'
        while 1:
            for i, engine in enumerate(self.engine_list):
                if engine.status == 'off':
                    continue

                # if engine.status == 'available':
                if not self.task_quere.empty():
                    if engine.can_accept(self.task_quere.head()):
                        t = self.task_quere.get()
                        engine.send_task(t)
                        print_message(' --> send task ' + str(t.id) + ' to ' + engine.address + ' ' + str(engine.engine_id), 'blue')

            time.sleep(2)
            # print self.task_quere[0]