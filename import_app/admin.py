# import_app/admin.py

# django
from django.contrib       import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Imports


class ImportsAdmin(ModelAdmin):
    '''Modify imports representation in admin site'''

    readonly_fields = ['id','entry_date']
    list_display    = ('items','id','quantity','entry_date')


# Register models for admin site
admin.site.register(Imports, ImportsAdmin)


