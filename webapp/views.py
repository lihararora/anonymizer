from django.shortcuts import render, render_to_response

from django.template import RequestContext

#pass context_instance=RequestContext(request) as 3rd argument


def index(request):
    #context = {}
    #return render(request, 'webapp/index.html', context)
    return render_to_response('webapp/example.html',{},context_instance=RequestContext(request))