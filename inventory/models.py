from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class InventoryUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=25)


class Item(models.Model):
    item_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

        def __unicode__(self):
            return u'%s'% self.item_name
