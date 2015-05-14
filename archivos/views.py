from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.template.defaulttags import register



from corpus.models import *
from archivos.models import *
from archivos.forms import UploadFileForm

import uuid
import os

DIR_FILES = '/Users/sergiomancera/Archivos/'

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):

    corp = ModeloCorpus.objects
    return render_to_response('archivos/index.html', {'Corpus': corp},
                              context_instance=RequestContext(request))

def listar(request):

    id = eval("request." + request.method + "['m_id']")
    mod = ModeloCorpus.objects(id=id)[0]
    sesiones = Sesiones.objects(corpus=mod)
    anidados = Anidados.objects(corpus=mod)
    
    subtags = Tag.objects(corpus=mod)
    params = {'m_id' : id , 'sesiones': sesiones, 'anidados' : anidados, 'tags': mod.tags, 'tagsf': mod.tags_f, 's_tags': subtags }
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))

def crear(request):

    id = request.POST['m_id']
    mod = ModeloCorpus.objects(id=id)[0]
    if request.POST.get('subtag',False) is False:
        tags = mod.tags
        tags_f = mod.tags_f
        params = {'m_id' : id , 'tags' : tags, 'tags_f' : tags_f}
        template = 'archivos/create.html'
    else:
        t_id = request.POST['subtag']
        s_id = request.POST['s_id']

        subtag = Tag.objects(id=t_id)[0]
        tags = subtag.tags
        tags_f = subtag.tags_f
        anidados = Anidados.objects(ref=subtag)

        params = {'m_id' : id ,'t_id': t_id, 's_id':s_id, 'tags' : tags, 'tags_f' : tags_f,'anidados': anidados,'nombre':subtag.main_tag}
        template = 'archivos/create_s.html'
    return render_to_response(template,params,
                              context_instance=RequestContext(request))

def guardar(request):

    id = request.POST['m_id']
    mod = ModeloCorpus.objects(id=id)[0]
    tags = mod.tags
    tags_f = mod.tags_f
    subtags = Tag.objects(corpus=mod)
    d = {}
    
    for etiqueta in tags:
        d[etiqueta] = request.POST.get(etiqueta,False)

    sesion = Sesiones(tags=d,corpus=mod)
    sesion.save()
    
    
    sesiones = Sesiones.objects(corpus=mod)
    anidados = Anidados.objects(corpus=mod)
    
    params = {'m_id' : id , 'sesiones': sesiones,'anidados': anidados , 'tags': tags, 'tagsf': tags_f, 's_tags': subtags }
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))

def guardar_s(request):
    
    id = request.POST['m_id']
    s_id = request.POST['s_id']
    t_id = request.POST['t_id']


    mod = ModeloCorpus.objects(id=id)[0]
    subtag = Tag.objects(id=t_id)[0]
    sesion = Sesiones.objects(id=s_id)[0]
    
    tags = subtag.tags
    tags_f = subtag.tags_f
    
    d = {}
    
    for etiqueta in tags:
        d[etiqueta] = request.POST.get(etiqueta,False)

    anidado = Anidados(ref=subtag,tags=d,corpus=mod)
    anidado.save()
    
    if subtag.nombre not in sesion.refa.keys():
        sesion.refa[subtag.nombre] = []
    sesion.refa[subtag.nombre].append(anidado.id)


    sesion.save()

    sesiones = Sesiones.objects(corpus=mod)
    subtags = Tag.objects(corpus=mod)
    anidados = Anidados.objects(corpus=mod)

    tags = mod.tags
    tags_f = mod.tags_f
    params = {'m_id' : id , 'sesiones': sesiones,'anidados':anidados, 'tags': tags, 'tagsf': tags_f, 's_tags': subtags }
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))


def add_s(request):
    
    id   = request.GET['m_id']
    a_id = request.GET['a_id']
    s_id = request.GET['s_id']
    t_id = request.GET['t_id']

    mod = ModeloCorpus.objects(id=id)[0]
    subtag = Tag.objects(id=t_id)[0]
    sesion = Sesiones.objects(id=s_id)[0]
    anidado = Anidados.objects(id=a_id)[0]
    
    tags = subtag.tags
    tags_f = subtag.tags_f
    
    if subtag.nombre not in sesion.refa.keys():
        sesion.refa[subtag.nombre] = []
    if anidado.id not in sesion.refa[subtag.nombre]:
        sesion.refa[subtag.nombre].append(anidado.id)


    sesion.save()
    
    sesiones = Sesiones.objects(corpus=mod)
    subtags = Tag.objects(corpus=mod)
    anidados = Anidados.objects(corpus=mod)
    tags = mod.tags
    tags_f = mod.tags_f
    params = {'m_id' : id , 'sesiones': sesiones,'anidados':anidados, 'tags': tags, 'tagsf': tags_f, 's_tags': subtags }
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))




def editar(request):
    if request.method == 'GET':
        a_id = eval("request." + request.method + "['a_id']")
        c_id = eval("request." + request.method + "['m_id']")
        
        arch = Sesiones.objects(id=a_id)[0]
        mod = ModeloCorpus.objects(id=c_id)[0]
        tags = mod.tags
        
        params = {'arch': arch, 'tags': tags, 'm_id': c_id}
        temp = 'archivos/edit.html'
            
    elif request.method == 'POST':
        
        a_id = request.POST['a_id']
        c_id = request.POST['m_id']

        arch = Sesiones.objects(id=a_id)[0]
        mod = ModeloCorpus.objects(id=c_id)[0]
        subtags = Tag.objects(corpus=mod)
        tags = mod.tags

        d = {}
        for etiqueta in tags:
            d[etiqueta] = request.POST.get(etiqueta,False)
        
        arch.tags = d
        arch.save()
        
        sesiones = Sesiones.objects(corpus=mod)
        params = {'m_id' : c_id , 'sesiones': sesiones, 'tags': tags, 'tagsf': mod.tags_f, 's_tags': subtags }
        temp = 'archivos/listar.html'
    
    return render_to_response(temp,params,
                              context_instance=RequestContext(request))


def borrar(request):
    if request.method == 'GET':
        a_id = eval("request." + request.method + "['a_id']")
        m_id = eval("request." + request.method + "['m_id']")
        
        params = {'a_id': a_id, 'm_id': m_id}
        temp = 'archivos/delete.html'
    
    elif request.method == 'POST':
        
        a_id = request.POST['a_id']
        m_id = request.POST['m_id']
        
        corp = ModeloCorpus.objects(id=m_id)[0]
        archivo = Sesiones.objects(id=a_id)[0]
        tags = Tag.objects(corpus=corp)

        #delete_file(DIR_FILES+archivo.archivo)
        archivo.delete()
        
        
        mod = ModeloCorpus.objects(id=m_id)[0]
        sesiones = Sesiones.objects(corpus=mod)
        anidados = Anidados.objects(corpus=mod)
    
        subtags = Tag.objects(corpus=mod)
        params = {'m_id' : m_id , 'sesiones': sesiones, 'anidados' : anidados, 'tags': mod.tags, 'tagsf': mod.tags_f, 's_tags': subtags }
        temp = 'archivos/listar.html'

    return render_to_response(temp, params,
                              context_instance=RequestContext(request))

def delete_file(nombre):
    os.remove(nombre)

def handle_uploaded_file(f,nombre):
    with open(nombre, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)