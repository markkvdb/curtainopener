import threading, queue

variableDict = {'curtain_open': False, 'job_queue': queue.PriorityQueue(), 'event': threading.Event()}
