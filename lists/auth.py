from django.db import connection
from django.db.models import Q

from lists.models import User

def login(account):
    search_user = User.objects.get(
        Q(username=account) | Q(mail=account)
    )	
    print('login:{}'.format(search_user))
    return search_user

def register(username, usermail, password):
    search_user = User.objects.filter(
        Q(username=username) | Q(mail=usermail)
        )
    if (search_user.exists()) or ('@' not in usermail):
        print('名稱、信箱重複,或信箱不符合格式')
        return False
    else:
        User.objects.create(username=username, mail=usermail, password=password)
        print('帳號申請成功')
        return True