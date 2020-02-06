import re
import json
import requests
import bcrypt

from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session

from lists.models import Goods, User, History
import lists.auth as auth
import lists.crawlers as crawlers

def home_page(request):
    goods = []
    search_history = []
    user_pk = request.session.get('account')
    user = []
    if request.method == 'POST':
        get_search = request.POST.get('search_text', '')
        min_pric = request.POST.get('min_pric', '')
        max_pric = request.POST.get('max_pric', '')
        check_store = request.POST.getlist('checkstore')
        if min_pric == '':
            min_pric = 0
        if max_pric == '':
            max_pric = 999999
        if get_search != '':
            goods = crawlers.crawlers_array(check_store, get_search, min_pric, max_pric)
            if user_pk:
                user = User.objects.get(pk=user_pk)
                History.objects.create(user=user, keyword=get_search)
    if user_pk:
        user = User.objects.get(pk=user_pk)
        search_history = crawlers.take_history(user)
    return render(request, 'home.html', {'goods':goods, 'histories':search_history, 'user':user})

def auth_page(request):
    request.session['account'] = None
    if request.method == 'POST':
        user_account = request.POST.get('account', '')
        if not user_account or not request.POST.get('password', ''):
            account_pass = False
            return render(request, 'auth.html', {'account_pass':account_pass})
        user_data = auth.login(user_account)
        if user_data:
            account_pass = bcrypt.checkpw(request.POST.get('password', '').encode('UTF-8'), user_data.password.encode('UTF-8'))
            if account_pass:
                request.session['account'] = user_data.pk
                return redirect('home')
            else:
                return render(request, 'auth.html', {'account_pass':account_pass})
        else:
            account_pass = False
            return render(request, 'auth.html', {'account_pass':account_pass})
    return render(request, 'auth.html', {})


def register_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        user_mail = request.POST.get('mail', '')
        user_password = bcrypt.hashpw(request.POST.get('password', '').encode('UTF-8'), bcrypt.gensalt(14))
        #此段加密
        if not user_name or not user_mail or not user_password:
            account_complete = False
            return render(request, 'register.html', {'complete':account_complete})
        else:
            auth.register(user_name, user_mail, user_password)
            return redirect('auth')

    return render(request, 'register.html', {})