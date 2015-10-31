import socket
import threading
import json

from taskpool import TaskPool
# from task import Task
from client_listener import ClientListener
from engine_listener import EngineListener

f = open('taskpool_config', 'r')
tp_conf = json.load(f)
f.close

tp = TaskPool(tp_conf)
clistener = ClientListener(tp)
elistener = EngineListener(tp)

threading.Thread(target=tp.loop, args=()).start()
threading.Thread(target=elistener.loop, args=()).start()

clistener.loop()


# task1 = Task('/home/myxo/univer/cloud/task1')
# task2 = Task('/home/myxo/univer/cloud/task2')
# task3 = Task('/home/myxo/univer/cloud/task3')
# tp.add_new_task(task1)
# tp.add_new_task(task2)
# tp.add_new_task(task3)

# tp.add_new_task("task2.py")
# tp.add_new_task("task3.py")

# tp.connect_to_engines()
# tp.run_task()
# tp.loop()
# tp.close_connection()