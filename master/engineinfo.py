import paramiko
import time
import threading
import subprocess

from utils import *

class EngineInfo:
    def __init__(self, address, engine_id, cores_available=1):
        self.address = address
        self.engine_username = 'worker'
        self.cores_available = cores_available
        self.task_active_list = {}
        self.summary_active_core = 0
        self.engine_id = engine_id

        self.working_directory = '/home/worker/' # FIXME get working path
        self.rsync_files(address, self.engine_username, self.working_directory)

        self.status = 'available' #FIXME not string status

    def send_task(self, task): #FIXME put client to engineInfo class   
        self.status = 'busy'
        self.task_active_list[task.id] = task
        task.start_time = int(time.time())

        sftp = self.client.open_sftp()
        # FIXME add exeption to this
        sftp.put(task.zip_file_path, self.working_directory + task.zip_filename)
        command = self.working_directory + 'engine_script.sh ' + str(task.id) + ' ' + str(self.engine_id)
        threading.Thread(target=engine_exec_command_handler, args=(self.client, command, task)).start()
        self.summary_active_core += task.core_require
        
    def task_done(self, task_id):
        task = self.task_active_list[int(task_id)]
        self.summary_active_core -= task.core_require
        del self.task_active_list[int(task_id)]

    def can_accept(self, task):
        return task.core_require <= self.cores_available - self.summary_active_core


    def connect(self, username, userpass):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.address, username=username, password=userpass)
        except:
            print 'ERROR in connection to engine ' + self.address
            self.status = 'off'

    def rsync_files(self, address, username, folder_to):
        files = ['../engine/engine_script.sh', 
                '../engine/check_is_done.py',
                '../engine/upload_result.py',
                '../engine/engine_config']
        for f in files:
            subprocess.call(['rsync', f, username + '@' + address + ':' + folder_to])

    def disconnect(self):
        self.client.close()


def engine_exec_command_handler(client, command, task):
    stdin, stdout, stderr = client.exec_command(command)
    task.stderr = stderr.read()