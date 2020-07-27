from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import InventoryUserCreationForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


class RegisterView(CreateView):
    form_class = InventoryUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'
