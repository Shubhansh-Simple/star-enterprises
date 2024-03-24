# report_app/models.py

# django
from django.db import models

# local
from items.models import Items


class Reports(models.Model):
    '''Canteen Daily Reports Model'''

    items      = models.ForeignKey(Items,
                                   on_delete=models.PROTECT,
                                   verbose_name='Item Report',
                                   help_text='Please choose a item to generate report'
                                  )

    # Allow negative values as well
    old_balance   = models.SmallIntegerField( default=0 )
    arrival_stock = models.SmallIntegerField( default=0 )
    total_stock   = models.SmallIntegerField( default=0 )
    balance_stock = models.SmallIntegerField( default=0 )
    sold_stock    = models.SmallIntegerField( default=0 )

    entry_date = models.DateField(auto_now_add=True, help_text='It will take todays date on it\'s own')


    class Meta:
        verbose_name        = 'Report'
        verbose_name_plural = 'Reports'
        ordering            = ['-entry_date']

        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','entry_date']      # will raise IntegrityError


    def __str__(self):
        return f'Report - {self.entry_date} - {self.items.name}'

