from django.shortcuts import render, render_to_response, redirect

from django.template import RequestContext
from webapp.models import User
from django.http.response import HttpResponse
import hashlib

#pass context_instance=RequestContext(request) as 3rd argument


def index(request):
    if "username" in request.session:
        return render_to_response('webapp/html/explorer.html',{},context_instance=RequestContext(request))
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def explorer(request):
    if "username" in request.session:
        return render_to_response('webapp/html/explorer.html',{},context_instance=RequestContext(request))
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def login(request):
    print "Login Ca"
    success = False
    try:
        user = User.objects.get(user_name=request.POST['username'])
        s = hashlib.sha256()
        s.update(request.POST['password'])
        passwd = s.hexdigest()
        if passwd == user.password:
            success = True
            request.session["username"] = user.user_name
    except Exception:
        pass
    if success:
        print "Login Successful"
        return redirect('webapp.views.explorer')
    else:
        print "Login Failed"
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))
    
def logout(request):
    try:
        del request.session["username"]
    except Exception:
        pass
    return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))