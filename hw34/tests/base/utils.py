import contextlib

import mock
from django.contrib import auth


class AuthBackend(object):
    _user = None

    def authenticate(self, request):
        if self._user:
            return self._user

    @classmethod
    def set(cls, user):
        cls._user = user

    @classmethod
    def clear(cls):
        cls._user = None


class AuthMiddleware(object):
    def process_request(self, request):
        user = auth.authenticate(request=request)
        if user:
            request.user = user


@contextlib.contextmanager
def authenticate(_user):
    """
    Context manager for resource tests that makes necessary patches to make
    all requests authenticated.
    """
    if not _user:
        # no user is supplied - no mocking
        yield
        return

    def auth_with_user(*credentials):
        """
        Patch that authenticates requests for the specified user.
        """
        return _user

    with mock.patch('mcalendar.auth.backends.CalDAVBasicAuthBackend.authenticate', auth_with_user):
        with mock.patch('mcalendar.auth.backends.SwaSessionBackend.authenticate', auth_with_user):
            yield
