from django.conf.urls import patterns, include, url



urlpatterns = patterns('',
    url(r'^$', 'login.views.index'),
    url(r'^index/', 'subida.views.index',name='index'),
    url(r'^importar/', 'subida.views.importar'),
    url(r'^importar_b/', 'subida.views.importar_b'),                       
    url(r'^corpus/', include('corpus.urls')),
    url(r'^archivos/', include('archivos.urls')),
    url(r'^login/', include('login.urls')),
)