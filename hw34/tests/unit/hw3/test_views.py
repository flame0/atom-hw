import pytest
from django.test import RequestFactory
from hw3.views import index


class TestIndex:
    def test_index(self):
        request = RequestFactory().get('/')
        response = index(request)
        assert response.status_code == 200
