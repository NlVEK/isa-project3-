from django.shortcuts import render_to_response, render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from test1.models import person, thing, auth
from test1.forms import person_forms, thing_forms
from django.contrib.auth.hashers import *
import os
import hmac
from foo import settings
import json
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


# @csrf_exempt
# def check_user_num(request):
#     a = person.objects.count()
#     if a :
#         # return JsonResponse({'result': 'ok', 'message': a})
#         return HttpResponse(json.dumps({'result': 'ok', 'message': a}))
#     else:
#         return HttpResponse(json.dumps({'result': 'error', 'message': a}))
#

# @csrf_exempt
# def get_all_users(request):
#     a = person.objects.all()
#     people = []
#     if a:
#         for users in a:
#             people.append([users[0].first_name, users[0].last_name]) #should be user_name and
#         return HttpResponse(json.dumps({'result': 'ok', 'message': people}))
#     else:
#         return HttpResponse(json.dumps({'result': 'error', 'message': people}))


@csrf_exempt
def person_login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        to_hash = make_password(request.POST['pwd'], salt="some_salt")
        pwd = str(to_hash)
        #check if they match
        try:
            get = person.objects.get(user_name=str(user_name))
        except ObjectDoesNotExist:
            return JsonResponse({'result': 'error', 'message': 'user name does not exist'})
        else:
            if str(get.pwd) == pwd:
                #create authenticator
                authen = hmac.new(key=settings.SECRET_KEY.encode('utf-8'), msg=os.urandom(32), digestmod='sha256').hexdigest()
                b = auth()
                b.user_name = get.user_name
                b.auth = authen
                # just check auth then, implemented later
                return JsonResponse({'result': 'ok', 'message': 'successfully log in', 'auth': b.auth, 'id': get.id, 'user': user_name})
            else:
                return JsonResponse({'result': 'error', 'message': 'password does not match'})

@csrf_exempt
def show_person(request, user):
    # auth = request.COOKIES.get('auth')
    # if not auth:
    #     return JsonResponse({'result': 'error', 'message': 'please log in first'})
    #will add invalid auth later
    a = person.objects.filter(pk=user)
    if a:
        a = a[0]
        # return render(request, 'db_showperson.html',{'first':a.first_name, 'last': a.last_name})
        data = {'result': 'ok',"user_name": a.user_name, 'pwd (in hex)': a.pwd}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse("person &nbsp DNE")

@csrf_exempt
def show_thing(request, id):
    a = thing.objects.filter(id=id)
    if a:
        a = a[0]
        # return render(request, 'db_showthing.html',{'info':a.info}
        return HttpResponse(json.dumps({'result':"ok",'info':a.info}), content_type='application/json')
    else:
        return HttpResponse("thing &nbsp DNE")

@csrf_exempt
def create_person(request):

    if request.method == 'POST':
        a = person()
        # form = person_forms(request.POST)
        # if form.is_valid():
        # #check user_name duplicates here

        #i think you can also
        # try save()
        # except django.db.IntegrityError

        # try:
        #     b = person.objects.filter(user_name=str(request.POST['user_name']))
        # except person.DoesNotExist:
            # good to go
        a.user_name = str(request.POST['user_name'])

        to_hash = make_password(request.POST['pwd'], salt="some_salt")
        a.pwd = str(to_hash)

        try:
            a.save()
        except IntegrityError:
            return JsonResponse({'result': 'error', 'message': 'username already registered'})

        else:
            data = {'result': "ok", 'message': 'successfully create new user', 'user_name': a.user_name, 'pwd': a.pwd,
                    'id': a.id}
            return HttpResponse(json.dumps(data), content_type='application/json')

    else:

        return JsonResponse(data={'result': 'error', 'message': 'please post data to create user'})

@csrf_exempt
def create_thing(request):

    if request.method == 'POST':
        a = thing()
        form = thing_forms(request.POST)
        if form.is_valid():
            a.info = form.cleaned_data['info']
            a.save()
            return HttpResponse(json.dumps({'result': 'ok', 'info': a.info}), content_type='application/json')
    else:
        form = thing_forms()
        return render(request, 'create_thing.html', {"form":form})


# @csrf_exempt
# def person_delete(request, user):
#     a = person.objects.filter(id=user).delete()
#     if str(a[0]) == "1" or a[1].values() == 1:
#         return (HttpResponse("delete &nbsp success"))
#     return HttpResponse("delete &nbsp failed")

@csrf_exempt
def delete_thing(request, id):
    a = thing.objects.filter(id=id).delete()
    if str(a[0]) == "1" or a[1].values() == 1:
        return (HttpResponse("delete &nbsp success"))
    return HttpResponse("delete &nbsp failed")
#
# @csrf_exempt
# def person_update(request, user):
#     if request.method == 'POST':
#         a = person()
#         form = person_forms(request.POST)
#         if form.is_valid():
#             a.first_name = form.cleaned_data['first_name']
#             a.last_name = form.cleaned_data['last_name']
#             try:
#                 b = person.objects.get(id=user)
#             except:
#                 return HttpResponse(json.dumps({'result': 'error', 'message': 'the person DNE'}), content_type='application/json')
#             else:
#                 b.first_name = a.first_name
#                 b.last_name = a.last_name
#                 b.save()
#                 return HttpResponse(json.dumps({'result': 'ok', 'message': 'update successful'}), content_type='application/json')
#     else:
#         form = person_forms()
#         return render(request, 'update_pserson.html', {"form":form})


@csrf_exempt
def update_thing(request, id):
    if request.method == 'POST':
        a = thing()
        form = thing_forms(request.POST)
        if form.is_valid():
            a.info = form.cleaned_data['info']

            try:
                b = thing.objects.get(id=id)
            except:
                return HttpResponse(json.dumps({'result': 'error', 'message': 'the thing DNE'}), content_type='application/json')
            else:
                b.info = a.info
                b.save()
                return HttpResponse(json.dumps({'result': 'ok', 'message': 'update successful'}), content_type='application/json')
    else:
        form = thing_forms()
        return render(request, 'update_thing.html', {"form":form})