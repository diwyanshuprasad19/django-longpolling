from celery import shared_task
import time

@shared_task
def timeout(message, t):
    time.sleep(t)
    return message
