# coding: utf-8
import os
import sys
import pytest

from django.conf import settings

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(BASE_DIR, 'todo'))

from tests.base.mocks.date import DatetimeMock
from tests.base.modules.client import HttpClientModule


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'hw3.settings'

    settings.DATABASES['default'] = settings.TEST_DATABASES[os.environ.get('DJANGO_TEST_DATABASE', 'default')]

    settings.DEBUG = False

    # settings.AUTHENTICATION_BACKENDS = ['tests.base.utils.AuthBackend']
    # settings.MIDDLEWARE += ['tests.base.utils.AuthMiddleware']
    # settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


@pytest.fixture()
def http():
    return HttpClientModule()


@pytest.fixture()
def models(db):
    from tests.base.modules.model import ModelModule
    return ModelModule()


# @pytest.yield_fixture(scope='session', autouse=True)
# def mocks():
#     _mocks = [DatetimeMock()]
#     for mock in _mocks:
#         mock.start()
#     yield
#     for mock in _mocks:
#         mock.stop()
