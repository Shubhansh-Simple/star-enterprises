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

    # NOTE : Negative values are also allow here

    # Last table balance stock
    old_stock     = models.SmallIntegerField( default=0 )

    # Import Stock
    arrival_stock = models.SmallIntegerField( default=0 )
    total_stock   = models.SmallIntegerField( default=0 )

    # Supply Stock
    balance_stock = models.SmallIntegerField( default=0 )
    sold_stock    = models.SmallIntegerField( default=0 )

    entry_date = models.DateField(auto_now_add=True, help_text='It will take todays date on it\'s own')


    class Meta:
        verbose_name        = 'Report'
        verbose_name_plural = 'Reports'
        ordering            = ['-entry_date']

        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','entry_date']      # will raise IntegrityError


    def save(self, *args, **kwargs):
        '''Handle total_stock & balance_stock on each saving'''

        # total_stock   = old_stock   + arrival_stock
        # balance_stock = total_stock - sold_stock      // tomorrow's old_stock

        self.total_stock   = self.old_stock   + self.arrival_stock
        self.balance_stock = self.total_stock - self.sold_stock

        super().save(*args, **kwargs)


    def __str__(self):
        return f'Report - {self.entry_date} - {self.items.name}'
