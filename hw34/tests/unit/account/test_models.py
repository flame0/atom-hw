import pytest
from mixer.backend.django import mixer
from account.models import User

pytestmark = pytest.mark.django_db


class TestUser:
    def test_full_name(self):
        obj = mixer.blend('account.User', first_name='Bob', last_name='Big')
        assert obj.get_full_name() == 'Bob Big', "Should be first name + space + last name"

    def test_short_name(self):
        obj = mixer.blend('account.User', first_name='Bob')
        assert obj.get_short_name() == 'Bob', "Should be first name"
