import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from hw2.parser import get_dataset
from hw1.task import Roadmap, Task


class WSGIApplication(object):

    default_headers = [
        ('Content-Type', 'text/html; charset=utf8'),
        ('Server', 'WSGIExample/1.0'),
    ]

    def __init__(self, environment, start_response_callback):
        self.environment = environment
        self.start_response = start_response_callback

    @property
    def params(self):
        params = getattr(self, '_params', None)
        if not params:
            query_string = self.environment.get('QUERY_STRING', '')
            params = {
                key: value if len(value) > 1 else value[0]
                for key, value in parse_qs(query_string).items()
            }
            setattr(self, '_params', params)
        return params

    def __iter__(self):
        self.start_response('200 OK', self.default_headers)
        tasks = []
        for data in get_dataset("dataset.yml"):
            tasks.append(Task(data[0], data[2], data[1]))
        road = Roadmap(tasks)
        greetings = ""
        for task in road.crit():
            greetings += "<li><b>{}</b>({}) - <date>{}</date></li>".format(
                task.title, task.state, task.estimate)
        yield greetings.encode('utf-8')

http_server = make_server('127.0.0.1', 9090, WSGIApplication)
http_server.handle_request()
