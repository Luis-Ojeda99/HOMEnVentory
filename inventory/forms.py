from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import InventoryUser


# Method to work with the forms related to user registration
class InventoryUserCreationForm(UserCreationForm):

    class Meta:
        model = InventoryUser
        fields = ('username', 'email')


class InventoryUserChangeForm(UserChangeForm):

    class Meta:
        model = InventoryUser
        fields = ('username', 'email')
