import pytest
import pytz
from mixer.backend.django import mixer
from roadmap.models import Task, Roadmap, Score
from datetime import datetime, date, time, timedelta
from django.utils import timezone
from freezegun import freeze_time
from itertools import chain
from pytest_django.fixtures import db

utc = pytz.UTC
pytestmark = pytest.mark.django_db


class TestRoadmap:
    @pytest.fixture
    def roadmap_ex(self, db):
        roadmap = mixer.blend(Roadmap)
        return roadmap

    @pytest.fixture
    def filtered_tasks(self, db, roadmap_ex):
        tasks = mixer.cycle(2).blend(Task, roadmap=roadmap_ex)
        tasks[0].state = 'ready'
        tasks[0].title = 'ready task'
        tasks[0].save()
        tasks[1].state = 'in_progress'
        tasks[1].title = 'in_progress task'
        tasks[1].save()

        return tasks

    @pytest.fixture
    def today_tasks(self, db, roadmap_ex):
        today_tasks = mixer.cycle(2).blend(Task, estimate=date.today(), state='in_progress', roadmap=roadmap_ex)
        return today_tasks

    def test_roadmap_today_method(self, roadmap_ex, today_tasks):
        model_today_tasks = roadmap_ex.today()
        assert model_today_tasks[0].estimate == today_tasks[0].estimate

    def test_roadmap_filter(self, roadmap_ex, filtered_tasks):
        model_filtered_tasks = roadmap_ex.filter(state='ready')
        assert filtered_tasks[0] == model_filtered_tasks[0]

    def test_roadmap_str_representation(self, roadmap_ex):
        assert roadmap_ex.name == roadmap_ex.__str__()


class TestTask:
    @pytest.fixture
    def task_ex(self, db):
        task = mixer.blend(Task, state = "in_progress")
        task.estimate = datetime(1900, 1, 1, tzinfo=utc)
        task.save()
        return task

    @pytest.fixture
    def task_crit(self, db):
        task = mixer.blend(Task, state = "in_progress")
        task.estimate = datetime(2012, 1, 3, tzinfo=utc)
        task.save()
        return task

    @pytest.fixture
    def tasks_ex(self, db):
        tasks = mixer.cycle(2).blend(Task)
        tasks[0].state = 'ready'
        tasks[0].title = 'ready task'
        tasks[0].save()
        tasks[1].state = 'in_progress'
        tasks[1].title = 'in_progress task'
        tasks[1].save()
        return tasks

    def test_roadmap_str_representation(self, task_ex):
        assert task_ex.title == task_ex.__str__()

    def test_task_remaining(self, tasks_ex):
        assert tasks_ex[0].remaining == timedelta(0)
        with freeze_time("2020-01-14"):
            assert tasks_ex[1].remaining == tasks_ex[1].estimate - timezone.now()

    def test_task_is_failed(self, task_ex):
        assert task_ex.is_failed is True

    def test_task_is_crit(self, task_ex, task_crit):
        with freeze_time("2012-1-2"):
            assert task_ex.is_crit is True
            assert task_crit.is_crit is True


class TestScore:
    @pytest.fixture
    def score_ex(self, db):
        score = mixer.blend(Score)
        return score

    def test_score_str_representation(self, score_ex):
        assert score_ex.__str__() == 'Score for ' + score_ex.task.title

