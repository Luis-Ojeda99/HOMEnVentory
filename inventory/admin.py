from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm
from .models import Account, Item, Category


class AccountAdmin(UserAdmin):
    # Forms to add and change users
    form = RegistrationForm
    add_form = RegistrationForm

    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Item)
admin.site.register(Category)
