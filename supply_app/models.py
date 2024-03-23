# supply_app/models.py

# django
from django.db    import models
from django.urls  import reverse

# local
from items.models import Items


class Supplys(models.Model):
    '''Canteen Export Stock Model'''

    items      = models.ForeignKey(Items, 
                                   on_delete=models.PROTECT,
                                   verbose_name='Item Supplied',
                                   help_text='Please choose a item to supply',
                                   limit_choices_to={'is_active' : True})

    # allow negative values
    quantity   = models.SmallIntegerField('Supply Quantity', help_text='Please enter your supplied quantity here')

    entry_date = models.DateField(auto_now_add=True, help_text='It will take todays date on it\'s own')


    class Meta:
        verbose_name        = 'Supply'
        verbose_name_plural = 'Supplys'
        ordering            = ['-entry_date']

        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','entry_date']         # will raise IntegrityError


    def get_absolute_url(self):
        '''Redirect the user after deletion and updation of items'''

        return reverse('supply_detail', kwargs={'entry_date' : self.entry_date}) + '#focus'


    def __str__(self):
        return f'{self.entry_date} - {self.items.name}'
