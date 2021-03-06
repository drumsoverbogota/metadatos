from django.conf.urls import patterns, include, url
from corpus import views


urlpatterns = patterns('',
    url(r'^$', 'corpus.views.index' , name='index_m'),
    url(r'^create/', 'corpus.views.create', name='create'),
    url(r'^choose/', 'corpus.views.choose'),
    url(r'^choose_s/', 'corpus.views.choose_s'),                       
    url(r'^delete/', 'corpus.views.delete', name='delete'),
    url(r'^tags/', 'corpus.views.tags', name='tags'),
    url(r'^subtags/', 'corpus.views.subtags', name='subtags'),
    url(r'^s_subtags/', 'corpus.views.s_subtags', name='subtags'),
    url(r'^tags_add/', 'corpus.views.tags_add', name='tags_add'),
    url(r'^subtags_add/', 'corpus.views.subtags_add', name='subtags_add'),
    url(r'^s_subtags_add/', 'corpus.views.s_subtags_add', name='subtags_add'),                                              
    url(r'^tags_delete/', 'corpus.views.tags_delete', name='tags_delete'),
    url(r'^subtags_delete/', 'corpus.views.subtags_delete', name='tags_delete'),
    url(r'^s_subtags_delete/', 'corpus.views.s_subtags_delete', name='tags_delete'),
)
