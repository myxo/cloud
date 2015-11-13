from BaseHTTPServer import BaseHTTPRequestHandler

import cgi
import threading

from task import Task


def httpServerFactory(init_args):
    class ClientHTTPListener(BaseHTTPRequestHandler, object):
        def __init__(self, *args, **kwargs):
            self.taskpool = init_args['taskpool']
            super(ClientHTTPListener, self).__init__(*args, **kwargs)


        def do_GET(self):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            self.wfile.write("hello !\nWrong way =))")

        def do_POST(self):
            form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                             'CONTENT_TYPE':self.headers['Content-Type'],
                             })

            
            filename    = form['file'].filename
            data        = form['file'].file.read()
            file_abs_path = "/home/myxo/univer/cloud/tmp_tasks/%s"%filename
            open(file_abs_path, "wb").write(data)


            request_type = form['request_type'].value
            lock = threading.Lock()
            print 'checkpoint (' + request_type + ')'
            if request_type == 'new_task':
                task = Task(file_abs_path)
                lock.acquire()
                self.taskpool.add_new_task(task)
                lock.release()

            elif request_type == 'task_done':
                task_id     = int(form['task_id'].value)
                engine_id   = int(form['engine_id'].value)
                task_status = form['task_status'].value
                lock.acquire()
                self.taskpool.task_done(task_id, task_status, engine_id)
                lock.release()
                

            self.send_response(200)


    return ClientHTTPListener