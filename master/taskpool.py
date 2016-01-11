import time
import json
import threading

from engineControl import EngineControl
from utils import *

class TaskPool:
    def __init__(self, config):
        self.config = config

        self.task_quere = Queue()
        self.alltask = {}
        self.engine_list = []
        self.username = self.config['engine username']
        self.userpass = self.config['engine password']

        self.init_engines()


    def init_engines(self):
        for i, engine_address in enumerate(self.config['engine address']):
            self.engine_list.append(EngineControl(engine_address, i, cores_available=1))

        for engine in self.engine_list:
            engine.connect(self.username, self.userpass)
            print engine.address + ' ready'


    def add_new_task(self, task):
        self.task_quere.put(task)
        self.alltask[task.id] = task
        print_message('  +  add new task ' + str(task.id))


    def task_done(self, task_id, task_status, engine_id):
        # self.alltask[task_id].done_event.wait()
        # print self.alltask[task_id].done_event.isSet()

        self.engine_list[engine_id].task_done(task_id)
        self.alltask[task_id].status = task_status

        if task_status == 'done':
            print_message('  -  task done ' + str(task_id), 'green')
        elif task_status == 'time':
            print_message(' !-! task timeout ' + str(task_id), 'red')


    def json_info(self):
        status = {}
        status['engine_names'] = [engine.address for engine in self.engine_list]
        status['task_waiting'] = [task.id for task in self.task_quere.get_list()]
        for engine in self.engine_list:
            status[str(engine.id)] = [task.id for task in engine.task_active_list.values()]

        filtered_list = filter(lambda x: x.status == 'done' or x.status == 'timeout', 
                            self.alltask.values())
        status['task_done'] = [task.id for task in filtered_list]
        return json.dumps(status)
                

    def close_connection(self):
        for engine in self.engine_list:
            engine.disconnect()


    def loop(self):
        print 'taskpool: start loop'
        lock = threading.Lock()
        while 1:
            lock.acquire()
            for i, engine in enumerate(self.engine_list):
                if engine.status == 'off':
                    continue

                # if engine.status == 'available':
                if not self.task_quere.empty():
                    if engine.can_accept(self.task_quere.head()):
                        t = self.task_quere.get()
                        self.alltask[t.id].engine_id = engine.id
                        self.alltask[t.id].status = 'proceed'
                        
                        engine.send_task(t)
                        print_message(' --> send task ' + str(t.id) + ' to ' + engine.address + ' ' + str(engine.id), 'blue')
            lock.release()
            time.sleep(1)
            # print self.task_quere[0]