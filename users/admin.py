# users/admin.py

# django
from django.contrib            import admin
from django.contrib.auth.admin import UserAdmin

# local
from .models import CustomUser


class CustomUserAdmin( UserAdmin ):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
