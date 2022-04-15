from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from account.models import MyUser, MyToken


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name',
                       'last_name',
                       'email')}),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_staff',
                       'is_superuser',
                       'groups',
                       'user_permissions',
                       'refresh_token'),
        }),
        (_('Important dates'), {
            'fields': ('last_login',
                       'date_joined')}),
    )


admin.site.register(MyUser, CustomUserAdmin)
admin.site.register(MyToken)
