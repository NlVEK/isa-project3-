from django.shortcuts import render_to_response, render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from test1.models import person, thing
from test1.forms import person_forms, thing_forms
import json
# Create your views here.


@csrf_exempt
def check_user_num(request):
    a = person.objects.count()
    if a :
        # return JsonResponse({'result': 'ok', 'message': a})
        return HttpResponse(json.dumps({'result': 'ok', 'message': a}))
    else:
        return HttpResponse(json.dumps({'result': 'error', 'message': a}))
@csrf_exempt
def show_person(request, user):
    a = person.objects.filter(id=user)
    if a:
        a = a[0]
        # return render(request, 'db_showperson.html',{'first':a.first_name, 'last': a.last_name})
        data = {"first_name": a.first_name, "last_name": a.last_name}
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
def create_person_result(request):

    if request.method == 'POST':
        a = person()
        form = person_forms(request.POST)
        if form.is_valid():
            a.first_name = form.cleaned_data['first_name']
            a.last_name = form.cleaned_data['last_name']
            a.save()
            data = {'result': "success", 'first name': a.first_name, 'last name': a.last_name}
            return HttpResponse( json.dumps(data), content_type='application/json')
    else:
        form = person_forms()
        return render(request, 'create_person.html', {"form":form})

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


@csrf_exempt
def person_delete(request, user):
    a = person.objects.filter(id=user).delete()
    if str(a[0]) == "1" or a[1].values() == 1:
        return (HttpResponse("delete &nbsp success"))
    return HttpResponse("delete &nbsp failed")

@csrf_exempt
def delete_thing(request, id):
    a = thing.objects.filter(id=id).delete()
    if str(a[0]) == "1" or a[1].values() == 1:
        return (HttpResponse("delete &nbsp success"))
    return HttpResponse("delete &nbsp failed")

@csrf_exempt
def person_update(request, user):
    if request.method == 'POST':
        a = person()
        form = person_forms(request.POST)
        if form.is_valid():
            a.first_name = form.cleaned_data['first_name']
            a.last_name = form.cleaned_data['last_name']
            try:
                b = person.objects.get(id=user)
            except:
                return HttpResponse(json.dumps({'result': 'error', 'message': 'the person DNE'}), content_type='application/json')
            else:
                b.first_name = a.first_name
                b.last_name = a.last_name
                b.save()
                return HttpResponse(json.dumps({'result': 'ok', 'message': 'update successful'}), content_type='application/json')
    else:
        form = person_forms()
        return render(request, 'update_pserson.html', {"form":form})


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