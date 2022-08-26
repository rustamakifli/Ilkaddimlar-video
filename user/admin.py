from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User



class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','image','birthday','gender','mobile' )}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)


# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user', )
#     list_filter = ('user',)
#     search_fields = ('user', )
#     classes = ['collapse']

# admin.site.register(Student, StudentAdmin) 


