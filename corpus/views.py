from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from mongoengine import *
from corpus.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
    # Get all posts from DB
    corp = ModeloCorpus.objects

    return render_to_response('corpus/index.html', {'Corpus': corp},
                              context_instance=RequestContext(request))

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def tags(request):
    id_corp = eval("request." + request.method + "['id']")
    corp = ModeloCorpus.objects(id=id_corp)[0]
    template = 'corpus/tags.html'
    tags_c = corp.tags
    subtags_c = Tag.objects(corpus=corp)
    params = {'Tags': tags_c,'Tagsf':corp.tags_f,'Subtags':subtags_c ,'id_corp': id_corp}
    return render_to_response(template, params, context_instance=RequestContext(request))

@login_required(login_url='/login')
def subtags(request):
    id_corp = eval("request." + request.method + "['id_corp']")

    if request.method == 'GET':
        
        id_tag = request.GET['id_tag']

        tags_c = Tag.objects(corpus=corp)

        params = {'Tags': tags_c,'id_tag':id_tag,}
        template = 'corpus/subtags.html'

    elif request.method == 'POST':
        corp = ModeloCorpus.objects(id=id_corp)[0]
        n_tag = request.POST['tag']
        
        new_tag = Tag(nombre=n_tag,corpus=corp)
        new_tag.save()
        
        tags_c = corp.tags
        subtags_c = Tag.objects(corpus=corp)
        params = {'Tags': tags_c,'Tagsf':corp.tags_f,'Subtags':subtags_c ,'id_corp': id_corp}
        template = 'corpus/tags.html'

    return render_to_response(template, params, context_instance=RequestContext(request))

@login_required(login_url='/login')
def s_subtags(request):

    if request.method == 'POST':
        
        id_corp = request.POST['id_corp']
        corp = ModeloCorpus.objects(id=id_corp)[0]
        
        n_tag = request.POST['tag']
        id_tag = request.POST['id_tag']

        tag = Subtag.objects(id=id_tag)[0]
        new_tag = Subtag(nombre=n_tag,ptag=tag)
        new_tag.save()
        
        tags_c = tag.tags
        subtags_c = Subtag.objects(ptag=tag)
        
        params = {'Tags': tags_c,'Tagsf':tag.tags_f,'Subtags':subtags_c ,'id_corp': id_corp,'id_tag': id_tag ,'id_back':tag.id }
        template = 'corpus/s_subtags.html'
    
    return render_to_response(template, params, context_instance=RequestContext(request))

@login_required(login_url='/login')
def tags_add(request):
    
    id_corp = request.POST['id_corp']
    corp = ModeloCorpus.objects(id=id_corp)[0]
    
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
    return render_to_response(template, {'Tags': corp.tags, 'Tagsf':corp.tags_f, 'id_corp': id_corp}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def subtags_add(request):
    
    tag_id = eval("request." + request.method + "['id_tag']")
    tag = Tag.objects(id=tag_id)[0]

    if request.method == 'GET':
        
        template = 'corpus/subtags.html'
        subtag = Subtag.objects(ptag=tag)
    
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
        subtag = Subtag.objects(ptag=tag)
    params = {'Tags': tag.tags , 'Tagsf': tag.tags_f, 'Subtags': subtag, 'id_tag': tag_id, 'id_corp' :tag.corpus.id}
    return render_to_response(template, params, context_instance=RequestContext(request))

@login_required(login_url='/login')
def s_subtags_add(request):
    
    tag_id = eval("request." + request.method + "['id_tag']")
    id_corp = eval("request." + request.method + "['id_corp']")
    tag = Subtag.objects(id=tag_id)[0]
    print(id_corp)
    if request.method == 'GET':

        subtag = Subtag.objects(ptag=tag)
        template = 'corpus/s_subtags.html'
    
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
        subtag = Subtag.objects(ptag=tag)
        tag.save()
        template = 'corpus/s_subtags.html'

    params = {'Tags': tag.tags , 'Tagsf': tag.tags_f, 'Subtags': subtag, 'id_tag': tag_id, 'id_corp' :id_corp, 'id_back': tag.ptag.id}
    return render_to_response(template, params, context_instance=RequestContext(request))


@login_required(login_url='/login')
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

@login_required(login_url='/login')
def tags_delete(request):
    id_corp = request.POST['id_corp']
    tag_id = request.POST['tag_id']
    corp = ModeloCorpus.objects(id=id_corp)[0]
    if request.POST.get('subtag',False) is False:
        template = 'corpus/tags.html'
        if request.POST.get('isfile',False) is not False:
            p = corp.tags_f
        else:
            p = corp.tags
        for tag in p:
            if tag == tag_id:
                p.remove(tag)
                break
    else:
        if len(Tag.objects(id=tag_id)) > 0:
            tag = Tag.objects(id=tag_id)
            template = 'corpus/tags.html'
        elif len(Subtag.objects(id=tag_id)) > 0:
            tag = Subtag.objects(id=tag_id)
            template = 'corpus/tags.html'
        tag.delete()

    
    #corp.update(pull__tags=tag)
    corp.save()
    

    corp.reload()

    subtags_c = Tag.objects(corpus=corp)

    return render_to_response(template, {'Tags': corp.tags , 'Tagsf':corp.tags_f,'Subtags':subtags_c,'id_corp': id_corp}, context_instance=RequestContext(request))

@login_required(login_url='/login')
def subtags_delete(request):
    id_corp = request.POST['id_corp']
    id_tag = request.POST['id_tag']


    corp = ModeloCorpus.objects(id=id_corp)[0]


    if request.POST.get('subtag',False) is False:
        template = 'corpus/tags.html'

        tag = Tag.objects(id=id_tag)[0]
        print(tag.tags)
        tag_n = request.POST['tag']
        
        if request.POST.get('isfile',False) is not False:
            p = tag.tags_f
        else:
            p = tag.tags

        for t in p:
            if t == tag_n:
                p.remove(t)
                tag.save()
                break
    else:
        tag = Subtag.objects(id=id_tag)[0]
        if len(Tag.objects(id=id_tag)) > 0:
            tag = Tag.objects(id=id_tag)
            template = 'corpus/tags.html'
        elif len(Subtag.objects(id=id_tag)) > 0:
            tag = Subtag.objects(id=id_tag)
            template = 'corpus/tags.html'
        tag.delete()
    
    
    #corp.update(pull__tags=tag)

    
    subtags_c = Tag.objects(corpus=corp)
    
    return render_to_response(template, {'Tags': corp.tags , 'Tagsf':corp.tags_f,'Subtags':subtags_c,'id_corp': id_corp}, context_instance=RequestContext(request))


@login_required(login_url='/login')
def s_subtags_delete(request):
    id_corp = eval("request." + request.method + "['id_corp']")
    id_tag = request.POST['id_tag']
    
    
    corp = ModeloCorpus.objects(id=id_corp)[0]
    
    
    if request.POST.get('subtag',False) is False:
        template = 'corpus/tags.html'
        
        tag = Subtag.objects(id=id_tag)[0]
        print(tag.tags)
        tag_n = request.POST['tag']
        
        if request.POST.get('isfile',False) is not False:
            p = tag.tags_f
        else:
            p = tag.tags
        
        for t in p:
            if t == tag_n:
                p.remove(t)
                tag.save()
                break
    else:
        tag = Subtag.objects(id=id_tag)[0]
        if len(Tag.objects(id=id_tag)) > 0:
            tag = Tag.objects(id=id_tag)
            template = 'corpus/tags.html'
        elif len(Subtag.objects(id=id_tag)) > 0:
            tag = Subtag.objects(id=id_tag)
            template = 'corpus/tags.html'
        tag.delete()


#corp.update(pull__tags=tag)


    subtags_c = Tag.objects(corpus=corp)
    
    return render_to_response(template, {'Tags': corp.tags , 'Tagsf':corp.tags_f,'Subtags':subtags_c,'id_corp': id_corp}, context_instance=RequestContext(request))

