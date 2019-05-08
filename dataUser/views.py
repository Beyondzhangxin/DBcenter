from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
# import _pickle as cPickle
from django.contrib import auth


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
# @login_required
def index(request):
    context = {}
    if request.user.is_authenticated:
        print (request.user.username)
        context['extras'] = request.user.date_joined

    return TemplateResponse(request, 'Index/Index.html', context)

def login(request):
    context = {}
    return TemplateResponse(request, 'Index/Login.html', context)

@login_required
def db_index(request):
    context = {}
    if request.user.is_authenticated:
        print (request.user.username)
        context['extras'] = request.user.date_joined

    return TemplateResponse(request, 'Index/DBIndex.html', context)

def logout(request):
    auth.logout(request)
    if 'username' in request.session:
        del request.session['username']
        del request.session['cname']
    return HttpResponseRedirect("/")