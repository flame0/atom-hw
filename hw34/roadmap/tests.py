from django.test import TestCase
from .models import Task,Roadmap,Score
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Create your tests here.

# тестирование функций set_score
# тестирование функций is_crit
# тестирование функций is_failed


class TestTaskMethod(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'user@test.net', 'secret')
        self.road = Roadmap.objects.create(name='testroadmap', account=self.user.account)
        self.road.task_set.create(title="task1", estimate=timezone.now()-timedelta(1))
        self.road.task_set.create(title="task2", estimate=timezone.now()+timedelta(1))
        self.road.task_set.create(title="task3", estimate=timezone.now()+timedelta(12))

    def test_is_failed_method(self):
        self.assertEqual(self.road.task_set.get(title='task1').is_failed, True)
        self.assertEqual(self.road.task_set.get(title='task2').is_failed, False)

    def test_is_crit(self):
        self.assertEqual(self.road.task_set.get(title='task1').is_crit, True)
        self.assertEqual(self.road.task_set.get(title='task2').is_crit, True)
        self.assertEqual(self.road.task_set.get(title='task3').is_crit, False)

    def test_remaining(self):
        self.assertEqual(self.road.task_set.get(title='task1').remaining, timedelta(-1))
        self.assertEqual(self.road.task_set.get(title='task2').remaining, timedelta(1))

    def tearDown(self):
        self.user.delete()