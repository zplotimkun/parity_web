from django.db import models

# Create your models here.

class Item(models.Model):
    text = models.TextField(default='')

class Goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    link = models.TextField()
    keyword = models.CharField(max_length=20, default='')
    store = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Goods"

class User(models.Model):
    username = models.CharField(max_length=20)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username