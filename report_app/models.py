# report_app/models.py

# django
from django.db import models


class Reports(models.Model):
    '''Canteen Daily Reports Model'''

    entry_date = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name        = 'Report'
        verbose_name_plural = 'Reports'


    def __str__(self):
        return f'{self.entry_date}'

