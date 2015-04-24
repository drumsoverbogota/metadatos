from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from mongoengine import *
from corpus.models import *

# Create your views here.
def index(request):
    # Get all posts from DB
    corp = Corpus.objects

    return render_to_response('corpus/index.html', {'Corpus': corp},
                              context_instance=RequestContext(request))

def create(request):
    # Get all posts from DB
    if request.method == 'POST':
        nombre = request.POST['nombre']
        corp = Corpus(nombre=nombre)
        corp.save()
        template = 'corpus/index.html'
    else:
        template = 'corpus/create.html'
    corp = Corpus.objects
    return render_to_response(template, {'Corpus': corp},context_instance=RequestContext(request))


def tags(request):
    id = eval("request." + request.method + "['id']")
    corp = Corpus.objects(id=id)[0]
    template = 'corpus/tags.html'
    tags_c = corp.tags
    params = {'Tags': tags_c,'id': id}
    return render_to_response(template, params, context_instance=RequestContext(request))


def subtags(request):
    id = eval("request." + request.method + "['id']")
    template = 'corpus/subtags.html'
    if request.method == 'GET':
        id = eval("request." + request.method + "['id']")
        corp = Corpus.objects(id=id)[0]
        template = 'corpus/tags.html'
        tags_c = Tag.objects(corpus=corp)
        params = {'Tags': tags_c,'id': id}

    elif request.method == 'POST':
        corp = Corpus.objects(id=id)[0]
        n_tag = request.POST['tag']
        
        new_tag = Tag(nombre=n_tag,corpus=corp)
        new_tag.save()
        
        tags_c = new_tag.tags
        
        params = {'Tags': tags_c,'id_corp': id, 'id_tag':new_tag.id}

    return render_to_response(template, params, context_instance=RequestContext(request))

def tags_add(request):
    
    id = request.POST['id']
    corp = Corpus.objects(id=id)[0]
    
    if request.method == 'POST':
        
        n_tag = request.POST['tag']
        corp.tags.append(n_tag)
        corp.save()
        template = 'corpus/tags.html'
        corp.reload()
            #url = reverse('corpus:tags', args = {'Tags': Corpus.objects(id=id)[0].tags,'id': id})
    return render_to_response(template, {'Tags': corp.tags , 'id': id}, context_instance=RequestContext(request))

def subtags_add(request):
    
    id = request.POST['id']
    corp = Corpus.objects(id=id)[0]
    
    if request.method == 'POST':
        
        n_tag = request.POST['tag']
        corp.tags.append(n_tag)
        corp.save()
        template = 'corpus/tags.html'
        corp.reload()
    #url = reverse('corpus:tags', args = {'Tags': Corpus.objects(id=id)[0].tags,'id': id})
    return render_to_response(template, {'Tags': corp.tags , 'id': id}, context_instance=RequestContext(request))


def delete(request):
    id = eval("request." + request.method + "['id']")
    if request.method == 'POST':
        corp = Corpus.objects(id=id)[0]
        tags_c = Tag.objects(corpus=corp)
        tags_c.delete()
        corp.delete()
        template = 'corpus/index.html'
        params = {'Corpus': Corpus.objects}
    elif request.method == 'GET':
        template = 'corpus/delete.html'
        params = { 'id': id }
    
    return render_to_response(template, params, context_instance=RequestContext(request))


def tags_delete(request):
    id = request.POST['id']
    tag_id = request.POST['tag_id']
    corp = Corpus.objects(id=id)[0]

    for tag in corp.tags:
        if tag == tag_id:
            corp.tags.remove(tag)
    
    #corp.update(pull__tags=tag)
    corp.save()
    
    template = 'corpus/tags.html'
    corp.reload()
    return render_to_response(template, {'Tags': corp.tags , 'id': id}, context_instance=RequestContext(request))
