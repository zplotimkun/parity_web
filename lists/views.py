import re
import json
import requests

from bs4 import BeautifulSoup
from lxml import etree

from django.http import HttpResponse
from django.shortcuts import render

from lists.models import Item
from lists.models import Goods
import lists.crawlers as crawlers


def home_page(request):
    goods = []
    if request.method == 'POST':
        get_search = request.POST.get('search_text', '')
        min_pric = request.POST.get('min_pric', '')
        max_pric = request.POST.get('max_pric', '')
        check_store = request.POST.getlist('checkstore')
        if min_pric == '':
            min_pric = 0
        if max_pric == '':
            max_pric = 999999
        print(check_store, get_search, min_pric, max_pric)
        if get_search != '':
            goods = crawlers.crawlers_array(check_store, get_search, min_pric, max_pric)
        else:
            return render(request, 'home.html', {})

    return render(request, 'home.html', {'goods': goods})