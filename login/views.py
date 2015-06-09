from django.shortcuts import render, render_to_response,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse
from mongoengine import *
#from django.contrib.auth import authenticate
from mongoengine.django.auth import User, Permission
from django.contrib import messages


from .models import Usuario


def login(request):
    from django.contrib.auth import login
    from mongoengine.django.auth import User
    from mongoengine.queryset import DoesNotExist
    from django.contrib import messages
    
    
    if request.user.is_authenticated():
        return redirect('index')
    
    try:
        usuario = request.POST.get('user',False)
        pswd  = request.POST.get('password',False)
        user = Usuario.objects.get(username=usuario)#request.POST['username'])
        print(user)
        if user.check_password(pswd):#request.POST['password']):
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
            print(login(request, user))
            return redirect('index')
        else:
            #print "malament"
            messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
            print('Test B')
    except DoesNotExist:
        messages.add_message(request,messages.ERROR,u"Incorrect login name or password !")
        print('Test C')
    template = 'login/index.html'
    return render_to_response(template,{},context_instance=RequestContext(request))

def logout(request):#NOT TESTED
    from django.contrib.auth import logout
    logout(request)
    
    template = 'login/index.html'
    return render_to_response(template,{},context_instance=RequestContext(request))

def init(request):
    user = Usuario.create_user('admin','admin','admin@admin.gov')
    user.perm = ['admin']
    user.save()
    return redirect('/')

def index(request):
    if request.user.is_authenticated():
        return redirect('index')
    template = 'login/index.html'
    return render_to_response(template,{},context_instance=RequestContext(request))

def create(request):
    if not request.user.is_authenticated():
        return redirect('index')
    
    template = 'login/create.html'
    return render_to_response(template,{'usu':Usuario.objects()},context_instance=RequestContext(request))

def delete_user(request):
    
    usuario = request.POST.get('id_user',False)
    user = Usuario.objects.get(username=usuario)#request.POST['username'])
    user.delete()
    template = 'login/create.html'
    return render_to_response(template,{'usu':Usuario.objects()},context_instance=RequestContext(request))



def create_user(request):
    if not request.user.is_authenticated():
        return redirect('index')
    
    usuario = request.POST.get('user',False)
    email = request.POST.get('email',False)
    pswd  = request.POST.get('password',False)
    pswd_c  = request.POST.get('c_password',False)

    import re

    if not pswd == pswd_c:
        messages.add_message(request, messages.INFO, 'Contraseñas no coinciden')
    if pswd == '':
        messages.add_message(request, messages.INFO, 'La contraseña no puede ser vacia')
    if usuario == '':
        messages.add_message(request, messages.INFO, 'El usuario no puede ser vacio')
    if email == '':
        messages.add_message(request, messages.INFO, 'El correo no puede ser vacio')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messages.add_message(request, messages.INFO, 'El correo no tiene un formato válido')

    if len(messages.get_messages(request)) > 0:
        template = 'login/create.html'
        return render_to_response(template,{'usu':Usuario.objects()},context_instance=RequestContext(request))
    user = Usuario.create_user(usuario,pswd,email)

    if request.POST.get('archivo',False) is not False:
        user.perm = ['admin']
        user.save()

    template = 'login/create.html'
    return render_to_response(template,{'usu':Usuario.objects()},context_instance=RequestContext(request))