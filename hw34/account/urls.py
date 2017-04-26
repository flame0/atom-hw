from django.conf.urls import url
from .forms import LoginFormView, RegisterFormView
from .views import profile
app_name = 'account'

urlpatterns = [
    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^signup/$', RegisterFormView.as_view(), name='reg'),
    url(r'^profile/$', profile, name='profile'),
]