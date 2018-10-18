from django.shortcuts import render
from django.shortcuts import HttpResponse

def hello(request):
    return render(request, "homepage.html")