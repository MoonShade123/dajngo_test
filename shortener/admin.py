from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm
from .models import User, Url


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class UrlAdmin(admin.ModelAdmin):
    list_display = ('default_url','shorted_url', 'user')
    ordering = ('id',)


admin.site.register(User, UserAdmin)
admin.site.register(Url, UrlAdmin)
