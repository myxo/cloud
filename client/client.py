# import socket
import time

import numpy.random
import os
import zipfile
import json
import requests


# def send_task(task_name):
#     print time.strftime("[ %H:%M:%S ] ") + 'send task ' + task_name
#     sock = socket.socket()
#     # sock.connect(('myxomaster.cloudapp.net', 9090))
#     sock.connect(('localhost', 9090))
#     sock.send('i am rock')
#     sock.send(task_name)

#     # data = sock.recv(1024)

#     # print data
#     sock.close()

def send_task(task_path):
    config = get_config(task_path)
    zip_path = zip(task_path, config['id'])
    print 'send task file ' + zip_path
    requests.post('http://localhost:8889', files={'file': open(zip_path, 'rb'), 'request_type': 'new_task'})
    os.remove(zip_path)


def get_config(path_to_task_folder):
    config = {}
    try:
        f = open(path_to_task_folder + '/task_configuration', 'r')
        config = json.load(f)
        f.close()
        config['id'] = numpy.random.randint(1e15)
    except:
        config = default_config(path_to_task_folder)

    f = open(path_to_task_folder + '/task_configuration', 'w')
    json.dump(config, f)
    f.close()
    return config

def default_config(path_to_task_folder):
    config = {}
    config['id'] = numpy.random.randint(1e15)
    config['core_require'] = 1
    config['timeout'] = 30
    return config

def zip(path_to_task_folder, task_id):
    folder = path_to_task_folder
    zip_filename = str(task_id) + '.zip'
    zipname = '/tmp/' + zip_filename
    zip_file_path = os.path.abspath(zipname)
    if os.path.isfile(zip_file_path):
        return zip_file_path

    # if not os.path.isdir(path_to_task_folder + '/result'):
    #     if os.path.exists(path_to_task_folder + '/result'):
    #         os.remove(path_to_task_folder + '/result')
    #     print path_to_task_folder + '/result'
    #     os.makedirs(path_to_task_folder + '/result')
    #     open(path_to_task_folder + '/result/1', 'a').close() #dirty hack (overwise result folder does not created)

    zipf = zipfile.ZipFile(zip_file_path, 'w')
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file == (str(id) + '.zip'):
                continue

            absolute_filename = os.path.join(root, file)
            zip_filename = absolute_filename[len(folder)+len(os.sep):] # arent should I use just 'file' ???
            zipf.write(absolute_filename, zip_filename) # hack, remove folder name
    zipf.close()
    return zip_file_path

# def zip(path_to_task_folder, task_id):
#     if not os.path.isdir(path_to_task_folder + '/result'):
#         if os.path.exists(path_to_task_folder + '/result'):
#             os.remove(path_to_task_folder + '/result')
#         os.makedirs(path_to_task_folder + '/result')

#     import subprocess
#     zip_filename = str(task_id) + '.zip'
#     cmd = 'zip {0} {1}', str()
#     subprocess.Popen(cmd)


send_task('/home/myxo/univer/cloud/task1')
# time.sleep(1)
# send_task('/home/myxo/univer/cloud/task2')
# time.sleep(1)
# send_task('/home/myxo/univer/cloud/task3')
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task2')
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task3')

