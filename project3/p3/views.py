from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from .forms import *
from .models import *
import json
import urllib.request
from django.views.decorators.csrf import csrf_exempt
#
@csrf_exempt
def home(request):
    #show all listings
    # a = urllib.request.Request('http://exp-api:8000/checknum')  # also micro service layer
    # a = urllib.request.urlopen(a).read().decode('utf-8')
    # result_num = json.loads(a)
    #
    # if result_num['result'] == 'ok':
    #     return render(request, 'home.html', {'message': result_num['message'], 'user': result_num['users'], 'display': 1})
    # else:
    #     #kinda redundant now but save for further progress
    #     return render(request, 'home.html', {'message': result_num['message'], 'user': result_num['users'], 'display': 0})
    id = request.COOKIES.get('id') or 0
    name = request.COOKIES.get('user')
    return render(request, 'home.html', {'id': id, 'user_name': name})



@csrf_exempt
def create(request):
    if request.method == 'POST':
        # a = person()
        form = person_forms(request.POST)
        if form.is_valid():
            #calls exp ser
            usr = form.cleaned_data['user_name']
            pwd = form.cleaned_data['pwd']
            data = {'user_name': usr, 'pwd': pwd}
            post_encoded = urllib.parse.urlencode(data).encode('utf-8')
            a = urllib.request.Request('http://exp-api:8000/create', data=post_encoded, method='POST')
            a = urllib.request.urlopen(a).read().decode('utf-8')
            res = json.loads(a)
            if res['result'] == "ok":
                return HttpResponse(res['message'])
            else:
                return HttpResponse(res['message']) #should be redirect with browser popup

    else:
        form = person_forms()
        return render(request, 'create.html', {"form":form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # a = person()
        form = person_forms(request.POST)
        if form.is_valid():
            usr = form.cleaned_data['user_name']
            pwd = form.cleaned_data['pwd']
            data = {'user_name': usr, 'pwd': pwd}
            post_encoded = urllib.parse.urlencode(data).encode('utf-8')
            a = urllib.request.Request('http://exp-api:8000/login', data=post_encoded, method='POST')
            a = urllib.request.urlopen(a).read().decode('utf-8')
            res = json.loads(a)
            if res['result'] == "error":
                form = person_forms()
                return render(request, 'login.html', { 'form': form, 'message': res['message']})
            else:

                # redirect to user page
                # id = str(res['id'])
                # 'http://models-api:8000/user/'+ id
                resp_redirect = HttpResponseRedirect("home")
                resp_redirect.set_cookie("auth", res['auth'])
                resp_redirect.set_cookie('id', res['id'])
                resp_redirect.set_cookie('user', res['user'])
                return resp_redirect
    else:
        if not request.COOKIES.get('auth'):
            form = person_forms()
            return render(request, 'login.html', {'form': form})
        else:
            id = request.COOKIES.get('id')
            data = {'id': id}
            post_encoded = urllib.parse.urlencode(data).encode('utf-8')
            a = urllib.request.Request('http://exp-api:8000/cookie', data=post_encoded, method='POST')
            a = urllib.request.urlopen(a).read().decode('utf-8')
            # a is a string
            return HttpResponse(a)

@csrf_exempt
def logout(request):
    #delete auth, delete id
    if request.COOKIES.get('auth'):
        response = HttpResponseRedirect("home")
        response.delete_cookie("auth")
        response.delete_cookie("id")

    else:
        response = HttpResponse("login expired")
    return response
# Create your views here.

