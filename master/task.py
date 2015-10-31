import numpy.random
import os
import zipfile

class Task:
    def __init__(self, path_to_task_folder):
        self.path_to_task_folder = path_to_task_folder
        self.core_require = 1
        self.timeout = 30
        self.start_time = 0
        self.id = numpy.random.randint(1e15)
        self.zip_file_path = ''
        self.zip_filename = str(self.id) + '.zip'

        self.zip()

    def read_from_file(self):
        pass

    def zip(self):
        folder = self.path_to_task_folder
        zipname = folder + '/' + self.zip_filename
        self.zip_file_path = os.path.abspath(zipname)
        zipf = zipfile.ZipFile(zipname, 'w')
        
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file == (str(self.id) + '.zip'):
                    continue

                absolute_filename = os.path.join(root, file)
                zip_filename = absolute_filename[len(folder)+len(os.sep):]
                zipf.write(absolute_filename, zip_filename) # hack, remove folder name
        zipf.close()

