import re
import json
import requests

from bs4 import BeautifulSoup
from lxml import etree

from django.http import HttpResponse
from django.shortcuts import render

from lists.models import Item


def reptile_pchome(search_text=''):
    '''
    [
        {
            '名稱': value,
            '超連結': value,
            '金額': value
        },
        {
            '名稱': value,
            '超連結': value,
            '金額': value
        }
    ]
    '''
    url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={search_text}&page=1&sort=sale/dc'
    res = requests.get(url)
    pchome_goods = json.loads(res.text)['prods']
    '''
        {'BU':x,
        'Id':x,
        'author':x,
        'brand':x,
        'cateId':x,
        'couponActid':[],
        'describe':x,
        'isNC17':x,
        'isPChome':x,
        'name':x,
        'originPrice':x,
        'picB':x,
        'picS':x,
        'price':x,
        'publishDate':x,
        'sellerId':x
        }
    '''
    goods_list = []
    for good in pchome_goods:
        goods_list.append({
            'name': good['name'],
            'hyperlink': 'https://24h.pchome.com.tw/prod/'+good['Id'],
            'price': good['price']
        })
        print('https://24h.pchome.com.tw/prod/'+good['Id'])

    return goods_list

def reptile_rakuten(search_text=''):
    rakuten_goods = []
    for page in range(1, 2):
        url = 'https://www.rakuten.com.tw/search/{search_text}/?minp={minprice}&p={page}&s=2&v=l&l-id=tw_search_list'.format(search_text=search_text, minprice='', page=page)
        res = requests.get(url)
        selector = etree.HTML(res.text)
        print('第'+str(page)+'頁')
        for i in range(1, 20):
            rakuten_dict = {}
            xpath_good = '//*[@id="contents"]/div[2]/div[2]/div[4]/div/ul/li[{}]/div/div[2]/div[1]/div[1]/b/a/text()'.format(i)
            xpath_hyperlink = '//*[@id="contents"]/div[2]/div[2]/div[4]/div/ul/li[{}]/div/div[2]/div[1]/div[1]/b/a/@href'.format(i)
            xpath_price = '//*[@id="contents"]/div[2]/div[2]/div[4]/div/ul/li[{}]/div/div[2]/div[2]/div[1]/div/a/div/b/span/text()'.format(i)
            takecon_good = selector.xpath(xpath_good)
            takecon_price = selector.xpath(xpath_price)
            if takecon_good == []:
                xpath_good = '//*[@id="contents"]/div[2]/div[2]/div[4]/div/ul/li[{}]/div/div[2]/div[1]/div[2]/b/a'.format(i)
                takecon_good = selector.xpath(xpath_good)
                xpath_hyperlink = '//*[@id="contents"]/div[2]/div[2]/div[4]/div/ul/li[{}]/div/div[2]/div[1]/div[2]/b/a/@href'.format(i)

            takecon_hyperlink = selector.xpath(xpath_hyperlink)
            text_good = [str(text) for text in takecon_good][0]
            text_price = [str(text) for text in takecon_price][0]
            text_link = [str(text) for text in takecon_hyperlink][0]
            rakuten_dict['name'] = text_good
            rakuten_dict['price'] = text_price
            rakuten_dict['hyperlink'] = text_link
            rakuten_goods.append(rakuten_dict)

    return rakuten_goods


def home_page(request):
    goods = reptile_rakuten('google')

    return render(request, 'home.html', {'goods': goods})