# supply_app/apps.py

# django
from django.apps import AppConfig


class SupplyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'supply_app'
    verbose_name       = 'Canteen Supply Items'
