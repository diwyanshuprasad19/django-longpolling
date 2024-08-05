# example/views.py
from django.shortcuts import render
from django.http import HttpResponse
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
import json
from .tasks import timeout
from gevent import monkey; monkey.patch_all()
from gevent.pool import Group
from gevent import Greenlet

def test(request):
    return render(request, 'test.html')

class CheckGreenlet(Greenlet):
    def __init__(self, task_id, group):
        super().__init__()
        self.task_id = task_id
        self.result = None
        self.done = False
        self.group = group
        self.task = AsyncResult(self.task_id)

        if self.task.ready():
            self.result = self.task.result
            self.done = True
        else:
            self.group.add(self)
            self.start()

    def _run(self):
        try:
            self.result = self.task.get(timeout=3)
            self.done = True
        except TimeoutError:
            pass
        finally:
            self.group.kill()

def poll(request):
    out = {'res': {}}
    ids = request.GET.get('ids')
    done = True

    if ids:
        group = Group()
        greenlets = []
        split_ids = ids.split(',')

        for task_id in split_ids:
            greenlet = CheckGreenlet(task_id, group)
            greenlets.append(greenlet)

        group.join()

        for greenlet in greenlets:
            out['res'][greenlet.task_id] = greenlet.result
            if not greenlet.done:
                done = False

        out['done'] = done

    return HttpResponse(json.dumps(out), content_type='application/json')

def trigger(request):
    timeouts = [4, 3, 2, 1]
    out = {'id': []}

    for timeout_value in timeouts:
        result = timeout.delay(f'hihi: {timeout_value}', timeout_value)
        out['id'].append(result.task_id)

    out['msg'] = 'started'
    return HttpResponse(json.dumps(out), content_type='application/json')
