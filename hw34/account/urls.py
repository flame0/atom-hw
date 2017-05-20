from django.conf.urls import url
from .views import LoginFormView, RegisterFormView, LogoutView, UserChangeFormView
from .views import change_password, profile_view
app_name = 'account'

urlpatterns = [
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^signup/$', RegisterFormView.as_view(), name='reg'),
    url(r'^password/$', change_password, name='change_pass'),
    url(r'^change-info/$', UserChangeFormView.as_view(), name='change_user'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', profile_view, name='profile'),

]