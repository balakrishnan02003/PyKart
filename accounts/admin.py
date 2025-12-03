from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Address


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'is_default', 'address_type', 'created_at']
    list_filter = ['is_default', 'address_type', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'full_name', 'city', 'state', 'postal_code']
    readonly_fields = ['created_at', 'updated_at']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

