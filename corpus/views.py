from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from mongoengine import *
from corpus.models import *

# Create your views here.
def index(request):
    # Get all posts from DB
    corp = ModeloCorpus.objects

    return render_to_response('corpus/index.html', {'Corpus': corp},
                              context_instance=RequestContext(request))

def create(request):
    # Get all posts from DB
    if request.method == 'POST':
        nombre = request.POST['nombre']
        corp = ModeloCorpus(nombre=nombre)
        corp.save()
        template = 'corpus/index.html'
    else:
        template = 'corpus/create.html'
    corp = ModeloCorpus.objects
    return render_to_response(template, {'Corpus': corp},context_instance=RequestContext(request))


def tags(request):
    id = eval("request." + request.method + "['id']")
    corp = ModeloCorpus.objects(id=id)[0]
    template = 'corpus/tags.html'
    tags_c = corp.tags
    subtags_c = Tag.objects(corpus=corp)
    params = {'Tags': tags_c,'Tagsf':corp.tags_f,'Subtags':subtags_c ,'id': id}
    return render_to_response(template, params, context_instance=RequestContext(request))


def subtags(request):
    id = eval("request." + request.method + "['id']")

    if request.method == 'GET':
        
        id_tag = request.GET['id_tag']

        tags_c = Tag.objects(corpus=corp)

        params = {'Tags': tags_c,'id_tag':id_tag}
        template = 'corpus/subtags.html'

    elif request.method == 'POST':
        corp = ModeloCorpus.objects(id=id)[0]
        n_tag = request.POST['tag']
        
        new_tag = Tag(nombre=n_tag,corpus=corp)
        new_tag.save()
        
        tags_c = corp.tags
        subtags_c = Tag.objects(corpus=corp)
        params = {'Tags': tags_c,'Tagsf':corp.tags_f,'Subtags':subtags_c ,'id': id}
        template = 'corpus/tags.html'

    return render_to_response(template, params, context_instance=RequestContext(request))

def tags_add(request):
    
    id = request.POST['id']
    corp = ModeloCorpus.objects(id=id)[0]
    
    if request.method == 'POST':
        
        n_tag = request.POST['tag']
        if request.POST.get('archivo',False) is not False:
            corp.tags_f.append(n_tag)
        else:
            corp.tags.append(n_tag)
        corp.save()
        template = 'corpus/tags.html'
        corp.reload()
            #url = reverse('corpus:tags', args = {'Tags': Corpus.objects(id=id)[0].tags,'id': id})
    return render_to_response(template, {'Tags': corp.tags, 'Tagsf':corp.tags_f, 'id': id}, context_instance=RequestContext(request))

def subtags_add(request):
    
    tag_id = eval("request." + request.method + "['id_tag']")
    tag = Tag.objects(id=tag_id)[0]

    if request.method == 'GET':
        
        template = 'corpus/subtags.html'

    elif request.method == 'POST':
        
        n_tag = request.POST['tag']

        if request.POST.get('archivo',False) is not False:
            tag.tags_f.append(n_tag)
        else:
            tag.tags.append(n_tag)
    
        print(tag.main_tag)
        if tag.main_tag is None:
            tag.main_tag = n_tag
        elif tag.main_tag is '':
            tag.main_tag = n_tag
        
        tag.save()
        template = 'corpus/subtags.html'

    params = {'Tags': tag.tags , 'Tagsf': tag.tags_f, 'id_tag': tag_id, 'id_corp' :tag.corpus.id}
    return render_to_response(template, params, context_instance=RequestContext(request))


def delete(request):
    id = eval("request." + request.method + "['id']")
    if request.method == 'POST':
        corp = ModeloCorpus.objects(id=id)[0]
        tags_c = Tag.objects(corpus=corp)
        tags_c.delete()
        corp.delete()
        template = 'corpus/index.html'
        params = {'Corpus': ModeloCorpus.objects}
    elif request.method == 'GET':
        template = 'corpus/delete.html'
        params = { 'id': id }
    
    return render_to_response(template, params, context_instance=RequestContext(request))


def tags_delete(request):
    id = request.POST['id']
    tag_id = request.POST['tag_id']
    corp = ModeloCorpus.objects(id=id)[0]
    if request.POST.get('subtag',False) is False:
        if request.POST.get('isfile',False) is not False:
            p = corp.tags_f
        else:
            p = corp.tags
        for tag in p:
            if tag == tag_id:
                p.remove(tag)
                break
    else:
        
        tag = Tag.objects(id=tag_id)
        tag.delete()
    
    #corp.update(pull__tags=tag)
    corp.save()
    
    template = 'corpus/tags.html'
    corp.reload()

    subtags_c = Tag.objects(corpus=corp)

    return render_to_response(template, {'Tags': corp.tags , 'Tagsf':corp.tags_f,'Subtags':subtags_c,'id': id}, context_instance=RequestContext(request))

def subtags_delete(request):
    id_tag = request.POST['id_tag']
    d_tag = request.POST['tag']
    tag = Tag.objects(id=id_tag)[0]
    
    if request.POST.get('subtag',False) is False:
        if request.POST.get('isfile',False) is not False:
            p = tag.tags_f
        else:
            p = tag.tags
        for tags in p:
            if tags == d_tag:
                p.remove(tags)
                if tag.main_tag == d_tag:
                    tag.main_tag = ''
                break
    else:
        
        tag = Tag.objects(id=tag_id)
        tag.delete()

    #corp.update(pull__tags=tag)
    tag.save()
    
    template = 'corpus/subtags.html'


    
    return render_to_response(template, {'Tags': tag.tags , 'Tagsf':tag.tags_f,'id_tag': id_tag,'id_corp':tag.corpus.id}, context_instance=RequestContext(request))
