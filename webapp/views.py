from django.shortcuts import render_to_response, redirect

from django.template import RequestContext
from webapp.models import User, Document
import hashlib
from django.http.response import HttpResponse
from xhtml2pdf import pisa
import nlp
import re

#pass context_instance=RequestContext(request) as 3rd argument



def index(request):
    if "username" in request.session:
        return redirect('/explorer/')
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def explorer(request):
    if "username" in request.session:
        documents = Document.objects.all()
        return render_to_response('webapp/html/explorer.html',{"documents" : documents},context_instance=RequestContext(request))
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def editor(request):
    f = request.FILES['file']
    content = f.read()
    content = content.replace('\n', '<br/>')
    entities = nlp.get_names(content)
    old_offset = 0
    contents = ""
    for entity in entities:
        temp = "<span id='entity"+str(entity.id)+"'>"+entity.name+"</span>"
        #print temp,
        new_offset = old_offset + content[old_offset:].find(entity.name) + len(entity.name)
        #print new_offset
        contents += content[old_offset:new_offset].replace(entity.name, temp, 1)
        old_offset = new_offset
    contents += content[old_offset:]
    content= contents
    if "username" in request.session:
        return render_to_response('webapp/html/editor.html',{"file_contents":content, "named_entities": entities},context_instance=RequestContext(request))
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def login(request):
    success = False
    try:
        user = User.objects.get(user_name=request.POST['username'])
        s = hashlib.sha256()
        s.update(request.POST['password'])
        passwd = s.hexdigest()
        if passwd == user.password:
            success = True
            request.session["username"] = user.user_name
            request.session["firstname"] = user.first_name
            request.session["lastname"] = user.last_name
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

def save(request):
    if "username" in request.session:
        doc = Document()
        doc.author_id = User.objects.get(user_name = request.session['username'])
        doc.file_name = request.POST['filename']
        doc.contents = request.POST['content']
        doc.save()
        return redirect('/viewer/'+str(doc.document_id))
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))

def viewer(request, document_id):
    if "username" in request.session:
        if document_id != '':
            doc = getAnonymizedDocument(request,document_id)
            return render_to_response('webapp/html/viewer.html',{"file_contents":doc.contents, "document_id":document_id},context_instance=RequestContext(request))
        else:
            return redirect('/explorer/')
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))
    
def download(request, document_id):
    if "username" in request.session:
        if document_id != '':
            doc = getAnonymizedDocument(request,document_id)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' % doc.file_name
            p = convertHtmlToPdf("<style> body { font-size: 14px; }</style>" + doc.contents, response)
            return response
        else:
            return redirect('/explorer/')
    else:
        return render_to_response('webapp/html/login.html',{},context_instance=RequestContext(request))
    
def convertHtmlToPdf(sourceHtml, outputFile):
    resultFile = outputFile
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result
    return pisaStatus.err

def getAnonymizedDocument(request, document_id):
    doc = Document.objects.get(document_id = document_id)
    anonymized_content = doc.contents
    user = User.objects.get(user_name = request.session['username'])
    level = int(user.role)
	#print anonymized_content
    if level > 1:
        anonymized_content = re.sub(r'<span1 class=\"level_1\">(.|\n)*?</span1>', r"&lt;&lt;AUTHORIZATION REQUIRED TO VIEW THIS LINE&gt;&gt;", anonymized_content)
    if level > 2:
        anonymized_content = re.sub(r'<span1 class=\"level_2\">(.|\n)*?</span1>', r"&lt;&lt;AUTHORIZATION REQUIRED TO VIEW THIS LINE&gt;&gt;", anonymized_content)
    if level > 3:
        anonymized_content = re.sub(r'<span1 class=\"level_3\">(.|\n)*?</span1>', r"&lt;&lt;AUTHORIZATION REQUIRED TO VIEW THIS LINE&gt;&gt;", anonymized_content)
    doc.contents = anonymized_content
    return doc
