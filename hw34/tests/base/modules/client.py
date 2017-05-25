
import json

from django.conf import settings
from django.test.client import Client, MULTIPART_CONTENT
from pyquery import PyQuery


class HttpClientModule(object):
    OCTET_STREAM = 'application/octet-stream'
    JSON = 'application/json'

    DELETE = 'DELETE'
    GET = 'GET'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'
    POST = 'POST'
    PUT = 'PUT'

    def __init__(self):
        super(HttpClientModule, self).__init__()
        self.client = Client()

    def get(self, url, data=None, content_type=OCTET_STREAM, **kwargs):
        response = self.client.get(
            url, data, content_type=content_type,
            HTTP_HOST=settings.PROJECT_HOST, **kwargs)
        response.html = self._get_html(response)
        return response

    def post(self, url, data=None, content_type=MULTIPART_CONTENT, **kwargs):
        response = self.client.post(
            url, data, content_type, HTTP_HOST=settings.PROJECT_HOST, **kwargs)
        response.html = self._get_html(response)
        return response

    def put(self, url, data=None, content_type=OCTET_STREAM, **kwargs):
        response = self.client.put(
            url, data, content_type, HTTP_HOST=settings.PROJECT_HOST, **kwargs)
        response.html = self._get_html(response)
        return response

    def delete(self, url, data='', content_type=OCTET_STREAM, **kwargs):
        response = self.client.delete(
            url, data, content_type, HTTP_HOST=settings.PROJECT_HOST, **kwargs)
        response.html = self._get_html(response)
        return response

    def get_partial(self, url, data=None, content_type=OCTET_STREAM):
        data = data or {}
        data['partial'] = 'true'
        return self.get(
            url, data, content_type, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def post_partial(self, url, data=None, content_type=MULTIPART_CONTENT):
        url = '{}?partial=true'.format(url)
        return self.post(
            url, data, content_type, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def put_partial(self, url, data=None, content_type=OCTET_STREAM):
        url = '{}?partial=true'.format(url)
        return self.put(
            url, data, content_type, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def delete_partial(self, url, data='', content_type=OCTET_STREAM):
        url = '{}?partial=true'.format(url)
        return self.delete(
            url, data, content_type, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def get_json(self, url, data=None):
        response = self.get(url, data or {})
        return response, self._parse_json_response(response)

    def post_json(self, url, data=None):
        if data is not None:
            data = json.dumps(data)
        response = self.post(url, data, self.JSON)
        return response, self._parse_json_response(response)

    def put_json(self, url, data=None):
        if data is not None:
            data = json.dumps(data)
        response = self.put(url, data, self.JSON)
        return response, self._parse_json_response(response)

    def delete_json(self, url, data=''):
        response = self.delete(url, data, self.JSON)
        return response, self._parse_json_response(response)

    def _parse_json_response(self, response):
        content = None
        if response.content:
            content = json.loads(response.content.decode('utf-8'))
        return content

    def _get_html(self, response):
        try:
            return PyQuery(response.content)
        except Exception:
            return None
