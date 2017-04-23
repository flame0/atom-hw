"""hw3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^task/(?P<pk>\d+)/$', views.task_detail, name='task'),
#    url(r'^task/new/$', views.task_new, name='task_new'),
    url(r'^task/(?P<pk>\d+)/edit/$', views.task_update, name='task_edit'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),
    url(r'^roadmaps/$', views.roadmaps_show, name='roadmaps'),
    url(r'^roadmaps/(?P<pk>\d+)/$', views.roadmap_detail, name='roadmap'),
    url(r'^roadmaps/new/$', views.roadmap_new, name='roadmap_new'),
    url(r'^roadmaps/(?P<pk>\d+)/delete/$', views.roadmap_delete, name='roadmap_delete'),
    url(r'^roadmaps/(?P<pk>\d+)/task_new/$', views.task_new, name='task_new'),
]
