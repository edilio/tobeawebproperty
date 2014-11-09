from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django.utils.translation import ugettext_lazy as _


class UserProfileAdmin(UserAdmin):
    model = UserProfile

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Photo'), {'fields': ('photo', )}),
        (_('Title'), {'fields': ('title', )}),
    )

admin.site.register(UserProfile, UserProfileAdmin)
