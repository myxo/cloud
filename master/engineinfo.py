import paramiko
import time
import threading

from utils import *

class EngineInfo:
    def __init__(self, address, engine_id, cores_available=1):
        self.address = address
        self.cores_available = cores_available
        self.task_active_list = []
        self.engine_id = engine_id

        self.working_directory = '/home/worker/'

        self.status = 'available' #FIXME not string status

    def send_task(self, task): #FIXME put client to engineInfo class
        print_message(' --> send task ' + str(task.id) + ' to ' + self.address)
        
        self.status = 'busy'
        self.task_active_list.append(task)
        task.start_time = int(time.time())

        sftp = self.client.open_sftp()
        sftp.put(task.zip_file_path, self.working_directory + task.zip_filename)
        command = self.working_directory + 'engine_script.sh ' + str(task.id) + ' ' + str(self.engine_id)
        threading.Thread(target=engine_exec_command_handler, args=(self.client, command)).start()
        


    def connect(self, username, userpass):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(hostname=self.address, username=username, password=userpass)
        except:
            print 'ERROR in connection to engine ' + self.address
            self.status = 'off'

    def disconnect(self):
        self.client.close()


def engine_exec_command_handler(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    for line in stderr:
        print line