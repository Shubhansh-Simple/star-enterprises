# import_app/models.py

# django
from django.db              import models
from django.core.validators import MinValueValidator

# local
from items.models import Items
from django.conf  import settings


class Imports(models.Model):
    '''Canteen Import Stock Model'''

    items           = models.ForeignKey(Items,                    on_delete=models.PROTECT, verbose_name='Item to be imported', limit_choices_to={'is_active':True})
    import_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Imported By')
    import_quantity = models.PositiveSmallIntegerField('Import Quantity', validators=[MinValueValidator(1)])
    import_date     = models.DateField(auto_now_add=True)

    class Meta:
        # Avoid duplicate entry of a item in same date
        unique_together     = ['items','import_date']
        verbose_name        = 'Import'
        verbose_name_plural = 'Imports'


    def save(self, *args, **kwargs):

        #Total quantity in Items model should incremented by import_quantity
        self.items.total_quantity += self.import_quantity
        self.items.save()

        self.import_date = timezone.now().date() + timezone.timedelta(1)

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.import_date} - {self.items.name}'
