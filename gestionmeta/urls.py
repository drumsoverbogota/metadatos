from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    url(r'^$', 'subida.views.index'),
    url(r'^login/', 'subida.views.login'),                       
    url(r'^update/', 'subida.views.update'),
    url(r'^delete/', 'subida.views.delete'),
    url(r'^corpus/', include('corpus.urls')),
    url(r'^archivos/', include('archivos.urls')),
)