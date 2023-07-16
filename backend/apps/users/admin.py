from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# internals
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(DjangoUserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone', 'password1', 'password2', 'is_staff', 'is_active')
        }
        ),
        ('Personal', {'fields': ('first_name', 'last_name',)}),
    )
    search_fields = ('email', 'username', 'phone',)
    ordering = ('email', 'username', 'phone',)
    list_display = ('email', 'username', 'phone', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'phone', 'is_staff', 'is_active',)


admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
