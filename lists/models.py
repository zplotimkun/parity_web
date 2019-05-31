from django.db import models

# Create your models here.

class Item(models.Model):
    text = models.TextField(default='')

class Goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    link = models.TextField()
    keyword = models.CharField(max_length=20, default='')