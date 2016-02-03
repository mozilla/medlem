from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^exists/?$', views.exists, name='exists'),
    url(r'^employee/?$', views.employee, name='employee'),
    url(r'^in-group/?$', views.ingroup, name='in-group'),
]
