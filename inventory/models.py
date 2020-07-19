from django.db import models
from django.urls import reverse


# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    price = models.IntegerField()


