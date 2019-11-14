import re
import json
import requests
import time

from bs4 import BeautifulSoup
from lxml import etree
from urllib.request import urlopen

from lists.models import Goods, User, History

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def take_history(user):
    search_history = History.objects.filter(user=user).order_by('-pk').values_list('keyword', flat=True)
    top3_search = []
    for history in search_history:
        if len(top3_search) <= 3:
            if len(top3_search) == 0:
                top3_search.append(history)
            else:
                if history not in top3_search:
                    top3_search.append(history)

    return top3_search

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
    html = requests.get(url)
    soup = BeautifulSoup(html.text, features='lxml')
    good_name = soup.find_all('a', {"class":"product-name"})
    good_price = soup.find_all('span', {"class":"b-text-prime"})
        
    for i in range(len(good_name)):
        rakuten_dict = {}
        take_name = re.findall('>(.*)<', str(good_name[i]))
        take_link = re.findall('href=\"\S+\"', str(good_name[i]))
        link = re.findall('\/\S+\/', str(take_link))
        take_price = re.findall('>(([0-9]*,)?([0-9]+))', str(good_price[i]))[0][0]
        price = take_price.split(',')
        if len(price) == 2:
            rakuten_dict['price'] = '{}{}'.format(price[0],price[1])
        else:
            rakuten_dict['price'] = '{}'.format(take_price)
        rakuten_dict['name'] = take_name[0]
        rakuten_dict['link'] = 'https://www.rakuten.com.tw{}'.format(link[0])
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
    # session = get_tor_session()
    session = requests.Session()
    etmall_data = session.post(url, data=post_data)

    etmall_goods = json.loads(etmall_data.text)['searchResult']['products']
    goods_list = []
    for good in etmall_goods:
        etmall_dict = {}
        etmall_dict['name'] = good['title']
        etmall_dict['link'] = 'https://www.etmall.com.tw/'+good['purchaseLink']
        etmall_dict['price'] = good['finalPrice']
        etmall_dict['store'] = 'etmall'

        goods_list.append(etmall_dict)
    return goods_list

def crawlers_array(check_store, search_text='', min_pric=0, max_pric=999999):
    search_history = Goods.objects.filter(
        keyword=search_text,
        price__gte=min_pric,
        price__lte=max_pric
        ).order_by("price")
    if (not search_history.exists()) or len(search_history) < 20:
        all_goods = []
        # etmall_goods = crawler_etmall(search_text, min_pric, max_pric)
        # all_goods.extend(etmall_goods)
        pchome_goods = crawler_pchome(search_text, min_pric, max_pric)
        all_goods.extend(pchome_goods)
        rakuten_goods = crawler_rakuten(search_text, min_pric, max_pric)
        all_goods.extend(rakuten_goods)

        for goods in all_goods:
            if Goods.objects.filter(link=goods['link'], keyword=search_text).exists():
                continue
            try:
                Goods.objects.create(
                    name=goods['name'],
                    price=goods['price'],
                    link=goods['link'],
                    keyword=search_text,
                    store=goods['store']
                )
            except Exception as e:
                print(f"Create object {goods} raise error: {e}")
    goods_array = Goods.objects.filter(
        keyword=search_text,
        store__in=check_store,
        price__gte=min_pric,
        price__lte=max_pric
        ).order_by("price")

    return goods_array