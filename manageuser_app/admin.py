from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from data_app.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('salutation', 'job_title', 'organisation', 'admin_priv')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('salutation', 'job_title', 'organisation', 'admin_priv')}),
    )


admin.site.register(User, CustomUserAdmin)
