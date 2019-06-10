import re
import json
import requests

from bs4 import BeautifulSoup
from lxml import etree

from django.db import connection
from lists.models import Goods

def crawler_pchome(search_text, min_pric, max_pric):
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
    url = '''https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={search_text}&page=1&sort=prc/ac&price={min_pric}-{max_pric}'''.format(search_text=search_text, min_pric=min_pric, max_pric=max_pric)
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
            'link': 'https://24h.pchome.com.tw/prod/{}'.format(good['Id']),
            'price': good['price'],
            'store': 'pchome'
        })

    return goods_list

def crawler_rakuten(search_text, min_pric, max_pric):
    rakuten_goods = []
    
    url = 'https://www.rakuten.com.tw/search/{search_text}/?minp={min_pric}&maxp={max_pric}&s=2&v=l&l-id=tw_search_list'.format(search_text=search_text, min_pric=min_pric, max_pric=max_pric)
    res = requests.get(url)
    selector = etree.HTML(res.text)
        
    for i in range(1, 20):
        rakuten_dict = {}
        xpath_good = '//*[@id="contents"]/div[2]/div[2]/div[5]/div/ul/li[{}]/div/div[2]/div[1]/div[1]/b/a/text()'.format(i)
        xpath_hyperlink = '//*[@id="contents"]/div[2]/div[2]/div[5]/div/ul/li[{}]/div/div[2]/div[1]/div[1]/b/a/@href'.format(i)
        xpath_price = '//*[@id="contents"]/div[2]/div[2]/div[5]/div/ul/li[{}]/div/div[2]/div[2]/div[1]/div/a/div/b/span/text()'.format(i)
        takecon_good = selector.xpath(xpath_good)
        takecon_price = selector.xpath(xpath_price)
        
        if takecon_good == []:
            xpath_good = '//*[@id="contents"]/div[2]/div[2]/div[5]/div/ul/li[{}]/div/div[2]/div[1]/div[2]/b/a/text()'.format(i)
            takecon_good = selector.xpath(xpath_good)
            xpath_hyperlink = '//*[@id="contents"]/div[2]/div[2]/div[5]/div/ul/li[{}]/div/div[2]/div[1]/div[2]/b/a/@href'.format(i)
            if takecon_good == []:
                continue
        takecon_hyperlink = selector.xpath(xpath_hyperlink)
            
        text_good = [str(text) for text in takecon_good][0]
        text_price = [str(text) for text in takecon_price][0]
        text_link = [str(text) for text in takecon_hyperlink][0]
        rakuten_dict['name'] = text_good
        rakuten_dict['link'] = 'https://www.rakuten.com.tw/' + text_link
        rakuten_dict['price'] = text_price
        rakuten_dict['store'] = 'rakuten'
        rakuten_goods.append(rakuten_dict)

    return rakuten_goods

def crawler_etmall(search_text, min_pric, max_pric):
    url = 'https://www.etmall.com.tw/Search/Get'
    post_data = {
        'keyword':search_text,
        'model[cateName]':'全站',
        'model[page]':0,
        'model[storeID]':'',
        'model[cateID]':'-1',
        'model[filterType]':'',
        'model[sortType]':4,
        'model[moneyMaximum]':max_pric,
        'model[moneyMinimum]':min_pric,
        'model[pageSize]':40,
        'page':0,
    }

    etmall_data = requests.post(url, data=post_data)

    etmall_goods = json.loads(etmall_data.text)['searchResult']['products']
    goods_list = []
    for good in etmall_goods:
        goods_list.append({
            'name': good['title'],
            'link': 'https://www.etmall.com.tw/'+good['purchaseLink'],
            'price': good['finalPrice'],
            'store': 'etmall'
        })
    return goods_list

def crawlers_array(check_store, search_text='', min_pric=0, max_pric=999999):
    print(check_store[0])
    search_history = Goods.objects.filter(
        keyword=search_text,
        price__gte=min_pric,
        price__lte=max_pric
        ).order_by("price")
    print("Before:{}".format(len(search_history)))
    if (not search_history.exists()) or len(search_history) < 20:
        all_goods = []
        pchome_goods = crawler_pchome(search_text, min_pric, max_pric)
        all_goods.extend(pchome_goods)
        rakuten_goods = crawler_rakuten(search_text, min_pric, max_pric)
        all_goods.extend(rakuten_goods)
        etmall_goods = crawler_etmall(search_text, min_pric, max_pric)
        all_goods.extend(etmall_goods)

        for goods in all_goods:
            if Goods.objects.filter(link=goods['link'], keyword=search_text).exists():
                continue
            Goods.objects.create(name=goods['name'], price=goods['price'], link=goods['link'], keyword=search_text, store=goods['store'])
    goods_array = Goods.objects.filter(
        keyword=search_text,
        store__in=check_store,
        price__gte=min_pric,
        price__lte=max_pric
        ).order_by("price")

    print("After:{}".format(len(goods_array)))
    print(min_pric, max_pric)

    return goods_array