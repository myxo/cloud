import sys
import requests


if __name__ == '__main__':
    filename    = sys.argv[1]
    task_id     = sys.argv[2]
    engine_id   = sys.argv[3]
    task_status = sys.argv[4]

    task_status_str = 'done' if int(task_status) == 0 else 'time'

    request_content = {}
    request_content['request_type']    = 'task_done'
    request_content['file']             = open(filename, 'rb')
    request_content['task_id']          = task_id
    request_content['engine_id']        = engine_id
    request_content['task_status']      = task_status_str

    requests.post('http://192.168.0.108:8889', files=request_content)
    # requests.post('http://localhost:8889', files=request_content)