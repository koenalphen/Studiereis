from django.conf.urls import patterns, url

from karma import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<person_name>\w+)/$', views.personView, name='personView'),
    url(r'^committee/(?P<committeeName>\w+)/$', views.committeeView, name='committeeView'),
    url(r'^(?P<person_name>\w+)/addTask/$', views.addTask, name='addTask')
)