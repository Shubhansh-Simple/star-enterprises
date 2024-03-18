# import_app/models.py

# django
from django.db              import models
from django.urls            import reverse
from django.core.validators import MinValueValidator

# local
from items.models import Items


class Imports(models.Model):
    '''Canteen Import Stock Model'''

    items           = models.ForeignKey(Items, 
                                        on_delete=models.PROTECT, 
                                        verbose_name='Item Imported', 
                                        help_text='Please choose a item to import',
                                        limit_choices_to={'is_active':True})

    quantity = models.PositiveSmallIntegerField('Import Quantity', 
                                                validators=[MinValueValidator(1)], 
                                                help_text='Please enter a quantity greater than or equal to 1')

    entry_date     = models.DateField(auto_now_add=True)


    class Meta:
        verbose_name        = 'Import'
        verbose_name_plural = 'Imports'
        ordering            = ['-entry_date']

        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','entry_date']        # will raise IntegrityError


    def get_absolute_url(self):
        '''Redirect the after creation & updation of items'''

        # UPDATE
        if self.pk:
            return reverse('import_detail', kwargs={'entry_date' : self.entry_date}) + '#focus'

        # CREATE
        else:
            return reverse('import_create') + '#focus'


    def __str__(self):
        return f'{self.entry_date} - {self.items.name}'
