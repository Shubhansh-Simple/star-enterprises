# users/models.py

# django
from django.contrib.auth.models import AbstractUser


class CustomUser( AbstractUser ):
    '''Overriding existing django's user model to add additional fields'''

    class Meta:
        db_table            = 'users_customuser'
        verbose_name        = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return str(self.username)


