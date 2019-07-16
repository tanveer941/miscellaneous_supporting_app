

from celery_run import app
import time


@app.task
def longtime_add(x, y):
    print 'long time task begins'
    # sleep 5 seconds
    time.sleep(10)
    print 'long time task finished'
    return x + y*25544964