import time

import numpy.random
import os
import zipfile
import json
import requests
import sys


def send_task(task_path, url=None):
    client_config   = get_client_config()
    task_config     = get_task_config(task_path)
    zip_path = zip(task_path, task_config['id'])
    print 'send task file ' + zip_path

    if url == None:
        url = client_config['master_url']
    requests.post(url, files={'file': open(zip_path, 'rb'), 'request_type': 'new_task'})
    os.remove(zip_path)


def get_client_config():
    config = {}
    try:
        f = open('client_config', 'r')
        config = json.load(f)
        f.close
    except:
        config['master_url': 'http://localhost:8889']
    return config


def get_task_config(path_to_task_folder):
    config = {}
    try:
        f = open(path_to_task_folder + '/task_configuration', 'r')
        config = json.load(f)
        f.close()
        config['id'] = numpy.random.randint(1e15)
    except:
        config = task_default_config(path_to_task_folder)

    f = open(path_to_task_folder + '/task_configuration', 'w')
    json.dump(config, f)
    f.close()
    return config


def task_default_config(path_to_task_folder):
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


url = sys.argv[1] if len(sys.argv) > 1 else None

send_task('/home/myxo/univer/cloud/task1', url)
# time.sleep(1)
send_task('/home/myxo/univer/cloud/task2', url)
# time.sleep(1)
send_task('/home/myxo/univer/cloud/task3', url)
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task2')
# time.sleep(2)
# send_task('/home/myxo/univer/cloud/task3')

