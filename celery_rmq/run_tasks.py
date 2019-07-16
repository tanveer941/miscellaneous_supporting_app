"""
 1. Start RabbitMQ server at C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin\rabbitmq-server.bat start
    Running RabbitMQ server on http://localhost:15672
 2. Run celery in the terminal celery -A tsk_que worker --loglevel=info
    celery -A celery_run worker --loglevel=info

 3. Use flower to check this in real time
      celery -A celery_run flower
      http://localhost:5555
 4. Run run_tasks.py

"""

# celery -A celery_rmq worker --loglevel=info
# celery -A celery_run worker --loglevel=info

from tasks import longtime_add
import time

if __name__ == '__main__':
    result = longtime_add.delay(7, 5)
    # at this time, our task is not finished, so it will return False
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result
    # sleep 10 seconds to ensure the task has been finished
    time.sleep(5)
    # now the task should be finished and ready method will return True
    print 'Task finished? ', result.ready()
    print 'Task result: ', result.result