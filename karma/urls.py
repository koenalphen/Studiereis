from django.conf.urls import patterns, url

from karma import views

urlpatterns = patterns('',
    url(r'^$', views.karmaHome, name='karmaHome'),
    url(r'^participants$', views.index, name='index'),
    url(r'^(?P<person_id>\d+)/$', views.personView, name='personView'),
    url(r'^committee/(?P<committeeName>\w+)/$', views.committeeView, name='committeeView'),
    url(r'^(?P<person_id>\w+)/addTask/$', views.addTask, name='addTask'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^removelog/$', views.removeTask, name='removeTask'),
    url(r'^yousuck/$', views.yousuck, name='yousuck'),
    url(r'^overview.pdf$', views.overviewgenpdf, name='overviewgenpdf'),
)
