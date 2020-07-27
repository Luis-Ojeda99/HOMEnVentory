from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import InventoryUserCreationForm, InventoryUserChangeForm
from .models import InventoryUser, Item, Category


# Create InventoryUserAdmin
class InventoryUserAdmin(UserAdmin):
    add_from = InventoryUserCreationForm
    form = InventoryUserChangeForm
    model = InventoryUser
    list_display = ['email', 'username']


# Register your models here.
admin.site.register(InventoryUser, InventoryUserAdmin)
admin.site.register(Item)
admin.site.register(Category)
