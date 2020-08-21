from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth import authenticate

from .models import Account, Item


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "username", "first_name", "last_name")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateAccountForm(UserChangeForm):
    """
    A form for updating an account. It includes all the fields an user can change, but the password is hashed.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff')

        def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            return self.initial["password"]


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid credentials. Check your username and password.")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already taken by another user.' % username)

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already taken by another user.' % email)


class AddItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['item_name', 'price']
