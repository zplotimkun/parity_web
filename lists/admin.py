from django.contrib import admin
from .models import Item, Goods, User
# Register your models here.


admin.site.register(Item)
admin.site.register(Goods)

@admin.register(User)
class Admin_user(admin.ModelAdmin):
    list_display = ('username', 'mail', 'password')