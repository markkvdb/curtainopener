import sched, time

variableDict = {'curtain_open': False, 'job_scheduler': sched.scheduler(time.time, time.sleep)}
