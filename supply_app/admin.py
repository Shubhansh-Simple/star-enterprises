# supply_app/admin.py

# django
from django.contrib       import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Supplys


class SupplysAdmin(ModelAdmin):
    '''Modify supplys representation in admin site'''

    readonly_fields = ['id', 'supply_date']
    list_display    = ('items','id','supply_quantity','supply_date')

# Register your models here.
admin.site.register(Supplys, SupplysAdmin)
