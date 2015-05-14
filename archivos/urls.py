from django.conf.urls import patterns, include, url
from corpus import views


urlpatterns = patterns('',
    url(r'^$', 'archivos.views.index' , name='index'),
    url(r'^listar/', 'archivos.views.listar' , name='listar'),
    url(r'^crear/', 'archivos.views.crear' , name='crear'),
    url(r'^guardar/', 'archivos.views.guardar' , name='guardar'),
    url(r'^guardar_s/', 'archivos.views.guardar_s' , name='guardar'),
    url(r'^add_s/', 'archivos.views.add_s' , name='guardar'),
    url(r'^editar/', 'archivos.views.editar' , name='editar'),
    url(r'^borrar/', 'archivos.views.borrar' , name='borrar'),
)
