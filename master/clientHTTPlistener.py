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
            self.send_response(200)

            task = Task(file_abs_path)
            lock = threading.Lock()
            lock.acquire()
            self.taskpool.add_new_task(task)
            lock.release()

    return ClientHTTPListener