from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_inventory/', views.user_inventory, name='user_inventory'),
    path('edit_item/<str:pk>', views.edit_item_view, name='edit_item'),
    path('delete_item/<str:pk>', views.delete_item_view, name='delete_item'),
    path('account_management/', views.account_management_view, name="account_management"),
    path('deactivate_account/', views.deactivate_account_view, name="deactivate_account"),
    path('admin_management/', views.admin_management_view, name="admin_management"),
    path('manage_categories/', views.manage_categories_view, name='manage_categories'),
    path('edit_category/<str:pk>/', views.edit_category_view, name='edit_category'),
    path('delete_account/<str:pk>/', views.delete_account_view, name='delete_account'),
    path('admin_update_user/<str:pk>/', views.admin_update_user_view, name='admin_update_user'),
    path('admin_deactivate_user/<str:pk>/', views.admin_deactivate_user_view, name='admin_deactivate_user'),
    path('admin_activate_user/<str:pk>/', views.admin_activate_user_view, name='admin_activate_user'),

    # Password reset links (Reference: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete')
]
