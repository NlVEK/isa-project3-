from django.shortcuts import render, HttpResponse
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

    # b = requests.get('models-api:8001/user/')#check other stuff
    #....

    return HttpResponse(json.dumps({'result':'ok', 'message': result_num['message']})) #res['msg'] is a number
    # return HttpResponse(result_num)

# @csrf_exempt
# def home_show_create(request): #posting for create
#     a = {}
#     if request.method == "POST":
#         if request.POST:
#             a['first_name'] = request.POST['firstname']
#             a['last_name'] = request.POST['lastname']
#
#         post_encoded = urllib.parse.urlencode(a).encode('utf-8')
#         req = urllib.request.Request('http://models-api:8000/user/create', data=post_encoded, method='POST')
#         resp_json = urllib.request.urlopen(req).read().decode('utf-8')
#         resp = json.loads(resp_json)
# Create your views here.
