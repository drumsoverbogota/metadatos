from django.conf.urls import patterns, include, url
from corpus import views


urlpatterns = patterns('',
    url(r'^$', 'corpus.views.index' , name='index'),
    url(r'^create/', 'corpus.views.create', name='create'),
    url(r'^delete/', 'corpus.views.delete', name='delete'),
    url(r'^tags/', 'corpus.views.tags', name='tags'),
    url(r'^tags_add/', 'corpus.views.tags_add', name='tags_add'),
    url(r'^tags_delete/', 'corpus.views.tags_delete', name='tags_delete'),                       
)
