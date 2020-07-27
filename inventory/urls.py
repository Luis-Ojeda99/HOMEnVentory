from django.urls import path
from .views import RegisterView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
]
