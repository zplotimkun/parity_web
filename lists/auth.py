from django.db import connection
from django.db.models import Q

from lists.models import User

def login(account):
    search_user = User.objects.filter(
        Q(username=account) | Q(mail=account)
    )	
    if search_user:
        search_user = User.objects.get(
            Q(username=account) | Q(mail=account)
        )
    return search_user

def register(username, usermail, password):
    search_user = User.objects.filter(
        Q(username=username) | Q(mail=usermail)
        )
    if (search_user.exists()) or ('@' not in usermail):
        return False
    else:
        User.objects.create(username=username, mail=usermail, password=password)
        return True