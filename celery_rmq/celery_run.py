


from celery import Celery

app = Celery('celery_rmq',
             broker='amqp://guest:guest@localhost:5672/',
             backend='rpc://',
             include=['tasks'])
