import sys
import requests
import json

def get_engine_config():
    config = {}
    try:
        f = open('../engine_config', 'r')
        config = json.load(f)
        f.close
    except:
        config['master_url'] = 'http://localhost:8889'
        with open('../engine_config', 'w') as f:
            json.dump(config, f)
    return config

if __name__ == '__main__':
    filename    = sys.argv[1]
    task_id     = sys.argv[2]
    engine_id   = sys.argv[3]
    task_status = sys.argv[4]

    task_status_str = 'done' if int(task_status) == 0 else 'time'

    request_content = {}
    request_content['request_type']     = 'task_done'
    request_content['file']             = open(filename, 'rb')
    request_content['task_id']          = task_id
    request_content['engine_id']        = engine_id
    request_content['task_status']      = task_status_str

    engine_config = get_engine_config()
    url = engine_config['master_url']

    requests.post(url, files=request_content)
