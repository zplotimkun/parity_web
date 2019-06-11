import re
import json
import requests
import bcrypt

from bs4 import BeautifulSoup
from lxml import etree

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from lists.models import Goods
from lists.models import User
import lists.auth as auth
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

def auth_page(request):
    if request.method == 'POST':
        user_account = request.POST.get('account', '')
        user_data = auth.login(user_account)
        if bcrypt.checkpw(request.POST.get('password', '').encode('UTF-8'), user_data.password.encode('UTF-8')):
            print('登入成功')
            return redirect('http://127.0.0.1:8000')
        else:
            print('登入失敗')
    return render(request, 'auth.html', {})


def register_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        user_mail = request.POST.get('mail', '')
        user_password = bcrypt.hashpw(request.POST.get('password', '').encode('UTF-8'), bcrypt.gensalt(14))
        #此段加密
        if not user_name or not user_mail or not user_password:
            print('缺資料失敗')
            return render(request, 'register.html', {})
        else:
            account_save = auth.register(user_name, user_mail, user_password)
            print(account_save)
            return redirect('http://127.0.0.1:8000/auth/')

    return render(request, 'register.html', {})