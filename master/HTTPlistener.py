from BaseHTTPServer import BaseHTTPRequestHandler

import cgi
import threading
import urlparse
import os
import zipfile

from task import Task
from utils import *


def httpServerFactory(init_args):
    class HTTPListener(BaseHTTPRequestHandler, object):
        def __init__(self, *args, **kwargs):
            self.taskpool = init_args['taskpool']
            self.file_storage = '../tmp_tasks/'
            super(HTTPListener, self).__init__(*args, **kwargs)


        def do_GET(self):
            url_splited = urlparse.urlsplit(self.path)
            path = url_splited.path
            args = urlparse.parse_qs(url_splited.query)



            if path == '/statusjson' or path == '/statusjson/':
                self.send_response(200)
                self.send_header('content-type','text/json')
                self.end_headers()
                self.wfile.write(self.taskpool.json_info())

            elif path == '/status' or path == '/status/':
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(open('status.html', 'rb').read())
            



            elif path == '' or path == '/':
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write('hello =)\n\n')
            



            elif path == '/task_status' or path == '/task_status/':
                if 'task_id' not in args:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("you should write propper task_id")
                    return

                task_id = int(args['task_id'][0])
                if task_id not in self.taskpool.alltask:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("there is no task with %d id"%task_id)
                    return

                task_status = self.taskpool.alltask[task_id].status
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(task_status)


            elif path == '/task_full_status' or path == '/task_full_status/':
                if 'task_id' not in args:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("you should write propper task_id")
                    return

                task_id = int(args['task_id'][0])
                if task_id not in self.taskpool.alltask:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("there is no task with %d id"%task_id)
                    return

                task_status = self.taskpool.alltask[task_id].get_status()
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(task_status)


            elif path == '/task_result' or path == '/task_result/':
                if 'task_id' not in args:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("you should write propper task_id")
                    return

                task_id = int(args['task_id'][0])
                if task_id not in self.taskpool.alltask:
                    self.send_response(400)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write("there is no task with %d id"%task_id)
                    return

                task_status = self.taskpool.alltask[task_id].status
                if task_status == 'done':
                    basename = str(task_id) + '_result.zip'
                    filename = self.file_storage + basename

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/zip')
                    self.send_header('Content-Length', os.path.getsize(filename))
                    self.send_header('Content-Disposition', 'attachment;'
                        'filename="%s"' % basename)
                    self.send_header('Filename', basename)
                    
                    self.end_headers()
                    self.wfile.write(open(filename, 'rb').read())
                else:
                    self.send_response(200)
                    self.send_header('content-type','text/html')
                    self.end_headers()
                    self.wfile.write(task_status)
                

            else:
                self.send_response(404)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write('0_o\n\n')

        def do_POST(self):
            form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                             })

            try:
                filename    = form['file'].filename
                data        = form['file'].file.read()
            except:
                self.send_response(400)
                return
            
            file_abs_path = self.file_storage + "%s"%filename
            open(file_abs_path, "wb").write(data)


            try:
                request_type = form['request_type'].value
            except:
                self.send_response(400)
                return

            lock = threading.Lock()
            if request_type == 'new_task':
                task = Task(file_abs_path)
                lock.acquire()
                self.taskpool.add_new_task(task)
                lock.release()

            elif request_type == 'task_done':
                task_id     = int(form['task_id'].value)
                engine_id   = int(form['engine_id'].value)
                task_status = form['task_status'].value
                # lock.acquire()
                self.taskpool.task_done(task_id, task_status, engine_id)
                # lock.release()
                

            self.send_response(200)

        def log_message(self, format, *args):
            LOGFILE = 'http.log'
            open(LOGFILE, "a").write("%s - - [%s] %s\n" % (self.address_string(),
                        self.log_date_time_string(),
                        format%args))

    return HTTPListener
