import zipfile
import json

class Task:
    def __init__(self, path_to_task):
        archive = zipfile.ZipFile(path_to_task, 'r')
        config_str = archive.read('task_configuration')
        self.config = json.loads(config_str)

        self.core_require   = self.config['core_require']
        self.timeout        = self.config['timeout']
        self.id             = self.config['id']

        self.zip_file_path = path_to_task
        self.zip_filename = str(self.id) + '.zip'
