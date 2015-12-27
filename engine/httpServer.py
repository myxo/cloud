from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Timer

import json
import cgi
import subprocess
import os
import signal
import zipfile
import requests
import sys
import threading


class StoppableHTTPServer(HTTPServer):
    def serve_forever(self):
        self.stopped = False
        while not self.stopped:
            self.handle_request()

class HTTPMasterListener(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):

        self.config = {}
        try:
            f = open('engine_config', 'r')
            self.config = json.load(f)
            f.close
        except:
            self.config['master_url'] = 'http://localhost:8889'
            self.config['file_storage'] = '/home/worker/tmp/'
            with open('engine_config', 'w') as f:
                json.dump(self.config, f)

        self.file_storage = self.config['file_storage']
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)


    def do_GET(self):
        if self.path == '/kill/':
            self.send_response(200)
            self.server.stopped = True
            self.server.shitdown()
            os._exit(0)

        if self.path == '':
            self.send_header(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            self.wfile.write('=)\n\n')


    def do_POST(self):
        # print 'checkpoint'
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })

        task_id     = int(form['task_id'].value)
        engine_id   = int(form['engine_id'].value)  # FIXME do we need engine_id here???
        print task_id, engine_id
        try:
            print 'qwerty'
            filename    = form['file'].filename
            print 'file: ' , filename
            data        = form['file'].file.read()
        except:
            self.send_response(400)
            return
        
        file_abs_path = self.file_storage + "%s"%filename
        open(file_abs_path, "wb").write(data)
        self.send_response(200)

        threading.Thread(target=run_task, args=(task_id, engine_id, self.file_storage, self.config['master_url'])).start()

    def log_message(self, format, *args):
        LOGFILE = 'http.log'
        open(LOGFILE, "a").write("%s - - [%s] %s\n" % (self.address_string(),
                    self.log_date_time_string(),
                    format%args))



def run_task(task_id, engine_id, file_storage, master_url):
    os.chdir(file_storage)
    subprocess.call(['unzip -o %d.zip -d%d'%(task_id, task_id)], shell=True)
    os.chdir(file_storage + '%d/'%task_id)

    timeout = 0
    with open('task_configuration', 'r') as f:
        timeout = json.load(f)['timeout']
    subprocess.call(['chmod', '+x', 'run.sh'])

    print 'start task...'
    task_status, ret_code, stdout_value, stderr_value = run_command_with_timeout('./run.sh', timeout)
    print task_status, ret_code
    print 'done.'

    if not os.path.isdir('result'):
        if os.path.exists('result'):
            os.remove('result')
        os.makedirs('result')

    result_filename = '%d_result.zip'%task_id
    subprocess.call(['zip -r %s result/'%result_filename], shell=True)
    
    if stdout_value != '':
        with zipfile.ZipFile(result_filename, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr('stdout_', stdout_value)
    if stderr_value != '':
        with zipfile.ZipFile(result_filename, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr('stderr_', stderr_value)


    upload_result(result_filename, task_id, engine_id, task_status, master_url)
    # unzip -o  $1.zip -d$1
    # cd $1
    # chmod +x run.sh
    # ./run.sh &
    # python ../check_is_done.py $!
    # task_status=$?
    # zip -r $1_result.zip result/
    # python ../upload_result.py $1_result.zip $1 $2 $task_status




def upload_result(filename, task_id, engine_id, task_status, url):

    # task_status_str = 'done' if int(task_status) == 0 else 'time'

    request_content = {}
    request_content['request_type']     = 'task_done'
    request_content['file']             = open(filename, 'rb')
    request_content['task_id']          = str(task_id)
    request_content['engine_id']        = str(engine_id)
    request_content['task_status']      = task_status

    requests.post(url, files=request_content)

def run_command_with_timeout(cmd, timeout_sec):
    """Execute `cmd` in a subprocess and enforce timeout `timeout_sec` seconds.
 
    Return subprocess exit code on natural completion of the subprocess.
    Raise an exception if timeout expires before subprocess completes."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print proc.pid
    def kill_proc():
        print 'kill proc timer!'
        timer.expired = True
        os.killpg(proc.pid, signal.SIGTERM)
        # proc.terminate()
    
    timer = Timer(timeout_sec, kill_proc)
    timer.expired = False
    timer.start()
    stdout_value, stderr_value = proc.communicate()
    if timer.expired:
        # Process killed by timer - raise exception
        return 'timeout', proc.returncode, stdout_value, stderr_value
    # Process completed naturally - cancel timer and return exit code
    timer.cancel()
    return 'done', proc.returncode, stdout_value, stderr_value




if __name__ == '__main__':
    # print 'hello'
    try :
        port = int(sys.argv[1])
    except:
        port = 8887
    print 'start server on %d port'%port
    serv = StoppableHTTPServer(("",8887),HTTPMasterListener)
    serv.serve_forever()
    # serv.handle_request()
    # serv.shutdown()