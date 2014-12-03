from django.conf.urls import patterns, include, url

from django.contrib import admin
from Studiereis import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Studiereis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': 'http://skoener.student.utwente.nl/StudiereisApps/karma/login/?next=/StudiereisApps/karma/'}, name='logout'),
    url(r'^karma/', include('karma.urls', namespace='karma')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^/$', views.index, name='index'),
    url(r'^password/$', 'django.contrib.auth.views.password_change', {'post_change_redirect' : '/StudiereisApps/karma/'}, name="passwd"),
    url(r'^$', views.index, name='index')
    # url(r'^polls/', include('polls.urls', namespace='polls')),
)
