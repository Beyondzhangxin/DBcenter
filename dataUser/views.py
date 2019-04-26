from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
import _pickle as cPickle

# Create your views here.


# return the file list that user owns or creats
def ownedFiles(request):
    pass


# return the file list that the user is shared with,including public files
def sharedFiles(request):
    pass

# make the file shared with a user
def addShareUser(request):
    pass

# make the file not share with a user
def cancelShareUser(request):
    pass

#change the file status , is public or private
def changeFileStatus(request):
    pass
@login_required
def index(request):
    context = {}
    if request.user is not None:
        print (request.user.username)
        context['extras'] = request.user.date_joined

    return TemplateResponse(request, 'Index/Index.html', context)
