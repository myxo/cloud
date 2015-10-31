import socket
import time
import os
import sys
import psutil

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def send_socket_message(task_status):
    sock = socket.socket()
    # sock.connect(('myxomaster.cloudapp.net', 9000))
    sock.connect(('localhost', 9000))
    sock.send('i am rock')
    sock.send(task_status)
    sock.close()

start_time = time.time()
timeout = 30
pid = int(sys.argv[1])
task_id = sys.argv[2]
engine_id = sys.argv[3]

while 1:
    # if not check_pid(pid):
    if not psutil.pid_exists(pid):
        send_socket_message('done' + engine_id + task_id)
        break

    if time.time() - start_time > timeout:
        send_socket_message('time' + engine_id + task_id)
        break

