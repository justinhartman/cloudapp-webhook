import os
import celery
app = celery.Celery('webhook')


# os.environ.setdefault('REDIS_URL', 'redis://127.0.0.1:6379')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'],
                CELERY_TIMEZONE='Africa/Johannesburg')


@app.task
def add(x, y):
    return x + y


def on_raw_message(body):
    print(body)
