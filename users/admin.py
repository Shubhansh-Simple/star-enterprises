# users/admin.py

# django
from django.contrib            import admin
from django.contrib.auth.admin import UserAdmin

# local
from .models import CustomUser


class CustomUserAdmin( UserAdmin ):
    model           = CustomUser
    readonly_fields = ['id']
    list_display    = ('username','id','is_staff')


# Register models for admin site
admin.site.register(CustomUser, CustomUserAdmin)

