# items/admin.py

# django
from django.contrib       import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Items


class ItemsAdmin(ModelAdmin):
    '''Modify item representation in admin site'''

    list_display = ('name','total_quantity','is_active','updated_at')


# Register models for admin site
admin.site.register(Items, ItemsAdmin)

