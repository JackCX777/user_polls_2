from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from custom_user_app.models import User


# class EditedUserAdmin(BaseUserAdmin):
#     model = User
#     ordering = ('email', )


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'email', 'is_active', 'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('id', )}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'id',)
    ordering = ('id', 'email',)


# admin.site.register(User, EditedUserAdmin)
admin.site.register(User, UserAdmin)
