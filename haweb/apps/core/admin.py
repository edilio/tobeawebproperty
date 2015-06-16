from django.contrib import admin
from django import forms
from .models import UserProfile, City, ZipCode, Unit, Tenant, Contract
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = UserProfile

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Photo'), {'fields': ('photo', )}),
        (_('Title'), {'fields': ('title', )}),
        (_('Phone'), {'fields': ('phone', )}),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'zip_code')
    list_filter = ('state', 'city')
    search_fields = ('city__name', 'zip_code')


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('tenant_id', 'order_on', 'cell_phone', 'home_phone', 'work_phone')
    search_fields = ('tenant_id', 'cell_phone', 'home_phone', 'work_phone', 'first_name', 'last_name')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_id', 'address', 'apartment', 'zip_code')
    search_fields = ('unit_id', 'address', 'apartment')
    list_filter = ('zip_code', )


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'unit', 'first_day', 'last_day')


admin.site.register(UserProfile, UserProfileAdmin)
