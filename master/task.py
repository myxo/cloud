import zipfile
import json
import time
# import threading

class Task:
    def __init__(self, path_to_task):
        archive = zipfile.ZipFile(path_to_task, 'r')
        config_str = archive.read('task_configuration')
        self.config = json.loads(config_str)
        archive.close()

        self.core_require   = self.config['core_require']
        self.timeout        = self.config['timeout']
        self.id             = self.config['id']

        self.zip_file_path  = path_to_task
        self.zip_filename   = str(self.id) + '.zip'
        self.zip_result_filename = str(self.id) + '_result.zip'

        # self.done_event = threading.Event()
        self.status = 'waiting'
        self.engine_id = None

        self.stderr = ''
        self.stdout = ''

        self.time_arrive = time.localtime()
        self.time_send = None
        self.time_done = None

        self.status_init()

    def status_init(self):
        self.st = {}
        self.st['core_require'] = self.core_require
        self.st['timeout']      = self.timeout
        self.st['id']           = self.id

    def get_status(self):
        self.st['status']       = self.status
        self.st['engine_id']    = self.engine_id

        ta = self.time_arrive
        self.st['time_arrive']  = {'sec': ta.tm_sec, 'min': ta.tm_min, 'hour':ta.tm_hour, 
                                    'day':ta.tm_mday, 'mon':ta.tm_mon, 'year':ta.tm_year}

        ts = self.time_send
        if ts != None:
            self.st['time_send']  = {'sec': ts.tm_sec, 'min': ts.tm_min, 'hour':ts.tm_hour, 
                                    'day':ts.tm_mday, 'mon':ts.tm_mon, 'year':ts.tm_year}

        td = self.time_done
        if td:
            self.st['time_done']  = {'sec': td.tm_sec, 'min': td.tm_min, 'hour':td.tm_hour, 
                                    'day':td.tm_mday, 'mon':td.tm_mon, 'year':td.tm_year}

        return json.dumps(self.st)
