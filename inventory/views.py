from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, AddItemForm, EditItemForm, \
    AddCategoryForm, EditCategoryForm
from .models import Item, Category, Account


# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have logout successfully')
    return redirect('index')


def login_view(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        if user.is_admin:
            return redirect("admin_management")
        else:
            return redirect("user_inventory")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("user_inventory")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, "registration/login.html", context)


def admin_management_view(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if not user.is_admin:
        return redirect("user_inventory")

    accounts = Account.objects.all()
    context['accounts'] = accounts

    return render(request, "admin/admin_management.html", context)

def admin_add_user_view(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if not user.is_admin:
        return redirect("user_inventory")

    if request.POST and 'save_user' in request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('admin_management') 
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, "admin/admin_add_user.html", context)

def user_inventory(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if user.is_admin:
        return redirect("admin_management")

    items = Item.objects.filter(owner=request.user)
    categories = Category.objects.all()
    context['categories'] = categories
    context['items'] = items
    form = AddItemForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            obj = form.save(commit=False)
            category = request.POST.get('category', None)
            cat = Category.objects.filter(category_name=category).first()
            obj.category = cat
            owner = Account.objects.filter(username=user.username).first()
            obj.owner = owner
            obj.save()
            context['success_message'] = 'The item was added successfully!'

    context['add_item_form'] = form

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
            messages.success(request, 'Your account was created successfully, you can now add items to your inventory')
            return redirect('index')
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
            form.initial = {
                "username": request.POST['username'],
                "email": request.POST['email'],
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name']
            }
            form.save()
            context['success_message'] = 'Your account has been updated.'
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


def deactivate_account_view(request):

    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, 'Your account has been successfully disabled. Contact an admin should you want to '
                              'activate it again.')
    return redirect('index')


def admin_deactivate_user_view(request, pk):

    account = Account.objects.get(username=pk)
    account.is_active = False
    account.save()
    messages.success(request, 'The user ' + pk + ' has been deactivated successfully.')

    return redirect('admin_management')


def admin_activate_user_view(request, pk):

    account = Account.objects.get(username=pk)
    account.is_active = True
    account.save()
    messages.success(request, 'The user ' + pk + ' has been activated again.')

    return redirect('admin_management')


def delete_account_view(request, pk):
    account = Account.objects.get(username=pk)
    if request.method == "POST":
        account.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('admin_management')


def delete_item_view(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, 'The item was deleted successfully.')
        return redirect('user_inventory')


def admin_update_user_view(request, pk):
    account = Account.objects.get(username=pk)
    form = AccountUpdateForm(instance=account)

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.initial = {
                "username": request.POST['username'],
                "email": request.POST['email'],
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name'],
                "is_active": request.POST.get("is_active", None)
            }
            form.save()
            messages.success(request, 'User information updated successfully.')
    else:
        form = AccountUpdateForm(
            initial={
                "username": account.username,
                "email": account.email,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "is_active": account.is_active
            }
        )

    context['account_form'] = form
    return render(request, 'admin/admin_update_user.html', context)


def edit_item_view(request, pk):
    item = Item.objects.get(id=pk)
    form = EditItemForm(instance=item)

    context = {}

    categories = Category.objects.all()
    context['categories'] = categories

    if request.POST:
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            category = request.POST.get('category', None)
            cat = Category.objects.filter(category_name=category).first()
            form.initial = {
                "category": cat,
                "item_name": request.POST['item_name'],
                "price": request.POST['price']
            }
            obj = form.save(commit=False)
            obj.category = cat
            obj.save()
            messages.success(request, 'The item information has been edited successfully.')
    else:
        form = EditItemForm(
            initial={
                "category": item.category,
                "item_name": item.item_name,
                "price": item.price
            }
        )

    context['edit_item_form'] = form
    return render(request, 'edit_item.html', context)


def manage_categories_view(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if not user.is_admin:
        return redirect("index")

    categories = Category.objects.all()
    context['categories'] = categories

    form = AddCategoryForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            form.save()
            category_name = form.cleaned_data.get('category_name')
            messages.success(request, 'Category added successfully')

    context['add_category_form'] = form

    return render(request, "manage_categories.html", context)


def edit_category_view(request, pk):
    category = Category.objects.get(category_name=pk)
    form = EditCategoryForm(instance=category)

    context = {}

    if request.POST:
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.initial = {
                "category_name": request.POST['category_name']
            }
            form.save()
            messages.success(request, 'The category information was updated successfully')
    else:
        form = EditCategoryForm(
            initial={
                "category_name": category.category_name
            }
        )

    context['edit_category_form'] = form
    return render(request, 'edit_category.html', context)
