# report_app/apps.py

# django
from django.apps import AppConfig


class ReportAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name               = 'report_app'
    verbose_name       = 'Canteen Daily Reports'
