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

    id = eval("request." + request.method + "['id']")
    mod = ModeloCorpus.objects(id=id)[0]
    sesiones = Sesiones.objects(corpus=mod)
    anidados = Anidados.objects(corpus=mod)
    
    subtags = Tag.objects(corpus=mod)
    params = {'id' : id , 'sesiones': sesiones, 'tags': mod.tags, 'tagsf': mod.tags_f, 's_tags': subtags }
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))

def crear(request):

    id = request.POST['id']
    mod = ModeloCorpus.objects(id=id)[0]
    tags = mod.tags
    tags_f = mod.tags
    form = UploadFileForm()
    params = {'id' : id , 'tags' : mod.tags, 'tags_f' : mod.tags_f,'form': form}
    return render_to_response('archivos/create.html',params,
                              context_instance=RequestContext(request))

def editar(request):
    if request.method == 'GET':
        a_id = eval("request." + request.method + "['a_id']")
        c_id = eval("request." + request.method + "['c_id']")
        
        arch = Archivo.objects(id=a_id)[0]
        corp = ModeloCorpus.objects(id=c_id)[0]
        tags = Tag.objects(corpus=corp)
        
        params = {'arch': arch, 'tags': tags, 'c_id': c_id}
        temp = 'archivos/edit.html'
            
    elif request.method == 'POST':
        
        a_id = request.POST['a_id']
        c_id = request.POST['c_id']

        corp = ModeloCorpus.objects(id=c_id)[0]
        arch = Archivo.objects(id=a_id)[0]
        tags = Tag.objects(corpus=corp)

        d = {}
        for etiqueta in tags:
            d[etiqueta.tag] = request.POST.get(etiqueta.tag,False)
        
        arch.tags = d
        arch.save()
        
        params = {'id' : c_id , 'archivos': Archivo.objects(corpus=corp), 'tags': tags}
        temp = 'archivos/listar.html'
    
    return render_to_response(temp,params,
                              context_instance=RequestContext(request))


def borrar(request):
    if request.method == 'GET':
        a_id = eval("request." + request.method + "['a_id']")
        c_id = eval("request." + request.method + "['c_id']")
        
        params = {'a_id': a_id, 'c_id': c_id}
        temp = 'archivos/delete.html'
    
    elif request.method == 'POST':
        
        a_id = request.POST['a_id']
        c_id = request.POST['c_id']
        
        corp = ModeloCorpus.objects(id=c_id)[0]
        archivo = Archivo.objects(id=a_id)[0]
        tags = Tag.objects(corpus=corp)

        delete_file(DIR_FILES+archivo.archivo)
        archivo.delete()
        

        
        
        
        arch = Archivo.objects(corpus=corp)
        
        params = {'id' : c_id , 'archivos': arch, 'tags': tags}
        
        temp = 'archivos/listar.html'

    return render_to_response(temp, params,
                              context_instance=RequestContext(request))

def guardar(request):

    id = request.POST['id']
    corp = ModeloCorpus.objects(id=id)[0]
    tags = corp.tags

    form = UploadFileForm(request.POST, request.FILES)

    nombre = id + '_' + uuid.uuid4().hex + '.mp3'
    total = DIR_FILES + nombre
    d = {}
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'],total)
    else:
        print('Man is the bastard')
    for etiqueta in tags:
        d[etiqueta.tag] = request.POST.get(etiqueta.tag,False)

    archivo = Archivo(archivo=nombre,tags=d,corpus=corp)
    archivo.save()


    arch = Archivo.objects(corpus=corp)

    params = {'id' : id , 'archivos': arch, 'tags': tags}
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))

def guardar_s(request):
    
    id = request.POST['id']
    corp = ModeloCorpus.objects(id=id)[0]
    tags = Tag.objects(corpus=corp)
    
    form = UploadFileForm(request.POST, request.FILES)
    
    nombre = id + '_' + uuid.uuid4().hex + '.mp3'
    total = DIR_FILES + nombre
    d = {}
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'],total)
    else:
        print('Man is the bastard')
    for etiqueta in tags:
        d[etiqueta.tag] = request.POST.get(etiqueta.tag,False)

    archivo = Archivo(archivo=nombre,tags=d,corpus=corp)
    archivo.save()


arch = Archivo.objects(corpus=corp)
    
    params = {'id' : id , 'archivos': arch, 'tags': tags}
    return render_to_response('archivos/listar.html', params,
                              context_instance=RequestContext(request))


def delete_file(nombre):
    os.remove(nombre)

def handle_uploaded_file(f,nombre):
    with open(nombre, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)