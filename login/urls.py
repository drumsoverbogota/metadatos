from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    url(r'^$', 'login.views.index'),
    url(r'^login/', 'login.views.login'),
    url(r'^logout/', 'login.views.logout'),
    url(r'^create/', 'login.views.create',name='create_user'),
    url(r'^create_user/', 'login.views.create_user'),
    url(r'^delete_user/', 'login.views.delete_user'),                       
    url(r'^init/', 'login.views.init'),                         
)