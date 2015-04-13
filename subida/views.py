from django.contrib.auth import *
from mongoengine.queryset import DoesNotExist
from django.shortcuts import *
import datetime

def index(request):

    return render_to_response('index.html', {},
                              context_instance=RequestContext(request))


def login(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        if user.check_password(request.POST['password']):
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            login(request, user)
            request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
            return HttpResponse(user)
        else:
            return HttpResponse('login failed')
    except DoesNotExist:
        return HttpResponse('user does not exist')

