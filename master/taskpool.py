from Queue import Queue
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
            self.engine_list.append(EngineInfo(engine_address, i))

        for engine in self.engine_list:
            engine.connect(self.username, self.userpass)

    def add_new_task(self, task):
        self.task_quere.put(task)

    def task_done(self, task_id, task_status, engine_id, engine_address):
        self.engine_list[engine_id].status = 'available'
        # print 'free ', engine_address
        # for engine in self.engine_list:
        #     if engine.address == engine_address:
        #         for task in engine.task_active_list:
        #             if task.id == task_id:
        #                 del task
        #                 engine.status = 'available'
        #                 return

        if task_status == 'done':
            print_message(' - task done ' + str(task_id))
        elif task_status == 'time':
            print_message(' -!! task timeout ' + str(task_id))


    def close_connection(self):
        for engine in self.engine_list:
            engine.disconnect()

    def loop(self):
        print 'taskpool: start loop'
        while 1:
            for i, engine in enumerate(self.engine_list):
                if engine.status == 'off':
                    continue

                if engine.status == 'available':
                    if not self.task_quere.empty():
                        engine.send_task(self.task_quere.get())

                # elif engine.status == 'busy':
                #     if (time.time() - engine.task_active_list[0].start_time > 
                #                 engine.task_active_list[0].timeout):
                #         print_message('task ' + str(engine.task_active_list[0].id) + ' done.')
                #         del engine.task_active_list[0]
                #         engine.status = 'available'
            # if self.task_quere.empty():
            #     break
            time.sleep(2)
            # print self.task_quere[0]