# items/models.py

# django
from django.db              import models
from django.urls            import reverse
from django.utils           import timezone
from django.core.validators import MinLengthValidator, MinValueValidator


class Items(models.Model):
    '''Canteen Item Model'''

    name       = models.CharField('Item Name',
                                  max_length=50,
                                  default='',
                                  validators=[MinLengthValidator(5)],
                                  help_text='Enter your item\'s name')

    price      = models.PositiveSmallIntegerField('Item Price',
                                                  validators=[MinValueValidator(5)],
                                                  help_text='Enter your item\'s price')

    # allow negative values
    quantity   = models.SmallIntegerField('Total quantity of Item',
                                          default=0,
                                          help_text='Item\'s current quantity')

    is_active  = models.BooleanField('Item Availability', 
                                     default=True, 
                                     help_text='Click to change item\'s availability')

    created_at = models.DateTimeField('Created Time Of Item',
                                      editable=False, 
                                      help_text='It will take todays date on it\'s itself')

    # update only on changed in total quantity
    updated_at = models.DateTimeField('Last Change In Quantity',
                                      editable=False, 
                                      help_text='It will take todays date on it\'s itself')

    class Meta:
        '''Adding sorting and user friendly model name for admin site'''

        ordering            = ['price','name']
        verbose_name        = 'Item'
        verbose_name_plural = 'Items'


    def __init__(self, *args, **kwargs):
        '''Cached the total quantity for future use'''

        super().__init__(*args, **kwargs)
        self.cached_quantity = self.quantity


    def save(self, *args, **kwargs):
        '''Handle datetime fields before save'''

        current_time = timezone.now()

        # UPDATE
        if self.id:
            # Update updated_at only change in total quantity
            if self.cached_quantity != self.quantity: self.updated_at = current_time

        # CREATE
        else:
            # Setting created_at and updated_at
            self.created_at, self.updated_at = current_time, current_time

        super().save(*args, **kwargs)


    def get_absolute_url(self):
        '''Always redirect to listview of items'''

        return reverse('item_list') + '#focus'


    def __str__(self):
        return f'{self.name} - ({self.quantity} left)'
