# items/models.py

# django
from django.db              import models
from django.utils           import timezone
from django.core.validators import MinValueValidator


class Items(models.Model):
    '''Canteen Item Model'''

    name           = models.CharField('Item Name',max_length=70)
    price          = models.PositiveSmallIntegerField('Item Price', validators=[MinValueValidator(10)])
    total_quantity = models.PositiveSmallIntegerField('Total quantity of Item', default=0)
    is_active      = models.BooleanField('Status of Item', default=True)
    created_at     = models.DateTimeField(editable=False)
    updated_at     = models.DateTimeField(editable=False)     # update only on changed in total quantity

    class Meta:
        '''Adding sorting and user friendly model name for admin site'''

        ordering            = ['name']
        verbose_name        = 'Item'
        verbose_name_plural = 'Items'


    def __init__(self, *args, **kwargs):
        '''Cached the total quantity for future use'''

        super().__init__(*args, **kwargs)
        self.cached_total_quantity = self.total_quantity


    def save(self, *args, **kwargs):
        '''Handle datetime fields before save'''

        current_time = timezone.now()

        # CREATE
        if self.id:
            # Update updated_at only change in total quantity
            if self.cached_total_quantity != self.total_quantity: self.updated_at = current_time

        # UPDATE
        else:
            # Setting created_at and updated_at
            self.created_at, self.updated_at = current_time, current_time

        self.name = self.name.title().strip()
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name)
