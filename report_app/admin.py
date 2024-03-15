# report_app/admin.py

# django
from django.contrib import admin
from django.contrib.admin import ModelAdmin

# local
from .models import Reports


class ReportsAdmin(ModelAdmin):
    '''Modify reports representation in admin site'''

    readonly_fields = ['id', 'entry_date']
    list_display    = ('id','entry_date')

# Register your models here.
admin.site.register(Reports, ReportsAdmin)
