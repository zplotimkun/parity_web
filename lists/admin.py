from django.contrib import admin
from .models import Item, Goods, User, History
# Register your models here.


admin.site.register(Item)
admin.site.register(Goods)

@admin.register(User)
class Admin_user(admin.ModelAdmin):
    list_display = ('username', 'mail', 'password', 'register_time')

@admin.register(History)
class Admin_history(admin.ModelAdmin):
    list_display = ('user', 'keyword', 'register_time')