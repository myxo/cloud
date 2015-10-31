import socket
import time

def send_task(task_name):
    print time.strftime("[ %H:%M:%S] ") + 'send task ' + task_name
    sock = socket.socket()
    # sock.connect(('myxomaster.cloudapp.net', 9090))
    sock.connect(('localhost', 9090))
    sock.send('i am rock')
    sock.send(task_name)

    # data = sock.recv(1024)

    # print data
    sock.close()


send_task('/home/myxo/univer/cloud/task1')
time.sleep(2)
send_task('/home/myxo/univer/cloud/task2')
time.sleep(2)
send_task('/home/myxo/univer/cloud/task3')
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task2')
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task3')

