# supply_app/admin.py

# django
from django.contrib       import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Supplys


class SupplysAdmin(ModelAdmin):
    '''Modify supplys representation in admin site'''

    readonly_fields = ['id', 'entry_date']
    list_display    = ('items','id','quantity','entry_date')

# Register your models here.
admin.site.register(Supplys, SupplysAdmin)
