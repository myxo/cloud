import socket
import time
import sys
import psutil
import json
import os

# def send_socket_message(task_status):
#     sock = socket.socket()
#     # sock.connect(('myxomaster.cloudapp.net', 9000))
#     sock.connect(('localhost', 9000))
#     sock.send('i am rock')
#     sock.send(task_status)
#     sock.close()

# def make_task_result_config_file(task_status, 
#                 task_id, 
#                 engine_id):
#     config = {}
#     config['task_status']   = task_status
#     config['task_id']       = task_id
#     config['engine_id']     = engine_id

#     if not os.path.isdir('result'):
#         if os.path.exists('result'):
#             os.remove('result')
#         os.makedirs('result')
#     with open('result/result_config', 'w') as f:
#         json.dump(config, f)


start_time = time.time()
timeout = 30
pid = int(sys.argv[1])
# task_id = sys.argv[2]
# engine_id = sys.argv[3]

if not os.path.isdir('result'):
    if os.path.exists('result'):
        os.remove('result')
    os.makedirs('result')

while 1:
    if not psutil.pid_exists(pid):
        # send_socket_message('done' + engine_id + task_id)
        # make_task_result_config_file('done', task_id, engine_id)
        sys.exit(0)
        break

    if time.time() - start_time > timeout:
        # make_task_result_config_file('done', task_id, engine_id)
        # send_socket_message('time' + engine_id + task_id)
        sys.exit(1)
        break

    time.sleep(1)

