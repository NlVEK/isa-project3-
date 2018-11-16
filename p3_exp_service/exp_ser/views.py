from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, Http404
from kafka import KafkaProducer, KafkaConsumer
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def home_number(request): #web front will call
    #show all listings
    a = urllib.request.Request('http://models-api:8000/user/checknum') #also micro service layer
    a = urllib.request.urlopen(a).read().decode('utf-8')
    result_num = json.loads(a)

    b = urllib.request.Request('http://models-api:8000/user/all_user')  # also micro service layer
    b = urllib.request.urlopen(b).read().decode('utf-8')
    result_user = json.loads(b)
    # b = requests.get('models-api:8001/user/')#check other stuff
    #....
    str = ""
    for i in range(int(result_num['message'])):
        str+= result_user['message'][2*i] + "&nbsp"+ result_user['message'][2*i+1] + "<br>"

    return HttpResponse(json.dumps({'result':'ok', 'message': result_num['message'], 'user': str})) #res['msg'] is a number
    # return HttpResponse(result_num)

@csrf_exempt
def home_show_create(request): #posting for create
    a = {}
    if request.method == "POST":
        if request.POST:
            a['user_name'] = request.POST['user_name']
            a['pwd'] = request.POST['pwd']

        post_encoded = urllib.parse.urlencode(a).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/user/create', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)

        #kafka
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('new_user', json.dumps(resp).encode('utf-8'))
        #relay it back to the front page
        return JsonResponse(data=resp)
    else:
        return HttpResponse("post some data")

@csrf_exempt
def login(request):
    a = {}
    if request.method == "POST":
        if request.POST:
            a['user_name'] = request.POST['user_name']
            a['pwd'] = request.POST['pwd']

        post_encoded = urllib.parse.urlencode(a).encode('utf-8')
        req = urllib.request.Request('http://models-api:8000/user/login', data=post_encoded, method='POST')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        # relay it back to the front page

        return JsonResponse(data=resp)
    else:
        return HttpResponse("error page")
@csrf_exempt
def login_with_cookie(request):
    if request.method == "POST":
        if request.POST:
            id = request.POST['id']
            req = urllib.request.Request('http://models-api:8000/user/' + id)
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)
            return JsonResponse(data=resp)


# @csrf_exempt
# def create_user_kafka(request):
#     producer = KafkaProducer(bootstrap_servers='kafka:9092')
#     if request.method == "POST":
#         if request.POST:
#             user =  request.POST['user_name']
#             pwd = request.POST['pwd']
#             new_user = {'user_name': user, 'pwd': pwd}
#             producer.send('new_user', json.dumps(new_user).encode('utf-8'))

# Create your views here.


