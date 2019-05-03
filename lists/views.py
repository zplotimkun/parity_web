from django.http import HttpResponse
from django.shortcuts import render
from lists.models import Item
import requests
import re
from bs4 import BeautifulSoup

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ''

    return render(request, 'home.html', {'new_item_text': new_item_text})

def reptile_pchome(requests):
    seach_text = ''
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=ssd&page=1&sort=sale/dc'
    res = requests.get(url)
    get_data = json.loads(res.text)
    for seach_data in get_data:
        goods_name = seach_data['name']
        goods_price = seach_data['prices']



