from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-inventory/', views.user_inventory, name='user-inventory'),
    path('account-management/', views.account_management_view, name="account-management"),
    path('new-password/', views.new_password_view, name='new-password'),
]
