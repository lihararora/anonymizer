from django.shortcuts import render, render_to_response

from django.template import RequestContext
from webapp.models import User
from django.http.response import HttpResponse
import hashlib

#pass context_instance=RequestContext(request) as 3rd argument


def index(request):
    #context = {}
    #return render(request, 'webapp/index.html', context)
    return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def explorer(request):
    #context = {}
    #return render(request, 'webapp/index.html', context)
    return render_to_response('webapp/html/explorer.html',{},context_instance=RequestContext(request))

def login(request):
    str = 'Invalid username/password'
    try:
        user = User.objects.get(user_name=request.POST['username'])
        s = hashlib.sha256()
        s.update(request.POST['password'])
        passwd = s.hexdigest()
        if passwd == user.password:
            str = 'Welcome ' + user.first_name + ' ' + user.last_name
    except Exception:
        pass
    return HttpResponse(str)