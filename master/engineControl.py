import paramiko
import time
import threading
import subprocess
import requests

from utils import *

class EngineControl:
    def __init__(self, config, engine_id):
        self.address =          config['address']
        self.port =             config['port']
        self.name =             config['name']  # FIXME try ... catch
        self.engine_username =  config['engine_username']
        self.cores_available =  config['cores_available']
        self.working_directory = config['working_directory']

        self.http_address = 'http://' + self.address + ':' + str(self.port)

        self.task_active_list = {}
        self.summary_active_core = 0
        self.id = engine_id

        self.rsync_files(self.address, self.engine_username, self.working_directory)

        self.status = 'available'

    def send_task(self, task): #FIXME put client to engineInfo class   
        self.status = 'busy'
        self.task_active_list[task.id] = task
        task.start_time = int(time.time())
        task.time_send = time.localtime()

        # sftp = self.client.open_sftp()
        # # FIXME add exeption to this
        # sftp.put(task.zip_file_path, self.working_directory + task.zip_filename)
        # command = self.working_directory + 'engine_script.sh ' + str(task.id) + ' ' + str(self.id)
        # threading.Thread(target=engine_exec_command_handler, args=(self.client, command, task)).start()

        content = {'file': open(task.zip_file_path, 'rb'),
                    'task_id': str(task.id),
                    'engine_id': str(self.id)}
        try:
            res = requests.post(self.http_address, files=content)
            status_code = res.status_code
        except requests.ConnectionError, e:
            # print e
            status_code = 0

        if status_code != 200:
            print "ERROR in post request to the engine, task id - %d, engine id - %d, status code - %d"%(task.id, self.id, status_code)
            return

        self.summary_active_core += task.core_require
        
    def task_done(self, task_id):
        task = self.task_active_list[int(task_id)]
        self.summary_active_core -= task.core_require
        del self.task_active_list[int(task_id)]

    def can_accept(self, task):
        return task.core_require <= self.cores_available - self.summary_active_core


    def connect(self, username, userpass):
        # FIXME we do not need client anymore
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.address, username=username, password=userpass)
        except:
            print 'ERROR in connection to engine ' + self.address
            self.status = 'off'
        # FIXME some freaking bug here. Should make keyboard interrupt twice. 
        # Tired. Have no idea. Fix later. 
        threading.Thread(target=server_upper_handler, args=(self.client, self.working_directory, 
                    self.address, self.port, self.name)).start()
        

    def rsync_files(self, address, username, folder_to):
        files = [#'../engine/engine_script.sh', 
                #'../engine/check_is_done.py',
                #'../engine/upload_result.py',
                '../engine/engine_config',
                '../engine/httpServer.py']
        for f in files:
            # pass
            subprocess.call(['rsync', f, username + '@' + address + ':' + folder_to])

    def disconnect(self):
        try:
            requests.get(self.http_address + '/kill/')
        except requests.exceptions.ConnectionError:
            print_message("ERROR in disconnect %s. Server is already down"%self.name, 'red')
        except:
            print 'some error =('
        self.client.close()
        print self.name + ' disconnected'


def server_upper_handler(client, working_directory, server_address, port, server_name):
    # stdin, stdout, stderr = client.exec_command('python ' + working_directory + 'httpServer.py ' + server_address + ' ' + str(port) + ' &')
    # # for line in stderr:
    # print '{ from ' + server_name + ' } ', stderr.read()
    pass
    # for line in stdout:
    #     print line
    # print stderr.read()

def engine_exec_command_handler(client, command, task):
    stdin, stdout, stderr = client.exec_command(command)
    task.stderr = stderr.read()