# supply_app/models.py

# django
from django.db    import models
from django.urls  import reverse

# local
from items.models import Items

class Supplys(models.Model):
    '''Canteen Export Stock Model'''

    items           = models.ForeignKey(Items, 
                              on_delete=models.PROTECT,
                              verbose_name='Item Supplied',
                              help_text='Please choose a item to supply',
                              limit_choices_to={'is_active' : True})

    supply_quantity = models.SmallIntegerField('Supply Quantity',
                                               help_text='Please enter a quantity greater than or equal to 1')

    supply_date     = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name        = 'Supply'
        verbose_name_plural = 'Supplys'
        ordering            = ['-supply_date']

        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','supply_date']         # will raise IntegrityError


    def get_absolute_url(self):
        '''Redirect the user after creation and updation of items'''

        # UPDATE
        if self.pk:
            pass

        # CREATE
        else:
            pass


    def __str__(self):
        return f'{self.supply_date} - {self.items.name}'
