# items/admin.py

# django
from django.contrib       import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Items


class ItemsAdmin(ModelAdmin):
    '''Modify item representation in admin site'''

    readonly_fields = ['id','created_at','updated_at']
    list_display    = ('name','id','quantity','price','is_active','updated_at')


# Register models for admin site
admin.site.register(Items, ItemsAdmin)

