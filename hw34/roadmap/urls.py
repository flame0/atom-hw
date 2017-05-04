from django.conf.urls import url
from . import views

app_name = 'roadmap'
urlpatterns = [
    url(r'^task/(?P<pk>\d+)/$', views.task_detail, name='task'),
	#url(r'^task/new/$', views.task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/edit/$', views.task_update, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),
    url(r'^roadmaps/$', views.roadmaps_show, name='roadmaps'),
    url(r'^roadmaps/(?P<pk>\d+)/$', views.roadmap_detail, name='roadmap'),
    url(r'^roadmaps/new/$', views.roadmap_new, name='roadmap_new'),
    url(r'^roadmaps/(?P<pk>\d+)/delete/$', views.roadmap_delete, name='roadmap_delete'),
    url(r'^roadmaps/(?P<pk>\d+)/task_new/$', views.task_new, name='task_new'),
    url(r'^roadmaps/stats/$', views.roadmap_stats, name='roadmap_stats'),
   ]