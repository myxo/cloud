from BaseHTTPServer import BaseHTTPRequestHandler

import time
import socket
import cgi

def send_task(task_name): # http server + socket at one machine... yeah...
    # print time.strftime("[ %H:%M:%S ] ") + 'send task ' + task_name
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('i am rock')
    sock.send(task_name)
    sock.close()


class ClientHTTPListener(BaseHTTPRequestHandler):
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
        open("/home/myxo/univer/cloud/tmp_tasks/%s"%filename, "wb").write(data)
        send_task("/home/myxo/univer/cloud/tmp_tasks/%s"%filename)
        self.send_response(200)
        # self.taskpool.add_new_task(filename)