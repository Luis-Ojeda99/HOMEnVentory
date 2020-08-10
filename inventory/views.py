from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Item


# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("user-inventory")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("user-inventory")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "registration/login.html", context)


def about_view(request):
    return render(request, 'about.html')


def user_inventory(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    items = Item.objects.filter(owner=request.user)
    context['items'] = items
    return render(request, 'user_inventory.html', context)


def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('user-inventory')
        else:
            context['registration_form'] = form
    else:  # GET request.
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'registration/register.html', context)


def account_management_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['Success_message'] = 'Your account has been updated.'
    else:  # GET request.
        form = AccountUpdateForm(
            initial={
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name
            }
        )

    context['account_form'] = form

    return render(request, "account_management.html", context)


def new_password_view(request):

    context = {}
    return render(request, "new_password.html", context)
