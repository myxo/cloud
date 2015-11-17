import time
import sys
import psutil
import json
import os


start_time = time.time()
timeout = 0
with open('task_configuration', 'r') as f:
    timeout = json.load(f)['timeout']

pid = int(sys.argv[1])

if not os.path.isdir('result'):
    if os.path.exists('result'):
        os.remove('result')
    os.makedirs('result')

while 1:
    if not psutil.pid_exists(pid):
        sys.exit(0)

    if time.time() - start_time > timeout:
        sys.exit(1)

    time.sleep(1)

