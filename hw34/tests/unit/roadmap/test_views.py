import pytest
import pytz
import datetime

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from roadmap import views
from account.models import User
from roadmap.models import Task, Roadmap

pytestmark = pytest.mark.django_db
utc = pytz.UTC


class TestRoadmapViews:
    @pytest.fixture
    def user(self, db):
        user = mixer.blend(User)
        return user

    @pytest.fixture
    def roadmap(self, db, user):
        roadmap = mixer.blend(Roadmap, user=user)
        return roadmap

    @pytest.fixture
    def task(self, db, roadmap):
        task = mixer.blend(Task, roadmap=roadmap)
        return task

    def test_roadmaps_show_by_anonymous(self):
        request = RequestFactory().get('/roadmaps/')
        request.user = AnonymousUser()
        response = views.roadmaps_show(request)
        assert response.status_code == 302

    def test_roadmaps_show_by_authenticated(self, user):
        request = RequestFactory().get('/roadmaps/')
        request.user = user
        response = views.roadmaps_show(request)
        assert response.status_code == 200

    def test_roadmap_detail_by_anonymous(self):
        request = RequestFactory().get('/roadmaps/1')
        request.user = AnonymousUser()
        response = views.roadmap_detail(request, 1)
        assert response.status_code == 302

    def test_roadmap_detail_by_authenticated(self, user, roadmap):
        request = RequestFactory().get('/roadmaps/' + str(roadmap.id))
        request.user = user
        response = views.roadmap_detail(request, roadmap.id)
        assert response.status_code == 200

    def test_roadmap_delete(self, user, roadmap):
        request = RequestFactory().get('/roadmaps/' + str(roadmap.id) + 'delete')
        request.user = user
        response = views.roadmap_delete(request, roadmap.id)
        r = Roadmap.objects.filter(pk=roadmap.id)
        assert response.status_code == 302
        assert not r

    def test_task_detail_by_authenticated(self, user, task):
        request = RequestFactory().get('/task/' + str(task.id))
        request.user = user
        response = views.task_detail(request, task.id)
        assert response.status_code == 200

    def test_task_delete(self, user, task):
        request = RequestFactory().get('/task/' + str(task.id) + 'delete')
        request.user = user
        response = views.task_delete(request, task.id)
        t = Task.objects.filter(pk=task.id)
        assert response.status_code == 302
        assert not t

    def test_task_update_get(self, task, user):
        request = RequestFactory().get('/task/' + str(task.id) + '/edit')
        request.user = user
        response = views.task_update(request, task.id)
        assert response.status_code == 200

    def test_task_new_get(self, roadmap, user):
        request = RequestFactory().get('/roadmaps/' + str(roadmap.id) + '/task_new')
        request.user = user
        response = views.task_new(request, roadmap.id)
        assert response.status_code == 200

    def test_roadmap_stats_get(self, user):
        request = RequestFactory().get('/roadmaps/stats')
        request.user = user
        response = views.roadmap_stats(request)
        assert response.status_code == 200

    def test_task_update_post(self, task, user):
        data = {'title': 'tested', 'estimate': datetime.datetime(2100, 1, 1, tzinfo=utc), 'state': 'in_progress'}
        request = RequestFactory().post('/task/' + str(task.id) + '/edit/', data=data)
        request.user = user
        request.method = 'POST'
        response = views.task_update(request, task.id)
        assert response.status_code == 200
        task.refresh_from_db()

