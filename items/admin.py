# items/admin.py

# django
from django.contrib import admin

# local
from .models import Items

# Register models for admin site
admin.site.register(Items)

