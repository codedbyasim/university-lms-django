from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your custom User model with the admin site
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin interface for the User model.
    Adds 'role' to the list display and fieldsets.
    """
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    search_fields = ('username', 'email', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
