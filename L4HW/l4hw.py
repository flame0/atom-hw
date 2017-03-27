from yaml import load
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from datetime import timedelta, date
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def get_dataset(filename):
    '''
    Iterator for dataset's items
    :param filename: Path to dataset's file
    :type filename: str
    :return: Dataset's items
    :raises OSError: if has problem with file
    :raises yaml.YAMLError: if has problem with format
    :raises ValueError: if has problem with content
    '''
    with open(filename, 'rt', encoding='utf-8') as input:
        package = load(input, Loader=Loader)
        dataset = package.get('dataset')
        if not isinstance(dataset, list):
            raise ValueError('wrong format')
        yield from dataset


def simple_wsgi_application(environment, start_response_callback):
    '''
    :param environment: Контекст окружения
    :type environment: dict

    :param start_response_callback: Обработчик запроса
    :type start_response_callback: callable

    :return: Тело ответа
    :rtype: iterable
    '''
    response_headers = [
        ('Content-type', 'text/html; charset=utf-8'),
    ]
    start_response_callback('200 OK', response_headers)
    return [
        b'Hello, WSGI-World!',
    ]


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
        greetings=""
        for data in get_dataset("dataset.yml"):
        	if (data[2]- date.today()<timedelta(3)) and data[2] =='in_pogress' :
        		greetings+="<li><b>{}</b>({}) - <date>{}</date></li>".format(data[0],data[1],data[2])            
        yield greetings.encode('utf-8')


http_server = make_server('127.0.0.1', 9090, WSGIApplication)
http_server.handle_request()

