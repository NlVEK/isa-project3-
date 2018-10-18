from django.shortcuts import render, HttpResponse, HttpResponseRedirect

import json
import urllib.request
from django.views.decorators.csrf import csrf_exempt
#
@csrf_exempt
def home(request):
    #show all listings
    a = urllib.request.Request('http://exp-api:8000/checknum')  # also micro service layer
    a = urllib.request.urlopen(a).read().decode('utf-8')
    result_num = json.loads(a)

    if result_num['result'] == 'ok':
        return render(request, 'home.html', {'message': result_num['message'], 'display': 1})
    else:
        #kinda redundant now but save for further progress
        return render(request, 'home.html', {'message': result_num['message'], 'display': 0})


# Create your views here.

