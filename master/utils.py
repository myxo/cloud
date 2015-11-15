import time
from termcolor import colored

def print_message(message, color=None):
    s = time.strftime("[ %H:%M:%S ] ") + message
    print colored(s, color)


class Queue:
    def __init__(self):
        self.list = []

    def put(self, obj):
        self.list.append(obj)

    def empty(self):
        return len(self.list) == 0

    def get(self):
        try :
            obj = self.list[0]
            del self.list[0]
            return obj
        except:
            print "ERROR in Queue: there is no element"
            return None

    def head(self):
        try:
            return self.list[0]
        except:
            print "ERROR in Queue: there is no element"
            return None

    def get_list(self):
        return [x for x in self.list]