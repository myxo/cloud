import numpy.random
import os
import zipfile
import json

class Task:
    def __init__(self, path_to_task_folder):
        self.path_to_task_folder = path_to_task_folder
        self.read_config_from_file()

        self.core_require = self.config['core_require']
        self.timeout = self.config['timeout']
        self.id = self.config['id']
        self.zip_file_path = ''
        self.zip_filename = str(self.id) + '.zip'

        self.zip()

    def read_config_from_file(self):
        try:
            f = open(self.path_to_task_folder + '/task_configuration', 'r')
            self.config = json.load(f)
            f.close()
        except:
            self.set_default_config()

    def set_default_config(self):
        self.config = {}
        self.config['id'] = numpy.random.randint(1e15)
        self.config['core_require'] = 1
        self.config['timeout'] = 30

        f = open(self.path_to_task_folder + '/task_configuration', 'w')
        json.dump(self.config, f)
        f.close()

    def zip(self):
        folder = self.path_to_task_folder
        zipname = folder + '/' + self.zip_filename
        self.zip_file_path = os.path.abspath(zipname)
        if os.path.isfile(self.zip_file_path):
            return

        zipf = zipfile.ZipFile(zipname, 'w')
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file == (str(self.id) + '.zip'):
                    continue

                absolute_filename = os.path.join(root, file)
                zip_filename = absolute_filename[len(folder)+len(os.sep):]
                zipf.write(absolute_filename, zip_filename) # hack, remove folder name
        zipf.close()

