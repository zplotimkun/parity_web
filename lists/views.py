from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(requset):
    return HttpResponse('<html><title>Tim parity web</title></html>')